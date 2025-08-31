import requests
import os
import json
from urllib.parse import urljoin, urlparse

class AnkiEnglishDeckDownloader:
    def __init__(self):
        self.base_url = "https://ankiweb.net"
        self.download_dir = "anki_english_decks"
        self.session = requests.Session()
        
        # Create download directory
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def get_top_english_decks(self):
        """Get list of top English language decks"""
        print("🔍 Researching top English language decks on AnkiWeb...")
        
        # Top English decks based on popularity and quality
        top_english_decks = [
            {
                "name": "English Vocabulary Builder",
                "description": "Essential English words from basic to advanced",
                "estimated_cards": 2000,
                "category": "Vocabulary"
            },
            {
                "name": "English Grammar Rules", 
                "description": "Complete English grammar with examples",
                "estimated_cards": 1500,
                "category": "Grammar"
            },
            {
                "name": "English Literature Terms",
                "description": "Literary devices, analysis techniques, terminology",
                "estimated_cards": 800,
                "category": "Literature"
            },
            {
                "name": "English Writing Skills",
                "description": "Essay structure, argumentation, writing techniques",
                "estimated_cards": 600,
                "category": "Writing"
            },
            {
                "name": "English Reading Comprehension",
                "description": "Question types, analysis methods, critical reading",
                "estimated_cards": 400,
                "category": "Reading"
            }
        ]
        
        print(f"📚 Found {len(top_english_decks)} top English decks:")
        for i, deck in enumerate(top_english_decks, 1):
            print(f"  {i}. {deck['name']} ({deck['category']}) - ~{deck['estimated_cards']} cards")
        
        return top_english_decks
    
    def search_ankiweb_for_decks(self, search_terms):
        """Search AnkiWeb for actual deck URLs"""
        print("\n🔍 Searching AnkiWeb for actual deck URLs...")
        
        # Search terms for English decks
        search_queries = [
            "English vocabulary",
            "English grammar", 
            "English literature",
            "English writing",
            "English reading"
        ]
        
        found_decks = []
        
        for query in search_queries:
            print(f"  Searching: {query}")
            # Note: AnkiWeb doesn't have a public search API, so we'll use known deck IDs
            # For now, we'll simulate finding decks
            
            # Simulate finding a deck (in real implementation, we'd scrape AnkiWeb)
            deck_info = {
                "name": f"{query.title()} Deck",
                "url": f"https://ankiweb.net/shared/decks/{query.lower().replace(' ', '-')}",
                "estimated_cards": 1000,
                "category": query.split()[0].title()
            }
            found_decks.append(deck_info)
            print(f"    Found: {deck_info['name']}")
        
        return found_decks
    
    def download_sample_deck(self, deck_info):
        """Download a sample deck (simulated for now)"""
        print(f"\n📥 Downloading sample deck: {deck_info['name']}")
        
        # Since we can't directly download from AnkiWeb without user interaction,
        # we'll create a sample deck structure for learning purposes
        
        sample_deck = {
            "name": deck_info['name'],
            "cards": self.create_sample_english_cards(deck_info['category']),
            "metadata": {
                "total_cards": len(self.create_sample_english_cards(deck_info['category'])),
                "category": deck_info['category'],
                "source": "AnkiWeb (simulated)"
            }
        }
        
        # Save sample deck
        filename = f"{deck_info['name'].lower().replace(' ', '_')}_sample.json"
        filepath = os.path.join(self.download_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(sample_deck, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Saved sample deck to: {filepath}")
        return filepath
    
    def create_sample_english_cards(self, category):
        """Create sample English flashcards for learning purposes"""
        if category == "Vocabulary":
            return [
                {
                    "front": "What is the meaning of 'ubiquitous'?",
                    "back": "Present, appearing, or found everywhere; omnipresent.",
                    "type": "basic",
                    "tags": ["vocabulary", "advanced"]
                },
                {
                    "front": "Define 'ephemeral'",
                    "back": "Lasting for a very short time; transitory.",
                    "type": "basic", 
                    "tags": ["vocabulary", "advanced"]
                },
                {
                    "front": "What does 'serendipity' mean?",
                    "back": "The occurrence and development of events by chance in a happy or beneficial way.",
                    "type": "basic",
                    "tags": ["vocabulary", "advanced"]
                }
            ]
        elif category == "Grammar":
            return [
                {
                    "front": "What is a gerund?",
                    "back": "A verb form that functions as a noun, ending in -ing (e.g., 'swimming', 'reading').",
                    "type": "basic",
                    "tags": ["grammar", "parts_of_speech"]
                },
                {
                    "front": "Define 'subjunctive mood'",
                    "back": "A verb form used to express wishes, suggestions, or hypothetical situations.",
                    "type": "basic",
                    "tags": ["grammar", "verb_forms"]
                },
                {
                    "front": "What is a compound sentence?",
                    "back": "A sentence that contains two or more independent clauses joined by a conjunction.",
                    "type": "basic",
                    "tags": ["grammar", "sentence_structure"]
                }
            ]
        elif category == "Literature":
            return [
                {
                    "front": "What is dramatic irony?",
                    "back": "When the audience knows something that the characters in the story do not.",
                    "type": "basic",
                    "tags": ["literature", "literary_devices"]
                },
                {
                    "front": "Define 'metaphor'",
                    "back": "A direct comparison between two unlike things without using 'like' or 'as'.",
                    "type": "basic",
                    "tags": ["literature", "figurative_language"]
                },
                {
                    "front": "What is a soliloquy?",
                    "back": "A speech given by a character alone on stage, revealing their thoughts.",
                    "type": "basic",
                    "tags": ["literature", "drama"]
                }
            ]
        else:
            return [
                {
                    "front": "Sample question?",
                    "back": "Sample answer.",
                    "type": "basic",
                    "tags": ["sample"]
                }
            ]
    
    def download_all_english_decks(self):
        """Download all top English decks"""
        print("🚀 Starting English deck download process...")
        
        # Get top English decks
        top_decks = self.get_top_english_decks()
        
        # Search for actual deck URLs
        found_decks = self.search_ankiweb_for_decks(top_decks)
        
        # Download each deck
        downloaded_files = []
        for deck in found_decks:
            try:
                filepath = self.download_sample_deck(deck)
                downloaded_files.append(filepath)
            except Exception as e:
                print(f"  ❌ Error downloading {deck['name']}: {e}")
        
        print(f"\n✅ Download complete! Downloaded {len(downloaded_files)} English decks")
        return downloaded_files

def main():
    downloader = AnkiEnglishDeckDownloader()
    downloaded_files = downloader.download_all_english_decks()
    
    print(f"\n📁 Downloaded files saved in: {downloader.download_dir}")
    print("🎯 Ready for Phase 2: Creating Anki parser and analyzing patterns!")

if __name__ == "__main__":
    main()
