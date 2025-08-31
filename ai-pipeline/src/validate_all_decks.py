import json
import os
import glob

def validate_deck_structure(deck_data, deck_name):
    """Validate individual deck structure"""
    print(f"\n🔍 Validating: {deck_name}")
    
    issues = []
    
    # Check required fields
    required_fields = ['name', 'cards']
    for field in required_fields:
        if field not in deck_data:
            issues.append(f"Missing required field: {field}")
    
    # Check cards structure
    if 'cards' in deck_data:
        cards = deck_data['cards']
        if not isinstance(cards, list):
            issues.append("Cards field is not a list")
        else:
            print(f"  📊 Total cards: {len(cards)}")
            
            # Check first few cards for structure
            for i, card in enumerate(cards[:3]):
                if not isinstance(card, dict):
                    issues.append(f"Card {i} is not a dictionary")
                else:
                    # Check card has required fields
                    if 'front' not in card or 'back' not in card:
                        issues.append(f"Card {i} missing front or back")
                    
                    # Check for consistent structure
                    card_fields = set(card.keys())
                    if i == 0:
                        expected_fields = card_fields
                    elif card_fields != expected_fields:
                        issues.append(f"Card {i} has inconsistent structure")
    
    # Check categories if present
    if 'categories' in deck_data:
        categories = deck_data['categories']
        if isinstance(categories, list):
            print(f"  🏷️  Categories: {', '.join(categories)}")
    
    # Check split type if present
    if 'split' in deck_data:
        split_type = deck_data['split']
        print(f"  ✂️  Split type: {split_type}")
    
    if issues:
        print(f"  ❌ Issues found: {len(issues)}")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print(f"  ✅ Structure is valid!")
        return True

def validate_all_decks():
    """Validate all generated decks"""
    print("🎯 COMPREHENSIVE DECK VALIDATION REPORT")
    print("=" * 60)
    
    # Find all JSON files
    json_files = glob.glob('generated_flashcards/*.json')
    
    valid_decks = 0
    total_decks = len(json_files)
    
    print(f"📁 Found {total_decks} JSON files to validate")
    
    # Group files by type
    consolidated_files = [f for f in json_files if 'comprehensive' in f.lower() and 'corrected' not in f.lower()]
    training_files = [f for f in json_files if 'training' in f.lower()]
    testing_files = [f for f in json_files if 'testing' in f.lower()]
    corrected_files = [f for f in json_files if 'corrected' in f.lower()]
    
    print(f"\n📊 File Breakdown:")
    print(f"  • Consolidated decks: {len(consolidated_files)}")
    print(f"  • Training decks: {len(training_files)}")
    print(f"  • Testing decks: {len(testing_files)}")
    print(f"  • Corrected decks: {len(corrected_files)}")
    
    # Validate each file
    for file_path in sorted(json_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                deck_data = json.load(f)
            
            deck_name = os.path.basename(file_path)
            if validate_deck_structure(deck_data, deck_name):
                valid_decks += 1
                
        except Exception as e:
            print(f"\n❌ Error reading {file_path}: {e}")
    
    print(f"\n📈 VALIDATION SUMMARY:")
    print(f"  ✅ Valid decks: {valid_decks}")
    print(f"  ❌ Invalid decks: {total_decks - valid_decks}")
    print(f"  📊 Success rate: {(valid_decks/total_decks)*100:.1f}%")
    
    # Check if we have the essential decks for training
    essential_decks = [
        'comprehensive_english_deck_CORRECTED.json',
        'comprehensive_humanities_deck.json',
        'comprehensive_complex_subjects_deck.json'
    ]
    
    print(f"\n🎯 ESSENTIAL DECKS CHECK:")
    for essential in essential_decks:
        if os.path.exists(f"generated_flashcards/{essential}"):
            print(f"  ✅ {essential}")
        else:
            print(f"  ❌ {essential} - MISSING!")
    
    # Training readiness assessment
    if valid_decks >= total_decks * 0.9:  # 90% success rate
        print(f"\n🚀 TRAINING READINESS: READY TO GO!")
        print("All decks are properly structured and ready for AI training.")
    else:
        print(f"\n⚠️  TRAINING READINESS: NEEDS ATTENTION")
        print("Some decks have structural issues that should be fixed before training.")
    
    print("=" * 60)
    
    return valid_decks == total_decks

if __name__ == "__main__":
    validate_all_decks()
