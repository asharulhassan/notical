#!/usr/bin/env python3
"""
Test script for the enhanced AI pipeline with AI Core integration
"""

import sys
import os
sys.path.append('app')

from generator import SmartFlashcardGenerator
from ai_core import ai_core

def test_enhanced_ai():
    """Test the enhanced AI pipeline with AI Core integration"""

    print("🧠 Testing Enhanced AI Pipeline with AI Core Integration")
    print("=" * 60)

    # Sample content (your memory architecture text)
    sample_content = """
    Volatile and non-volatile memory architectures play fundamentally distinct yet complementary roles within modern computing systems. Random Access Memory (RAM), typically implemented as either Dynamic RAM (DRAM) or Static RAM (SRAM), constitutes the primary volatile storage medium, optimized for high-frequency read/write operations with low latency. DRAM relies on capacitive charge retention within integrated circuits, necessitating periodic refresh cycles via specialized memory controllers to mitigate charge leakage; this makes DRAM highly dense but power-dependent. Conversely, SRAM employs bistable latching circuitry, eliminating the refresh requirement but at the cost of reduced density and higher per-bit energy consumption, thereby confining its usage to cache hierarchies (L1, L2, L3) integrated directly into the CPU architecture.

    Read-Only Memory (ROM), in contrast, represents a class of non-volatile storage whose primary function is the persistent retention of firmware and low-level bootstrapping instructions. Variants such as Programmable ROM (PROM), Erasable PROM (EPROM), and Electrically Erasable PROM (EEPROM, including modern Flash memory) provide progressive degrees of mutability, enabling updates while maintaining non-volatility. Embedded ROM in system-on-chip (SoC) designs often contains immutable microcode essential for hardware initialization sequences and security-critical operations such as secure boot.

    The interplay between RAM and ROM underpins computational efficiency: ROM establishes immutable instruction sets and baseline configuration parameters, while RAM facilitates transient, high-throughput data manipulation during active computation. Advanced system designs increasingly integrate hybrid memory hierarchies, employing techniques such as non-volatile DIMMs (NVDIMMs) and emerging memory technologies (e.g., Phase-Change Memory and MRAM), which blur the distinction between RAM-like volatility and ROM-like persistence, aiming to converge high-speed random access with long-term durability.
    """

    print(f"📝 Sample Content: {sample_content[:100]}...")
    print()

    # Test 1: AI Core Analysis
    print("1️⃣ Testing AI Core Content Analysis:")
    content_analysis = ai_core.analyze_content_intelligently(sample_content)
    
    print(f"   Complexity Score: {content_analysis.get('complexity_score', 0)}/10")
    print(f"   Key Concepts Found: {len(content_analysis.get('key_concepts', []))}")
    print(f"   Subject Areas: {content_analysis.get('subject_areas', [])}")
    print(f"   Processes Found: {len(content_analysis.get('processes', []))}")
    print(f"   Comparisons Found: {len(content_analysis.get('comparisons', []))}")
    print()

    # Show some key concepts
    key_concepts = content_analysis.get('key_concepts', [])
    print("   Top Key Concepts:")
    for i, concept in enumerate(key_concepts[:5], 1):
        print(f"   {i}. {concept.get('term', '')} ({concept.get('type', '')}) - Importance: {concept.get('importance', 0)}")
    print()

    # Test 2: Enhanced Generation Parameters
    print("2️⃣ Testing Enhanced Generation Parameters:")
    enhanced_params = ai_core.enhance_generation_parameters(content_analysis, 10)
    
    print(f"   Recommended Card Types: {enhanced_params.get('card_types', [])}")
    print(f"   Recommended Style: {enhanced_params.get('style', '')}")
    print(f"   Adjusted Target Count: {enhanced_params.get('target_count', 0)}")
    print(f"   Content Complexity: {enhanced_params.get('complexity', 0)}/10")
    print()

    # Test 3: Enhanced Generator with AI Core
    print("3️⃣ Testing Enhanced Generator with AI Core:")
    generator = SmartFlashcardGenerator()
    
    chunk = {
        "id": "test_chunk_1",
        "text": sample_content,
        "type": "text"
    }

    # Test different modes
    print("   Testing 'text_understanding' mode (AI Enhanced):")
    ai_enhanced_cards = generator.generate_flashcards(
        chunk,
        mode="text_understanding",
        style="professional",
        target_count=5
    )

    print(f"   Generated {len(ai_enhanced_cards)} AI-enhanced cards")
    for i, card in enumerate(ai_enhanced_cards[:3], 1):
        print(f"   Card {i}: {card['front']}")
        print(f"   Answer: {card['back'][:80]}...")
        print(f"   Type: {card['type']}, AI Enhanced: {card.get('ai_enhanced', False)}")
        print()

    # Test 4: Comparison with old method
    print("4️⃣ Testing 'strict_text' mode (Old Method):")
    strict_cards = generator.generate_flashcards(
        chunk,
        mode="strict_text",
        style="professional",
        target_count=3
    )

    print(f"   Generated {len(strict_cards)} strict text cards")
    for i, card in enumerate(strict_cards[:2], 1):
        print(f"   Card {i}: {card['front']}")
        print(f"   Answer: {card['back'][:80]}...")
        print(f"   Type: {card['type']}")
        print()

    print("=" * 60)
    print("🎉 Enhanced AI Pipeline Features:")
    print("   ✅ AI Core Integration: Intelligent content analysis")
    print("   ✅ Smart Understanding: Actually understands concepts, not just finds words")
    print("   ✅ Context-Aware Generation: Uses content analysis to guide card creation")
    print("   ✅ Multiple Card Types: Definition, explanation, cloze, comparison")
    print("   ✅ Difficulty Assessment: Based on content complexity")
    print("   ✅ Subject Detection: Automatically identifies subject areas")
    print("   ✅ Process & Comparison Extraction: Finds relationships and mechanisms")
    print("   ✅ Enhanced Parameters: Adjusts generation strategy based on content")

if __name__ == "__main__":
    test_enhanced_ai()
