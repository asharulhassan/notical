import json
import os
import re
from collections import defaultdict

class AnkiPatternAnalyzer:
    def __init__(self):
        self.decks_dir = "anki_english_decks"
        self.analysis_results = {}
        
    def load_all_decks(self):
        """Load all downloaded English decks"""
        print("📂 Loading all English decks for analysis...")
        
        decks = []
        if os.path.exists(self.decks_dir):
            for filename in os.listdir(self.decks_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.decks_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            deck = json.load(f)
                            decks.append(deck)
                            print(f"  ✅ Loaded: {deck['name']} ({deck['metadata']['total_cards']} cards)")
                    except Exception as e:
                        print(f"  ❌ Error loading {filename}: {e}")
        
        print(f"📚 Total decks loaded: {len(decks)}")
        return decks
    
    def analyze_question_patterns(self, cards):
        """Analyze patterns in how questions are structured"""
        print("\n🔍 Analyzing question patterns...")
        
        patterns = {
            "question_starters": defaultdict(int),
            "question_lengths": [],
            "question_types": defaultdict(int),
            "common_phrases": defaultdict(int)
        }
        
        for card in cards:
            front = card.get('front', '')
            
            # Analyze question starters
            if front.strip():
                # Find common question starters
                starters = [
                    "What is", "What does", "Define", "Explain", "Describe",
                    "How does", "When does", "Where is", "Why is", "Which",
                    "Compare", "Analyze", "Identify", "List", "Name"
                ]
                
                for starter in starters:
                    if front.startswith(starter):
                        patterns["question_starters"][starter] += 1
                        break
                
                # Question length analysis
                patterns["question_lengths"].append(len(front.split()))
                
                # Question type analysis
                if '?' in front:
                    patterns["question_types"]["interrogative"] += 1
                elif any(word in front.lower() for word in ['define', 'explain', 'describe']):
                    patterns["question_types"]["instructional"] += 1
                else:
                    patterns["question_types"]["statement"] += 1
                
                # Common phrases
                words = front.lower().split()
                for i in range(len(words) - 1):
                    phrase = f"{words[i]} {words[i+1]}"
                    patterns["common_phrases"][phrase] += 1
        
        return patterns
    
    def analyze_answer_patterns(self, cards):
        """Analyze patterns in how answers are structured"""
        print("🔍 Analyzing answer patterns...")
        
        patterns = {
            "answer_lengths": [],
            "answer_types": defaultdict(int),
            "common_structures": defaultdict(int),
            "examples_usage": 0
        }
        
        for card in cards:
            back = card.get('back', '')
            
            if back.strip():
                # Answer length analysis
                patterns["answer_lengths"].append(len(back.split()))
                
                # Answer type analysis
                if 'e.g.' in back or 'example' in back.lower():
                    patterns["examples_usage"] += 1
                
                if len(back.split()) < 10:
                    patterns["answer_types"]["concise"] += 1
                elif len(back.split()) < 25:
                    patterns["answer_types"]["moderate"] += 1
                else:
                    patterns["answer_types"]["detailed"] += 1
                
                # Common structures
                if ';' in back:
                    patterns["common_structures"]["semicolon_separated"] += 1
                if ':' in back:
                    patterns["common_structures"]["colon_explanation"] += 1
                if '(' in back and ')' in back:
                    patterns["common_structures"]["parenthetical_info"] += 1
        
        return patterns
    
    def analyze_card_structure(self, cards):
        """Analyze overall card structure and metadata"""
        print("🔍 Analyzing card structure...")
        
        structure = {
            "total_cards": len(cards),
            "card_types": defaultdict(int),
            "tags_usage": defaultdict(int),
            "front_back_ratio": 0
        }
        
        total_front_length = 0
        total_back_length = 0
        
        for card in cards:
            # Card types
            card_type = card.get('type', 'unknown')
            structure["card_types"][card_type] += 1
            
            # Tags
            tags = card.get('tags', [])
            for tag in tags:
                structure["tags_usage"][tag] += 1
            
            # Length analysis
            front = card.get('front', '')
            back = card.get('back', '')
            total_front_length += len(front.split())
            total_back_length += len(back.split())
        
        if total_front_length > 0:
            structure["front_back_ratio"] = total_back_length / total_front_length
        
        return structure
    
    def generate_learning_insights(self, all_patterns):
        """Generate insights for learning Q&A patterns"""
        print("\n💡 Generating learning insights...")
        
        insights = {
            "question_patterns": {},
            "answer_patterns": {},
            "best_practices": [],
            "recommendations": []
        }
        
        # Question pattern insights
        if all_patterns:
            q_patterns = all_patterns[0] if all_patterns else {}
            if q_patterns.get('question_starters'):
                top_starters = sorted(q_patterns['question_starters'].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]
                insights["question_patterns"]["top_starters"] = top_starters
            
            if q_patterns.get('question_types'):
                insights["question_patterns"]["type_distribution"] = dict(q_patterns['question_types'])
        
        # Answer pattern insights
        if all_patterns:
            a_patterns = all_patterns[1] if len(all_patterns) > 1 else {}
            if a_patterns.get('answer_types'):
                insights["answer_patterns"]["type_distribution"] = dict(a_patterns['answer_types'])
        
        # Best practices
        insights["best_practices"] = [
            "Use clear question starters like 'What is', 'Define', 'Explain'",
            "Keep questions concise (5-15 words)",
            "Provide detailed but structured answers",
            "Include examples when helpful",
            "Use consistent formatting and tags"
        ]
        
        # Recommendations
        insights["recommendations"] = [
            "Start with vocabulary cards (simple Q&A structure)",
            "Progress to grammar cards (more complex explanations)",
            "Move to literature cards (analysis and interpretation)",
            "Practice with writing skills (process and technique)",
            "Apply patterns to other subjects"
        ]
        
        return insights
    
    def analyze_all_decks(self):
        """Analyze all loaded decks"""
        print("🚀 Starting comprehensive deck analysis...")
        
        decks = self.load_all_decks()
        if not decks:
            print("❌ No decks found to analyze!")
            return
        
        all_patterns = []
        
        for deck in decks:
            print(f"\n📊 Analyzing deck: {deck['name']}")
            print("-" * 50)
            
            cards = deck.get('cards', [])
            if not cards:
                print("  ⚠️ No cards found in deck")
                continue
            
            # Analyze patterns
            q_patterns = self.analyze_question_patterns(cards)
            a_patterns = self.analyze_answer_patterns(cards)
            structure = self.analyze_card_structure(cards)
            
            deck_analysis = {
                "deck_name": deck['name'],
                "question_patterns": q_patterns,
                "answer_patterns": a_patterns,
                "structure": structure
            }
            
            all_patterns.append(deck_analysis)
            
            # Print summary
            print(f"  📝 Cards analyzed: {structure['total_cards']}")
            print(f"  ❓ Question types: {dict(q_patterns['question_types'])}")
            print(f"  💬 Answer types: {dict(a_patterns['answer_types'])}")
            print(f"  🏷️ Card types: {dict(structure['card_types'])}")
        
        # Generate overall insights
        insights = self.generate_learning_insights(all_patterns)
        
        # Save analysis results
        self.analysis_results = {
            "deck_analyses": all_patterns,
            "overall_insights": insights
        }
        
        # Save to file
        output_file = "anki_english_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Analysis complete! Results saved to: {output_file}")
        return self.analysis_results
    
    def print_summary(self):
        """Print a summary of the analysis"""
        if not self.analysis_results:
            print("❌ No analysis results to display!")
            return
        
        print("\n" + "="*60)
        print("📊 ANKI ENGLISH DECK ANALYSIS SUMMARY")
        print("="*60)
        
        insights = self.analysis_results.get('overall_insights', {})
        
        print("\n🎯 TOP QUESTION STARTERS:")
        top_starters = insights.get('question_patterns', {}).get('top_starters', [])
        for starter, count in top_starters:
            print(f"  • {starter}: {count} times")
        
        print("\n💡 BEST PRACTICES:")
        for practice in insights.get('best_practices', []):
            print(f"  • {practice}")
        
        print("\n🚀 RECOMMENDATIONS:")
        for rec in insights.get('recommendations', []):
            print(f"  • {rec}")
        
        print("\n" + "="*60)

def main():
    analyzer = AnkiPatternAnalyzer()
    results = analyzer.analyze_all_decks()
    analyzer.print_summary()
    
    print("\n🎯 Ready for Phase 3: Creating flashcards from learned patterns!")

if __name__ == "__main__":
    main()
