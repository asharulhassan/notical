import json
import time
import os

class HumanitiesDeckCreator:
    def __init__(self):
        self.decks = []
        
    def create_history_deck(self):
        """Create comprehensive History deck"""
        print("Creating History deck...")
        
        history_deck = {
            'name': 'World History Master',
            'category': 'History',
            'cards': []
        }
        
        # Ancient History
        ancient_history = [
            ('Egyptian Pyramids', 'What were the Egyptian pyramids primarily used for?', 'Tombs for pharaohs and their families'),
            ('Roman Empire', 'When did the Roman Empire fall?', '476 CE'),
            ('Greek Democracy', 'Which city-state is considered the birthplace of democracy?', 'Athens'),
            ('Mesopotamia', 'What does "Mesopotamia" mean?', 'Land between two rivers (Tigris and Euphrates)'),
            ('Chinese Dynasties', 'Which dynasty built the Great Wall of China?', 'Qin Dynasty'),
            ('Persian Empire', 'Who was the founder of the Persian Empire?', 'Cyrus the Great'),
            ('Phoenicians', 'What were the Phoenicians known for?', 'Sea trade and the alphabet'),
            ('Indus Valley', 'What was the main city of the Indus Valley Civilization?', 'Mohenjo-daro'),
            ('Maya Civilization', 'Where was the Maya civilization located?', 'Central America'),
            ('Aztec Empire', 'What was the capital of the Aztec Empire?', 'Tenochtitlan')
        ]
        
        # Medieval History
        medieval_history = [
            ('Feudalism', 'What was the main economic system in medieval Europe?', 'Feudalism'),
            ('Crusades', 'What were the Crusades?', 'Religious wars between Christians and Muslims'),
            ('Black Death', 'When did the Black Death occur in Europe?', '1347-1351'),
            ('Magna Carta', 'What year was the Magna Carta signed?', '1215'),
            ('Hundred Years War', 'How long did the Hundred Years War last?', '116 years (1337-1453)'),
            ('Byzantine Empire', 'What was the capital of the Byzantine Empire?', 'Constantinople'),
            ('Mongol Empire', 'Who was the founder of the Mongol Empire?', 'Genghis Khan'),
            ('Islamic Golden Age', 'When was the Islamic Golden Age?', '8th-14th centuries'),
            ('Viking Age', 'When was the Viking Age?', '793-1066 CE'),
            ('Renaissance', 'What does "Renaissance" mean?', 'Rebirth')
        ]
        
        # Modern History
        modern_history = [
            ('Industrial Revolution', 'When did the Industrial Revolution begin?', 'Late 18th century'),
            ('French Revolution', 'What year did the French Revolution begin?', '1789'),
            ('American Civil War', 'When was the American Civil War?', '1861-1865'),
            ('World War I', 'When did World War I begin?', '1914'),
            ('World War II', 'When did World War II end?', '1945'),
            ('Cold War', 'When was the Cold War?', '1947-1991'),
            ('Space Race', 'Who was the first person in space?', 'Yuri Gagarin'),
            ('Berlin Wall', 'When did the Berlin Wall fall?', '1989'),
            ('Civil Rights Movement', 'Who was the leader of the Civil Rights Movement?', 'Martin Luther King Jr.'),
            ('Fall of Soviet Union', 'When did the Soviet Union collapse?', '1991')
        ]
        
        # Add all history cards
        for period in [ancient_history, medieval_history, modern_history]:
            for item in period:
                history_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'history',
                    'difficulty': 'medium'
                })
        
        self.decks.append(history_deck)
        print(f"Created History deck with {len(history_deck['cards'])} cards")
    
    def create_geography_deck(self):
        """Create comprehensive Geography deck"""
        print("Creating Geography deck...")
        
        geography_deck = {
            'name': 'World Geography Master',
            'category': 'Geography',
            'cards': []
        }
        
        # Physical Geography
        physical_geo = [
            ('Continents', 'How many continents are there?', '7'),
            ('Oceans', 'What is the largest ocean?', 'Pacific Ocean'),
            ('Mountains', 'What is the highest mountain in the world?', 'Mount Everest'),
            ('Rivers', 'What is the longest river in the world?', 'Nile River'),
            ('Deserts', 'What is the largest desert in the world?', 'Sahara Desert'),
            ('Volcanoes', 'What is the most active volcano?', 'Kilauea'),
            ('Earthquakes', 'What causes earthquakes?', 'Movement of tectonic plates'),
            ('Climate Zones', 'How many main climate zones are there?', '5'),
            ('Biomes', 'What is a biome?', 'Large ecological area with similar climate and vegetation'),
            ('Weather', 'What is the difference between weather and climate?', 'Weather is short-term, climate is long-term')
        ]
        
        # Human Geography
        human_geo = [
            ('Population', 'What is the most populous country?', 'China'),
            ('Cities', 'What is the most populous city?', 'Tokyo'),
            ('Languages', 'What is the most spoken language?', 'Mandarin Chinese'),
            ('Religions', 'What is the largest religion?', 'Christianity'),
            ('Economy', 'What is GDP?', 'Gross Domestic Product'),
            ('Migration', 'What is migration?', 'Movement of people from one place to another'),
            ('Urbanization', 'What is urbanization?', 'Growth of cities and urban areas'),
            ('Globalization', 'What is globalization?', 'Integration of economies and cultures worldwide'),
            ('Trade', 'What is international trade?', 'Exchange of goods and services between countries'),
            ('Development', 'What is a developed country?', 'Country with high standard of living and economy')
        ]
        
        # Add all geography cards
        for category in [physical_geo, human_geo]:
            for item in category:
                geography_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'geography',
                    'difficulty': 'medium'
                })
        
        self.decks.append(geography_deck)
        print(f"Created Geography deck with {len(geography_deck['cards'])} cards")
    
    def create_philosophy_deck(self):
        """Create comprehensive Philosophy deck"""
        print("Creating Philosophy deck...")
        
        philosophy_deck = {
            'name': 'Philosophy Master',
            'category': 'Philosophy',
            'cards': []
        }
        
        # Ancient Philosophy
        ancient_philosophy = [
            ('Socrates', 'Who said "The unexamined life is not worth living"?', 'Socrates'),
            ('Plato', 'Who wrote "The Republic"?', 'Plato'),
            ('Aristotle', 'Who was the student of Plato?', 'Aristotle'),
            ('Epicurus', 'What did Epicurus believe was the goal of life?', 'Pleasure and absence of pain'),
            ('Stoicism', 'What is the main principle of Stoicism?', 'Accept what you cannot change'),
            ('Confucius', 'Who said "Do not do to others what you do not want done to yourself"?', 'Confucius'),
            ('Buddha', 'What are the Four Noble Truths?', 'Suffering, cause of suffering, end of suffering, path to end suffering'),
            ('Taoism', 'What is the Tao?', 'The way or path'),
            ('Vedanta', 'What does "Vedanta" mean?', 'End of the Vedas'),
            ('Cynicism', 'Who was the founder of Cynicism?', 'Diogenes')
        ]
        
        # Modern Philosophy
        modern_philosophy = [
            ('Descartes', 'Who said "I think, therefore I am"?', 'René Descartes'),
            ('Kant', 'What is Kant\'s categorical imperative?', 'Act only according to universal law'),
            ('Nietzsche', 'Who said "God is dead"?', 'Friedrich Nietzsche'),
            ('Existentialism', 'What is existentialism?', 'Philosophy focusing on individual existence and freedom'),
            ('Utilitarianism', 'What is the principle of utilitarianism?', 'Greatest good for greatest number'),
            ('Pragmatism', 'What is pragmatism?', 'Truth is what works in practice'),
            ('Phenomenology', 'What is phenomenology?', 'Study of conscious experience'),
            ('Postmodernism', 'What is postmodernism?', 'Questioning of modern assumptions'),
            ('Feminism', 'What is feminist philosophy?', 'Philosophy from women\'s perspective'),
            ('Environmental Ethics', 'What is environmental ethics?', 'Moral consideration of nature')
        ]
        
        # Add all philosophy cards
        for period in [ancient_philosophy, modern_philosophy]:
            for item in period:
                philosophy_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'philosophy',
                    'difficulty': 'medium'
                })
        
        self.decks.append(philosophy_deck)
        print(f"Created Philosophy deck with {len(philosophy_deck['cards'])} cards")
    
    def create_sociology_deck(self):
        """Create comprehensive Sociology deck"""
        print("Creating Sociology deck...")
        
        sociology_deck = {
            'name': 'Sociology Master',
            'category': 'Sociology',
            'cards': []
        }
        
        # Social Theory
        social_theory = [
            ('Functionalism', 'What is functionalism?', 'Society as a system of interconnected parts'),
            ('Conflict Theory', 'What is conflict theory?', 'Society characterized by inequality and conflict'),
            ('Symbolic Interactionism', 'What is symbolic interactionism?', 'Focus on social interaction and meaning'),
            ('Social Constructionism', 'What is social constructionism?', 'Reality is socially constructed'),
            ('Feminist Theory', 'What is feminist theory?', 'Analysis of gender inequality'),
            ('Postmodern Theory', 'What is postmodern theory?', 'Questioning of modern social structures'),
            ('Critical Theory', 'What is critical theory?', 'Analysis of power and domination'),
            ('Rational Choice Theory', 'What is rational choice theory?', 'Individuals act rationally to maximize benefits'),
            ('Social Exchange Theory', 'What is social exchange theory?', 'Social behavior as exchange of rewards'),
            ('Labeling Theory', 'What is labeling theory?', 'Deviance as result of social labeling')
        ]
        
        # Social Institutions
        social_institutions = [
            ('Family', 'What is a family?', 'Basic social unit for reproduction and socialization'),
            ('Education', 'What is education?', 'Formal process of learning and socialization'),
            ('Religion', 'What is religion?', 'System of beliefs and practices about sacred things'),
            ('Government', 'What is government?', 'System of political authority and control'),
            ('Economy', 'What is economy?', 'System of production and distribution'),
            ('Media', 'What is media?', 'Means of mass communication'),
            ('Healthcare', 'What is healthcare?', 'System of medical services'),
            ('Criminal Justice', 'What is criminal justice?', 'System of law enforcement and punishment'),
            ('Military', 'What is military?', 'Armed forces for national defense'),
            ('Science', 'What is science?', 'Systematic study of natural world')
        ]
        
        # Add all sociology cards
        for category in [social_theory, social_institutions]:
            for item in category:
                sociology_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'sociology',
                    'difficulty': 'medium'
                })
        
        self.decks.append(sociology_deck)
        print(f"Created Sociology deck with {len(sociology_deck['cards'])} cards")
    
    def create_psychology_deck(self):
        """Create comprehensive Psychology deck"""
        print("Creating Psychology deck...")
        
        psychology_deck = {
            'name': 'Psychology Master',
            'category': 'Psychology',
            'cards': []
        }
        
        # Cognitive Psychology
        cognitive_psych = [
            ('Memory', 'What are the three stages of memory?', 'Encoding, storage, retrieval'),
            ('Attention', 'What is selective attention?', 'Focusing on specific stimuli while ignoring others'),
            ('Learning', 'What is classical conditioning?', 'Learning through association of stimuli'),
            ('Perception', 'What is perception?', 'Process of organizing and interpreting sensory information'),
            ('Language', 'What is language acquisition?', 'Process of learning language'),
            ('Thinking', 'What is problem solving?', 'Process of finding solutions to problems'),
            ('Intelligence', 'What is intelligence?', 'Ability to learn and adapt'),
            ('Creativity', 'What is creativity?', 'Ability to produce novel and valuable ideas'),
            ('Decision Making', 'What is decision making?', 'Process of choosing between alternatives'),
            ('Problem Solving', 'What is problem solving?', 'Process of finding solutions to problems')
        ]
        
        # Social Psychology
        social_psych = [
            ('Attitudes', 'What are attitudes?', 'Evaluations of people, objects, and ideas'),
            ('Prejudice', 'What is prejudice?', 'Negative attitude toward group members'),
            ('Conformity', 'What is conformity?', 'Changing behavior to match group norms'),
            ('Obedience', 'What is obedience?', 'Following orders from authority'),
            ('Aggression', 'What is aggression?', 'Behavior intended to harm others'),
            ('Altruism', 'What is altruism?', 'Helping others without expecting reward'),
            ('Attraction', 'What is attraction?', 'Positive feelings toward others'),
            ('Group Dynamics', 'What are group dynamics?', 'Patterns of interaction within groups'),
            ('Leadership', 'What is leadership?', 'Influencing group members toward goals'),
            ('Social Influence', 'What is social influence?', 'Effect of others on thoughts and behavior')
        ]
        
        # Add all psychology cards
        for category in [cognitive_psych, social_psych]:
            for item in category:
                psychology_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'psychology',
                    'difficulty': 'medium'
                })
        
        self.decks.append(psychology_deck)
        print(f"Created Psychology deck with {len(psychology_deck['cards'])} cards")
    
    def consolidate_decks(self):
        """Consolidate all humanities decks"""
        print("Consolidating all Humanities decks...")
        
        all_cards = []
        total_cards = 0
        
        for deck in self.decks:
            all_cards.extend(deck['cards'])
            total_cards += len(deck['cards'])
            print(f"Added {len(deck['cards'])} cards from {deck['name']}")
        
        consolidated_deck = {
            'name': 'Comprehensive Humanities Master Deck',
            'total_cards': total_cards,
            'categories': [deck['category'] for deck in self.decks],
            'cards': all_cards,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return consolidated_deck
    
    def create_training_test_split(self, consolidated_deck):
        """Create 80/20 training/testing split"""
        print("Creating 80/20 training/testing split...")
        
        total_cards = len(consolidated_deck['cards'])
        training_size = int(total_cards * 0.8)
        testing_size = total_cards - training_size
        
        # Shuffle cards
        import random
        random.shuffle(consolidated_deck['cards'])
        
        training_deck = {
            'name': 'Humanities Training Deck (80%)',
            'total_cards': training_size,
            'cards': consolidated_deck['cards'][:training_size],
            'split': 'training'
        }
        
        testing_deck = {
            'name': 'Humanities Testing Deck (20%)',
            'total_cards': testing_size,
            'cards': consolidated_deck['cards'][training_size:],
            'split': 'testing'
        }
        
        return training_deck, testing_deck
    
    def save_decks(self, consolidated_deck, training_deck, testing_deck):
        """Save all decks to JSON files"""
        print("Saving Humanities decks to JSON files...")
        
        # Create output directory
        os.makedirs('generated_flashcards', exist_ok=True)
        
        # Save consolidated deck
        with open('generated_flashcards/comprehensive_humanities_deck.json', 'w', encoding='utf-8') as f:
            json.dump(consolidated_deck, f, indent=2, ensure_ascii=False)
        
        # Save training deck
        with open('generated_flashcards/humanities_training_deck.json', 'w', encoding='utf-8') as f:
            json.dump(training_deck, f, indent=2, ensure_ascii=False)
        
        # Save testing deck
        with open('generated_flashcards/humanities_testing_deck.json', 'w', encoding='utf-8') as f:
            json.dump(testing_deck, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {consolidated_deck['total_cards']} total Humanities cards")
        print(f"✅ Training deck: {training_deck['total_cards']} cards")
        print(f"✅ Testing deck: {testing_deck['total_cards']} cards")
    
    def run(self):
        """Main execution method"""
        print("🚀 Starting Humanities Deck Creation Process...")
        
        # Create all humanities decks
        self.create_history_deck()
        self.create_geography_deck()
        self.create_philosophy_deck()
        self.create_sociology_deck()
        self.create_psychology_deck()
        
        print(f"Created {len(self.decks)} Humanities decks")
        
        # Consolidate all decks
        consolidated_deck = self.consolidate_decks()
        
        # Create training/testing split
        training_deck, testing_deck = self.create_training_test_split(consolidated_deck)
        
        # Save all decks
        self.save_decks(consolidated_deck, training_deck, testing_deck)
        
        print("🎉 Humanities Deck Creation Complete!")
        print(f"📊 Total Cards: {consolidated_deck['total_cards']}")
        print(f"📚 Training Set: {training_deck['total_cards']} cards (80%)")
        print(f"🧪 Testing Set: {testing_deck['total_cards']} cards (20%)")
        
        return consolidated_deck, training_deck, testing_deck

if __name__ == "__main__":
    creator = HumanitiesDeckCreator()
    creator.run()
