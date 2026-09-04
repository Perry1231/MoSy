import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class PCA9685Driver:
    """
    I2C Hardware Driver for the PCA9685 16-channel PWM servo controller.
    Translates microsecond pulse widths (500us - 2500us) into 12-bit PWM values (0 - 4095).
    """
    def __init__(self, i2c_bus: int = 1, address: int = 0x40, frequency: int = 50):
        self.address = address
        self.frequency = frequency
        self.is_connected = False
        self.kit = None

        try:
            from adafruit_servokit import ServoKit
            self.kit = ServoKit(channels=16, address=self.address)
            self.is_connected = True
            logging.info(f"PCA9685 driver initialized on I2C bus {i2c_bus} @ address {hex(self.address)}.")
        except Exception as e:
            logging.warning(f"Hardware PCA9685 not detected ({e}). Falling back to Simulation/Dry-Run mode.")

    def set_pwm(self, channel: int, pulse_us: int):
        """Sets the raw microsecond pulse width for a given PWM channel."""
        if channel < 0 or channel > 15:
            logging.error(f"Invalid servo channel: {channel}")
            return

        clamped_pulse = max(500, min(2500, int(pulse_us)))

        if self.is_connected and self.kit:
            try:
                self.kit.servo[channel].set_pulse_width_range(500, 2500)
                self.kit.servo[channel].fraction = (clamped_pulse - 500) / 2000.0
            except Exception as e:
                logging.error(f"Error setting PWM on channel {channel}: {e}")
        else:
            # Dry-run logging for testing without hardware connected
            pass

    def update_all_servos(self, pwm_dict: dict):
        """Updates all servo channels simultaneously using a dictionary of {channel_id: pulse_us}."""
        for channel, pulse in pwm_dict.items():
            self.set_pwm(channel, pulse)