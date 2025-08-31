import json
import os
from datetime import datetime

class FlashcardGenerator:
    def __init__(self):
        self.analysis_file = "anki_english_analysis.json"
        self.output_dir = "generated_flashcards"
        self.learned_patterns = {}
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_learned_patterns(self):
        """Load the patterns learned from English deck analysis"""
        print("📚 Loading learned patterns from English deck analysis...")
        
        if os.path.exists(self.analysis_file):
            with open(self.analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
                self.learned_patterns = analysis
                print("  ✅ Loaded analysis results")
        else:
            print("  ⚠️ No analysis file found, using default patterns")
            self.learned_patterns = self.get_default_patterns()
        
        return self.learned_patterns
    
    def get_default_patterns(self):
        """Default patterns if no analysis file exists"""
        return {
            "question_patterns": {
                "starters": ["What is", "Define", "Explain", "Describe", "How does"],
                "types": ["interrogative", "instructional", "statement"]
            },
            "answer_patterns": {
                "types": ["concise", "moderate", "detailed"],
                "structures": ["simple", "with_examples", "step_by_step"]
            }
        }
    
    def generate_vocabulary_cards(self, subject, words_list):
        """Generate vocabulary flashcards using learned patterns"""
        print(f"📝 Generating vocabulary cards for {subject}...")
        
        cards = []
        for word, definition in words_list.items():
            # Apply learned patterns: clear question starters, concise answers
            card = {
                "front": f"What is the meaning of '{word}'?",
                "back": definition,
                "type": "vocabulary",
                "subject": subject,
                "tags": ["vocabulary", subject.lower()],
                "difficulty": "basic"
            }
            cards.append(card)
        
        return cards
    
    def generate_grammar_cards(self, subject, grammar_rules):
        """Generate grammar flashcards using learned patterns"""
        print(f"📝 Generating grammar cards for {subject}...")
        
        cards = []
        for rule, explanation in grammar_rules.items():
            # Apply learned patterns: instructional questions, detailed answers
            card = {
                "front": f"Explain the grammar rule: {rule}",
                "back": explanation,
                "type": "grammar",
                "subject": subject,
                "tags": ["grammar", subject.lower()],
                "difficulty": "intermediate"
            }
            cards.append(card)
        
        return cards
    
    def generate_concept_cards(self, subject, concepts):
        """Generate concept explanation flashcards"""
        print(f"📝 Generating concept cards for {subject}...")
        
        cards = []
        for concept, details in concepts.items():
            # Apply learned patterns: clear questions, structured answers
            card = {
                "front": f"Define and explain: {concept}",
                "back": details,
                "type": "concept",
                "subject": subject,
                "tags": ["concept", subject.lower()],
                "difficulty": "advanced"
            }
            cards.append(card)
        
        return cards
    
    def generate_question_cards(self, subject, qa_pairs):
        """Generate Q&A flashcards from existing content"""
        print(f"📝 Generating Q&A cards for {subject}...")
        
        cards = []
        for question, answer in qa_pairs.items():
            # Apply learned patterns: proper question formatting
            card = {
                "front": question,
                "back": answer,
                "type": "qa",
                "subject": subject,
                "tags": ["qa", subject.lower()],
                "difficulty": "mixed"
            }
            cards.append(card)
        
        return cards
    
    def create_english_literature_deck(self):
        """Create a comprehensive English Literature deck"""
        print("📚 Creating English Literature deck...")
        
        literature_concepts = {
            "Metaphor": "A direct comparison between two unlike things without using 'like' or 'as'. Example: 'Life is a journey.'",
            "Simile": "A comparison between two unlike things using 'like' or 'as'. Example: 'Life is like a box of chocolates.'",
            "Personification": "Giving human qualities to non-human objects or ideas. Example: 'The wind whispered through the trees.'",
            "Alliteration": "Repetition of initial consonant sounds in nearby words. Example: 'Peter Piper picked a peck of pickled peppers.'",
            "Irony": "A contrast between expectation and reality. Example: A fire station burning down.",
            "Foreshadowing": "Hints or clues about what will happen later in the story.",
            "Symbolism": "Using objects, characters, or events to represent abstract ideas or qualities.",
            "Theme": "The central message or underlying meaning of a literary work.",
            "Characterization": "The way an author reveals and develops a character's personality.",
            "Plot": "The sequence of events that make up a story."
        }
        
        return self.generate_concept_cards("English Literature", literature_concepts)
    
    def create_english_grammar_deck(self):
        """Create a comprehensive English Grammar deck"""
        print("📚 Creating English Grammar deck...")
        
        grammar_rules = {
            "Parts of Speech": "The eight parts of speech are: noun, pronoun, verb, adjective, adverb, preposition, conjunction, and interjection.",
            "Subject-Verb Agreement": "The verb must agree with the subject in number (singular/plural). Example: 'He runs' vs 'They run.'",
            "Tenses": "Verbs change form to show when an action occurs: past, present, future, and their perfect and continuous forms.",
            "Active vs Passive Voice": "Active voice: subject performs action. Passive voice: subject receives action. Example: 'I wrote the letter' vs 'The letter was written by me.'",
            "Conditional Sentences": "Sentences that express hypothetical situations using 'if' clauses and different verb forms.",
            "Modal Verbs": "Auxiliary verbs that express necessity, possibility, permission, or ability (can, could, may, might, must, shall, should, will, would).",
            "Gerunds": "Verbs ending in -ing that function as nouns. Example: 'Swimming is good exercise.'",
            "Infinitives": "The base form of a verb, usually preceded by 'to'. Example: 'I want to learn.'",
            "Relative Clauses": "Clauses that provide additional information about a noun, introduced by relative pronouns (who, which, that, whose).",
            "Subjunctive Mood": "A verb form used to express wishes, suggestions, or hypothetical situations."
        }
        
        return self.generate_grammar_cards("English Grammar", grammar_rules)
    
    def create_writing_skills_deck(self):
        """Create a Writing Skills deck"""
        print("📚 Creating Writing Skills deck...")
        
        writing_concepts = {
            "Essay Structure": "Introduction (hook, background, thesis), Body paragraphs (topic sentence, evidence, analysis), Conclusion (restate thesis, summarize, closing thought).",
            "Thesis Statement": "A clear, specific statement that presents the main argument or point of an essay.",
            "Topic Sentences": "The first sentence of each body paragraph that introduces the main idea of that paragraph.",
            "Evidence": "Facts, examples, statistics, or expert opinions that support your claims.",
            "Analysis": "Explanation of how your evidence supports your argument and why it matters.",
            "Transitions": "Words or phrases that connect ideas and help readers follow your logic.",
            "Counterarguments": "Addressing opposing viewpoints to strengthen your own argument.",
            "Conclusion Strategies": "Restate thesis, summarize main points, provide broader implications, or end with a memorable quote or question.",
            "Active Voice": "Writing where the subject performs the action, making sentences more direct and engaging.",
            "Concise Writing": "Eliminating unnecessary words and phrases to make writing clear and powerful."
        }
        
        return self.generate_concept_cards("Writing Skills", writing_concepts)
    
    def create_history_deck(self):
        """Create a History deck using learned patterns"""
        print("📚 Creating History deck...")
        
        history_concepts = {
            "Industrial Revolution": "A period from 1760-1840 when manufacturing shifted from hand production to machines, leading to urbanization and social change.",
            "French Revolution": "A period of radical social and political upheaval in France from 1789-1799 that overthrew the monarchy and established a republic.",
            "World War I": "A global conflict from 1914-1918 involving most European nations, the United States, and others, resulting in millions of casualties.",
            "Cold War": "A period of geopolitical tension between the United States and Soviet Union from 1947-1991, characterized by proxy wars and nuclear arms race.",
            "Civil Rights Movement": "A social movement in the United States from 1954-1968 that aimed to end racial segregation and discrimination against African Americans.",
            "Renaissance": "A period of European cultural, artistic, political, and scientific rebirth from the 14th to 17th centuries.",
            "Age of Exploration": "A period from the 15th to 17th centuries when European nations explored and colonized other parts of the world.",
            "Enlightenment": "An intellectual and philosophical movement in 18th-century Europe that emphasized reason, individualism, and skepticism.",
            "American Revolution": "A colonial revolt from 1765-1783 that resulted in the United States gaining independence from Great Britain.",
            "World War II": "A global conflict from 1939-1945 involving most nations, including all great powers, forming two opposing alliances."
        }
        
        return self.generate_concept_cards("History", history_concepts)
    
    def create_geography_deck(self):
        """Create a Geography deck using learned patterns"""
        print("📚 Creating Geography deck...")
        
        geography_concepts = {
            "Plate Tectonics": "The theory that Earth's outer shell is divided into plates that move over the mantle, causing earthquakes, volcanoes, and mountain formation.",
            "Climate Zones": "Large areas of Earth with similar weather patterns, including tropical, temperate, and polar zones.",
            "Ecosystems": "Communities of living organisms interacting with their physical environment, such as forests, deserts, and oceans.",
            "Population Density": "The number of people living in a given area, usually measured as people per square kilometer.",
            "Urbanization": "The process of population concentration in cities and towns, leading to urban growth and development.",
            "Natural Resources": "Materials from nature that humans use, including renewable (solar, wind) and non-renewable (fossil fuels, minerals) resources.",
            "Weather vs Climate": "Weather is short-term atmospheric conditions, while climate is long-term weather patterns in a region.",
            "Erosion": "The process of wearing away Earth's surface by water, wind, or ice, creating landforms like valleys and canyons.",
            "Migration": "The movement of people from one place to another, either within a country (internal) or between countries (international).",
            "Sustainable Development": "Development that meets present needs without compromising the ability of future generations to meet their own needs."
        }
        
        return self.generate_concept_cards("Geography", geography_concepts)
    
    def generate_all_decks(self):
        """Generate all flashcard decks using learned patterns"""
        print("🚀 Starting comprehensive flashcard generation...")
        
        # Load learned patterns
        self.load_learned_patterns()
        
        # Generate English decks
        english_literature = self.create_english_literature_deck()
        english_grammar = self.create_english_grammar_deck()
        writing_skills = self.create_writing_skills_deck()
        
        # Generate Humanities decks
        history = self.create_history_deck()
        geography = self.create_geography_deck()
        
        # Combine all decks
        all_decks = {
            "English Literature": {
                "cards": english_literature,
                "total_cards": len(english_literature),
                "subject": "English Literature",
                "type": "concept"
            },
            "English Grammar": {
                "cards": english_grammar,
                "total_cards": len(english_grammar),
                "subject": "English Grammar", 
                "type": "grammar"
            },
            "Writing Skills": {
                "cards": writing_skills,
                "total_cards": len(writing_skills),
                "subject": "Writing Skills",
                "type": "concept"
            },
            "History": {
                "cards": history,
                "total_cards": len(history),
                "subject": "History",
                "type": "concept"
            },
            "Geography": {
                "cards": geography,
                "total_cards": len(geography),
                "subject": "Geography",
                "type": "concept"
            }
        }
        
        # Save individual deck files
        for deck_name, deck_data in all_decks.items():
            filename = f"{deck_name.lower().replace(' ', '_')}_deck.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(deck_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ Saved {deck_name} deck: {deck_data['total_cards']} cards")
        
        # Save combined master file
        master_file = os.path.join(self.output_dir, "all_flashcards_master.json")
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(all_decks, f, indent=2, ensure_ascii=False)
        
        # Calculate totals
        total_cards = sum(deck['total_cards'] for deck in all_decks.values())
        
        print(f"\n✅ Flashcard generation complete!")
        print(f"📊 Total cards generated: {total_cards}")
        print(f"📁 Files saved in: {self.output_dir}")
        print(f"🎯 Ready for Phase 4: Testing with complex subjects!")
        
        return all_decks

def main():
    generator = FlashcardGenerator()
    all_decks = generator.generate_all_decks()
    
    print(f"\n🎉 PHASE 3 COMPLETE!")
    print("🚀 We've successfully learned from English decks and created comprehensive flashcards!")
    print("🎯 Next: Apply these patterns to complex subjects like Physics!")

if __name__ == "__main__":
    main()
