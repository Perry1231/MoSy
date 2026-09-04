import numpy as np
import logging

class BNO055Mapper:
    """
    Maps telemetry packets from the HS-1 suit (Shoulder, Forearm, Hand)
    into the 112-dimensional state vector required by the ONNX policy.
    """
    def __init__(self, state_dim: int = 112):
        self.state_dim = state_dim

    def map_telemetry_to_vector(self, raw_packet: dict) -> np.ndarray:
        """
        Translates raw HS-1 JSON packets into an normalized numpy state array [1, 112].
        Incoming packet schema:
        {
          "shoulder": {"p": float, "y": float, "r": float},
          "forearm":  {"p": float, "y": float, "r": float},
          "hand":     {"p": float, "y": float, "r": float}
        }
        """
        vector = np.zeros(self.state_dim, dtype=np.float32)

        if not raw_packet:
            return np.expand_dims(vector, axis=0)

        try:
            # Extract Pitch, Yaw, Roll for each arm segment
            sh = raw_packet.get("shoulder", {"p": 0.0, "y": 0.0, "r": 0.0})
            fo = raw_packet.get("forearm",  {"p": 0.0, "y": 0.0, "r": 0.0})
            hd = raw_packet.get("hand",     {"p": 0.0, "y": 0.0, "r": 0.0})

            # Normalize Euler angles (-180..180 deg to -1.0..1.0 range)
            angles = [
                sh.get("p", 0.0) / 180.0, sh.get("y", 0.0) / 180.0, sh.get("r", 0.0) / 180.0,
                fo.get("p", 0.0) / 180.0, fo.get("y", 0.0) / 180.0, fo.get("r", 0.0) / 180.0,
                hd.get("p", 0.0) / 180.0, hd.get("y", 0.0) / 180.0, hd.get("r", 0.0) / 180.0,
            ]

            # Populate initial slots of the state vector
            vector[:len(angles)] = angles

        except Exception as e:
            logging.warning(f"Error mapping HS-1 packet to state vector: {e}")

        return np.expand_dims(vector, axis=0)