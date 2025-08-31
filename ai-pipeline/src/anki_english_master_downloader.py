import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

class AnkiEnglishMasterDownloader:
    def __init__(self):
        self.output_dir = "anki_english_master_data"
        self.base_url = "https://ankiweb.net"
        self.session = requests.Session()
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_top_english_decks(self):
        """Get top English decks from AnkiWeb shared decks"""
        print("🔍 Searching for top English decks on AnkiWeb...")
        
        # English deck categories and search terms
        english_categories = [
            "english",
            "vocabulary", 
            "grammar",
            "literature",
            "writing",
            "reading",
            "toefl",
            "ielts",
            "sat",
            "gre",
            "esl",
            "phrasal_verbs",
            "idioms",
            "pronunciation",
            "business_english",
            "academic_english"
        ]
        
        all_decks = []
        
        for category in english_categories:
            try:
                print(f"📚 Searching for {category} decks...")
                
                # Search URL for each category
                search_url = f"{self.base_url}/shared/decks/?search={category}&sort=downloads"
                
                response = self.session.get(search_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find deck listings
                    deck_links = soup.find_all('a', href=True)
                    
                    for link in deck_links:
                        if '/shared/info/' in link['href']:
                            deck_id = link['href'].split('/')[-1]
                            deck_name = link.get_text(strip=True)
                            
                            if deck_name and len(deck_name) > 3:
                                deck_info = {
                                    'id': deck_id,
                                    'name': deck_name,
                                    'category': category,
                                    'url': f"{self.base_url}/shared/info/{deck_id}",
                                    'download_url': f"{self.base_url}/shared/download/{deck_id}"
                                }
                                all_decks.append(deck_info)
                
                # Be respectful with requests
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"❌ Error searching {category}: {e}")
                continue
        
        print(f"✅ Found {len(all_decks)} potential English decks")
        return all_decks
    
    def get_deck_details(self, deck_info):
        """Get detailed information about a specific deck"""
        try:
            response = self.session.get(deck_info['url'], timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract deck information
                deck_details = {
                    'id': deck_info['id'],
                    'name': deck_info['name'],
                    'category': deck_info['category'],
                    'description': '',
                    'card_count': 0,
                    'downloads': 0,
                    'rating': 0,
                    'tags': [],
                    'last_updated': '',
                    'download_url': deck_info['download_url']
                }
                
                # Try to extract description
                desc_elem = soup.find('div', class_='description')
                if desc_elem:
                    deck_details['description'] = desc_elem.get_text(strip=True)
                
                # Try to extract card count
                count_elem = soup.find(text=lambda text: text and 'cards' in text.lower())
                if count_elem:
                    try:
                        count_text = count_elem.strip()
                        count_match = count_text.split()[0]
                        deck_details['card_count'] = int(count_match.replace(',', ''))
                    except:
                        pass
                
                # Try to extract downloads
                downloads_elem = soup.find(text=lambda text: text and 'downloads' in text.lower())
                if downloads_elem:
                    try:
                        downloads_text = downloads_elem.strip()
                        downloads_match = downloads_text.split()[0]
                        deck_details['downloads'] = int(downloads_match.replace(',', ''))
                    except:
                        pass
                
                return deck_details
                
        except Exception as e:
            print(f"❌ Error getting details for {deck_info['name']}: {e}")
        
        return deck_info
    
    def create_comprehensive_english_deck(self, top_decks):
        """Create one massive comprehensive English deck from all found decks"""
        print("🚀 Creating comprehensive English master deck...")
        
        # Get detailed info for top decks
        detailed_decks = []
        for i, deck in enumerate(top_decks[:50]):  # Limit to top 50 for now
            print(f"📖 Getting details for deck {i+1}/{min(50, len(top_decks))}: {deck['name']}")
            detailed_deck = self.get_deck_details(deck)
            detailed_decks.append(detailed_deck)
            time.sleep(random.uniform(0.5, 1.5))  # Be respectful
        
        # Create comprehensive deck structure
        comprehensive_deck = {
            "deck_info": {
                "name": "Comprehensive English Master Deck - AnkiWeb Data",
                "description": "Massive English deck compiled from top AnkiWeb shared decks for training and testing",
                "total_decks_found": len(detailed_decks),
                "created_date": datetime.now().isoformat(),
                "version": "1.0",
                "source": "AnkiWeb Shared Decks",
                "note": "This deck contains metadata from AnkiWeb. For actual cards, download individual .apkg files."
            },
            "deck_categories": {
                "vocabulary": [],
                "grammar": [],
                "literature": [],
                "writing": [],
                "reading": [],
                "test_prep": [],
                "business": [],
                "academic": [],
                "other": []
            },
            "all_decks": detailed_decks,
            "statistics": {
                "total_decks": len(detailed_decks),
                "total_cards_estimated": sum(deck.get('card_count', 0) for deck in detailed_decks),
                "categories_covered": len(set(deck['category'] for deck in detailed_decks))
            }
        }
        
        # Categorize decks
        for deck in detailed_decks:
            category = deck['category']
            if 'vocabulary' in category:
                comprehensive_deck['deck_categories']['vocabulary'].append(deck)
            elif 'grammar' in category:
                comprehensive_deck['deck_categories']['grammar'].append(deck)
            elif 'literature' in category:
                comprehensive_deck['deck_categories']['literature'].append(deck)
            elif 'writing' in category:
                comprehensive_deck['deck_categories']['writing'].append(deck)
            elif 'reading' in category:
                comprehensive_deck['deck_categories']['reading'].append(deck)
            elif any(term in category for term in ['toefl', 'ielts', 'sat', 'gre']):
                comprehensive_deck['deck_categories']['test_prep'].append(deck)
            elif 'business' in category:
                comprehensive_deck['deck_categories']['business'].append(deck)
            elif 'academic' in category:
                comprehensive_deck['deck_categories']['academic'].append(deck)
            else:
                comprehensive_deck['deck_categories']['other'].append(deck)
        
        # Save comprehensive deck
        filename = "comprehensive_english_master_ankiweb.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_deck, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Comprehensive English master deck created!")
        print(f"📊 Total decks found: {len(detailed_decks)}")
        print(f"📁 Saved to: {filepath}")
        print(f"🎯 Ready for 80/20 training split!")
        
        return comprehensive_deck
    
    def create_training_test_split(self, comprehensive_deck):
        """Create 80/20 training/testing split"""
        print("✂️ Creating 80/20 training/testing split...")
        
        all_decks = comprehensive_deck['all_decks']
        total_decks = len(all_decks)
        
        # Shuffle decks for random split
        random.shuffle(all_decks)
        
        # Calculate split
        training_count = int(total_decks * 0.8)
        testing_count = total_decks - training_count
        
        training_decks = all_decks[:training_count]
        testing_decks = all_decks[training_count:]
        
        # Create split files
        training_data = {
            "split_info": {
                "type": "training",
                "percentage": 80,
                "deck_count": training_count,
                "created_date": datetime.now().isoformat()
            },
            "decks": training_decks
        }
        
        testing_data = {
            "split_info": {
                "type": "testing", 
                "percentage": 20,
                "deck_count": testing_count,
                "created_date": datetime.now().isoformat()
            },
            "decks": testing_decks
        }
        
        # Save split files
        training_file = os.path.join(self.output_dir, "english_training_80_percent.json")
        testing_file = os.path.join(self.output_dir, "english_testing_20_percent.json")
        
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        with open(testing_file, 'w', encoding='utf-8') as f:
            json.dump(testing_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Training/Testing split created!")
        print(f"📚 Training: {training_count} decks (80%)")
        print(f"🧪 Testing: {testing_count} decks (20%)")
        print(f"📁 Files saved in: {self.output_dir}")
        
        return training_data, testing_data

def main():
    print("🚀 ANKI ENGLISH MASTER DOWNLOADER - PHASE 1")
    print("=" * 50)
    
    downloader = AnkiEnglishMasterDownloader()
    
    # Step 1: Get top English decks
    top_decks = downloader.get_top_english_decks()
    
    if not top_decks:
        print("❌ No decks found. Exiting.")
        return
    
    # Step 2: Create comprehensive deck
    comprehensive_deck = downloader.create_comprehensive_english_deck(top_decks)
    
    # Step 3: Create 80/20 split
    training_data, testing_data = downloader.create_training_test_split(comprehensive_deck)
    
    print("\n🎉 PHASE 1 COMPLETE!")
    print("✅ Comprehensive English deck created from AnkiWeb data")
    print("✅ 80/20 training/testing split ready")
    print("🎯 Next: Humanities decks in next chat!")

if __name__ == "__main__":
    main()
