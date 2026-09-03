import numpy as np

class ServoMapper:
    """
    Converts normalized policy action values [-1.0, 1.0] from ONNX inference
    into physical PWM pulse widths (microseconds) or joint angles (degrees).
    """
    def __init__(self, min_angle: float = 0.0, max_angle: float = 180.0, 
                 min_pwm: int = 500, max_pwm: int = 2500):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_pwm = min_pwm
        self.max_pwm = max_pwm
        
        # Center reference point for 8 joint servos (default 90 degrees)
        self.joint_offsets = np.full(8, 90.0, dtype=np.float32)

    def actions_to_degrees(self, actions: np.ndarray, motion_range: float = 45.0) -> np.ndarray:
        """
        Maps normalized action vector [-1.0, 1.0] to target joint angles in degrees.
        `motion_range` sets the maximum angular deflection from center offset (e.g. 90° ± 45°).
        """
        clipped_actions = np.clip(actions, -1.0, 1.0)
        target_angles = self.joint_offsets + (clipped_actions * motion_range)
        return np.clip(target_angles, self.min_angle, self.max_angle)

    def degrees_to_pwm(self, angles: np.ndarray) -> np.ndarray:
        """
        Converts joint angles (0° - 180°) to standard PCA9685/servo PWM pulse widths (500us - 2500us).
        """
        pwm_values = self.min_pwm + (angles / 180.0) * (self.max_pwm - self.min_pwm)
        return np.round(pwm_values).astype(int)