import json
import os
from datetime import datetime

class ComprehensiveEnglishDeckCreator:
    def __init__(self):
        self.output_dir = "comprehensive_english_deck"
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_vocabulary_section(self):
        """Create comprehensive vocabulary section"""
        print("📚 Creating Vocabulary section...")
        
        vocabulary = {
            # Basic Vocabulary
            "Ubiquitous": "Present, appearing, or found everywhere; omnipresent.",
            "Ephemeral": "Lasting for a very short time; transitory.",
            "Serendipity": "The occurrence and development of events by chance in a happy or beneficial way.",
            "Mellifluous": "Sweet or musical; pleasant to hear.",
            "Perspicacious": "Having a ready insight into and understanding of things.",
            "Ineffable": "Too great or extreme to be expressed or described in words.",
            "Sycophant": "A person who acts obsequiously toward someone important in order to gain advantage.",
            "Ubiquitous": "Present, appearing, or found everywhere; omnipresent.",
            "Ephemeral": "Lasting for a very short time; transitory.",
            "Serendipity": "The occurrence and development of events by chance in a happy or beneficial way.",
            
            # Advanced Vocabulary
            "Pulchritudinous": "Beautiful, especially in a way that is pleasing to the eye.",
            "Defenestration": "The act of throwing someone out of a window.",
            "Sesquipedalian": "Given to using long words; characterized by long words.",
            "Antidisestablishmentarianism": "Opposition to the withdrawal of state support from an established church.",
            "Hippopotomonstrosesquippedaliophobia": "Fear of long words.",
            "Pneumonoultramicroscopicsilicovolcanoconios": "A lung disease caused by inhaling very fine silicate or quartz dust.",
            "Supercalifragilisticexpialidocious": "Extraordinarily good; wonderful.",
            "Floccinaucinihilipilification": "The action or habit of estimating something as worthless.",
            "Honorificabilitudinitatibus": "The state of being able to achieve honors.",
            "Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphiokarabomelitokatakechymenokichlepikossyphophattoperisteralektryonoptekephalliokigklopeleiolagoiosiraiobaphetraganopterygon": "A fictional dish mentioned in Aristophanes' comedy Assemblywomen."
        }
        
        cards = []
        for word, definition in vocabulary.items():
            card = {
                "front": f"What is the meaning of '{word}'?",
                "back": definition,
                "type": "vocabulary",
                "category": "vocabulary",
                "difficulty": "advanced" if len(word) > 15 else "intermediate",
                "tags": ["vocabulary", "english", "words"]
            }
            cards.append(card)
        
        return cards
    
    def create_grammar_section(self):
        """Create comprehensive grammar section"""
        print("📚 Creating Grammar section...")
        
        grammar_rules = {
            # Parts of Speech
            "Noun": "A word that names a person, place, thing, or idea. Examples: cat, London, happiness, democracy.",
            "Pronoun": "A word that takes the place of a noun. Examples: he, she, it, they, we, you, I.",
            "Verb": "A word that expresses action or state of being. Examples: run, jump, is, was, have, do.",
            "Adjective": "A word that describes or modifies a noun or pronoun. Examples: big, red, beautiful, intelligent.",
            "Adverb": "A word that describes or modifies a verb, adjective, or other adverb. Examples: quickly, very, well, often.",
            "Preposition": "A word that shows the relationship between a noun/pronoun and other words. Examples: in, on, at, by, for, with.",
            "Conjunction": "A word that connects words, phrases, or clauses. Examples: and, but, or, because, although.",
            "Interjection": "A word that expresses emotion or surprise. Examples: wow, oh, ouch, hurray.",
            
            # Sentence Structure
            "Subject": "The person, place, thing, or idea that performs the action or is described in the sentence.",
            "Predicate": "The part of the sentence that contains the verb and tells what the subject does or is.",
            "Direct Object": "The noun or pronoun that receives the action of the verb directly.",
            "Indirect Object": "The noun or pronoun that receives the direct object or for whom the action is done.",
            "Object of Preposition": "The noun or pronoun that follows a preposition.",
            
            # Verb Tenses
            "Present Simple": "Used for habits, general truths, and scheduled events. Example: 'I work every day.'",
            "Present Continuous": "Used for actions happening now or around now. Example: 'I am working right now.'",
            "Present Perfect": "Used for actions that started in the past and continue to the present. Example: 'I have worked here for five years.'",
            "Past Simple": "Used for completed actions in the past. Example: 'I worked yesterday.'",
            "Past Continuous": "Used for actions that were in progress at a specific time in the past. Example: 'I was working when you called.'",
            "Past Perfect": "Used for actions that were completed before another action in the past. Example: 'I had worked before you arrived.'",
            "Future Simple": "Used for predictions and spontaneous decisions. Example: 'I will work tomorrow.'",
            "Future Continuous": "Used for actions that will be in progress at a specific time in the future. Example: 'I will be working at 3 PM.'",
            "Future Perfect": "Used for actions that will be completed before a specific time in the future. Example: 'I will have worked for ten years by next month.'",
            
            # Advanced Grammar
            "Subjunctive Mood": "A verb form used to express wishes, suggestions, or hypothetical situations. Example: 'If I were rich...'",
            "Conditional Sentences": "Sentences that express hypothetical situations using 'if' clauses and different verb forms.",
            "Passive Voice": "A sentence structure where the subject receives the action rather than performing it. Example: 'The book was written by the author.'",
            "Active Voice": "A sentence structure where the subject performs the action. Example: 'The author wrote the book.'",
            "Gerund": "A verb form ending in -ing that functions as a noun. Example: 'Swimming is good exercise.'",
            "Infinitive": "The base form of a verb, usually preceded by 'to'. Example: 'I want to learn.'",
            "Participle": "A verb form that can function as an adjective. Examples: 'The running water' (present participle), 'The broken glass' (past participle).",
            "Modal Verbs": "Auxiliary verbs that express necessity, possibility, permission, or ability. Examples: can, could, may, might, must, shall, should, will, would.",
            "Relative Clauses": "Clauses that provide additional information about a noun, introduced by relative pronouns (who, which, that, whose).",
            "Subordinate Clauses": "Clauses that cannot stand alone as sentences and depend on a main clause for meaning."
        }
        
        cards = []
        for rule, explanation in grammar_rules.items():
            card = {
                "front": f"Explain the grammar rule: {rule}",
                "back": explanation,
                "type": "grammar",
                "category": "grammar",
                "difficulty": "intermediate",
                "tags": ["grammar", "english", "rules"]
            }
            cards.append(card)
        
        return cards
    
    def create_literature_section(self):
        """Create comprehensive literature section"""
        print("📚 Creating Literature section...")
        
        literature_concepts = {
            # Literary Devices
            "Metaphor": "A direct comparison between two unlike things without using 'like' or 'as'. Example: 'Life is a journey.'",
            "Simile": "A comparison between two unlike things using 'like' or 'as'. Example: 'Life is like a box of chocolates.'",
            "Personification": "Giving human qualities to non-human objects or ideas. Example: 'The wind whispered through the trees.'",
            "Alliteration": "Repetition of initial consonant sounds in nearby words. Example: 'Peter Piper picked a peck of pickled peppers.'",
            "Assonance": "Repetition of vowel sounds in nearby words. Example: 'The rain in Spain falls mainly on the plain.'",
            "Consonance": "Repetition of consonant sounds in nearby words. Example: 'The lumpy, bumpy road.'",
            "Onomatopoeia": "Words that imitate sounds. Examples: buzz, hiss, roar, meow, bang.",
            "Hyperbole": "Exaggeration for emphasis or effect. Example: 'I've told you a million times.'",
            "Understatement": "Presenting something as less significant than it actually is. Example: 'It's just a scratch' (for a major injury).",
            "Irony": "A contrast between expectation and reality. Example: A fire station burning down.",
            "Dramatic Irony": "When the audience knows something that the characters in the story do not.",
            "Verbal Irony": "When someone says the opposite of what they mean, often sarcastically.",
            "Situational Irony": "When the outcome is the opposite of what was expected.",
            
            # Literary Elements
            "Plot": "The sequence of events that make up a story. Includes exposition, rising action, climax, falling action, and resolution.",
            "Character": "A person, animal, or being in a story. Can be round (complex) or flat (simple), static (unchanging) or dynamic (changing).",
            "Setting": "The time and place where a story takes place. Includes physical location, historical period, and social environment.",
            "Theme": "The central message or underlying meaning of a literary work. Examples: love, death, good vs. evil, coming of age.",
            "Point of View": "The perspective from which a story is told. First person (I), second person (you), third person (he/she/they).",
            "Tone": "The author's attitude toward the subject or audience. Examples: serious, humorous, sarcastic, formal, informal.",
            "Mood": "The emotional atmosphere created by a literary work. Examples: mysterious, tense, peaceful, gloomy.",
            "Symbolism": "Using objects, characters, or events to represent abstract ideas or qualities. Example: A dove representing peace.",
            "Foreshadowing": "Hints or clues about what will happen later in the story.",
            "Flashback": "A scene that interrupts the present action to show events from the past.",
            "Climax": "The turning point or highest point of tension in a story.",
            "Resolution": "The conclusion of a story where conflicts are resolved.",
            
            # Poetry Terms
            "Rhyme": "The repetition of similar sounds at the end of lines in poetry.",
            "Rhythm": "The pattern of stressed and unstressed syllables in poetry.",
            "Meter": "The regular pattern of stressed and unstressed syllables in a line of poetry.",
            "Stanza": "A group of lines in poetry, similar to a paragraph in prose.",
            "Couplet": "Two consecutive lines of poetry that rhyme.",
            "Quatrain": "A four-line stanza in poetry.",
            "Sonnet": "A 14-line poem with a specific rhyme scheme, often written in iambic pentameter.",
            "Haiku": "A traditional Japanese poem with three lines of 5, 7, and 5 syllables.",
            "Free Verse": "Poetry that doesn't follow a regular meter or rhyme scheme.",
            "Blank Verse": "Unrhymed poetry written in iambic pentameter."
        }
        
        cards = []
        for concept, explanation in literature_concepts.items():
            card = {
                "front": f"Define and explain: {concept}",
                "back": explanation,
                "type": "literature",
                "category": "literature",
                "difficulty": "intermediate",
                "tags": ["literature", "english", "devices"]
            }
            cards.append(card)
        
        return cards
    
    def create_writing_section(self):
        """Create comprehensive writing section"""
        print("📚 Creating Writing section...")
        
        writing_concepts = {
            # Essay Structure
            "Introduction": "The opening paragraph that introduces the topic, provides background information, and presents the thesis statement.",
            "Thesis Statement": "A clear, specific statement that presents the main argument or point of an essay.",
            "Body Paragraphs": "The main sections of an essay that develop and support the thesis statement with evidence and analysis.",
            "Topic Sentence": "The first sentence of each body paragraph that introduces the main idea of that paragraph.",
            "Evidence": "Facts, examples, statistics, or expert opinions that support your claims.",
            "Analysis": "Explanation of how your evidence supports your argument and why it matters.",
            "Transitions": "Words or phrases that connect ideas and help readers follow your logic.",
            "Conclusion": "The final paragraph that restates the thesis, summarizes main points, and provides closing thoughts.",
            
            # Writing Techniques
            "Active Voice": "Writing where the subject performs the action, making sentences more direct and engaging.",
            "Passive Voice": "Writing where the subject receives the action. Can be useful but often makes writing less clear.",
            "Concise Writing": "Eliminating unnecessary words and phrases to make writing clear and powerful.",
            "Parallel Structure": "Using the same grammatical form for similar ideas in a sentence or paragraph.",
            "Varied Sentence Structure": "Mixing different sentence types (simple, compound, complex) to create rhythm and interest.",
            "Strong Verbs": "Using specific, action-oriented verbs instead of weak or vague ones.",
            "Specific Details": "Including concrete, specific information rather than general statements.",
            "Show, Don't Tell": "Using descriptive details and examples instead of simply stating facts.",
            
            # Argumentation
            "Claim": "A statement that presents your position on an issue.",
            "Counterargument": "Addressing opposing viewpoints to strengthen your own argument.",
            "Rebuttal": "Responding to counterarguments and explaining why your position is stronger.",
            "Logical Fallacies": "Errors in reasoning that weaken arguments. Examples: ad hominem, straw man, false dilemma.",
            "Ethos": "Appealing to credibility and character to persuade an audience.",
            "Pathos": "Appealing to emotions to persuade an audience.",
            "Logos": "Appealing to logic and reason to persuade an audience.",
            
            # Research and Citation
            "Primary Source": "Original documents or firsthand accounts of events.",
            "Secondary Source": "Sources that analyze, interpret, or comment on primary sources.",
            "Plagiarism": "Using someone else's words or ideas without proper attribution.",
            "Citation": "Giving credit to sources used in your writing.",
            "Bibliography": "A list of all sources consulted during research.",
            "Works Cited": "A list of sources actually cited in your paper."
        }
        
        cards = []
        for concept, explanation in writing_concepts.items():
            card = {
                "front": f"Explain the writing concept: {concept}",
                "back": explanation,
                "type": "writing",
                "category": "writing",
                "difficulty": "intermediate",
                "tags": ["writing", "english", "techniques"]
            }
            cards.append(card)
        
        return cards
    
    def create_reading_section(self):
        """Create comprehensive reading section"""
        print("📚 Creating Reading section...")
        
        reading_concepts = {
            # Reading Strategies
            "Skimming": "Reading quickly to get the main idea or overview of a text.",
            "Scanning": "Reading quickly to find specific information or details.",
            "Close Reading": "Reading carefully and attentively to understand the text deeply.",
            "Active Reading": "Engaging with the text by asking questions, making connections, and taking notes.",
            "Annotation": "Adding notes, comments, or marks to a text while reading.",
            "Summarizing": "Briefly restating the main ideas and key points of a text in your own words.",
            "Paraphrasing": "Restating information from a text in your own words while maintaining the original meaning.",
            "Inferring": "Drawing conclusions or making educated guesses based on evidence in the text.",
            "Predicting": "Making educated guesses about what will happen next in a text.",
            "Questioning": "Asking questions about the text to deepen understanding.",
            
            # Comprehension Skills
            "Main Idea": "The central point or most important message of a text.",
            "Supporting Details": "Facts, examples, or information that support the main idea.",
            "Context Clues": "Information in surrounding text that helps determine the meaning of unfamiliar words.",
            "Text Structure": "The organization and arrangement of information in a text.",
            "Cause and Effect": "A relationship where one event leads to another.",
            "Compare and Contrast": "Examining similarities and differences between two or more things.",
            "Chronological Order": "Arrangement of events in the order they occurred.",
            "Problem and Solution": "A structure that presents a problem and then offers solutions.",
            "Sequence": "A series of steps or events in a specific order.",
            "Description": "A structure that provides detailed information about a topic.",
            
            # Critical Reading
            "Author's Purpose": "The reason why an author wrote a text (to inform, persuade, entertain, etc.).",
            "Author's Bias": "A preference or prejudice that influences how an author presents information.",
            "Fact vs. Opinion": "Distinguishing between statements that can be proven (facts) and personal beliefs (opinions).",
            "Credibility": "The quality of being believable or trustworthy.",
            "Reliability": "The consistency and dependability of information.",
            "Relevance": "How closely information relates to the topic or question at hand.",
            "Currency": "How up-to-date or recent the information is.",
            "Authority": "The expertise or qualifications of the author or source.",
            "Accuracy": "The correctness and truthfulness of information.",
            "Objectivity": "The absence of bias or personal opinion in information."
        }
        
        cards = []
        for concept, explanation in reading_concepts.items():
            card = {
                "front": f"What is {concept} in reading?",
                "back": explanation,
                "type": "reading",
                "category": "reading",
                "difficulty": "intermediate",
                "tags": ["reading", "english", "comprehension"]
            }
            cards.append(card)
        
        return cards
    
    def create_comprehensive_english_deck(self):
        """Create one massive comprehensive English deck"""
        print("🚀 Creating ONE comprehensive English deck with ALL content...")
        
        # Generate all sections
        vocabulary_cards = self.create_vocabulary_section()
        grammar_cards = self.create_grammar_section()
        literature_cards = self.create_literature_section()
        writing_cards = self.create_writing_section()
        reading_cards = self.create_reading_section()
        
        # Combine all cards
        all_cards = vocabulary_cards + grammar_cards + literature_cards + writing_cards + reading_cards
        
        # Create comprehensive deck
        comprehensive_deck = {
            "deck_info": {
                "name": "Comprehensive English Master Deck",
                "description": "Complete English language deck covering vocabulary, grammar, literature, writing, and reading",
                "total_cards": len(all_cards),
                "created_date": datetime.now().isoformat(),
                "version": "1.0"
            },
            "sections": {
                "vocabulary": {
                    "name": "Vocabulary",
                    "cards": vocabulary_cards,
                    "total_cards": len(vocabulary_cards),
                    "description": "Advanced vocabulary words and definitions"
                },
                "grammar": {
                    "name": "Grammar",
                    "cards": grammar_cards,
                    "total_cards": len(grammar_cards),
                    "description": "Complete English grammar rules and explanations"
                },
                "literature": {
                    "name": "Literature",
                    "cards": literature_cards,
                    "total_cards": len(literature_cards),
                    "description": "Literary devices, elements, and poetry terms"
                },
                "writing": {
                    "name": "Writing",
                    "cards": writing_cards,
                    "total_cards": len(writing_cards),
                    "description": "Writing techniques, essay structure, and argumentation"
                },
                "reading": {
                    "name": "Reading",
                    "cards": reading_cards,
                    "total_cards": len(reading_cards),
                    "description": "Reading strategies and comprehension skills"
                }
            },
            "all_cards": all_cards,
            "statistics": {
                "total_cards": len(all_cards),
                "vocabulary_cards": len(vocabulary_cards),
                "grammar_cards": len(grammar_cards),
                "literature_cards": len(literature_cards),
                "writing_cards": len(writing_cards),
                "reading_cards": len(reading_cards)
            }
        }
        
        # Save comprehensive deck
        filename = "comprehensive_english_master_deck.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_deck, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Comprehensive English deck created!")
        print(f"📊 Total cards: {len(all_cards)}")
        print(f"📁 Saved to: {filepath}")
        print(f"🎯 Ready for Humanities next!")
        
        return comprehensive_deck

def main():
    creator = ComprehensiveEnglishDeckCreator()
    comprehensive_deck = creator.create_comprehensive_english_deck()
    
    print(f"\n🎉 COMPREHENSIVE ENGLISH DECK COMPLETE!")
    print("🚀 We now have ONE massive English deck with everything!")
    print("🎯 Next: Create comprehensive Humanities deck!")

if __name__ == "__main__":
    main()
