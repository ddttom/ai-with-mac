#!/usr/bin/env python3

"""
Semantic versioning utility for ML models.
"""

import os
import re
import json
import argparse
from datetime import datetime

class MLVersioning:
    """
    Semantic versioning for machine learning models.
    
    MAJOR: Architecture changes
    MINOR: Training improvements
    PATCH: Bug fixes and minor adjustments
    """
    
    @staticmethod
    def parse_version(version_str):
        """Parse version string into components."""
        match = re.match(r'v?(\d+)\.(\d+)\.(\d+)', version_str)
        if not match:
            raise ValueError(f"Invalid version format: {version_str}")
        
        major, minor, patch = map(int, match.groups())
        return major, minor, patch
    
    @staticmethod
    def format_version(major, minor, patch):
        """Format version components into a string."""
        return f"v{major}.{minor}.{patch}"
    
    @staticmethod
    def increment_version(version_str, level="patch"):
        """
        Increment version at specified level.
        
        Args:
            version_str (str): Version string
            level (str): Level to increment (major, minor, patch)
            
        Returns:
            str: New version string
        """
        major, minor, patch = MLVersioning.parse_version(version_str)
        
        if level == "major":
            return MLVersioning.format_version(major + 1, 0, 0)
        elif level == "minor":
            return MLVersioning.format_version(major, minor + 1, 0)
        elif level == "patch":
            return MLVersioning.format_version(major, minor, patch + 1)
        else:
            raise ValueError(f"Invalid increment level: {level}")
    
    @staticmethod
    def update_model_version(model_dir, level="patch", metadata=None):
        """
        Update model version in metadata file.
        
        Args:
            model_dir (str): Model directory
            level (str): Level to increment
            metadata (dict, optional): Additional metadata
            
        Returns:
            str: New version string
        """
        metadata_file = os.path.join(model_dir, "metadata.json")
        
        # Load existing metadata or create new
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                model_metadata = json.load(f)
            
            current_version = model_metadata.get("version", "v0.0.0")
            new_version = MLVersioning.increment_version(current_version, level)
        else:
            # Start with v0.1.0 for new models
            if level == "major":
                new_version = "v1.0.0"
            elif level == "minor":
                new_version = "v0.1.0"
            else:
                new_version = "v0.0.1"
            
            model_metadata = {}
        
        # Update metadata
        model_metadata["version"] = new_version
        model_metadata["last_updated"] = datetime.now().isoformat()
        
        # Add additional metadata
        if metadata:
            model_metadata.update(metadata)
        
        # Save metadata
        with open(metadata_file, 'w') as f:
            json.dump(model_metadata, f, indent=2)
        
        return new_version
    
    @staticmethod
    def tag_model_version(model_dir, version=None):
        """
        Create a Git tag for a model version.
        
        Args:
            model_dir (str): Model directory
            version (str, optional): Version to tag
            
        Returns:
            bool: True if successful
        """
        try:
            # Get model name from directory
            model_name = os.path.basename(model_dir)
            
            # Get version from metadata if not provided
            if not version:
                metadata_file = os.path.join(model_dir, "metadata.json")
                if not os.path.exists(metadata_file):
                    print(f"Metadata file not found: {metadata_file}")
                    return False
                
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                version = metadata.get("version")
                if not version:
                    print("Version not found in metadata")
                    return False
            
            # Create a tag name
            tag_name = f"model-{model_name}-{version}"
            
            # Create git tag
            commit_msg = f"Model {model_name} version {version}"
            os.system(f'git tag -a "{tag_name}" -m "{commit_msg}"')
            
            print(f"Created git tag: {tag_name}")
            return True
            
        except Exception as e:
            print(f"Error creating git tag: {e}")
            return False

def main():
    """Main function for the versioning utility."""
    parser = argparse.ArgumentParser(description="Semantic versioning for ML models")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Increment version command
    increment_parser = subparsers.add_parser("increment", help="Increment model version")
    increment_parser.add_argument("--model-dir", required=True, help="Model directory")
    increment_parser.add_argument("--level", choices=["major", "minor", "patch"],
                                default="patch", help="Version level to increment")
    increment_parser.add_argument("--metadata", help="Additional metadata as JSON string")
    
    # Tag version command
    tag_parser = subparsers.add_parser("tag", help="Create git tag for model version")
    tag_parser.add_argument("--model-dir", required=True, help="Model directory")
    tag_parser.add_argument("--version", help="Version string (read from metadata if not provided)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "increment":
        metadata = json.loads(args.metadata) if args.metadata else None
        new_version = MLVersioning.update_model_version(args.model_dir, args.level, metadata)
        print(f"Updated model version to {new_version}")
    
    elif args.command == "tag":
        MLVersioning.tag_model_version(args.model_dir, args.version)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
