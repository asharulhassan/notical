# NOTICAL AI Learning Platform
# Clean imports for working modules only

__version__ = "1.0.0"
__author__ = "NOTICAL Team"

# Only import working modules
try:
    from .ai_core import ai_core
    __all__ = ['ai_core']
except ImportError as e:
    print(f"Warning: Could not import ai_core: {e}")
    __all__ = []
