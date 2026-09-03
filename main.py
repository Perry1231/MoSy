import sys
import os
import time
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ai_core.onnx_engine import MoSyInferenceEngine
from src.telemetry.bno055_mapper import TelemetryMapper
from src.kinematics.servo_mapper import ServoMapper

def main():
    print("=== Starting MoSy Edge AI Engine ===")
    
    engine = MoSyInferenceEngine("models/mosy_policy.onnx")
    mapper = TelemetryMapper()
    kinematics = ServoMapper()
    
    print("Engine, Telemetry Mapper, and Kinematics initialized successfully.\n")

    try:
        loop_count = 0
        while True:
            sim_quat = [1.0, 0.0, 0.0, 0.0]
            sim_gyro = [0.01, -0.02, 0.005]
            sim_accel = [0.0, 0.0, 9.81]
            sim_joints = [0.0] * 8

            observation = mapper.format_observation(
                orientation_quat=sim_quat,
                gyro=sim_gyro,
                accel=sim_accel,
                joint_positions=sim_joints
            )

            start_time = time.perf_counter()
            actions = engine.predict(observation)
            latency_ms = (time.perf_counter() - start_time) * 1000

            # Convert normalized [-1.0, 1.0] actions to Servo Angles and PWM
            target_angles = kinematics.actions_to_degrees(actions[0], motion_range=45.0)
            target_pwm = kinematics.degrees_to_pwm(target_angles)

            loop_count += 1
            if loop_count % 50 == 0:
                print(f"[Loop #{loop_count}] Latency: {latency_ms:.3f} ms")
                print(f"Action Vector [-1, 1] : {np.round(actions[0], 3)}")
                print(f"Joint Angles (Degrees): {np.round(target_angles, 1)}")
                print(f"Servo PWM (us)        : {target_pwm}\n")

            time.sleep(0.02)  # 50 Hz control loop

    except KeyboardInterrupt:
        print("\n=== Control loop terminated by user. ===")

if __name__ == "__main__":
    main()