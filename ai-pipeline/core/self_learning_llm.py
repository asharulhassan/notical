#!/usr/bin/env python3
"""
Self-Learning LLM Core for NOTICAL
Replaces rule-based system with real AI that learns from user feedback
"""

import torch
import json
import os
from typing import Dict, List, Optional, Tuple
from transformers import (
    AutoTokenizer, 
    AutoModelForSeq2SeqLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from datasets import Dataset
import numpy as np
from datetime import datetime
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelfLearningLLM:
    """
    Self-Learning LLM that continuously improves from user feedback
    """
    
    def __init__(self, model_name: str = "google/flan-t5-base", device: str = "auto"):
        """
        Initialize the self-learning LLM
        
        Args:
            model_name: Base model to use (flan-t5-small is faster for MVP testing)
            device: Device to use (auto will detect GPU)
        """
        print("🚀 Initializing Self-Learning LLM...")
        
        # Model configuration
        self.model_name = "google/flan-t5-base"  # Use the base model you already have
        self.model_path = "models/self_learning_llm"  # Point to your existing model
        self.device = self._setup_device(device)
        self.model = None
        self.tokenizer = None
        self.training_data = []
        self.feedback_data = []
        
        # Create models directory if it doesn't exist
        os.makedirs("models", exist_ok=True)
        
        print(f"📍 Using device: {self.device}")
        print(f"📁 Model path: {self.model_path}")
        
        # Initialize the model
        self._load_or_download_model()
        
        print("✅ Self-Learning LLM initialized successfully!")
        logger.info(f"Self-Learning LLM initialized on device: {self.device}")
    
    def _setup_device(self, device: str) -> str:
        """Setup the best available device"""
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                logger.info(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
            else:
                device = "cpu"
                logger.warning("CUDA not available, using CPU (training will be slow)")
        return device
    
    def _load_or_download_model(self):
        """Load existing model or download base model"""
        if os.path.exists(self.model_path):
            logger.info("Loading existing trained model...")
            self._load_model()
        else:
            logger.info(f"Downloading base model: {self.model_name}")
            self._download_base_model()
    
    def _download_base_model(self):
        """Download the base model from HuggingFace"""
        try:
            logger.info("Downloading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            logger.info("Downloading model...")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            # Save the base model
            self._save_model()
            logger.info("Base model downloaded and saved successfully!")
            
        except Exception as e:
            logger.error(f"Error downloading model: {e}")
            raise
    
    def _load_model(self):
        """Load existing trained model with real-time status"""
        try:
            print("🔄 Loading existing trained model...")
            logger.info("🔄 Loading existing trained model...")
            
            # Load tokenizer
            print("📥 Loading tokenizer...")
            start_time = time.time()
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            tokenizer_time = time.time() - start_time
            print(f"✅ Tokenizer loaded in {tokenizer_time:.1f} seconds")
            
            # Load model
            print("📥 Loading model weights...")
            start_time = time.time()
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            model_time = time.time() - start_time
            print(f"✅ Model loaded in {model_time:.1f} seconds")
            
            print("✅ Existing model loaded successfully!")
            logger.info("Existing model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            logger.error(f"Error loading model: {e}")
            print("📥 Downloading fresh base model...")
            logger.info("Downloading fresh base model...")
            self._download_base_model()
    
    def _save_model(self):
        """Save the current model"""
        try:
            self.model.save_pretrained(self.model_path)
            self.tokenizer.save_pretrained(self.model_path)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def generate_flashcards(self, content: str, num_cards: int = 5) -> List[Dict]:
        """
        Generate flashcards using the trained model
        
        Args:
            content: The content to generate flashcards from
            num_cards: Number of flashcards to generate
            
        Returns:
            List of flashcard dictionaries
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded")
        
        try:
            # Create prompt for flashcard generation
            prompt = f"""Generate {num_cards} high-quality flashcards from this content:

Content: {content}

Instructions:
1. Create clear, complete questions
2. Provide accurate, contextual answers
3. Focus on key concepts and important details
4. Make questions specific and relevant

Format each flashcard as:
Q: [Complete question]
A: [Detailed answer]

Flashcards:"""

            # Tokenize input
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                max_length=1024, 
                truncation=True
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=512,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Parse flashcards from response
            flashcards = self._parse_flashcards(response, content)
            
            # If parsing failed, use fallback generation
            if not flashcards:
                logger.info("Parsing failed, using fallback generation")
                flashcards = self._fallback_generation(content, num_cards)
            
            # Ensure we have the right number of cards (with timeout protection)
            max_attempts = 2  # Reduced attempts to prevent crashes
            attempts = 0
            
            while len(flashcards) < num_cards and attempts < max_attempts:
                attempts += 1
                logger.info(f"Attempt {attempts}: Generating additional card (have {len(flashcards)}, need {num_cards})")
                
                # Generate additional cards if needed
                additional = self._generate_single_card(content)
                if additional:
                    flashcards.append(additional)
                    logger.info(f"Successfully generated additional card {len(flashcards)}")
                else:
                    logger.warning(f"Failed to generate additional card on attempt {attempts}")
                    break  # Stop if we can't generate more
            
            if len(flashcards) < num_cards:
                logger.warning(f"Only generated {len(flashcards)} cards instead of requested {num_cards}")
            
            return flashcards[:num_cards]
            
        except Exception as e:
            logger.error(f"Error generating flashcards: {e}")
            # Fallback to basic generation
            return self._fallback_generation(content, num_cards)
    
    def _parse_flashcards(self, response: str, content: str) -> List[Dict]:
        """Parse flashcards from model response"""
        flashcards = []
        
        # Split by "Question:" to find individual Q&A pairs
        parts = response.split("Question:")
        
        for part in parts[1:]:  # Skip first part (before first Question:)
            if "Answer:" in part:
                # Split by "Answer:" to separate question and answer
                qa_parts = part.split("Answer:", 1)
                if len(qa_parts) == 2:
                    question = qa_parts[0].strip()
                    answer = qa_parts[1].strip()
                    
                    # Clean up the answer (remove any trailing text)
                    if "\n" in answer:
                        answer = answer.split("\n")[0].strip()
                    
                    if question and answer:
                        flashcards.append({
                            'question': question,
                            'answer': answer,
                            'content_context': content[:200] + "..." if len(content) > 200 else content
                        })
        
        logger.info(f"Parsed {len(flashcards)} flashcards from response")
        return flashcards
    
    def _generate_single_card(self, content: str) -> Optional[Dict]:
        """Generate a single flashcard"""
        try:
            prompt = f"Generate one flashcard from this content:\n\nContent: {content}\n\nQ: "
            
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=256,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Simple parsing
            if 'Q:' in response and 'A:' in response:
                parts = response.split('A:')
                question = parts[0].replace('Q:', '').strip()
                answer = parts[1].strip()
                
                return {
                    'question': question,
                    'answer': answer,
                    'content_context': content[:200] + "..." if len(content) > 200 else content
                }
        
        except Exception as e:
            logger.error(f"Error generating single card: {e}")
        
        return None
    
    def _fallback_generation(self, content: str, num_cards: int) -> List[Dict]:
        """Fallback generation if main method fails"""
        logger.warning("Using fallback generation method")
        
        # Simple keyword-based generation as fallback
        words = content.split()
        important_words = [w for w in words if len(w) > 5 and w.isalpha()]
        
        flashcards = []
        for i in range(min(num_cards, len(important_words))):
            word = important_words[i]
            flashcards.append({
                'question': f"What is {word}?",
                'answer': f"{word} is a term mentioned in the content.",
                'content_context': content[:200] + "..." if len(content) > 200 else content
            })
        
        return flashcards
    
    def collect_feedback(self, flashcard_id: str, user_rating: int, user_correction: str = None):
        """
        Collect user feedback for continuous learning
        
        Args:
            flashcard_id: ID of the flashcard
            user_rating: 1-5 rating (1=bad, 5=excellent)
            user_correction: User's corrected version if rating < 3
        """
        feedback = {
            'flashcard_id': flashcard_id,
            'rating': user_rating,
            'correction': user_correction,
            'timestamp': datetime.now().isoformat()
        }
        
        self.feedback_data.append(feedback)
        logger.info(f"Feedback collected: {feedback}")
        
        # Save feedback to disk
        self._save_feedback()
        
        # Retrain if we have enough feedback
        if len(self.feedback_data) >= 10:
            logger.info("Enough feedback collected, scheduling retraining...")
            self._schedule_retraining()
    
    def _save_feedback(self):
        """Save feedback data to disk"""
        try:
            feedback_file = "models/feedback_data.json"
            with open(feedback_file, 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
            logger.info(f"Feedback saved to {feedback_file}")
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
    
    def _schedule_retraining(self):
        """Schedule model retraining with collected feedback"""
        # This will be implemented in the training pipeline
        logger.info("Retraining scheduled - will be handled by training pipeline")
    
    def get_model_stats(self) -> Dict:
        """Get current model statistics"""
        if not self.model:
            return {"status": "Model not loaded"}
        
        stats = {
            "model_name": self.model_name,
            "device": self.device,
            "total_parameters": sum(p.numel() for p in self.model.parameters()),
            "trainable_parameters": sum(p.numel() for p in self.model.parameters() if p.requires_grad),
            "feedback_samples": len(self.feedback_data),
            "model_path": self.model_path
        }
        
        if self.device == "cuda":
            stats["gpu_memory_allocated"] = torch.cuda.memory_allocated(0)
            stats["gpu_memory_reserved"] = torch.cuda.memory_reserved(0)
        
        return stats
