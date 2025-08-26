#!/usr/bin/env python3
"""
NOTICAL AI Model Training Script
================================
Script to train all AI models for the pipeline.
"""

import sys
import os
import logging
from pathlib import Path

# Add core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from training.trainer import trainer
from core.enhanced_ai_core import enhanced_ai_core

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main training function"""
    logger.info("🚀 Starting NOTICAL AI Model Training...")
    
    try:
        # Check if we have training data
        training_data_path = Path("data/training/training_data.json")
        if not training_data_path.exists():
            logger.warning("⚠️  No training data found. Creating sample training data...")
            
            # Create sample content files
            sample_content_dir = Path("data/training/content")
            sample_content_dir.mkdir(parents=True, exist_ok=True)
            
            # Create sample content
            sample_content = """
            Computer Memory Systems
            
            Computer memory systems are essential components that store and retrieve data for processing. 
            There are several types of memory, each serving different purposes in the computing hierarchy.
            
            RAM (Random Access Memory) is volatile memory that provides fast access to data and instructions. 
            It loses its contents when power is turned off, but offers the fastest read and write speeds.
            
            ROM (Read-Only Memory) is non-volatile memory that contains permanent instructions and data. 
            It cannot be modified during normal operation and retains data even when power is off.
            
            Cache memory is a small, high-speed memory that stores frequently accessed data. It acts as a 
            buffer between the CPU and main memory, significantly improving system performance.
            
            Memory hierarchy refers to the organization of different memory types based on speed, cost, and capacity. 
            The hierarchy typically includes CPU registers, cache, RAM, and storage devices.
            
            Memory controllers manage data flow between the CPU and memory modules. They optimize memory 
            access patterns and ensure data integrity through error correction mechanisms.
            
            Performance optimization in memory systems involves balancing speed, capacity, and cost. 
            Techniques include caching strategies, memory mapping, and bandwidth optimization.
            """
            
            with open(sample_content_dir / "computer_memory.txt", 'w', encoding='utf-8') as f:
                f.write(sample_content)
            
            # Prepare training data
            logger.info("📚 Preparing training data...")
            training_data = trainer.prepare_training_data([str(sample_content_dir / "computer_memory.txt")])
            logger.info(f"✅ Training data prepared: {len(training_data['concepts'])} concepts")
        
        # Train all models
        logger.info("🧠 Training all AI models...")
        training_summary = trainer.train_all_models([])
        
        logger.info("🎉 Training completed successfully!")
        logger.info(f"📊 Models trained: {training_summary['models_trained']}")
        logger.info(f"📈 Overall accuracy: {training_summary['overall_accuracy']:.2f}")
        
        # Test enhanced AI core
        logger.info("🧪 Testing enhanced AI core...")
        test_text = """
        Dynamic RAM (DRAM) is a type of volatile memory that stores each bit of data in a separate 
        capacitor within an integrated circuit. The capacitor can be either charged or discharged, 
        representing the two values of a bit, conventionally called 0 and 1.
        """
        
        analysis = enhanced_ai_core.analyze_content_intelligently(test_text)
        logger.info(f"✅ AI Core test successful: Complexity={analysis.get('complexity_score', 0)}, Concepts={len(analysis.get('key_concepts', []))}")
        
        # Get learning stats
        stats = enhanced_ai_core.get_learning_stats()
        logger.info(f"📚 Learning stats: {stats['total_examples']} examples, {stats['models_loaded']['concept_extractor']} models loaded")
        
        logger.info("🎯 NOTICAL AI Pipeline is ready for production!")
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
