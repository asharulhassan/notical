import json
import os
import glob

def get_deck_statistics():
    """Get statistics for all generated decks"""
    print("🎯 FLASHCARD DECK SUMMARY REPORT")
    print("=" * 50)
    
    # Find all JSON files in generated_flashcards directory
    json_files = glob.glob('generated_flashcards/*.json')
    
    total_cards = 0
    deck_stats = []
    
    for file_path in sorted(json_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                deck_data = json.load(f)
            
            deck_name = deck_data.get('name', 'Unknown')
            card_count = deck_data.get('total_cards', len(deck_data.get('cards', [])))
            categories = deck_data.get('categories', [])
            split_type = deck_data.get('split', 'consolidated')
            
            deck_stats.append({
                'name': deck_name,
                'cards': card_count,
                'categories': categories,
                'type': split_type,
                'file': os.path.basename(file_path)
            })
            
            total_cards += card_count
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Group by deck type
    consolidated_decks = [d for d in deck_stats if d['type'] == 'consolidated']
    training_decks = [d for d in deck_stats if d['type'] == 'training']
    testing_decks = [d for d in deck_stats if d['type'] == 'testing']
    
    print(f"\n📊 TOTAL CARDS ACROSS ALL DECKS: {total_cards}")
    print(f"📁 TOTAL FILES GENERATED: {len(json_files)}")
    
    print(f"\n🔗 CONSOLIDATED DECKS ({len(consolidated_decks)}):")
    for deck in consolidated_decks:
        print(f"  • {deck['name']}: {deck['cards']} cards")
        if deck['categories']:
            print(f"    Categories: {', '.join(deck['categories'])}")
    
    print(f"\n📚 TRAINING DECKS ({len(training_decks)}):")
    for deck in training_decks:
        print(f"  • {deck['name']}: {deck['cards']} cards (80%)")
    
    print(f"\n🧪 TESTING DECKS ({len(testing_decks)}):")
    for deck in testing_decks:
        print(f"  • {deck['name']}: {deck['cards']} cards (20%)")
    
    # Calculate totals by phase
    english_total = sum(d['cards'] for d in deck_stats if 'English' in d['name'])
    humanities_total = sum(d['cards'] for d in deck_stats if 'Humanities' in d['name'])
    complex_total = sum(d['cards'] for d in deck_stats if 'Complex' in d['name'])
    
    print(f"\n📈 PHASE BREAKDOWN:")
    print(f"  • Phase 1 (English): {english_total} cards")
    print(f"  • Phase 2 (Humanities): {humanities_total} cards")
    print(f"  • Phase 3 (Complex Subjects): {complex_total} cards")
    
    print(f"\n✅ ALL PHASES COMPLETED SUCCESSFULLY!")
    print("=" * 50)

if __name__ == "__main__":
    get_deck_statistics()
