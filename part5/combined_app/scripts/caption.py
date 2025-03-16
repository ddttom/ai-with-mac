#!/usr/bin/env python3

"""
Image captioning using PyTorch with Metal acceleration.
"""

import os
import torch
import torchvision.transforms as transforms
from PIL import Image

class ImageCaptioner:
    """Image captioner using PyTorch with Metal acceleration."""
    def __init__(self):
        """Initialize the captioner."""
        # Check if Metal is available
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print("Using Metal Performance Shaders (MPS)")
        else:
            self.device = torch.device("cpu")
            print("Metal not available, using CPU")
        
        # Load pre-trained model
        print("Loading image captioning model...")
        self.model = torch.hub.load('saahiluppal/catr', 'v3', pretrained=True).to(self.device)
        self.model.eval()
        
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
    
    def generate_caption(self, image_path):
        """Generate a caption for the image."""
        # Load and transform image
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            print(f"Error loading image: {e}")
            return "Error loading image"
        
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Generate caption
        with torch.no_grad():
            output = self.model(input_tensor)
            caption = self.model.caption_generator.decode(output[0])
        
        return caption

# Example usage
if __name__ == "__main__":
    captioner = ImageCaptioner()
    
    # Example image
    image_path = "data/sample.jpg"
    
    if os.path.exists(image_path):
        caption = captioner.generate_caption(image_path)
        print("\nCaption:")
        print(caption)
    else:
        print(f"Image not found at {image_path}")
