#!/usr/bin/env python3
"""
A simple script to check your Mac hardware specs for AI readiness.

This is a basic example from Part 1 of the AI with Mac series.
"""
import platform
import os
import subprocess
import re
import sys

def get_mac_model():
    """Get the Mac model identifier."""
    try:
        result = subprocess.run(['sysctl', 'hw.model'], capture_output=True, text=True)
        if result.returncode == 0:
            match = re.search(r'hw.model: (.*)', result.stdout)
            if match:
                return match.group(1)
    except Exception:
        pass
    return "Unknown Mac Model"

def is_apple_silicon():
    """Check if the Mac is running on Apple Silicon."""
    return platform.processor() == 'arm' or 'arm' in platform.machine().lower()

def get_total_memory():
    """Get the total system memory in GB."""
    try:
        result = subprocess.run(['sysctl', 'hw.memsize'], capture_output=True, text=True)
        if result.returncode == 0:
            match = re.search(r'hw.memsize: (\d+)', result.stdout)
            if match:
                return int(match.group(1)) / (1024**3)  # Convert to GB
    except Exception:
        pass
    
    # Fallback
    import psutil
    try:
        return psutil.virtual_memory().total / (1024**3)
    except:
        return 0

def get_ai_readiness_score(is_silicon, memory_gb):
    """Calculate a simple AI readiness score for the Mac."""
    base_score = 0
    
    # Apple Silicon is a major factor
    if is_silicon:
        base_score += 50
    else:
        return 0  # Intel Macs get a zero score for this AI series
    
    # Memory is important for running models
    if memory_gb >= 128:
        base_score += 50  # Mac Studio/Pro territory
    elif memory_gb >= 64:
        base_score += 40  # High-end MacBook Pro
    elif memory_gb >= 32:
        base_score += 30  # Mid-range
    elif memory_gb >= 16:
        base_score += 20  # Base MacBook Pro
    elif memory_gb >= 8:
        base_score += 10  # Base models
    
    return base_score

def main():
    """Main function to check Mac hardware and display AI readiness."""
    print("=" * 60)
    print("Mac AI Readiness Check")
    print("=" * 60)
    
    # Get basic info
    mac_model = get_mac_model()
    is_silicon = is_apple_silicon()
    memory_gb = get_total_memory()
    
    # Display information
    print(f"Mac Model: {mac_model}")
    print(f"Processor Type: {'Apple Silicon' if is_silicon else 'Intel'}")
    print(f"Total Memory: {memory_gb:.1f} GB")
    print(f"macOS Version: {platform.mac_ver()[0]}")
    
    # Calculate and display AI readiness
    ai_score = get_ai_readiness_score(is_silicon, memory_gb)
    
    print("\nAI Readiness Assessment:")
    if ai_score >= 80:
        print("✅ Excellent! Your Mac is well-equipped for all AI tasks.")
        print("   You can run large language models and train custom models.")
    elif ai_score >= 60:
        print("✅ Very Good! Your Mac can handle most AI workloads.")
        print("   Large models and training should work well.")
    elif ai_score >= 40:
        print("✅ Good! Your Mac is suitable for many AI tasks.")
        print("   You can run medium-sized models effectively.")
    elif ai_score >= 20:
        print("🟡 Moderate. Your Mac can run smaller AI models.")
        print("   Quantized models will work best.")
    elif ai_score > 0:
        print("🟡 Limited. Your Mac has basic AI capabilities.")
        print("   Focus on the smallest models and optimization.")
    else:
        print("❌ Not compatible with this series.")
        print("   This series focuses on Apple Silicon Macs.")
    
    print(f"\nAI Readiness Score: {ai_score}/100")
    
    # Recommendation
    print("\nRecommendation:")
    if not is_silicon:
        print("This series is designed for Apple Silicon Macs.")
        print("Consider upgrading to a Mac with Apple Silicon for AI tasks.")
    elif memory_gb < 8:
        print("Your Mac has limited memory for AI tasks.")
        print("Consider upgrading if you plan to do serious AI work.")
    elif memory_gb < 16:
        print("For optimal AI performance, consider using smaller, quantized models.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
