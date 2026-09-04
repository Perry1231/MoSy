import time
import logging
import numpy as np

from src.ai_core.onnx_engine import MoSyONNXEngine
from src.telemetry.serial_reader import ESP32SerialReader
from src.telemetry.bno055_mapper import BNO055Mapper
from src.kinematics.servo_mapper import ServoMapper
from src.kinematics.pca9685_driver import PCA9685Driver

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    logging.info("Starting MoSy Edge AI Motion Engine...")

    # 1. Initialize System Modules
    ai_engine = MoSyONNXEngine(model_path="models/mosy_policy.onnx")
    telemetry_reader = ESP32SerialReader(port="COM3", baudrate=115200) # Change to /dev/ttyUSB0 on Linux
    bno_mapper = BNO055Mapper()
    servo_mapper = ServoMapper(config_path="config/joints.json")
    pca_driver = PCA9685Driver(address=0x40, frequency=50)

    # 2. Connect Hardware Telemetry
    telemetry_reader.connect()

    target_loop_time = 1.0 / 50.0  # 50 Hz control loop (20 ms)
    logging.info("MoSy active loop running at 50 Hz. Press Ctrl+C to stop.")

    try:
        while True:
            start_time = time.perf_counter()

            # Step 1: Read live UART packet from ESP32-C3
            raw_packet = telemetry_reader.read_latest_packet()
            
            # Step 2: Format telemetry into 112-dim state vector
            state_vector = bno_mapper.map_telemetry_to_vector(raw_packet)

            # Step 3: Run AI Inference (< 0.1 ms latency)
            actions = ai_engine.predict(state_vector)

            # Step 4: Map normalized actions to PWM pulse widths
            pwm_signals = servo_mapper.actions_to_pwm(actions)

            # Step 5: Send PWM to PCA9685 Driver
            pca_driver.update_all_servos(pwm_signals)

            # Maintain strict 50 Hz execution timing
            elapsed = time.perf_counter() - start_time
            sleep_time = target_loop_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        logging.info("Stopping MoSy Control Engine...")
    finally:
        telemetry_reader.close()
        logging.info("MoSy shutdown complete.")

if __name__ == "__main__":
    main()