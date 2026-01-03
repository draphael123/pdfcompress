import os
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, parent_dir)

# Import the Flask app
from app import app as application

# Export for Vercel
app = application

