#!/usr/bin/env python3

"""
Real-time image classification using PyTorch with Metal acceleration.
"""

import os
import time
import argparse
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

class ImageClassifier:
    """Real-time image classifier using PyTorch with Metal acceleration."""
    def __init__(self, model_name="mobilenet_v3_small"):
        """Initialize the classifier."""
        # Check if Metal is available
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print("Using Metal Performance Shaders (MPS)")
        else:
            self.device = torch.device("cpu")
            print("Metal not available, using CPU")
        
        # Load pre-trained model
        print(f"Loading {model_name} model...")
        if model_name == "mobilenet_v3_small":
            self.model = models.mobilenet_v3_small(weights="DEFAULT")
        elif model_name == "resnet18":
            self.model = models.resnet18(weights="DEFAULT")
        elif model_name == "efficientnet_b0":
            self.model = models.efficientnet_b0(weights="DEFAULT")
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Load ImageNet class labels
        with open("data/imagenet_classes.txt", "r") as f:
            self.class_names = [line.strip() for line in f.readlines()]
        
        # Set up image transformation
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def classify_image(self, image_path):
        """Classify an image."""
        # Load and transform image
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
        
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Perform inference
        start_time = time.time()
        with torch.no_grad():
            output = self.model(input_tensor)
        inference_time = time.time() - start_time
        
        # Get top-5 predictions
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top5_prob, top5_indices = torch.topk(probabilities, 5)
        
        # Convert to human-readable results
        results = []
        for i, (prob, idx) in enumerate(zip(top5_prob, top5_indices)):
            class_name = self.class_names[idx]
            results.append((class_name, prob.item()))
        
        return results, inference_time

def ensure_imagenet_labels():
    """Ensure ImageNet class labels file exists."""
    labels_file = "data/imagenet_classes.txt"
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(labels_file):
        print("Downloading ImageNet class labels...")
        import urllib.request
        url = "https://raw.githubusercontent.com/pytorch/vision/main/torchvision/models/imagenet_classes.txt"
        urllib.request.urlretrieve(url, labels_file)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Real-time image classification using PyTorch with Metal")
    parser.add_argument("--model", type=str, default="mobilenet_v3_small",
                        choices=["mobilenet_v3_small", "resnet18", "efficientnet_b0"],
                        help="Model architecture to use")
    parser.add_argument("--image", type=str, required=True,
                        help="Path to image for classification")
    args = parser.parse_args()
    
    ensure_imagenet_labels()
    
    classifier = ImageClassifier(args.model)
    
    print(f"\nClassifying image: {args.image}")
    results, inference_time = classifier.classify_image(args.image)
    
    print(f"\nResults (inference time: {inference_time*1000:.2f} ms):")
    
    if results:
        for i, (class_name, probability) in enumerate(results):
            print(f"{i+1}. {class_name}: {probability*100:.2f}%")
    else:
        print("Failed to classify image.")

if __name__ == "__main__":
    main()
