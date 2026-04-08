"""
Invoice Dispute Resolution Environment — HuggingFace Entry Point

This is the entry point for HuggingFace Spaces deployment.
It imports and exposes the FastAPI app from server.app
"""

import os
import sys

# Add the server module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app from server.app
from server.app import app

# The app is now available for HuggingFace to serve
# HuggingFace will run: python -m uvicorn app:app --host 0.0.0.0 --port 7860

if __name__ == "__main__":
    import uvicorn
    # Run directly
    uvicorn.run(app, host="0.0.0.0", port=7860)
