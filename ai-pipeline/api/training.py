# ai-pipeline/api/training.py
"""
Training API endpoints for NOTICAL AI Pipeline
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any
import logging
import sys
import os

# Fix import paths
current_dir = os.path.dirname(os.path.abspath(__file__))
ai_pipeline_root = os.path.dirname(current_dir)
sys.path.insert(0, ai_pipeline_root)

try:
    from training.trainer import trainer
    logger = logging.getLogger(__name__)
    logger.info("✅ Training trainer imported successfully")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"❌ Training import error: {e}")
    raise

router = APIRouter(prefix="/training", tags=["training"])

@router.get("/status")
async def get_training_status():
    """Get current training status"""
    return trainer.get_training_status()

@router.get("/models")
async def get_models_status():
    """Get status of all models"""
    return trainer.evaluate_models()

@router.post("/prepare-data")
async def prepare_training_data(content_files: List[str]):
    """Prepare training data from content files"""
    try:
        training_data = trainer.prepare_training_data(content_files)
        return {
            "status": "success",
            "message": "Training data prepared successfully",
            "data": training_data
        }
    except Exception as e:
        logger.error(f"Error preparing training data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/concept-extractor")
async def train_concept_extractor():
    """Train the concept extraction model"""
    try:
        # Load existing training data
        training_data_path = trainer.training_data_path / "training_data.json"
        if not training_data_path.exists():
            raise HTTPException(status_code=400, detail="No training data available. Please prepare training data first.")
        
        with open(training_data_path, 'r', encoding='utf-8') as f:
            import json
            training_data = json.load(f)
        
        metrics = trainer.train_concept_extractor(training_data)
        return {
            "status": "success",
            "message": "Concept extractor trained successfully",
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Error training concept extractor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/difficulty-assessor")
async def train_difficulty_assessor():
    """Train the difficulty assessment model"""
    try:
        # Load existing training data
        training_data_path = trainer.training_data_path / "training_data.json"
        if not training_data_path.exists():
            raise HTTPException(status_code=400, detail="No training data available. Please prepare training data first.")
        
        with open(training_data_path, 'r', encoding='utf-8') as f:
            import json
            training_data = json.load(f)
        
        metrics = trainer.train_difficulty_assessor(training_data)
        return {
            "status": "success",
            "message": "Difficulty assessor trained successfully",
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Error training difficulty assessor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/subject-classifier")
async def train_subject_classifier():
    """Train the subject classification model"""
    try:
        # Load existing training data
        training_data_path = trainer.training_data_path / "training_data.json"
        if not training_data_path.exists():
            raise HTTPException(status_code=400, detail="No training data available. Please prepare training data first.")
        
        with open(training_data_path, 'r', encoding='utf-8') as f:
            import json
            training_data = json.load(f)
        
        metrics = trainer.train_subject_classifier(training_data)
        return {
            "status": "success",
            "message": "Subject classifier trained successfully",
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Error training subject classifier: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/all")
async def train_all_models():
    """Train all AI models"""
    try:
        # Load existing training data
        training_data_path = trainer.training_data_path / "training_data.json"
        if not training_data_path.exists():
            raise HTTPException(status_code=400, detail="No training data available. Please prepare training data first.")
        
        with open(training_data_path, 'r', encoding='utf-8') as f:
            import json
            training_data = json.load(f)
        
        summary = trainer.train_all_models([])  # Empty list since we're using existing data
        return {
            "status": "success",
            "message": "All models trained successfully",
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error training all models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-content")
async def upload_training_content(file: UploadFile = File(...)):
    """Upload content for training"""
    try:
        # Save uploaded file
        content_dir = trainer.training_data_path / "content"
        content_dir.mkdir(exist_ok=True)
        
        file_path = content_dir / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Analyze content for training
        with open(file_path, 'r', encoding='utf-8') as f:
            content_text = f.read()
        
        # Use AI Core to analyze
        from core.ai_core import ai_core
        analysis = ai_core.analyze_content_intelligently(content_text)
        
        return {
            "status": "success",
            "message": f"Content uploaded and analyzed successfully",
            "filename": file.filename,
            "analysis": {
                "complexity_score": analysis.get("complexity_score", 0),
                "key_concepts": len(analysis.get("key_concepts", [])),
                "subject_areas": analysis.get("subject_areas", [])
            }
        }
    except Exception as e:
        logger.error(f"Error uploading content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/content")
async def list_training_content():
    """List available training content"""
    try:
        content_dir = trainer.training_data_path / "content"
        if not content_dir.exists():
            return {"content_files": []}
        
        content_files = []
        for file_path in content_dir.glob("*.txt"):
            content_files.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "path": str(file_path)
            })
        
        return {"content_files": content_files}
    except Exception as e:
        logger.error(f"Error listing content: {e}")
        raise HTTPException(status_code=500, detail=str(e))
