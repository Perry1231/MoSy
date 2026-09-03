import numpy as np
import onnxruntime as ort

class MoSyInferenceEngine:
    def __init__(self, model_path: str = "models/mosy_policy.onnx"):
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape
        self.output_shape = self.session.get_outputs()[0].shape

    def predict(self, observation: np.ndarray) -> np.ndarray:
        """
        Executes inference on a [1, 112] observation vector.
        Returns an [1, 8] motor action array.
        """
        if observation.shape != tuple(self.input_shape):
            raise ValueError(f"Invalid observation shape: {observation.shape}. Expected: {self.input_shape}")
            
        outputs = self.session.run([self.output_name], {self.input_name: observation.astype(np.float32)})
        return outputs[0]