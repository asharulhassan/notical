# ai-pipeline/core/enhanced_ai_core.py
"""
Enhanced NOTICAL AI Core
========================
AI core with training integration and improved capabilities.
"""

import re
import random
import logging
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedNOTICALAICore:
    """
    Enhanced AI core with training integration
    """
    
    def __init__(self):
        """Initialize the enhanced AI core"""
        self.knowledge_base = {}
        self.learning_history = []
        
        # Use relative paths from the core directory
        current_dir = Path(__file__).parent
        self.model_path = current_dir.parent / "models"
        self.training_data_path = current_dir.parent / "data" / "training"
        
        # Create directories if they don't exist
        self.model_path.mkdir(parents=True, exist_ok=True)
        self.training_data_path.mkdir(parents=True, exist_ok=True)
        
        # Load trained models if available
        self.load_trained_models()
        
        logger.info("✅ Enhanced NOTICAL AI Core initialized")
        logger.info(f"📁 Model path: {self.model_path}")
        logger.info(f"📁 Training data path: {self.training_data_path}")
    
    def load_trained_models(self):
        """Load trained models if available"""
        try:
            if (self.model_path / "concept_extractor.json").exists():
                with open(self.model_path / "concept_extractor.json", 'r') as f:
                    self.concept_model = json.load(f)
                logger.info("✅ Concept extractor model loaded")
            else:
                self.concept_model = None
                logger.info("ℹ️  No concept extractor model found")
            
            if (self.model_path / "difficulty_assessor.json").exists():
                with open(self.model_path / "difficulty_assessor.json", 'r') as f:
                    self.difficulty_model = json.load(f)
                logger.info("✅ Difficulty assessor model loaded")
            else:
                self.difficulty_model = None
                logger.info("ℹ️  No difficulty assessor model found")
            
            if (self.model_path / "subject_classifier.json").exists():
                with open(self.model_path / "subject_classifier.json", 'r') as f:
                    self.subject_model = json.load(f)
                logger.info("✅ Subject classifier model loaded")
            else:
                self.subject_model = None
                logger.info("ℹ️  No subject classifier model found")
                
        except Exception as e:
            logger.warning(f"Could not load trained models: {e}")
            self.concept_model = None
            self.difficulty_model = None
            self.subject_model = None
    
    def analyze_content_intelligently(self, text: str) -> Dict[str, Any]:
        """
        Enhanced content analysis using trained models when available
        """
        if not text.strip():
            return {}
        
        # Split into sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]
        
        # Extract key concepts using trained model if available
        if self.concept_model:
            key_concepts = self._extract_concepts_with_trained_model(text)
        else:
            key_concepts = self._extract_key_concepts_intelligently(text)
        
        # Find processes and mechanisms
        processes = self._extract_processes(sentences)
        
        # Find comparisons and relationships
        comparisons = self._extract_comparisons(sentences)
        
        # Find technical terms and acronyms
        technical_terms = self._extract_technical_terms(text)
        
        # Find implications and applications
        implications = self._extract_implications(sentences)
        
        # Find cause-effect relationships
        cause_effects = self._extract_cause_effects(sentences)
        
        # Assess complexity using trained model if available
        if self.difficulty_model:
            complexity_score = self._assess_complexity_with_trained_model(text)
        else:
            complexity_score = self._assess_complexity(text)
        
        # Detect subjects using trained model if available
        if self.subject_model:
            subject_areas = self._detect_subjects_with_trained_model(text)
        else:
            subject_areas = self._detect_subject_areas(text)
        
        # Store learning history
        self._store_learning_example(text, key_concepts, complexity_score, subject_areas)
        
        return {
            'sentences': sentences,
            'key_concepts': key_concepts,
            'processes': processes,
            'comparisons': comparisons,
            'technical_terms': technical_terms,
            'implications': implications,
            'cause_effects': cause_effects,
            'word_count': len(text.split()),
            'sentence_count': len(sentences),
            'complexity_score': complexity_score,
            'subject_areas': subject_areas,
            'model_used': {
                'concept_extractor': self.concept_model is not None,
                'difficulty_assessor': self.difficulty_model is not None,
                'subject_classifier': self.subject_model is not None
            }
        }
    
    def _extract_concepts_with_trained_model(self, text: str) -> List[Dict[str, Any]]:
        """Extract concepts using trained model"""
        # Simulate using trained model
        concepts = self._extract_key_concepts_intelligently(text)
        
        # Apply model improvements
        for concept in concepts:
            if self.concept_model:
                # Simulate model confidence
                concept['confidence'] = min(0.95, concept.get('importance', 0) / 10)
                concept['model_enhanced'] = True
        
        return concepts
    
    def _assess_complexity_with_trained_model(self, text: str) -> int:
        """Assess complexity using trained model"""
        base_complexity = self._assess_complexity(text)
        
        if self.difficulty_model:
            # Apply model improvements
            accuracy = self.difficulty_model.get('accuracy', 0.8)
            adjusted_complexity = int(base_complexity * accuracy)
            return max(1, min(10, adjusted_complexity))
        
        return base_complexity
    
    def _detect_subjects_with_trained_model(self, text: str) -> List[str]:
        """Detect subjects using trained model"""
        base_subjects = self._detect_subject_areas(text)
        
        if self.subject_model:
            # Apply model improvements
            accuracy = self.subject_model.get('accuracy', 0.9)
            if accuracy > 0.85:
                # High confidence - return base subjects
                return base_subjects
            else:
                # Lower confidence - add general category
                if not base_subjects:
                    base_subjects.append('general')
        
        return base_subjects
    
    def _store_learning_example(self, text: str, concepts: List[Dict], complexity: int, subjects: List[str]):
        """Store learning example for future training"""
        example = {
            'timestamp': datetime.now().isoformat(),
            'text_length': len(text),
            'concepts_count': len(concepts),
            'complexity': complexity,
            'subjects': subjects,
            'concepts': [c.get('term', '') for c in concepts[:5]]  # Store first 5 concepts
        }
        
        self.learning_history.append(example)
        
        # Keep only last 100 examples
        if len(self.learning_history) > 100:
            self.learning_history = self.learning_history[-100:]
        
        # Save learning history periodically
        if len(self.learning_history) % 10 == 0:
            self._save_learning_history()
    
    def _save_learning_history(self):
        """Save learning history to file"""
        try:
            history_file = self.training_data_path / "learning_history.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Could not save learning history: {e}")
    
    def _extract_key_concepts_intelligently(self, text: str) -> List[Dict[str, Any]]:
        """Extract key concepts based on importance, not just word frequency"""
        concepts = []

        # Find technical terms and concepts
        technical_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Capitalized terms
            r'\b[a-z]+(?:\s+[a-z]+)*\s+(?:RAM|ROM|CPU|DRAM|SRAM|NVDIMM|MRAM|memory|storage|system|algorithm|function|method|process|mechanism)\b',  # Technical terms
            r'\b(?:volatile|non-volatile|dynamic|static|cache|hierarchy|controller|management|optimization|efficiency|performance|latency|throughput)\b'  # Key concepts
        ]

        for pattern in technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) > 3 and match.lower() not in ['the', 'and', 'for', 'with', 'that', 'this']:
                    # Find context for this concept
                    context = self._find_concept_context(match, text)
                    concepts.append({
                        'term': match,
                        'context': context,
                        'importance': self._assess_concept_importance(match, text),
                        'type': self._classify_concept_type(match)
                    })

        # Remove duplicates and sort by importance
        unique_concepts = {}
        for concept in concepts:
            term = concept['term'].lower()
            if term not in unique_concepts or concept['importance'] > unique_concepts[term]['importance']:
                unique_concepts[term] = concept

        return sorted(unique_concepts.values(), key=lambda x: x['importance'], reverse=True)

    def _find_concept_context(self, concept: str, text: str) -> str:
        """Find the context/sentence that explains this concept"""
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if concept in sentence:
                # Look for definition patterns
                if any(word in sentence.lower() for word in ['is', 'are', 'refers to', 'means', 'constitutes', 'represents', 'employs', 'uses', 'consists of']):
                    return sentence.strip()
        return ""

    def _assess_concept_importance(self, concept: str, text: str) -> int:
        """Assess how important a concept is based on frequency and context"""
        # Count occurrences
        frequency = len(re.findall(rf'\b{re.escape(concept)}\b', text, re.IGNORECASE))

        # Check if it's in definition sentences
        definition_sentences = len(re.findall(rf'.*{re.escape(concept)}.*(?:is|are|refers to|means).*', text, re.IGNORECASE))

        # Check if it's capitalized (likely important)
        capitalized = concept[0].isupper() if concept else False

        # Calculate importance score
        importance = frequency * 2 + definition_sentences * 5 + (10 if capitalized else 0)

        return importance

    def _classify_concept_type(self, concept: str) -> str:
        """Classify what type of concept this is"""
        concept_lower = concept.lower()

        if any(word in concept_lower for word in ['memory', 'ram', 'rom', 'storage']):
            return 'memory_component'
        elif any(word in concept_lower for word in ['controller', 'management', 'system']):
            return 'control_component'
        elif any(word in concept_lower for word in ['cache', 'hierarchy', 'performance']):
            return 'performance_component'
        elif any(word in concept_lower for word in ['algorithm', 'function', 'method']):
            return 'functional_component'
        else:
            return 'general_concept'

    def _extract_processes(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """Extract processes and mechanisms from sentences"""
        processes = []

        process_keywords = ['process', 'mechanism', 'procedure', 'method', 'technique', 'approach', 'strategy']

        for sentence in sentences:
            for keyword in process_keywords:
                if keyword in sentence.lower():
                    processes.append({
                        'sentence': sentence,
                        'keyword': keyword,
                        'type': 'process'
                    })
                    break

        return processes

    def _extract_comparisons(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """Extract comparisons and relationships"""
        comparisons = []

        comparison_keywords = ['while', 'whereas', 'however', 'but', 'unlike', 'compared to', 'in contrast', 'on the other hand']

        for sentence in sentences:
            for keyword in comparison_keywords:
                if keyword in sentence.lower():
                    comparisons.append({
                        'sentence': sentence,
                        'keyword': keyword,
                        'type': 'comparison'
                    })
                    break

        return comparisons

    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms and acronyms"""
        # Find acronyms
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)

        # Find technical terms
        technical_terms = re.findall(r'\b(?:volatile|non-volatile|dynamic|static|cache|hierarchy|controller|management|optimization|efficiency|performance|latency|throughput|algorithm|function|method|process|mechanism)\b', text, re.IGNORECASE)

        return list(set(acronyms + technical_terms))

    def _extract_implications(self, sentences: List[str]) -> List[str]:
        """Extract implications and applications"""
        implications = []

        implication_keywords = ['therefore', 'thus', 'consequently', 'as a result', 'this means', 'this leads to', 'this results in']

        for sentence in sentences:
            for keyword in implication_keywords:
                if keyword in sentence.lower():
                    implications.append(sentence)
                    break

        return implications

    def _extract_cause_effects(self, sentences: List[str]) -> List[Dict[str, str]]:
        """Extract cause-effect relationships"""
        cause_effects = []

        cause_keywords = ['because', 'since', 'as', 'due to', 'caused by', 'leads to', 'results in', 'causes']

        for sentence in sentences:
            for keyword in cause_keywords:
                if keyword in sentence.lower():
                    cause_effects.append({
                        'sentence': sentence,
                        'keyword': keyword,
                        'type': 'cause_effect'
                    })
                    break

        return cause_effects

    def _assess_complexity(self, text: str) -> int:
        """Assess the complexity of the text"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)

        # Average sentence length
        avg_sentence_length = len(words) / max(len(sentences), 1)

        # Technical term density
        technical_terms = len(self._extract_technical_terms(text))
        technical_density = technical_terms / max(len(words), 1) * 100

        # Complexity score (1-10)
        complexity = min(10, (avg_sentence_length / 20) * 5 + (technical_density / 10) * 5)

        return int(complexity)

    def _detect_subject_areas(self, text: str) -> List[str]:
        """Detect subject areas from the text"""
        subjects = []
        text_lower = text.lower()

        # Computer Science / Technology
        if any(word in text_lower for word in ['memory', 'cpu', 'algorithm', 'system', 'computer', 'technology']):
            subjects.append('computer_science')

        # Physics / Engineering
        if any(word in text_lower for word in ['voltage', 'current', 'power', 'energy', 'force', 'motion']):
            subjects.append('physics')

        # Biology / Medicine
        if any(word in text_lower for word in ['cell', 'organism', 'disease', 'treatment', 'medicine', 'biology']):
            subjects.append('biology')

        # Chemistry
        if any(word in text_lower for word in ['molecule', 'reaction', 'chemical', 'compound', 'element']):
            subjects.append('chemistry')

        # Mathematics
        if any(word in text_lower for word in ['equation', 'formula', 'calculation', 'mathematical', 'function']):
            subjects.append('mathematics')

        return subjects if subjects else ['general']

    def enhance_generation_parameters(self, content_analysis: Dict[str, Any], target_count: int) -> Dict[str, Any]:
        """
        Enhance generation parameters based on content analysis
        """
        complexity = content_analysis.get('complexity_score', 5)
        subject_areas = content_analysis.get('subject_areas', ['general'])
        key_concepts = content_analysis.get('key_concepts', [])

        # Adjust generation strategy based on content
        if complexity > 7:
            # High complexity - focus on explanations and comparisons
            card_types = ['explanation', 'comparison', 'definition']
            style = 'professional'
        elif complexity > 4:
            # Medium complexity - balanced approach
            card_types = ['definition', 'explanation', 'cloze']
            style = 'professional'
        else:
            # Low complexity - focus on definitions and simple explanations
            card_types = ['definition', 'cloze']
            style = 'simple'

        # Adjust target count based on content richness
        if len(key_concepts) > 10:
            adjusted_count = min(target_count * 2, 50)  # More concepts = more cards
        elif len(key_concepts) > 5:
            adjusted_count = target_count
        else:
            adjusted_count = max(target_count // 2, 3)  # Fewer concepts = fewer cards

        return {
            'card_types': card_types,
            'style': style,
            'target_count': adjusted_count,
            'complexity': complexity,
            'subject_areas': subject_areas,
            'key_concepts_count': len(key_concepts)
        }

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            'total_examples': len(self.learning_history),
            'models_loaded': {
                'concept_extractor': self.concept_model is not None,
                'difficulty_assessor': self.difficulty_model is not None,
                'subject_classifier': self.subject_model is not None
            },
            'recent_activity': len([ex for ex in self.learning_history if ex.get('timestamp', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
        }
    
    def generate_intelligent_hint(self, question: str, content: str) -> str:
        """Generate intelligent hints based on actual content analysis"""
        try:
            # Extract relevant information from the content
            analysis = self.analyze_content_intelligently(content)
            
            # Find the most relevant sentence or concept for this question
            question_lower = question.lower()
            
            # Look for sentences that contain key terms from the question
            relevant_sentences = []
            for sentence in analysis.get('sentences', []):
                if any(term.lower() in sentence.lower() for term in question_lower.split()):
                    relevant_sentences.append(sentence)
            
            # If we found relevant sentences, use them for the hint
            if relevant_sentences:
                best_sentence = max(relevant_sentences, key=len)
                # Create a helpful hint based on the content
                if "what is" in question_lower:
                    return f"Look for the definition in: '{best_sentence[:100]}...'"
                elif "explain" in question_lower:
                    return f"Find the explanation in: '{best_sentence[:100]}...'"
                else:
                    return f"Key information: '{best_sentence[:100]}...'"
            
            # Fallback: provide context about what to look for
            key_concepts = analysis.get('key_concepts', [])
            if key_concepts:
                return f"Focus on these key concepts: {', '.join(key_concepts[:3])}"
            
            return "Analyze the provided content for relevant information"
            
        except Exception as e:
            logger.error(f"Error generating intelligent hint: {e}")
            return "Review the content carefully for the answer"

# Create global enhanced instance
enhanced_ai_core = EnhancedNOTICALAICore()
