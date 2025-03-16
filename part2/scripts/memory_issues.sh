#!/bin/bash
# Set environment variable to prevent NumPy from allocating too much memory during initialization
export NUMPY_MAX_OPEN_FILES=256

# For extremely large operations, you may need to increase system limits
ulimit -n 4096  # Increase open file limit
