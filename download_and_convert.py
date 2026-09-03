import torch
import torch.nn as nn
from huggingface_sb3 import load_from_hub
from stable_baselines3 import PPO

print("1. Downloading model from Hugging Face...")
checkpoint = load_from_hub(
    repo_id="sb3/ppo-Ant-v3",
    filename="ppo-Ant-v3.zip"
)

model = PPO.load(checkpoint)
print("   Model loaded successfully!")

# Extract actor network directly to obtain deterministic actions
class OnnxablePolicy(nn.Module):
    def __init__(self, policy):
        super().__init__()
        self.policy = policy.to("cpu")

    def forward(self, observation):
        # Directly call feature extractor and action_net, bypassing proba_distribution
        features = self.policy.extract_features(observation)
        latent_pi, _ = self.policy.mlp_extractor(features)
        return self.policy.action_net(latent_pi)

onnx_policy = OnnxablePolicy(model.policy)
onnx_policy.eval()

# Generate dummy observation vector matching model input shape
dummy_input = torch.randn(1, model.observation_space.shape[0])

onnx_path = "mosy_policy.onnx"
print("2. Exporting model to ONNX format...")

# Use legacy TorchScript exporter (dynamo=False) to bypass data-dependent dynamic graph errors
torch.onnx.export(
    onnx_policy,
    dummy_input,
    onnx_path,
    opset_version=11,
    input_names=["observation"],
    output_names=["action"],
    dynamo=False
)

print(f"\nSuccess! ONNX policy exported to '{onnx_path}'")