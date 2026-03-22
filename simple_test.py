#!/usr/bin/env python
"""Simple test to verify imports work"""

import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Add the script directory to Python path
sys.path.insert(0, script_dir)

# Now try to import using the underscore version
try:
    # Add the vm2-backend directory to the path
    vm2_backend_path = os.path.join(script_dir, 'vm2-backend')
    print(f"Adding {vm2_backend_path} to path")
    sys.path.insert(0, vm2_backend_path)
    
    # Now import from app (which should be found in vm2-backend/app)
    from app.main import app
    print("✓ Successfully imported app from vm2-backend")
    
    # Clean up
    sys.path.remove(vm2_backend_path)
    
except Exception as e:
    print(f"✗ Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    
    # Clean up if needed
    vm2_backend_path = os.path.join(script_dir, 'vm2-backend')
    if vm2_backend_path in sys.path:
        sys.path.remove(vm2_backend_path)

# Test the routers
try:
    vm2_backend_path = os.path.join(script_dir, 'vm2-backend')
    if vm2_backend_path not in sys.path:
        sys.path.insert(0, vm2_backend_path)
        
    from app.routers import auth_router, data_router, chat_router
    print("✓ Successfully imported routers")
    
    # Clean up
    sys.path.remove(vm2_backend_path)
    
except Exception as e:
    print(f"✗ Failed to import routers: {e}")
    import traceback
    traceback.print_exc()
    
    # Clean up if needed
    vm2_backend_path = os.path.join(script_dir, 'vm2-backend')
    if vm2_backend_path in sys.path:
        sys.path.remove(vm2_backend_path)

print("Test completed.")