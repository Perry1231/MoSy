import numpy as np
import onnxruntime as ort

# 1. Load ONNX model session
model_path = "mosy_policy.onnx"
session = ort.InferenceSession(model_path)

# 2. Get input and output layer metadata
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

input_shape = session.get_inputs()[0].shape
output_shape = session.get_outputs()[0].shape

print(f"Model loaded successfully!")
print(f"Input Name:  '{input_name}' | Shape: {input_shape}")
print(f"Output Name: '{output_name}' | Shape: {output_shape}")

# 3. Create dummy observation tensor (matching 111-dim observation space)
dummy_observation = np.random.randn(*input_shape).astype(np.float32)

# 4. Run inference
outputs = session.run([output_name], {input_name: dummy_observation})
actions = outputs[0]

print("\n--- Test Run Successful ---")
print(f"Action vector shape: {actions.shape}")
print(f"Generated motor action commands:\n{actions[0]}")