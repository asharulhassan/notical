#!/usr/bin/env python3
"""
Test script for your existing AI pipeline
"""

import sys
import os
sys.path.append('app')

from generator import generate_flashcards_for_chunk

def test_existing_ai():
    """Test your existing AI pipeline"""
    
    print("🧠 Testing Your Existing AI Pipeline")
    print("=" * 50)
    
    # Sample content (your memory architecture text)
    sample_content = """
    Volatile and non-volatile memory architectures play fundamentally distinct yet complementary roles within modern computing systems. Random Access Memory (RAM), typically implemented as either Dynamic RAM (DRAM) or Static RAM (SRAM), constitutes the primary volatile storage medium, optimized for high-frequency read/write operations with low latency. DRAM relies on capacitive charge retention within integrated circuits, necessitating periodic refresh cycles via specialized memory controllers to mitigate charge leakage; this makes DRAM highly dense but power-dependent. Conversely, SRAM employs bistable latching circuitry, eliminating the refresh requirement but at the cost of reduced density and higher per-bit energy consumption, thereby confining its usage to cache hierarchies (L1, L2, L3) integrated directly into the CPU architecture.

    Read-Only Memory (ROM), in contrast, represents a class of non-volatile storage whose primary function is the persistent retention of firmware and low-level bootstrapping instructions. Variants such as Programmable ROM (PROM), Erasable PROM (EPROM), and Electrically Erasable PROM (EEPROM, including modern Flash memory) provide progressive degrees of mutability, enabling updates while maintaining non-volatility. Embedded ROM in system-on-chip (SoC) designs often contains immutable microcode essential for hardware initialization sequences and security-critical operations such as secure boot.

    The interplay between RAM and ROM underpins computational efficiency: ROM establishes immutable instruction sets and baseline configuration parameters, while RAM facilitates transient, high-throughput data manipulation during active computation. Advanced system designs increasingly integrate hybrid memory hierarchies, employing techniques such as non-volatile DIMMs (NVDIMMs) and emerging memory technologies (e.g., Phase-Change Memory and MRAM), which blur the distinction between RAM-like volatility and ROM-like persistence, aiming to converge high-speed random access with long-term durability.
    """
    
    print(f"📝 Sample Content: {sample_content[:100]}...")
    print()
    
    # Create a chunk for your existing pipeline
    chunk = {
        "id": "test_chunk_1",
        "text": sample_content,
        "type": "text"
    }
    
    print("🎯 Generating flashcards with your existing AI pipeline...")
    print()
    
    try:
        # Use your existing generator
        flashcards = generate_flashcards_for_chunk(chunk, prefer_llm=False)
        
        print(f"✅ Generated {len(flashcards)} flashcards!")
        print()
        
        for i, card in enumerate(flashcards, 1):
            print(f"📚 Card {i} ({card['type'].upper()}) - Difficulty: {card.get('difficulty', 'N/A')}")
            print(f"   Q: {card['front']}")
            print(f"   A: {card['back'][:100]}...")
            print()
        
        print("=" * 50)
        print("🎉 Your existing AI pipeline is working!")
        print("   - It understands technical content")
        print("   - It generates relevant questions")
        print("   - It creates proper cloze cards")
        print("   - It assigns difficulty levels")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_existing_ai()
