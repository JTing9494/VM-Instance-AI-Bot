import sys
import os
# Add the current directory to the path so we can import vm2-backend as a module
sys.path.append('.')

print("Testing imports...")

# Since we can't directly import from a directory with a hyphen in the name,
# we'll test by trying to import the modules directly
try:
    # Add the vm2-backend directory to the path
    sys.path.append('./vm2-backend')
    from app.main import app
    print("✓ FastAPI app imported successfully")
except Exception as e:
    print(f"✗ Failed to import app: {e}")
    # Remove the added path to avoid conflicts
    if './vm2-backend' in sys.path:
        sys.path.remove('./vm2-backend')

# Test routers
try:
    sys.path.append('./vm2-backend')
    from app.routers import auth_router, data_router, chat_router
    print("✓ All routers imported successfully")
except Exception as e:
    print(f"✗ Failed to import routers: {e}")
finally:
    if './vm2-backend' in sys.path:
        sys.path.remove('./vm2-backend')

# Test auth module
try:
    sys.path.append('./vm2-backend')
    from app.auth import get_current_user
    print("✓ Auth module imported successfully")
except Exception as e:
    print(f"✗ Failed to import auth: {e}")
finally:
    if './vm2-backend' in sys.path:
        sys.path.remove('./vm2-backend')

# Test gemini service
try:
    sys.path.append('./vm2-backend')
    from app.services.gemini_service import GeminiService
    print("✓ Gemini service imported successfully")
except Exception as e:
    print(f"✗ Failed to import gemini service: {e}")
finally:
    if './vm2-backend' in sys.path:
        sys.path.remove('./vm2-backend')

print("Import test completed.")