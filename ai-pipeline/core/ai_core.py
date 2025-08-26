"""
NOTICAL AI Core
===============
Enhanced AI core that works with your SmartFlashcardGenerator
to provide better understanding and intelligence.
"""

import re
import random
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class NOTICALAICore:
    """
    Enhanced AI core that provides intelligent content analysis
    and works with your SmartFlashcardGenerator
    """
    
    def __init__(self):
        """Initialize the AI core"""
        self.knowledge_base = {}
        self.learning_history = []
        logger.info("✅ NOTICAL AI Core initialized")
    
    def analyze_content_intelligently(self, text: str) -> Dict[str, Any]:
        """
        Intelligently analyze content to extract meaningful information
        """
        if not text.strip():
            return {}
        
        # Split into sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]
        
        # Extract key concepts (not just random words)
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
            'complexity_score': self._assess_complexity(text),
            'subject_areas': self._detect_subject_areas(text)
        }
    
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

# Create global instance
ai_core = NOTICALAICore()
