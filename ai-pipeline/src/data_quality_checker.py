import json
import os
import glob
from collections import defaultdict

def check_data_quality():
    """Comprehensive data quality check for the massive flashcard dataset"""
    print("🔍 COMPREHENSIVE DATA QUALITY ASSESSMENT")
    print("=" * 80)
    
    # Find all massive deck files
    massive_files = glob.glob('generated_flashcards/massive_*.json')
    
    if not massive_files:
        print("❌ No massive deck files found!")
        return False
    
    print(f"📁 Found {len(massive_files)} massive deck files")
    
    quality_issues = []
    total_cards = 0
    deck_stats = {}
    
    # Check each massive deck
    for file_path in sorted(massive_files):
        print(f"\n🔍 Analyzing: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                deck_data = json.load(f)
            
            deck_name = deck_data.get('name', 'Unknown')
            card_count = deck_data.get('total_cards', len(deck_data.get('cards', [])))
            cards = deck_data.get('cards', [])
            
            deck_stats[deck_name] = {
                'file': os.path.basename(file_path),
                'total_cards': card_count,
                'actual_cards': len(cards),
                'issues': []
            }
            
            total_cards += len(cards)
            
            # Check basic structure
            if not isinstance(cards, list):
                quality_issues.append(f"{deck_name}: Cards field is not a list")
                deck_stats[deck_name]['issues'].append("Cards field is not a list")
                continue
            
            if len(cards) == 0:
                quality_issues.append(f"{deck_name}: No cards found")
                deck_stats[deck_name]['issues'].append("No cards found")
                continue
            
            # Check card structure and quality
            card_issues = check_card_quality(cards, deck_name)
            quality_issues.extend(card_issues)
            deck_stats[deck_name]['issues'].extend(card_issues)
            
            # Check for duplicates
            duplicate_issues = check_for_duplicates(cards, deck_name)
            quality_issues.extend(duplicate_issues)
            deck_stats[deck_name]['issues'].extend(duplicate_issues)
            
            # Check content diversity
            diversity_issues = check_content_diversity(cards, deck_name)
            quality_issues.extend(diversity_issues)
            deck_stats[deck_name]['issues'].extend(diversity_issues)
            
            print(f"  ✅ Cards: {len(cards):,}")
            print(f"  ✅ Issues found: {len(deck_stats[deck_name]['issues'])}")
            
        except Exception as e:
            error_msg = f"Error reading {file_path}: {e}"
            quality_issues.append(error_msg)
            print(f"  ❌ {error_msg}")
    
    # Overall quality assessment
    print(f"\n" + "=" * 80)
    print("📊 OVERALL QUALITY ASSESSMENT")
    print("=" * 80)
    
    print(f"📊 Total cards analyzed: {total_cards:,}")
    print(f"📁 Total files checked: {len(massive_files)}")
    print(f"❌ Total quality issues: {len(quality_issues)}")
    
    # Calculate quality score
    total_issues = len(quality_issues)
    quality_score = max(0, 100 - (total_issues * 2))  # Deduct 2 points per issue
    quality_score = min(100, quality_score)
    
    print(f"🎯 QUALITY SCORE: {quality_score}/100")
    
    if quality_score >= 90:
        print("🏆 EXCELLENT QUALITY - Ready for training!")
    elif quality_score >= 80:
        print("✅ GOOD QUALITY - Minor issues, ready for training")
    elif quality_score >= 70:
        print("⚠️  ACCEPTABLE QUALITY - Some issues, should be addressed")
    else:
        print("❌ POOR QUALITY - Major issues need fixing")
    
    # Detailed issue breakdown
    if quality_issues:
        print(f"\n🔍 DETAILED ISSUE BREAKDOWN:")
        for i, issue in enumerate(quality_issues[:20], 1):  # Show first 20 issues
            print(f"  {i}. {issue}")
        
        if len(quality_issues) > 20:
            print(f"  ... and {len(quality_issues) - 20} more issues")
    
    # Deck-by-deck summary
    print(f"\n📋 DECK-BY-DECK SUMMARY:")
    for deck_name, stats in deck_stats.items():
        status = "✅" if not stats['issues'] else f"⚠️ ({len(stats['issues'])} issues)"
        print(f"  {status} {deck_name}: {stats['actual_cards']:,} cards")
    
    # Training readiness assessment
    print(f"\n🚀 TRAINING READINESS ASSESSMENT:")
    if quality_score >= 80:
        print("✅ READY FOR TRAINING - Data quality is sufficient")
        print("✅ Massive dataset will provide excellent learning material")
        print("✅ 80/20 split ensures proper validation")
    else:
        print("⚠️  NEEDS ATTENTION - Quality issues should be addressed")
        print("⚠️  Training may be less effective with current data")
    
    print("=" * 80)
    
    return quality_score >= 80

def check_card_quality(cards, deck_name):
    """Check individual card quality"""
    issues = []
    
    for i, card in enumerate(cards):
        # Check required fields
        if not isinstance(card, dict):
            issues.append(f"Card {i} is not a dictionary")
            continue
        
        required_fields = ['front', 'back']
        for field in required_fields:
            if field not in card:
                issues.append(f"Card {i} missing required field: {field}")
        
        # Check field types and content
        if 'front' in card and not isinstance(card['front'], str):
            issues.append(f"Card {i} front field is not a string")
        
        if 'back' in card and not isinstance(card['back'], str):
            issues.append(f"Card {i} back field is not a string")
        
        # Check content length
        if 'front' in card and len(card['front'].strip()) < 3:
            issues.append(f"Card {i} front content too short: '{card['front']}'")
        
        if 'back' in card and len(card['back'].strip()) < 5:
            issues.append(f"Card {i} back content too short: '{card['back']}'")
        
        # Check for placeholder content
        if 'back' in card and 'comprehensive explanation' in card['back'].lower():
            if len(card['back']) < 50:  # Too short for comprehensive
                issues.append(f"Card {i} back content seems like placeholder")
        
        # Check difficulty field if present
        if 'difficulty' in card:
            valid_difficulties = ['easy', 'medium', 'hard']
            if card['difficulty'] not in valid_difficulties:
                issues.append(f"Card {i} has invalid difficulty: {card['difficulty']}")
        
        # Check type field if present
        if 'type' in card:
            if not isinstance(card['type'], str):
                issues.append(f"Card {i} type field is not a string")
    
    return issues

def check_for_duplicates(cards, deck_name):
    """Check for duplicate cards"""
    issues = []
    
    # Check for exact duplicates
    seen_cards = set()
    duplicates = []
    
    for i, card in enumerate(cards):
        # Create a hash of the card content
        card_hash = f"{card.get('front', '')}|{card.get('back', '')}"
        
        if card_hash in seen_cards:
            duplicates.append(i)
        else:
            seen_cards.add(card_hash)
    
    if duplicates:
        issues.append(f"Found {len(duplicates)} duplicate cards")
    
    # Check for similar content (potential duplicates)
    front_texts = [card.get('front', '').lower().strip() for card in cards]
    unique_fronts = len(set(front_texts))
    
    if unique_fronts < len(cards) * 0.9:  # Less than 90% unique fronts
        issues.append(f"Many similar front texts - potential duplicates")
    
    return issues

def check_content_diversity(cards, deck_name):
    """Check content diversity and variety"""
    issues = []
    
    if len(cards) < 10:
        return issues
    
    # Check category distribution
    categories = defaultdict(int)
    types = defaultdict(int)
    difficulties = defaultdict(int)
    
    for card in cards:
        if 'category' in card:
            categories[card['category']] += 1
        if 'type' in card:
            types[card['type']] += 1
        if 'difficulty' in card:
            difficulties[card['difficulty']] += 1
    
    # Check if categories are well distributed
    if len(categories) > 1:
        min_category_count = min(categories.values())
        max_category_count = max(categories.values())
        
        if max_category_count > min_category_count * 5:  # One category has 5x more cards
            issues.append(f"Uneven category distribution: {dict(categories)}")
    
    # Check if difficulties are well distributed
    if len(difficulties) > 1:
        min_diff_count = min(difficulties.values())
        max_diff_count = max(difficulties.values())
        
        if max_diff_count > min_diff_count * 3:  # One difficulty has 3x more cards
            issues.append(f"Uneven difficulty distribution: {dict(difficulties)}")
    
    # Check for repetitive patterns
    front_patterns = [card.get('front', '')[:20] for card in cards[:100]]  # Check first 100
    unique_patterns = len(set(front_patterns))
    
    if unique_patterns < len(front_patterns) * 0.7:  # Less than 70% unique patterns
        issues.append(f"Many repetitive front text patterns")
    
    return issues

if __name__ == "__main__":
    is_ready = check_data_quality()
    print(f"\n🎯 FINAL VERDICT: {'READY FOR TRAINING' if is_ready else 'NEEDS ATTENTION'}")

