#!/usr/bin/env python3

"""
Model registry system for AI projects.
"""

import os
import json
import shutil
import hashlib
import datetime
import argparse
from typing import Dict, List, Optional, Any

class ModelRegistry:
    """
    Model registry for versioning and tracking ML models.
    
    This class provides functionality to register, version, and
    track machine learning models and their associated metadata.
    """
    
    def __init__(self, registry_path: str = "model_registry"):
        """Initialize the model registry."""
        self.registry_path = registry_path
        self.index_file = os.path.join(registry_path, "registry_index.json")
        
        # Create registry directory if it doesn't exist
        os.makedirs(registry_path, exist_ok=True)
        
        # Initialize or load the registry index
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                self.registry_index = json.load(f)
        else:
            self.registry_index = {
                "models": {},
                "datasets": {},
                "last_updated": datetime.datetime.now().isoformat()
            }
            self._save_index()
    
    def _save_index(self):
        """Save the registry index to disk."""
        self.registry_index["last_updated"] = datetime.datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            json.dump(self.registry_index, f, indent=2)
    
    def register_model(self, model_name: str, model_path: str, 
                       version: str = None, metadata: Dict = None) -> str:
        """
        Register a model in the registry.
        
        Args:
            model_name (str): Name of the model
            model_path (str): Path to the model directory or file
            version (str, optional): Version string (auto-generated if None)
            metadata (dict, optional): Additional metadata
            
        Returns:
            str: The model version
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path does not exist: {model_path}")
        
        # Generate version if not provided
        if version is None:
            version = self._generate_version()
        
        # Initialize model entry if it doesn't exist
        if model_name not in self.registry_index["models"]:
            self.registry_index["models"][model_name] = {
                "versions": {},
                "latest_version": None,
                "created": datetime.datetime.now().isoformat()
            }
        
        # Create model directory in registry
        model_dir = os.path.join(self.registry_path, "models", model_name, version)
        os.makedirs(model_dir, exist_ok=True)
        
        # Copy model files
        if os.path.isdir(model_path):
            # Copy directory contents
            for item in os.listdir(model_path):
                s = os.path.join(model_path, item)
                d = os.path.join(model_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
        else:
            # Copy single file
            shutil.copy2(model_path, model_dir)
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        
        # Add standard metadata
        metadata.update({
            "registered_at": datetime.datetime.now().isoformat(),
            "original_path": model_path,
            "registry_path": model_dir
        })
        
        # Calculate model size and file hash
        if os.path.isdir(model_path):
            total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                             for dirpath, _, filenames in os.walk(model_path)
                             for filename in filenames)
            metadata["model_size_bytes"] = total_size
        else:
            metadata["model_size_bytes"] = os.path.getsize(model_path)
            metadata["file_hash"] = self._calculate_file_hash(model_path)
        
        # Update registry index
        self.registry_index["models"][model_name]["versions"][version] = metadata
        self.registry_index["models"][model_name]["latest_version"] = version
        self._save_index()
        
        print(f"Model {model_name} version {version} registered successfully.")
        return version
    
    def register_dataset(self, dataset_name: str, dataset_path: str,
                         version: str = None, metadata: Dict = None) -> str:
        """
        Register a dataset in the registry.
        
        Args:
            dataset_name (str): Name of the dataset
            dataset_path (str): Path to the dataset directory or file
            version (str, optional): Version string (auto-generated if None)
            metadata (dict, optional): Additional metadata
            
        Returns:
            str: The dataset version
        """
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset path does not exist: {dataset_path}")
        
        # Generate version if not provided
        if version is None:
            version = self._generate_version()
        
        # Initialize dataset entry if it doesn't exist
        if dataset_name not in self.registry_index["datasets"]:
            self.registry_index["datasets"][dataset_name] = {
                "versions": {},
                "latest_version": None,
                "created": datetime.datetime.now().isoformat()
            }
        
        # Create dataset directory in registry
        dataset_dir = os.path.join(self.registry_path, "datasets", dataset_name, version)
        os.makedirs(dataset_dir, exist_ok=True)
        
        # Copy dataset files (or reference)
        is_large_dataset = False
        if os.path.isdir(dataset_path):
            # Check dataset size
            total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                             for dirpath, _, filenames in os.walk(dataset_path)
                             for filename in filenames)
            
            # If dataset is larger than 1GB, just store reference
            if total_size > 1_000_000_000:  # 1GB
                is_large_dataset = True
                with open(os.path.join(dataset_dir, "dataset_reference.txt"), 'w') as f:
                    f.write(f"Original dataset path: {os.path.abspath(dataset_path)}\n")
                    f.write(f"Dataset size: {total_size / (1024**2):.2f} MB\n")
            else:
                # Copy directory contents
                for item in os.listdir(dataset_path):
                    s = os.path.join(dataset_path, item)
                    d = os.path.join(dataset_dir, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
        else:
            # Copy single file
            shutil.copy2(dataset_path, dataset_dir)
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        
        # Add standard metadata
        metadata.update({
            "registered_at": datetime.datetime.now().isoformat(),
            "original_path": dataset_path,
            "registry_path": dataset_dir,
            "is_reference_only": is_large_dataset
        })
        
        # Calculate dataset statistics
        if not is_large_dataset:
            if os.path.isdir(dataset_path):
                metadata["dataset_size_bytes"] = total_size
            else:
                metadata["dataset_size_bytes"] = os.path.getsize(dataset_path)
                metadata["file_hash"] = self._calculate_file_hash(dataset_path)
        
        # Update registry index
        self.registry_index["datasets"][dataset_name]["versions"][version] = metadata
        self.registry_index["datasets"][dataset_name]["latest_version"] = version
        self._save_index()
        
        print(f"Dataset {dataset_name} version {version} registered successfully.")
        return version
    
    def get_model(self, model_name: str, version: str = "latest") -> Optional[Dict]:
        """
        Get information about a registered model.
        
        Args:
            model_name (str): Name of the model
            version (str): Model version or "latest"
            
        Returns:
            dict or None: Model information
        """
        if model_name not in self.registry_index["models"]:
            print(f"Model {model_name} not found in registry.")
            return None
        
        if version == "latest":
            version = self.registry_index["models"][model_name]["latest_version"]
        
        if version not in self.registry_index["models"][model_name]["versions"]:
            print(f"Version {version} of model {model_name} not found.")
            return None
        
        model_info = self.registry_index["models"][model_name]["versions"][version].copy()
        model_info["name"] = model_name
        model_info["version"] = version
        
        return model_info
    
    def get_dataset(self, dataset_name: str, version: str = "latest") -> Optional[Dict]:
        """
        Get information about a registered dataset.
        
        Args:
            dataset_name (str): Name of the dataset
            version (str): Dataset version or "latest"
            
        Returns:
            dict or None: Dataset information
        """
        if dataset_name not in self.registry_index["datasets"]:
            print(f"Dataset {dataset_name} not found in registry.")
            return None
        
        if version == "latest":
            version = self.registry_index["datasets"][dataset_name]["latest_version"]
        
        if version not in self.registry_index["datasets"][dataset_name]["versions"]:
            print(f"Version {version} of dataset {dataset_name} not found.")
            return None
        
        dataset_info = self.registry_index["datasets"][dataset_name]["versions"][version].copy()
        dataset_info["name"] = dataset_name
        dataset_info["version"] = version
        
        return dataset_info
    
    def list_models(self) -> List[Dict]:
        """
        List all registered models.
        
        Returns:
            list: List of model information dictionaries
        """
        models = []
        
        for model_name, model_data in self.registry_index["models"].items():
            latest_version = model_data["latest_version"]
            if latest_version:
                model_info = self.get_model(model_name, latest_version)
                models.append(model_info)
        
        return models
    
    def list_datasets(self) -> List[Dict]:
        """
        List all registered datasets.
        
        Returns:
            list: List of dataset information dictionaries
        """
        datasets = []
        
        for dataset_name, dataset_data in self.registry_index["datasets"].items():
            latest_version = dataset_data["latest_version"]
            if latest_version:
                dataset_info = self.get_dataset(dataset_name, latest_version)
                datasets.append(dataset_info)
        
        return datasets
    
    def _generate_version(self) -> str:
        """
        Generate a version string based on date and time.
        
        Returns:
            str: Version string (format: v{year}.{month}.{day}.{hour}{minute})
        """
        now = datetime.datetime.now()
        return f"v{now.year}.{now.month:02d}.{now.day:02d}.{now.hour:02d}{now.minute:02d}"
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: SHA-256 hash hexadecimal string
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read the file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()

def main():
    """Main function for the model registry utility."""
    parser = argparse.ArgumentParser(description="Model and dataset versioning utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Register model command
    register_model_parser = subparsers.add_parser("register-model", help="Register a model")
    register_model_parser.add_argument("--name", required=True, help="Model name")
    register_model_parser.add_argument("--path", required=True, help="Path to model directory or file")
    register_model_parser.add_argument("--version", help="Version string (optional)")
    register_model_parser.add_argument("--metadata", help="JSON metadata string (optional)")
    
    # Register dataset command
    register_dataset_parser = subparsers.add_parser("register-dataset", help="Register a dataset")
    register_dataset_parser.add_argument("--name", required=True, help="Dataset name")
    register_dataset_parser.add_argument("--path", required=True, help="Path to dataset directory or file")
    register_dataset_parser.add_argument("--version", help="Version string (optional)")
    register_dataset_parser.add_argument("--metadata", help="JSON metadata string (optional)")
    
    # List models command
    subparsers.add_parser("list-models", help="List all registered models")
    
    # List datasets command
    subparsers.add_parser("list-datasets", help="List all registered datasets")
    
    # Get model command
    get_model_parser = subparsers.add_parser("get-model", help="Get model information")
    get_model_parser.add_argument("--name", required=True, help="Model name")
    get_model_parser.add_argument("--version", default="latest", help="Model version (default: latest)")
    
    # Get dataset command
    get_dataset_parser = subparsers.add_parser("get-dataset", help="Get dataset information")
    get_dataset_parser.add_argument("--name", required=True, help="Dataset name")
    get_dataset_parser.add_argument("--version", default="latest", help="Dataset version (default: latest)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create registry
    registry = ModelRegistry()
    
    # Execute command
    if args.command == "register-model":
        metadata = json.loads(args.metadata) if args.metadata else None
        registry.register_model(args.name, args.path, args.version, metadata)
    
    elif args.command == "register-dataset":
        metadata = json.loads(args.metadata) if args.metadata else None
        registry.register_dataset(args.name, args.path, args.version, metadata)
    
    elif args.command == "list-models":
        models = registry.list_models()
        print(json.dumps(models, indent=2))
    
    elif args.command == "list-datasets":
        datasets = registry.list_datasets()
        print(json.dumps(datasets, indent=2))
    
    elif args.command == "get-model":
        model_info = registry.get_model(args.name, args.version)
        if model_info:
            print(json.dumps(model_info, indent=2))
    
    elif args.command == "get-dataset":
        dataset_info = registry.get_dataset(args.name, args.version)
        if dataset_info:
            print(json.dumps(dataset_info, indent=2))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
