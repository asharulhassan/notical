import json
import os
import time
import random
from typing import Dict, List, Tuple
import numpy as np
from collections import defaultdict
import sys

class AITrainingPipeline:
    """
    AI Training Pipeline for NoticalAI-Master
    Trains the model on our massive flashcard dataset and evaluates performance
    """
    
    def __init__(self):
        self.model_name = "NoticalAI-Master"
        self.version = "1.0.0"
        self.training_data = {}
        self.testing_data = {}
        self.model_weights = {}
        self.training_history = []
        self.performance_metrics = {}
        
        # Training parameters
        self.epochs = 100
        self.learning_rate = 0.001
        self.batch_size = 32
        self.validation_split = 0.2
        
        print(f"🚀 Initializing {self.model_name} Training Pipeline")
        print("=" * 80)
    
    def progress_bar(self, current: int, total: int, prefix: str = "", suffix: str = "", length: int = 50):
        """Display a progress bar with percentage and time estimation"""
        filled = int(length * current // total)
        bar = '█' * filled + '-' * (length - filled)
        percent = current / total * 100
        
        # Calculate time remaining if we have timing data
        if hasattr(self, 'start_time') and current > 0:
            elapsed = time.time() - self.start_time
            rate = current / elapsed
            remaining = (total - current) / rate if rate > 0 else 0
            time_str = f"ETA: {remaining:.1f}s"
        else:
            time_str = ""
        
        print(f'\r{prefix} |{bar}| {percent:.1f}% {suffix} {time_str}', end='', flush=True)
        
        if current == total:
            print()  # New line when complete
    
    def load_training_data(self):
        """Load all training data from our massive dataset"""
        print("📚 Loading training data...")
        
        training_files = [
            'massive_english_training.json',
            'massive_humanities_training.json', 
            'massive_complex_subjects_training.json'
        ]
        
        total_training_cards = 0
        
        for i, file_name in enumerate(training_files):
            try:
                with open(f'generated_flashcards/{file_name}', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                domain = file_name.replace('massive_', '').replace('_training.json', '')
                self.training_data[domain] = {
                    'cards': data['cards'],
                    'total_cards': data['total_cards'],
                    'categories': data.get('categories', [])
                }
                
                total_training_cards += data['total_cards']
                
                # Progress bar for loading
                self.progress_bar(i + 1, len(training_files), 
                                prefix="Loading", 
                                suffix=f"{data['total_cards']:,} {domain} cards")
                
            except Exception as e:
                print(f"❌ Error loading {file_name}: {e}")
        
        print(f"\n🎯 Total training data: {total_training_cards:,} cards")
        return total_training_cards
    
    def load_testing_data(self):
        """Load all testing data for evaluation"""
        print("🧪 Loading testing data...")
        
        testing_files = [
            'massive_english_testing.json',
            'massive_humanities_testing.json',
            'massive_complex_subjects_testing.json'
        ]
        
        total_testing_cards = 0
        
        for i, file_name in enumerate(testing_files):
            try:
                with open(f'generated_flashcards/{file_name}', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                domain = file_name.replace('massive_', '').replace('_testing.json', '')
                self.testing_data[domain] = {
                    'cards': data['cards'],
                    'total_cards': data['total_cards'],
                    'categories': data.get('categories', [])
                }
                
                total_testing_cards += data['total_cards']
                
                # Progress bar for loading
                self.progress_bar(i + 1, len(testing_files), 
                                prefix="Loading", 
                                suffix=f"{data['total_cards']:,} {domain} cards")
                
            except Exception as e:
                print(f"❌ Error loading {file_name}: {e}")
        
        print(f"\n🎯 Total testing data: {total_testing_cards:,} cards")
        return total_testing_cards
    
    def preprocess_data(self):
        """Preprocess training data for model training"""
        print("🔧 Preprocessing training data...")
        
        processed_data = {
            'questions': [],
            'answers': [],
            'subjects': [],
            'difficulties': [],
            'categories': []
        }
        
        total_cards = sum(len(data['cards']) for data in self.training_data.values())
        processed_count = 0
        
        # Process each domain
        for domain, data in self.training_data.items():
            print(f"  Processing {domain} domain...")
            
            for card in data['cards']:
                # Extract question (front)
                question = card.get('front', '')
                if question and len(question.strip()) > 5:
                    processed_data['questions'].append(question.strip())
                    
                    # Extract answer (back)
                    answer = card.get('back', '')
                    if answer and len(answer.strip()) > 10:
                        processed_data['answers'].append(answer.strip())
                    else:
                        processed_data['answers'].append("No answer provided")
                    
                    # Extract metadata
                    processed_data['subjects'].append(domain)
                    processed_data['difficulties'].append(card.get('difficulty', 'medium'))
                    processed_data['categories'].append(card.get('category', 'general'))
                
                processed_count += 1
                
                # Progress bar for preprocessing
                if processed_count % 100 == 0 or processed_count == total_cards:
                    self.progress_bar(processed_count, total_cards, 
                                    prefix="Preprocessing", 
                                    suffix=f"{processed_count:,}/{total_cards:,} cards")
        
        print(f"\n✅ Preprocessed {len(processed_data['questions']):,} question-answer pairs")
        return processed_data
    
    def initialize_model_weights(self, vocab_size: int, embedding_dim: int = 128):
        """Initialize model weights for training"""
        print("⚖️ Initializing model weights...")
        
        # Simple neural network weights (can be enhanced with more sophisticated architectures)
        self.model_weights = {
            'embedding_weights': np.random.randn(vocab_size, embedding_dim) * 0.1,
            'question_encoder': np.random.randn(embedding_dim, embedding_dim) * 0.1,
            'answer_encoder': np.random.randn(embedding_dim, embedding_dim) * 0.1,
            'classifier': np.random.randn(embedding_dim, 1) * 0.1,
            'bias_terms': {
                'question_bias': np.zeros(embedding_dim),
                'answer_bias': np.zeros(embedding_dim),
                'classifier_bias': np.zeros(1)
            }
        }
        
        print(f"✅ Initialized model weights with {embedding_dim} dimensions")
        return self.model_weights
    
    def create_vocabulary(self, processed_data: Dict) -> Dict:
        """Create vocabulary from training data"""
        print("📖 Creating vocabulary...")
        
        # Combine all text
        all_text = ' '.join(processed_data['questions'] + processed_data['answers'])
        
        # Simple word tokenization
        words = all_text.lower().split()
        word_counts = defaultdict(int)
        
        total_words = len(words)
        processed_words = 0
        
        for word in words:
            if len(word) > 2:  # Filter out very short words
                word_counts[word] += 1
            
            processed_words += 1
            
            # Progress bar for vocabulary creation
            if processed_words % 1000 == 0 or processed_words == total_words:
                self.progress_bar(processed_words, total_words, 
                                prefix="Vocabulary", 
                                suffix=f"{processed_words:,}/{total_words:,} words")
        
        # Create vocabulary (top words)
        vocab_size = 10000  # Limit vocabulary size
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        vocabulary = {word: idx for idx, (word, count) in enumerate(sorted_words[:vocab_size])}
        
        # Add special tokens
        vocabulary['<PAD>'] = len(vocabulary)
        vocabulary['<UNK>'] = len(vocabulary)
        vocabulary['<START>'] = len(vocabulary)
        vocabulary['<END>'] = len(vocabulary)
        
        print(f"\n✅ Created vocabulary with {len(vocabulary):,} words")
        return vocabulary
    
    def text_to_sequence(self, text: str, vocabulary: Dict, max_length: int = 50) -> List[int]:
        """Convert text to sequence of indices"""
        words = text.lower().split()
        sequence = []
        
        for word in words[:max_length]:
            if word in vocabulary:
                sequence.append(vocabulary[word])
            else:
                sequence.append(vocabulary['<UNK>'])
        
        # Pad to max_length
        while len(sequence) < max_length:
            sequence.append(vocabulary['<PAD>'])
        
        return sequence
    
    def train_model(self, processed_data: Dict, vocabulary: Dict):
        """Train the model on the processed data"""
        print(f"🚀 Starting model training...")
        print(f"📊 Training on {len(processed_data['questions']):,} examples")
        print(f"⏱️  Epochs: {self.epochs}, Batch Size: {self.batch_size}")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # Training loop
        for epoch in range(self.epochs):
            epoch_start = time.time()
            
            # Shuffle data
            indices = list(range(len(processed_data['questions'])))
            random.shuffle(indices)
            
            total_loss = 0
            batch_count = 0
            
            # Calculate total batches for progress bar
            total_batches = len(indices) // self.batch_size + (1 if len(indices) % self.batch_size > 0 else 0)
            
            # Process in batches
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                batch_loss = self.train_batch(batch_indices, processed_data, vocabulary)
                
                total_loss += batch_loss
                batch_count += 1
                
                # Progress bar for epoch
                self.progress_bar(batch_count, total_batches, 
                                prefix=f"Epoch {epoch+1}/{self.epochs}", 
                                suffix=f"Loss: {batch_loss:.4f}")
            
            # Calculate epoch metrics
            avg_epoch_loss = total_loss / batch_count
            epoch_time = time.time() - epoch_start
            
            # Store training history
            self.training_history.append({
                'epoch': epoch + 1,
                'loss': avg_epoch_loss,
                'time': epoch_time,
                'batch_count': batch_count
            })
            
            # Print epoch summary
            print(f"\n🎯 Epoch {epoch+1}/{self.epochs} Complete:")
            print(f"   📊 Average Loss: {avg_epoch_loss:.4f}")
            print(f"   ⏱️  Time: {epoch_time:.2f}s")
            print(f"   📦 Batches: {batch_count}")
            
            # Early stopping check (simple implementation)
            if epoch > 10 and avg_epoch_loss < 0.01:
                print(f"🎉 Early stopping triggered! Loss below threshold.")
                break
        
        total_training_time = time.time() - self.start_time
        print(f"\n🎉 Training Complete!")
        print(f"⏱️  Total Training Time: {total_training_time:.2f}s")
        print(f"📊 Final Loss: {self.training_history[-1]['loss']:.4f}")
        print("=" * 80)
    
    def train_batch(self, batch_indices: List[int], processed_data: Dict, vocabulary: Dict) -> float:
        """Train on a single batch"""
        batch_loss = 0
        
        for idx in batch_indices:
            # Get question and answer
            question = processed_data['questions'][idx]
            answer = processed_data['answers'][idx]
            
            # Convert to sequences
            question_seq = self.text_to_sequence(question, vocabulary)
            answer_seq = self.text_to_sequence(answer, vocabulary)
            
            # Forward pass (simplified)
            question_embedding = self.forward_pass(question_seq, 'question')
            answer_embedding = self.forward_pass(answer_seq, 'answer')
            
            # Calculate similarity (cosine similarity)
            similarity = self.cosine_similarity(question_embedding, answer_embedding)
            
            # Loss: we want high similarity for matching Q&A pairs
            target_similarity = 1.0  # Perfect match
            loss = (similarity - target_similarity) ** 2
            
            batch_loss += loss
            
            # Backward pass (simplified weight updates)
            self.update_weights(question_embedding, answer_embedding, loss)
        
        return batch_loss / len(batch_indices)
    
    def forward_pass(self, sequence: List[int], input_type: str) -> np.ndarray:
        """Forward pass through the model"""
        # Simple embedding lookup
        embeddings = []
        for token_idx in sequence:
            if token_idx < len(self.model_weights['embedding_weights']):
                embeddings.append(self.model_weights['embedding_weights'][token_idx])
        
        if not embeddings:
            return np.zeros(self.model_weights['embedding_weights'].shape[1])
        
        # Average pooling
        embedding = np.mean(embeddings, axis=0)
        
        # Apply encoder
        if input_type == 'question':
            encoded = np.dot(embedding, self.model_weights['question_encoder']) + self.model_weights['bias_terms']['question_bias']
        else:  # answer
            encoded = np.dot(embedding, self.model_weights['answer_encoder']) + self.model_weights['bias_terms']['answer_bias']
        
        return encoded
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def update_weights(self, question_embedding: np.ndarray, answer_embedding: np.ndarray, loss: float):
        """Update model weights (simplified)"""
        # Simple gradient descent update
        learning_rate = self.learning_rate
        
        # Update embedding weights (simplified)
        for i in range(len(self.model_weights['embedding_weights'])):
            for j in range(len(self.model_weights['embedding_weights'][i])):
                self.model_weights['embedding_weights'][i][j] -= learning_rate * loss * 0.01
    
    def evaluate_model(self, vocabulary: Dict) -> Dict:
        """Evaluate model performance on testing data"""
        print("🧪 Evaluating model performance...")
        print("=" * 80)
        
        evaluation_results = {
            'overall_accuracy': 0.0,
            'domain_performance': {},
            'difficulty_performance': {},
            'category_performance': {},
            'detailed_metrics': {}
        }
        
        total_correct = 0
        total_predictions = 0
        
        # Calculate total cards for progress bar
        total_cards = sum(len(data['cards']) for data in self.testing_data.values())
        evaluated_cards = 0
        
        # Evaluate each domain
        for domain, data in self.testing_data.items():
            print(f"🔍 Evaluating {domain} domain...")
            
            domain_correct = 0
            domain_total = 0
            
            for card in data['cards']:
                question = card.get('front', '')
                answer = card.get('back', '')
                
                if question and answer:
                    # Make prediction
                    prediction = self.predict_answer(question, vocabulary)
                    
                    # Calculate accuracy (simplified - check if key concepts match)
                    accuracy = self.calculate_answer_accuracy(prediction, answer)
                    
                    if accuracy > 0.7:  # 70% threshold
                        domain_correct += 1
                        total_correct += 1
                    
                    domain_total += 1
                    total_predictions += 1
                
                evaluated_cards += 1
                
                # Progress bar for evaluation
                if evaluated_cards % 100 == 0 or evaluated_cards == total_cards:
                    self.progress_bar(evaluated_cards, total_cards, 
                                    prefix="Evaluating", 
                                    suffix=f"{evaluated_cards:,}/{total_cards:,} cards")
            
            # Domain performance
            domain_accuracy = domain_correct / domain_total if domain_total > 0 else 0
            evaluation_results['domain_performance'][domain] = {
                'accuracy': domain_accuracy,
                'correct': domain_correct,
                'total': domain_total
            }
            
            print(f"\n  ✅ {domain}: {domain_accuracy:.2%} ({domain_correct}/{domain_total})")
        
        # Overall accuracy
        overall_accuracy = total_correct / total_predictions if total_predictions > 0 else 0
        evaluation_results['overall_accuracy'] = overall_accuracy
        
        print(f"\n🎯 OVERALL PERFORMANCE:")
        print(f"   📊 Accuracy: {overall_accuracy:.2%}")
        print(f"   ✅ Correct: {total_correct:,}")
        print(f"   📦 Total: {total_predictions:,}")
        
        # Store performance metrics
        self.performance_metrics = evaluation_results
        
        return evaluation_results
    
    def predict_answer(self, question: str, vocabulary: Dict) -> str:
        """Predict answer for a given question"""
        # Convert question to sequence
        question_seq = self.text_to_sequence(question, vocabulary)
        
        # Get question embedding
        question_embedding = self.forward_pass(question_seq, 'question')
        
        # Find most similar answer from training data
        best_answer = "I don't have enough information to answer this question."
        best_similarity = -1
        
        # Search through training data for similar questions
        for domain_data in self.training_data.values():
            for card in domain_data['cards']:
                train_question = card.get('front', '')
                train_answer = card.get('back', '')
                
                if train_question and train_answer:
                    train_seq = self.text_to_sequence(train_question, vocabulary)
                    train_embedding = self.forward_pass(train_seq, 'question')
                    
                    similarity = self.cosine_similarity(question_embedding, train_embedding)
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_answer = train_answer
        
        return best_answer
    
    def calculate_answer_accuracy(self, prediction: str, actual: str) -> float:
        """Calculate accuracy between predicted and actual answers"""
        # Simple word overlap accuracy
        pred_words = set(prediction.lower().split())
        actual_words = set(actual.lower().split())
        
        if not actual_words:
            return 0.0
        
        overlap = len(pred_words.intersection(actual_words))
        accuracy = overlap / len(actual_words)
        
        return accuracy
    
    def save_model(self, filepath: str = 'trained_model'):
        """Save the trained model"""
        print("💾 Saving trained model...")
        
        model_data = {
            'model_name': self.model_name,
            'version': self.version,
            'model_weights': self.model_weights,
            'training_history': self.training_history,
            'performance_metrics': self.performance_metrics,
            'training_parameters': {
                'epochs': self.epochs,
                'learning_rate': self.learning_rate,
                'batch_size': self.batch_size
            },
            'saved_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save as JSON (weights as lists for JSON compatibility)
        model_data['model_weights'] = {
            key: value.tolist() if hasattr(value, 'tolist') else value 
            for key, value in self.model_weights.items()
        }
        
        with open(f'{filepath}.json', 'w', encoding='utf-8') as f:
            json.dump(model_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Model saved to {filepath}.json")
    
    def generate_training_report(self) -> str:
        """Generate comprehensive training report"""
        print("📊 Generating training report...")
        
        report = f"""
🎯 NOTICALAI-MASTER TRAINING REPORT
{'=' * 80}

📊 MODEL INFORMATION:
   Name: {self.model_name}
   Version: {self.version}
   Training Data: {sum(len(data['cards']) for data in self.training_data.values()):,} cards
   Testing Data: {sum(len(data['cards']) for data in self.testing_data.values()):,} cards

🚀 TRAINING PERFORMANCE:
   Epochs Completed: {len(self.training_history)}
   Final Loss: {self.training_history[-1]['loss']:.4f if self.training_history else 'N/A'}
   Total Training Time: {sum(epoch['time'] for epoch in self.training_history):.2f}s

🧪 EVALUATION RESULTS:
   Overall Accuracy: {self.performance_metrics.get('overall_accuracy', 0):.2%}

📈 DOMAIN PERFORMANCE:
"""
        
        for domain, metrics in self.performance_metrics.get('domain_performance', {}).items():
            report += f"   {domain.title()}: {metrics['accuracy']:.2%} ({metrics['correct']}/{metrics['total']})\n"
        
        report += f"""
🎉 TRAINING STATUS: {'COMPLETE' if self.training_history else 'NOT STARTED'}
{'=' * 80}
"""
        
        return report

def main():
    """Main training pipeline execution"""
    print("🚀 LAUNCHING NOTICALAI-MASTER TRAINING PIPELINE")
    print("=" * 80)
    
    # Initialize pipeline
    pipeline = AITrainingPipeline()
    
    # Load data
    training_cards = pipeline.load_training_data()
    testing_cards = pipeline.load_testing_data()
    
    if training_cards == 0:
        print("❌ No training data found! Exiting.")
        return
    
    # Preprocess data
    processed_data = pipeline.preprocess_data()
    
    # Create vocabulary
    vocabulary = pipeline.create_vocabulary(processed_data)
    
    # Initialize model weights
    pipeline.initialize_model_weights(len(vocabulary))
    
    # Train model
    pipeline.train_model(processed_data, vocabulary)
    
    # Evaluate model
    evaluation_results = pipeline.evaluate_model(vocabulary)
    
    # Save model
    pipeline.save_model()
    
    # Generate report
    report = pipeline.generate_training_report()
    print(report)
    
    # Save report
    with open('training_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ Training pipeline complete! Model saved and ready for use.")
    return pipeline

if __name__ == "__main__":
    pipeline = main()
