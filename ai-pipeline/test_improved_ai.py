#!/usr/bin/env python3
"""
Test script for the improved AI flashcard pipeline
"""

import sys
import os
sys.path.append('app')

from ai_core import AICore

def test_improved_ai():
    """Test the improved AI pipeline"""
    
    print("🧠 Testing Improved AI Flashcard Pipeline")
    print("=" * 50)
    
    # Sample content (your memory architecture text)
    sample_content = """
    Volatile and non-volatile memory architectures play fundamentally distinct yet complementary roles within modern computing systems. Random Access Memory (RAM), typically implemented as either Dynamic RAM (DRAM) or Static RAM (SRAM), constitutes the primary volatile storage medium, optimized for high-frequency read/write operations with low latency. DRAM relies on capacitive charge retention within integrated circuits, necessitating periodic refresh cycles via specialized memory controllers to mitigate charge leakage; this makes DRAM highly dense but power-dependent. Conversely, SRAM employs bistable latching circuitry, eliminating the refresh requirement but at the cost of reduced density and higher per-bit energy consumption, thereby confining its usage to cache hierarchies (L1, L2, L3) integrated directly into the CPU architecture.

    Read-Only Memory (ROM), in contrast, represents a class of non-volatile storage whose primary function is the persistent retention of firmware and low-level bootstrapping instructions. Variants such as Programmable ROM (PROM), Erasable PROM (EPROM), and Electrically Erasable PROM (EEPROM, including modern Flash memory) provide progressive degrees of mutability, enabling updates while maintaining non-volatility. Embedded ROM in system-on-chip (SoC) designs often contains immutable microcode essential for hardware initialization sequences and security-critical operations such as secure boot.

    The interplay between RAM and ROM underpins computational efficiency: ROM establishes immutable instruction sets and baseline configuration parameters, while RAM facilitates transient, high-throughput data manipulation during active computation. Advanced system designs increasingly integrate hybrid memory hierarchies, employing techniques such as non-volatile DIMMs (NVDIMMs) and emerging memory technologies (e.g., Phase-Change Memory and MRAM), which blur the distinction between RAM-like volatility and ROM-like persistence, aiming to converge high-speed random access with long-term durability.
    """
    
    print(f"📝 Sample Content: {sample_content[:100]}...")
    print()
    
    # Initialize AI core
    ai_core = AICore()
    
    print("🎯 Generating flashcards with improved AI...")
    print()
    
    try:
        # Test different card counts
        for count in [5, 10, 15]:
            print(f"📚 Generating {count} cards:")
            flashcards = ai_core.generate_flashcards(sample_content, count)
            
            print(f"✅ Generated {len(flashcards)} flashcards!")
            
            for i, card in enumerate(flashcards[:3], 1):  # Show first 3
                print(f"   Card {i} ({card['type'].upper()}) - {card['difficulty']}")
                print(f"   Q: {card['question']}")
                print(f"   A: {card['answer'][:80]}...")
                print()
            
            print("-" * 40)
            print()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_ai()
