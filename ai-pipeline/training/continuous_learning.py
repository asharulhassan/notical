#!/usr/bin/env python3
"""
Continuous Learning Pipeline for NOTICAL
Retrains the model based on user feedback to improve flashcard quality
"""

import torch
import json
import os
from typing import Dict, List, Tuple
from transformers import (
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback
)
from datasets import Dataset
import numpy as np
from datetime import datetime
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContinuousLearningPipeline:
    """
    Pipeline for continuously improving the model based on user feedback
    """
    
    def __init__(self, model_path: str = "models/self_learning_llm"):
        self.model_path = model_path
        self.feedback_file = "models/feedback_data.json"
        self.training_history = []
        self.min_feedback_for_training = 10
        
        # Create necessary directories
        os.makedirs("models", exist_ok=True)
        os.makedirs("training_logs", exist_ok=True)
        
        logger.info("Continuous Learning Pipeline initialized")
    
    def prepare_training_data(self) -> Tuple[Dataset, Dataset]:
        """
        Prepare training data from user feedback
        
        Returns:
            Tuple of (train_dataset, eval_dataset)
        """
        if not os.path.exists(self.feedback_file):
            logger.warning("No feedback data found")
            return None, None
        
        try:
            with open(self.feedback_file, 'r') as f:
                feedback_data = json.load(f)
            
            if len(feedback_data) < self.min_feedback_for_training:
                logger.info(f"Not enough feedback for training. Need {self.min_feedback_for_training}, have {len(feedback_data)}")
                return None, None
            
            # Convert feedback to training examples
            training_examples = self._convert_feedback_to_training_data(feedback_data)
            
            # Split into train/eval
            split_idx = int(len(training_examples) * 0.8)
            train_data = training_examples[:split_idx]
            eval_data = training_examples[split_idx:]
            
            # Create datasets
            train_dataset = Dataset.from_list(train_data)
            eval_dataset = Dataset.from_list(eval_data)
            
            logger.info(f"Prepared {len(train_data)} training and {len(eval_data)} evaluation examples")
            return train_dataset, eval_dataset
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return None, None
    
    def _convert_feedback_to_training_data(self, feedback_data: List[Dict]) -> List[Dict]:
        """
        Convert user feedback into training examples
        
        Args:
            feedback_data: List of feedback dictionaries
            
        Returns:
            List of training examples
        """
        training_examples = []
        
        for feedback in feedback_data:
            if feedback.get('correction') and feedback.get('rating', 0) < 3:
                # User provided a correction - this is valuable training data
                example = {
                    'input_text': feedback.get('content_context', ''),
                    'target_text': feedback['correction'],
                    'rating': feedback['rating']
                }
                training_examples.append(example)
            
            elif feedback.get('rating', 0) >= 4:
                # High-rated flashcards - use as positive examples
                # We'll need to reconstruct the original flashcard
                example = {
                    'input_text': feedback.get('content_context', ''),
                    'target_text': self._reconstruct_flashcard(feedback),
                    'rating': feedback['rating']
                }
                training_examples.append(example)
        
        return training_examples
    
    def _reconstruct_flashcard(self, feedback: Dict) -> str:
        """
        Reconstruct the original flashcard from feedback
        This is a simplified version - in production you'd store the original
        """
        # For now, create a generic positive example
        return "Q: What is the main concept discussed?\nA: The main concept is clearly explained in the content."
    
    def train_model(self, model, tokenizer, train_dataset: Dataset, eval_dataset: Dataset) -> bool:
        """
        Train the model on the prepared data
        
        Args:
            model: The model to train
            tokenizer: The tokenizer
            train_dataset: Training dataset
            eval_dataset: Evaluation dataset
            
        Returns:
            True if training successful, False otherwise
        """
        try:
            logger.info("Starting model training...")
            
            # Tokenize datasets
            def tokenize_function(examples):
                inputs = tokenizer(
                    examples['input_text'],
                    truncation=True,
                    padding='max_length',
                    max_length=512,
                    return_tensors='pt'
                )
                
                targets = tokenizer(
                    examples['target_text'],
                    truncation=True,
                    padding='max_length',
                    max_length=256,
                    return_tensors='pt'
                )
                
                return {
                    'input_ids': inputs['input_ids'],
                    'attention_mask': inputs['attention_mask'],
                    'labels': targets['input_ids']
                }
            
            # Apply tokenization
            train_dataset = train_dataset.map(tokenize_function, batched=True)
            eval_dataset = eval_dataset.map(tokenize_function, batched=True)
            
            # Data collator
            data_collator = DataCollatorForSeq2Seq(
                tokenizer=tokenizer,
                model=model,
                padding=True
            )
            
            # Training arguments
            training_args = TrainingArguments(
                output_dir="training_logs",
                evaluation_strategy="steps",
                eval_steps=50,
                save_steps=100,
                learning_rate=5e-5,
                per_device_train_batch_size=2,
                per_device_eval_batch_size=2,
                num_train_epochs=3,
                weight_decay=0.01,
                logging_dir="training_logs",
                logging_steps=10,
                save_total_limit=2,
                load_best_model_at_end=True,
                metric_for_best_model="eval_loss",
                greater_is_better=False,
                dataloader_pin_memory=False,
                remove_unused_columns=False,
                report_to=None,  # Disable wandb for now
            )
            
            # Initialize trainer
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=eval_dataset,
                data_collator=data_collator,
                callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
            )
            
            # Train the model
            logger.info("Training started...")
            trainer.train()
            
            # Save the trained model
            trainer.save_model(self.model_path)
            tokenizer.save_pretrained(self.model_path)
            
            # Log training results
            training_result = {
                'timestamp': datetime.now().isoformat(),
                'training_examples': len(train_dataset),
                'eval_examples': len(eval_dataset),
                'final_eval_loss': trainer.evaluate()['eval_loss']
            }
            
            self.training_history.append(training_result)
            self._save_training_history()
            
            logger.info(f"Training completed successfully! Final eval loss: {training_result['final_eval_loss']:.4f}")
            return True
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False
    
    def _save_training_history(self):
        """Save training history to disk"""
        try:
            history_file = "models/training_history.json"
            with open(history_file, 'w') as f:
                json.dump(self.training_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving training history: {e}")
    
    def get_training_status(self) -> Dict:
        """Get current training status"""
        status = {
            'feedback_samples': 0,
            'ready_for_training': False,
            'last_training': None,
            'training_history': len(self.training_history)
        }
        
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    feedback_data = json.load(f)
                status['feedback_samples'] = len(feedback_data)
                status['ready_for_training'] = len(feedback_data) >= self.min_feedback_for_training
            except:
                pass
        
        if self.training_history:
            status['last_training'] = self.training_history[-1]['timestamp']
        
        return status
    
    def cleanup_old_feedback(self, max_samples: int = 1000):
        """
        Clean up old feedback data to prevent dataset from growing too large
        
        Args:
            max_samples: Maximum number of feedback samples to keep
        """
        if not os.path.exists(self.feedback_file):
            return
        
        try:
            with open(self.feedback_file, 'r') as f:
                feedback_data = json.load(f)
            
            if len(feedback_data) > max_samples:
                # Keep the most recent feedback
                feedback_data = sorted(feedback_data, key=lambda x: x.get('timestamp', ''))[-max_samples:]
                
                with open(self.feedback_file, 'w') as f:
                    json.dump(feedback_data, f, indent=2)
                
                logger.info(f"Cleaned up feedback data. Kept {len(feedback_data)} most recent samples.")
        
        except Exception as e:
            logger.error(f"Error cleaning up feedback: {e}")
    
    def run_continuous_learning_cycle(self, model, tokenizer) -> bool:
        """
        Run a complete continuous learning cycle
        
        Args:
            model: The model to improve
            tokenizer: The tokenizer
            
        Returns:
            True if cycle completed successfully
        """
        logger.info("Starting continuous learning cycle...")
        
        # Check if we have enough feedback
        status = self.get_training_status()
        if not status['ready_for_training']:
            logger.info("Not enough feedback for training cycle")
            return False
        
        # Prepare training data
        train_dataset, eval_dataset = self.prepare_training_data()
        if not train_dataset or not eval_dataset:
            logger.warning("Could not prepare training data")
            return False
        
        # Train the model
        success = self.train_model(model, tokenizer, train_dataset, eval_dataset)
        
        if success:
            # Clean up old feedback after successful training
            self.cleanup_old_feedback()
            
            # Reset feedback data (since we've learned from it)
            self._reset_feedback_after_training()
        
        return success
    
    def _reset_feedback_after_training(self):
        """Reset feedback data after successful training"""
        try:
            # Archive the feedback data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = f"models/feedback_archive_{timestamp}.json"
            
            if os.path.exists(self.feedback_file):
                os.rename(self.feedback_file, archive_file)
                logger.info(f"Feedback archived to {archive_file}")
            
            # Create empty feedback file
            with open(self.feedback_file, 'w') as f:
                json.dump([], f)
                
        except Exception as e:
            logger.error(f"Error resetting feedback: {e}")
