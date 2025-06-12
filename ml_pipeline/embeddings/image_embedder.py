import requests
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import numpy as np
import io
import base64
import mlflow


class ImageEmbedder:
    def __init__(self):
        self.model_name = "resnet50"
        self.model = resnet50(weights=ResNet50_Weights.DEFAULT)
        self.model.fc = torch.nn.Identity()  # Remove classification head
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

        # Log model name
        mlflow.log_param("image_encoder", self.model_name)

    def encode(self, image_input: str) -> np.ndarray:
        try:
            # Load image from URL or base64
            if image_input.startswith("http"):
                response = requests.get(image_input)
                image = Image.open(io.BytesIO(response.content)).convert("RGB")
            else:
                image_input = image_input.split(",")[-1]
                image = Image.open(io.BytesIO(base64.b64decode(image_input))).convert("RGB")

            image_tensor = self.transform(image).unsqueeze(0)

            with torch.no_grad():
                embedding = self.model(image_tensor).squeeze().numpy()
                embedding = embedding / np.linalg.norm(embedding)

            return embedding

        except Exception as e:
            mlflow.log_param("image_embedding_failure", str(e))
            print(f"❌ Failed to embed image: {e}")
            return np.zeros(2048)
