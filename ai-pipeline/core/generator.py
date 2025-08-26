# app/generator.py
"""
Enhanced generator.py
--------------------
Self-learning flashcard generation with:
1. Content understanding (not just word finding)
2. Online research capability
3. Multiple generation modes
4. Context-aware learning (exam boards, university levels)
5. AI Core integration for intelligent analysis
"""

import re
import uuid
import logging
import requests
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json

# Import our AI core for enhanced intelligence
from .ai_core import ai_core

logger = logging.getLogger(__name__)

class SmartFlashcardGenerator:
    """
    Self-learning flashcard generator that understands content and can research online
    Now enhanced with AI Core for intelligent analysis
    """
    
    def __init__(self):
        self.knowledge_base = {}  # Store learned concepts
        self.online_sources = {}  # Store online research results
        self.ai_core = ai_core  # Use our enhanced AI core
        
    def generate_flashcards(
        self, 
        chunk: Dict[str, Any], 
        mode: str = "text_understanding",
        style: str = "professional",
        include_online: bool = False,
        exam_board: str = None,
        level: str = "university",
        target_count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Generate intelligent flashcards based on mode and style
        
        Modes:
        - "text_understanding": Understand concepts from text (default)
        - "strict_text": Word-to-word from text
        - "online_research": Research online for accurate info
        
        Styles:
        - "professional": Academic/professional language
        - "simple": Simple explanations
        - "exam_focused": Tailored for specific exam boards
        """
        
        if mode == "online_research":
            return self._generate_with_online_research(chunk, target_count, exam_board, level)
        elif mode == "strict_text":
            return self._generate_strict_text_cards(chunk, target_count)
        else:  # text_understanding
            return self._generate_understanding_cards(chunk, target_count, style, exam_board, level)
    
    def _generate_understanding_cards(
        self, 
        chunk: Dict[str, Any], 
        target_count: int, 
        style: str,
        exam_board: str = None,
        level: str = "university"
    ) -> List[Dict[str, Any]]:
        """Generate cards that actually understand the content using AI Core"""
        text = chunk.get("text", "").strip()
        cards = []
        
        # Use AI Core for intelligent content analysis
        content_analysis = self.ai_core.analyze_content_intelligently(text)
        
        # Get enhanced generation parameters based on content analysis
        enhanced_params = self.ai_core.enhance_generation_parameters(content_analysis, target_count)
        
        # Use the enhanced parameters to guide generation
        adjusted_style = enhanced_params.get('style', style)
        adjusted_target_count = enhanced_params.get('target_count', target_count)
        
        logger.info(f"AI Core Analysis: Complexity={content_analysis.get('complexity_score', 5)}, "
                   f"Key Concepts={len(content_analysis.get('key_concepts', []))}, "
                   f"Subject Areas={content_analysis.get('subject_areas', [])}")
        
        # Generate cards based on key concepts from AI analysis
        key_concepts = content_analysis.get('key_concepts', [])
        
        for concept_data in key_concepts[:adjusted_target_count]:
            if len(cards) >= adjusted_target_count:
                break
            
            concept = concept_data.get('term', '')
            concept_type = concept_data.get('type', 'general_concept')
            context = concept_data.get('context', '')
            
            # Create different types of cards based on concept type
            card_types = self._get_card_types_for_ai_concept(concept_type, content_analysis)
            
            for card_type in card_types:
                if len(cards) >= adjusted_target_count:
                    break
                
                card = self._create_ai_enhanced_card(
                    concept, concept_data, card_type, adjusted_style, exam_board, level, content_analysis
                )
                if card:
                    cards.append(card)
        
        # If we don't have enough cards, generate some from processes and comparisons
        if len(cards) < adjusted_target_count:
            additional_cards = self._generate_from_processes_and_comparisons(
                content_analysis, adjusted_target_count - len(cards), adjusted_style, exam_board, level
            )
            cards.extend(additional_cards)
        
        return cards[:target_count]
    
    def _get_card_types_for_ai_concept(self, concept_type: str, content_analysis: Dict[str, Any]) -> List[str]:
        """Determine what types of cards to create for an AI-analyzed concept"""
        card_types = ["definition"]
        
        # Add cloze if we have good context
        if content_analysis.get("sentences"):
            card_types.append("cloze")
        
        # Add explanation if we understand the role
        if concept_type != "general_concept":
            card_types.append("explanation")
        
        # Add comparison if we have related concepts
        if content_analysis.get("comparisons"):
            card_types.append("comparison")
        
        return card_types
    
    def _create_ai_enhanced_card(
        self,
        concept: str,
        concept_data: Dict[str, Any],
        card_type: str,
        style: str,
        exam_board: str = None,
        level: str = "university",
        content_analysis: Dict[str, Any] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a card using AI-enhanced understanding"""
        
        if card_type == "definition":
            return self._create_ai_definition_card(concept, concept_data, style, exam_board, level)
        elif card_type == "cloze":
            return self._create_ai_cloze_card(concept, concept_data, style, content_analysis)
        elif card_type == "explanation":
            return self._create_ai_explanation_card(concept, concept_data, style, exam_board, level)
        elif card_type == "comparison":
            return self._create_ai_comparison_card(concept, concept_data, style, content_analysis)
        
        return None
    
    def _create_ai_definition_card(
        self,
        concept: str,
        concept_data: Dict[str, Any],
        style: str,
        exam_board: str = None,
        level: str = "university"
    ) -> Dict[str, Any]:
        """Create a definition card using AI understanding"""
        
        context = concept_data.get("context", "")
        concept_type = concept_data.get("type", "general_concept")
        
        # Create a proper question
        question = f"What is {concept}?"
        
        # Create an answer based on AI understanding
        if context:
            # Use the context we found
            answer = context
        else:
            # Create answer based on concept type
            if concept_type == "memory_component":
                answer = f"{concept} is a memory component that stores and retrieves data in computer systems."
            elif concept_type == "control_component":
                answer = f"{concept} is a control mechanism that manages and coordinates system operations."
            elif concept_type == "performance_component":
                answer = f"{concept} is a performance optimization component that improves system efficiency."
            else:
                answer = f"{concept} is a key concept in computer architecture and system design."
        
        # Style the answer
        if style == "professional":
            answer = f"{concept} is a technical component that {answer.lower()}"
        elif style == "exam_focused" and exam_board:
            answer = f"For {exam_board}: {answer}"
        
        return {
            "id": str(uuid.uuid4()),
            "type": "definition",
            "front": question,
            "back": answer,
            "concept": concept,
            "difficulty": self._assess_difficulty(concept, answer, level),
            "style": style,
            "exam_board": exam_board,
            "level": level,
            "ai_enhanced": True
        }
    
    def _create_ai_cloze_card(
        self,
        concept: str,
        concept_data: Dict[str, Any],
        style: str,
        content_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a cloze card using AI understanding"""
        
        sentences = content_analysis.get("sentences", [])
        if not sentences:
            return None
        
        # Find a good sentence that contains the concept
        for sentence in sentences:
            if concept in sentence and len(sentence) > 30:
                # Find a good word to blank out
                words = sentence.split()
                good_words = []
                
                for word in words:
                    word_clean = re.sub(r'[^\w]', '', word)
                    if (len(word_clean) > 5 and
                        word_clean[0].isupper() or
                        word_clean.lower() in ['memory', 'storage', 'system', 'technology', 'process', 'volatile', 'non-volatile']):
                        good_words.append(word_clean)
                
                if good_words:
                    answer = good_words[0]
                    cloze_question = sentence.replace(answer, "_____")
                    
                    return {
                        "id": str(uuid.uuid4()),
                        "type": "cloze",
                        "front": f"Complete: {cloze_question}",
                        "back": answer,
                        "concept": concept,
                        "difficulty": 1,
                        "style": style,
                        "ai_enhanced": True
                    }
        
        return None
    
    def _create_ai_explanation_card(
        self,
        concept: str,
        concept_data: Dict[str, Any],
        style: str,
        exam_board: str = None,
        level: str = "university"
    ) -> Optional[Dict[str, Any]]:
        """Create an explanation card using AI understanding"""
        
        concept_type = concept_data.get("type", "")
        context = concept_data.get("context", "")
        
        if not concept_type:
            return None
        
        # Create question based on concept type
        if concept_type == "memory_component":
            question = f"How does {concept} function in memory systems?"
            answer = f"{concept} functions as a memory component that stores and retrieves data. It is designed for specific memory operations and performance characteristics."
        elif concept_type == "control_component":
            question = f"What is the role of {concept} in system control?"
            answer = f"{concept} manages and coordinates system operations, ensuring proper communication and control between different components."
        elif concept_type == "performance_component":
            question = f"How does {concept} improve system performance?"
            answer = f"{concept} optimizes system performance by improving efficiency, reducing latency, and enhancing overall system capabilities."
        else:
            question = f"How does {concept} work in computer architecture?"
            answer = f"{concept} works as a key component in computer architecture, {context[:100] if context else 'providing essential functionality'}..."
        
        if style == "exam_focused" and exam_board:
            answer = f"For {exam_board}: {answer}"
        
        return {
            "id": str(uuid.uuid4()),
            "type": "explanation",
            "front": question,
            "back": answer,
            "concept": concept,
            "difficulty": 3,
            "style": style,
            "exam_board": exam_board,
            "level": level,
            "ai_enhanced": True
        }
    
    def _create_ai_comparison_card(
        self,
        concept: str,
        concept_data: Dict[str, Any],
        style: str,
        content_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a comparison card using AI understanding"""
        
        comparisons = content_analysis.get("comparisons", [])
        if not comparisons:
            return None
        
        # Find a good comparison
        for comparison in comparisons[:3]:
            sentence = comparison.get("sentence", "")
            if concept in sentence:
                # Extract other concepts from this comparison
                other_concepts = []
                for comp_concept in content_analysis.get("key_concepts", []):
                    other_term = comp_concept.get("term", "")
                    if other_term != concept and other_term in sentence:
                        other_concepts.append(other_term)
                
                if other_concepts:
                    other_concept = other_concepts[0]
                    question = f"What is the difference between {concept} and {other_concept}?"
                    
                    # Create comparison answer
                    if "volatile" in concept.lower() or "volatile" in other_concept.lower():
                        answer = f"{concept} and {other_concept} differ in their data retention characteristics. {concept} may lose data when power is removed, while {other_concept} maintains data persistence."
                    elif "memory" in concept.lower() or "memory" in other_concept.lower():
                        answer = f"{concept} and {other_concept} are both memory components but serve different purposes. {concept} is optimized for specific use cases while {other_concept} has different performance characteristics."
                    else:
                        answer = f"{concept} and {other_concept} are related components in computer architecture. {concept} focuses on one aspect while {other_concept} handles different functionality."
                    
                    return {
                        "id": str(uuid.uuid4()),
                        "type": "comparison",
                        "front": question,
                        "back": answer,
                        "concept": concept,
                        "difficulty": 4,
                        "style": style,
                        "ai_enhanced": True
                    }
        
        return None
    
    def _generate_from_processes_and_comparisons(
        self,
        content_analysis: Dict[str, Any],
        target_count: int,
        style: str,
        exam_board: str = None,
        level: str = "university"
    ) -> List[Dict[str, Any]]:
        """Generate additional cards from processes and comparisons"""
        cards = []
        
        # Generate from processes
        processes = content_analysis.get("processes", [])
        for process in processes[:target_count//2]:
            sentence = process.get("sentence", "")
            if sentence:
                question = f"What process is described here: {sentence[:50]}..."
                answer = sentence
                
                cards.append({
                    "id": str(uuid.uuid4()),
                    "type": "explanation",
                    "front": question,
                    "back": answer,
                    "concept": "process",
                    "difficulty": 2,
                    "style": style,
                    "exam_board": exam_board,
                    "level": level,
                    "ai_enhanced": True
                })
        
        # Generate from cause-effects
        cause_effects = content_analysis.get("cause_effects", [])
        for cause_effect in cause_effects[:target_count//2]:
            sentence = cause_effect.get("sentence", "")
            if sentence:
                question = f"What relationship is described: {sentence[:50]}..."
                answer = sentence
                
                cards.append({
                    "id": str(uuid.uuid4()),
                    "type": "explanation",
                    "front": question,
                    "back": answer,
                    "concept": "cause_effect",
                    "difficulty": 3,
                    "style": style,
                    "exam_board": exam_board,
                    "level": level,
                    "ai_enhanced": True
                })
        
        return cards[:target_count]
    
    def _extract_and_understand_concepts(self, text: str) -> Dict[str, Dict[str, Any]]:
        """Extract concepts and actually understand what they mean"""
        concepts = {}
        
        # Find technical terms and understand their context
        technical_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        
        all_terms = list(set(technical_terms + acronyms))
        
        for term in all_terms:
            if len(term) < 3 or term.lower() in ['the', 'and', 'for', 'with', 'that', 'this']:
                continue
                
            # Understand what this term means in context
            understanding = self._understand_term_in_context(term, text)
            if understanding:
                concepts[term] = understanding
        
        return concepts
    
    def _understand_term_in_context(self, term: str, text: str) -> Optional[Dict[str, Any]]:
        """Actually understand what a term means in the given context"""
        # Find sentences that explain this term
        sentences = re.split(r'[.!?]+', text)
        explanations = []
        
        for sentence in sentences:
            if term in sentence:
                # Look for definition patterns
                if any(word in sentence.lower() for word in ['is', 'are', 'refers to', 'means', 'constitutes', 'represents', 'employs', 'uses']):
                    explanations.append(sentence.strip())
        
        if not explanations:
            return None
        
        # Extract the actual meaning
        best_explanation = explanations[0]
        
        # Find related concepts mentioned with this term
        related_concepts = []
        for sentence in sentences:
            if term in sentence:
                # Extract other technical terms from this sentence
                other_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', sentence)
                related_concepts.extend([t for t in other_terms if t != term and len(t) > 3])
        
        # Understand the role/function
        role = self._extract_role_from_context(term, text)
        
        return {
            "explanation": best_explanation,
            "related_concepts": list(set(related_concepts)),
            "role": role,
            "context_sentences": explanations
        }
    
    def _extract_role_from_context(self, term: str, text: str) -> str:
        """Extract what role/function the term plays"""
        text_lower = text.lower()
        term_lower = term.lower()
        
        if any(word in text_lower for word in ['memory', 'storage']):
            if 'volatile' in text_lower:
                return "volatile_memory"
            elif 'non-volatile' in text_lower:
                return "non_volatile_memory"
            else:
                return "memory_component"
        elif any(word in text_lower for word in ['controller', 'management']):
            return "control_component"
        elif any(word in text_lower for word in ['cache', 'hierarchy']):
            return "performance_component"
        else:
            return "general_component"
    
    def _get_card_types_for_concept(self, concept: str, understanding: Dict[str, Any]) -> List[str]:
        """Determine what types of cards to create for a concept"""
        card_types = ["definition"]
        
        # Add cloze if we have good context
        if understanding.get("context_sentences"):
            card_types.append("cloze")
        
        # Add explanation if we understand the role
        if understanding.get("role"):
            card_types.append("explanation")
        
        # Add comparison if we have related concepts
        if understanding.get("related_concepts"):
            card_types.append("comparison")
        
        return card_types
    
    def _create_understanding_card(
        self, 
        concept: str, 
        understanding: Dict[str, Any], 
        card_type: str, 
        style: str,
        exam_board: str = None,
        level: str = "university"
    ) -> Optional[Dict[str, Any]]:
        """Create a card that actually demonstrates understanding"""
        
        if card_type == "definition":
            return self._create_definition_card(concept, understanding, style, exam_board, level)
        elif card_type == "cloze":
            return self._create_cloze_card(concept, understanding, style)
        elif card_type == "explanation":
            return self._create_explanation_card(concept, understanding, style, exam_board, level)
        elif card_type == "comparison":
            return self._create_comparison_card(concept, understanding, style)
        
        return None
    
    def _create_definition_card(
        self, 
        concept: str, 
        understanding: Dict[str, Any], 
        style: str,
        exam_board: str = None,
        level: str = "university"
    ) -> Dict[str, Any]:
        """Create a definition card that actually answers the question"""
        
        explanation = understanding.get("explanation", "")
        role = understanding.get("role", "")
        
        # Create a proper question
        question = f"What is {concept}?"
        
        # Create an answer that actually explains the concept
        if style == "professional":
            answer = self._create_professional_answer(concept, explanation, role, level)
        elif style == "exam_focused" and exam_board:
            answer = self._create_exam_focused_answer(concept, explanation, role, exam_board)
        else:
            answer = self._create_simple_answer(concept, explanation, role)
        
        return {
            "id": str(uuid.uuid4()),
            "type": "definition",
            "front": question,
            "back": answer,
            "concept": concept,
            "difficulty": self._assess_difficulty(concept, explanation, level),
            "style": style,
            "exam_board": exam_board,
            "level": level
        }
    
    def _create_professional_answer(self, concept: str, explanation: str, role: str, level: str) -> str:
        """Create a professional, academic answer"""
        
        # Extract the core definition
        core_def = self._extract_core_definition(explanation)
        
        if role == "volatile_memory":
            return f"{concept} is a type of volatile memory that requires periodic refresh cycles to maintain data integrity. {core_def}"
        elif role == "non_volatile_memory":
            return f"{concept} is a non-volatile storage medium that retains data without power. {core_def}"
        elif role == "control_component":
            return f"{concept} is a control mechanism that manages and coordinates system operations. {core_def}"
        else:
            return f"{concept} is a key component in computer architecture. {core_def}"
    
    def _create_exam_focused_answer(self, concept: str, explanation: str, role: str, exam_board: str) -> str:
        """Create an answer tailored for specific exam boards"""
        
        core_def = self._extract_core_definition(explanation)
        
        if exam_board == "AQA":
            return f"For AQA: {concept} is defined as {core_def}. Key points: {self._extract_key_points(explanation)}"
        elif exam_board == "OCR":
            return f"For OCR: {concept} refers to {core_def}. Remember: {self._extract_key_points(explanation)}"
        else:
            return f"{concept}: {core_def}. Exam focus: {self._extract_key_points(explanation)}"
    
    def _create_simple_answer(self, concept: str, explanation: str, role: str) -> str:
        """Create a simple, easy-to-understand answer"""
        
        core_def = self._extract_core_definition(explanation)
        
        if role == "volatile_memory":
            return f"{concept} is memory that loses data when power is turned off. {core_def}"
        elif role == "non_volatile_memory":
            return f"{concept} is memory that keeps data even without power. {core_def}"
        else:
            return f"{concept} is {core_def}"
    
    def _extract_core_definition(self, explanation: str) -> str:
        """Extract the core definition from an explanation"""
        # Find the part that actually defines the concept
        sentences = explanation.split('.')
        for sentence in sentences:
            if any(word in sentence.lower() for word in ['is', 'are', 'refers to', 'means']):
                return sentence.strip()
        return explanation[:100] + "..." if len(explanation) > 100 else explanation
    
    def _extract_key_points(self, explanation: str) -> str:
        """Extract key points for exam-focused answers"""
        # Find technical details and key facts
        key_points = []
        words = explanation.split()
        
        for i, word in enumerate(words):
            if word.lower() in ['volatile', 'non-volatile', 'refresh', 'capacitor', 'flip-flop']:
                if i > 0:
                    key_points.append(f"{words[i-1]} {word}")
        
        return ", ".join(key_points[:3]) if key_points else "Focus on the technical characteristics"
    
    def _assess_difficulty(self, concept: str, explanation: str, level: str) -> int:
        """Assess the difficulty level of a concept"""
        if level == "high_school":
            return 1 if len(concept) < 6 else 2
        elif level == "university":
            return 2 if len(concept) < 8 else 3
        else:  # postgraduate
            return 3 if len(concept) < 10 else 4
    
    def _generate_with_online_research(self, chunk: Dict[str, Any], target_count: int, exam_board: str = None, level: str = "university") -> List[Dict[str, Any]]:
        """Generate cards using online research for accurate information"""
        # This would integrate with external APIs for research
        # For now, return enhanced understanding cards
        return self._generate_understanding_cards(chunk, target_count, "professional", exam_board, level)
    
    def _generate_strict_text_cards(self, chunk: Dict[str, Any], target_count: int) -> List[Dict[str, Any]]:
        """Generate cards strictly from text (word-to-word)"""
        text = chunk.get("text", "").strip()
        cards = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Find technical terms and create definition cards
        technical_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        
        all_terms = list(set(technical_terms + acronyms))
        
        for term in all_terms[:target_count]:
            if len(term) < 3 or term.lower() in ['the', 'and', 'for', 'with', 'that', 'this']:
                continue
            
            # Find the sentence that contains this term
            containing_sentence = ""
            for sentence in sentences:
                if term in sentence:
                    containing_sentence = sentence.strip()
                    break
            
            if containing_sentence:
                # Create a simple definition card
                question = f"What is {term}?"
                answer = containing_sentence
                
                cards.append({
                    "id": str(uuid.uuid4()),
                    "type": "definition",
                    "front": question,
                    "back": answer,
                    "concept": term,
                    "difficulty": 2,
                    "style": "simple",
                    "ai_enhanced": False
                })
        
        return cards[:target_count]

    def _create_cloze_card(self, concept: str, understanding: Dict[str, Any], style: str) -> Optional[Dict[str, Any]]:
        """Create a cloze card that demonstrates understanding"""
        
        context_sentences = understanding.get("context_sentences", [])
        if not context_sentences:
            return None
        
        # Find a good sentence for cloze
        sentence = context_sentences[0]
        if len(sentence) < 30:
            return None
        
        # Find a good word to blank out
        words = sentence.split()
        good_words = []
        
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word)
            if (len(word_clean) > 5 and 
                word_clean[0].isupper() or 
                word_clean.lower() in ['memory', 'storage', 'system', 'technology', 'process', 'volatile', 'non-volatile']):
                good_words.append(word_clean)
        
        if not good_words:
            return None
        
        answer = good_words[0]
        cloze_question = sentence.replace(answer, "_____")
        
        return {
            "id": str(uuid.uuid4()),
            "type": "cloze",
            "front": f"Complete: {cloze_question}",
            "back": answer,
            "concept": concept,
            "difficulty": 1,
            "style": style
        }
    
    def _create_explanation_card(self, concept: str, understanding: Dict[str, Any], style: str, exam_board: str = None, level: str = "university") -> Optional[Dict[str, Any]]:
        """Create an explanation card about how something works"""
        
        role = understanding.get("role", "")
        explanation = understanding.get("explanation", "")
        
        if not role:
            return None
        
        # Create question based on role
        if role == "volatile_memory":
            question = f"How does {concept} maintain data integrity?"
            answer = f"{concept} requires periodic refresh cycles to maintain data integrity because it uses capacitors that lose charge over time."
        elif role == "non_volatile_memory":
            question = f"How does {concept} retain data without power?"
            answer = f"{concept} retains data without power because it uses non-volatile storage mechanisms that don't require electrical charge to maintain information."
        elif role == "control_component":
            question = f"What is the role of {concept} in the system?"
            answer = f"{concept} manages and coordinates system operations, ensuring proper communication and control between different components."
        else:
            question = f"How does {concept} function in computer architecture?"
            answer = f"{concept} functions as a key component in computer architecture, {explanation[:100]}..."
        
        return {
            "id": str(uuid.uuid4()),
            "type": "explanation",
            "front": question,
            "back": answer,
            "concept": concept,
            "difficulty": 3,
            "style": style,
            "exam_board": exam_board,
            "level": level
        }
    
    def _create_comparison_card(self, concept: str, understanding: Dict[str, Any], style: str) -> Optional[Dict[str, Any]]:
        """Create a comparison card between related concepts"""
        
        related_concepts = understanding.get("related_concepts", [])
        if not related_concepts:
            return None
        
        # Find a good comparison
        for related in related_concepts[:3]:  # Limit to first 3
            if related != concept and len(related) > 3:
                # Create comparison question
                question = f"What is the difference between {concept} and {related}?"
                
                # Create comparison answer based on context
                if "volatile" in concept.lower() or "volatile" in related.lower():
                    answer = f"{concept} is volatile memory that loses data when power is off, while {related} may have different characteristics. The key difference lies in their data retention mechanisms."
                elif "memory" in concept.lower() or "memory" in related.lower():
                    answer = f"{concept} and {related} are both memory components but serve different purposes. {concept} is optimized for specific use cases while {related} has different performance characteristics."
                else:
                    answer = f"{concept} and {related} are related components in computer architecture. {concept} focuses on one aspect while {related} handles different functionality."
                
                return {
                    "id": str(uuid.uuid4()),
                    "type": "comparison",
                    "front": question,
                    "back": answer,
                    "concept": concept,
                    "difficulty": 4,
                    "style": style
                }
        
        return None

# Backward compatibility
def generate_flashcards_for_chunk(chunk: Dict[str, Any], prefer_llm: bool = False, target_count: int = 10) -> List[Dict[str, Any]]:
    """Backward compatibility function"""
    generator = SmartFlashcardGenerator()
    return generator.generate_flashcards(chunk, "text_understanding", "professional", False, None, "university", target_count)
