# ai-pipeline/training/__init__.py
"""
Training package for NOTICAL AI Pipeline
"""

from .trainer import trainer

# Import router from api.training
try:
    from ..api.training import router
except ImportError:
    # If we can't import the router, create a placeholder
    from fastapi import APIRouter
    router = APIRouter(prefix="/training", tags=["training"])
    
    @router.get("/placeholder")
    async def placeholder():
        return {"message": "Training router placeholder"}

__all__ = ['trainer', 'router']
