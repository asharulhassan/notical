import json
import os

def fix_english_deck():
    """Fix the English deck with proper vocabulary definitions"""
    print("🔧 Fixing English deck with proper vocabulary definitions...")
    
    # Correct vocabulary definitions
    vocab_definitions = {
        'serendipity': 'The occurrence and development of events by chance in a happy or beneficial way',
        'ephemeral': 'Lasting for a very short time; transitory',
        'ubiquitous': 'Present, appearing, or found everywhere',
        'mellifluous': 'Sweet or musical; pleasant to hear',
        'petrichor': 'A pleasant smell that frequently accompanies the first rain after a long period of warm, dry weather',
        'aurora': 'Natural light display in the sky, especially in polar regions',
        'ethereal': 'Extremely delicate and light in a way that seems not to be of this world',
        'luminous': 'Giving off light; bright or shining',
        'resplendent': 'Attractive and impressive through being richly colorful or sumptuous',
        'magnificent': 'Extremely beautiful, elaborate, or impressive',
        'eloquent': 'Fluent or persuasive in speaking or writing',
        'articulate': 'Having or showing the ability to speak fluently and coherently',
        'persuasive': 'Good at persuading someone to do or believe something',
        'compelling': 'Evoking interest, attention, or admiration in a powerfully irresistible way',
        'convincing': 'Able to persuade someone that something is true or right',
        'authentic': 'Of undisputed origin and not a copy; genuine',
        'genuine': 'Truly what something is said to be; authentic',
        'legitimate': 'Conforming to the law or to rules',
        'credible': 'Able to be believed; convincing',
        'reliable': 'Consistently good in quality or performance; able to be trusted',
        'innovative': 'Featuring new methods or ideas',
        'creative': 'Relating to or involving the imagination or original ideas',
        'imaginative': 'Having or showing creativity or inventiveness',
        'inventive': 'Having the ability to create or design new things',
        'original': 'Present or existing from the beginning; first or earliest',
        'resilient': 'Able to withstand or recover quickly from difficult conditions',
        'persistent': 'Continuing firmly or obstinately in a course of action',
        'determined': 'Having made a firm decision and being resolved not to change it',
        'tenacious': 'Tending to keep a firm hold of something; clinging or adhering closely',
        'steadfast': 'Resolutely or dutifully firm and unwavering',
        'compassionate': 'Feeling or showing sympathy and concern for others',
        'empathetic': 'Showing an ability to understand and share the feelings of another',
        'sympathetic': 'Feeling, showing, or expressing sympathy',
        'caring': 'Displaying kindness and concern for others',
        'kind': 'Having or showing a friendly, generous, and considerate nature',
        'diligent': 'Having or showing care and conscientiousness in one\'s work or duties',
        'industrious': 'Diligent and hardworking',
        'hardworking': 'Tending to work with energy and commitment; diligent',
        'conscientious': 'Wishing to do what is right, especially to do one\'s work well',
        'meticulous': 'Showing great attention to detail; very careful and precise',
        'fluent': 'Able to express oneself easily and articulately',
        'expressive': 'Effectively conveying thought or feeling',
        'communicative': 'Willing, eager, or able to talk or impart information'
    }
    
    # Create corrected English deck
    corrected_english_deck = {
        'name': 'Comprehensive English Master Deck (Corrected)',
        'total_cards': 55,
        'categories': ['Vocabulary', 'Grammar', 'Literature'],
        'cards': [],
        'created_at': '2024-12-19 (Corrected)'
    }
    
    # Add corrected vocabulary cards
    for word, definition in vocab_definitions.items():
        corrected_english_deck['cards'].append({
            'front': f"Define: {word}",
            'back': definition,
            'type': 'vocabulary',
            'difficulty': 'medium'
        })
    
    # Add grammar cards (these were correct)
    grammar_cards = [
        {
            'front': 'Present Perfect vs Past Simple',
            'question': 'When do you use "have been" vs "was"?',
            'back': 'Present perfect for ongoing/recent actions, past simple for completed actions',
            'type': 'grammar',
            'difficulty': 'medium'
        },
        {
            'front': 'Conditional Sentences',
            'question': 'What are the 4 types of conditional sentences?',
            'back': 'Zero, First, Second, and Third conditionals',
            'type': 'grammar',
            'difficulty': 'medium'
        },
        {
            'front': 'Passive Voice',
            'question': 'How do you form passive voice?',
            'back': 'Object + be + past participle + by + subject',
            'type': 'grammar',
            'difficulty': 'medium'
        },
        {
            'front': 'Reported Speech',
            'question': 'How do you change direct to reported speech?',
            'back': 'Change tense back one step and adjust pronouns/time expressions',
            'type': 'grammar',
            'difficulty': 'medium'
        },
        {
            'front': 'Modal Verbs',
            'question': 'What do modal verbs express?',
            'back': 'Possibility, necessity, ability, permission, obligation',
            'type': 'grammar',
            'difficulty': 'medium'
        }
    ]
    
    corrected_english_deck['cards'].extend(grammar_cards)
    
    # Add literature cards (these were correct)
    literature_cards = [
        {
            'front': 'Shakespeare',
            'question': 'Who wrote "Romeo and Juliet"?',
            'back': 'William Shakespeare',
            'type': 'literature',
            'difficulty': 'medium'
        },
        {
            'front': 'Pride and Prejudice',
            'question': 'Who is the protagonist of "Pride and Prejudice"?',
            'back': 'Elizabeth Bennet',
            'type': 'literature',
            'difficulty': 'medium'
        },
        {
            'front': '1984',
            'question': 'Who wrote "1984"?',
            'back': 'George Orwell',
            'type': 'literature',
            'difficulty': 'medium'
        },
        {
            'front': 'To Kill a Mockingbird',
            'question': 'Who is the narrator of "To Kill a Mockingbird"?',
            'back': 'Scout Finch',
            'type': 'literature',
            'difficulty': 'medium'
        },
        {
            'front': 'The Great Gatsby',
            'question': 'What is the green light a symbol of in "The Great Gatsby"?',
            'back': 'The American Dream',
            'type': 'literature',
            'difficulty': 'medium'
        }
    ]
    
    corrected_english_deck['cards'].extend(literature_cards)
    
    # Update total count
    corrected_english_deck['total_cards'] = len(corrected_english_deck['cards'])
    
    # Create training/testing split
    import random
    random.shuffle(corrected_english_deck['cards'])
    
    total_cards = len(corrected_english_deck['cards'])
    training_size = int(total_cards * 0.8)
    testing_size = total_cards - training_size
    
    training_deck = {
        'name': 'English Training Deck (80%) - Corrected',
        'total_cards': training_size,
        'cards': corrected_english_deck['cards'][:training_size],
        'split': 'training'
    }
    
    testing_deck = {
        'name': 'English Testing Deck (20%) - Corrected',
        'total_cards': testing_size,
        'cards': corrected_english_deck['cards'][training_size:],
        'split': 'testing'
    }
    
    # Save corrected decks
    os.makedirs('generated_flashcards', exist_ok=True)
    
    with open('generated_flashcards/comprehensive_english_deck_CORRECTED.json', 'w', encoding='utf-8') as f:
        json.dump(corrected_english_deck, f, indent=2, ensure_ascii=False)
    
    with open('generated_flashcards/english_training_deck_CORRECTED.json', 'w', encoding='utf-8') as f:
        json.dump(training_deck, f, indent=2, ensure_ascii=False)
    
    with open('generated_flashcards/english_testing_deck_CORRECTED.json', 'w', encoding='utf-8') as f:
        json.dump(testing_deck, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fixed English deck created with {total_cards} cards")
    print(f"✅ Training deck: {training_size} cards (80%)")
    print(f"✅ Testing deck: {testing_size} cards (20%)")
    print("✅ All vocabulary definitions are now correct!")
    
    return corrected_english_deck, training_deck, testing_deck

if __name__ == "__main__":
    fix_english_deck()
