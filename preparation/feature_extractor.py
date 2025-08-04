import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models import ResNet50_Weights
from tqdm import tqdm
import os
import numpy as np
from PIL import Image

class ResNetFeatureExtractor:
    def __init__(self, device=None):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])  # remove FC
        self.model.eval().to(self.device)

        self.transform = transforms.Compose([
            transforms.Resize((448, 448)),  # or (256, 256) with CenterCrop(224)
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],  # ImageNet
                std=[0.229, 0.224, 0.225]
            )
        ])

    def extract(self, image: Image.Image) -> torch.Tensor:
        """Returns a (2048,) feature vector as a torch.Tensor."""
        with torch.no_grad():
            img_tensor = self.transform(image).unsqueeze(0).to(self.device)
            features = self.model(img_tensor)  # shape: (1, 2048, 1, 1)
            return features.squeeze().cpu()    # shape: (2048,)

def is_image_file(filename):
    valid_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    return os.path.splitext(filename)[1].lower() in valid_exts

def main():
    input_dir = os.path.expanduser('~/data/marki/images')
    output_dir = os.path.expanduser('~/data/marki/features')

    os.makedirs(output_dir, exist_ok=True)
    extractor = ResNetFeatureExtractor()

    for filename in tqdm(os.listdir(input_dir), desc="Extracting features"):
        if not is_image_file(filename):
            continue

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".npy")

        try:
            image = Image.open(input_path).convert("RGB")
            features = extractor.extract(image)
            np.save(output_path, features.numpy())
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    ## NOTE: NOT NEEDED, TAKEN CARE OF IN build_index.py
    main()