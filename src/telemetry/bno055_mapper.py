import numpy as np

class TelemetryMapper:
    def __init__(self):
        self.observation_dim = 112

    def format_observation(self, orientation_quat: list, gyro: list, accel: list, joint_positions: list = None) -> np.ndarray:
        """
        Packs BNO055 telemetry and joint states into a [1, 112] observation vector.
        """
        obs = np.zeros((1, self.observation_dim), dtype=np.float32)
        
        # 0..3: Orientation Quaternion [w, x, y, z]
        obs[0, 0:4] = orientation_quat
        
        # 4..6: Angular Velocities [gx, gy, gz]
        obs[0, 4:7] = gyro
        
        # 7..9: Linear Accelerations [ax, ay, az]
        obs[0, 7:10] = accel
        
        # 10..17: Joint positions (if available, default to zero)
        if joint_positions and len(joint_positions) == 8:
            obs[0, 10:18] = joint_positions

        return obs