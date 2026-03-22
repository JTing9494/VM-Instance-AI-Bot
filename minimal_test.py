#!/usr/bin/env python
"""Minimal test to verify FastAPI works"""

import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
print("Script directory:", script_dir)

# Add the script directory to Python path
sys.path.insert(0, script_dir)

# Try importing FastAPI directly
try:
    import fastapi
    print("FastAPI version", fastapi.__version__, "imported successfully")
except Exception as e:
    print("Failed to import FastAPI:", e)
    import traceback
    traceback.print_exc()

# Try importing uvicorn
try:
    import uvicorn
    print("Uvicorn imported successfully")
except Exception as e:
    print("Failed to import uvicorn:", e)

print("Minimal test completed.")