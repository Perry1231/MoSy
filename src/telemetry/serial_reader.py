import serial
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class ESP32SerialReader:
    """
    Manages non-blocking UART/Serial streaming from an ESP32-C3 microcontroller.
    Parses incoming telemetry packets containing BNO055 IMU readings (Quaternions, Gyro, Accel).
    """
    def __init__(self, port: str = "COM3", baudrate: int = 115200, timeout: float = 0.1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.is_connected = False

    def connect(self) -> bool:
        """Establishes connection with the ESP32-C3 serial device."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2.0)  # Allow ESP32-C3 boot sequence to complete
            self.is_connected = True
            logging.info(f"Connected to ESP32-C3 telemetry on {self.port} @ {self.baudrate} baud.")
            return True
        except serial.SerialException as e:
            logging.error(f"Failed to connect to port {self.port}: {e}")
            self.is_connected = False
            return False

    def read_latest_packet(self) -> dict:
        """
        Reads lines from the serial buffer and parses the latest JSON telemetry packet.
        Expected format from ESP32-C3:
        {"quat": [w, x, y, z], "gyro": [gx, gy, gz], "accel": [ax, ay, az]}
        """
        if not self.is_connected or self.ser is None:
            return None

        latest_data = None
        try:
            # Read all available lines to flush queue and get the freshest packet
            while self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        latest_data = json.loads(line)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logging.warning(f"Error reading serial packet: {e}")

        return latest_data

    def close(self):
        """Closes the serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.is_connected = False
            logging.info("Serial connection closed.")