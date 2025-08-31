import fitz  # PyMuPDF
import re
import json
from typing import List, Dict, Tuple, Optional

class WinterPaperTester:
    """
    Test our QA matcher on the winter Paper 1 MCQ
    """
    
    def __init__(self):
        # For Multiple Choice papers, questions are numbered 1-40
        self.valid_question_numbers = set(str(i) for i in range(1, 41))
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def find_multiple_choice_questions(self, text: str) -> List[Dict[str, str]]:
        """
        Find Multiple Choice questions by looking for the pattern: number + options A, B, C, D
        """
        questions = []
        
        # Split text into lines
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Look for question patterns in Multiple Choice format
            # Pattern: number followed by options A, B, C, D
            question_patterns = [
                r'^(\d+)\s*[A-D]\)',  # 1A), 2B), etc.
                r'^(\d+)\s+[A-D]',    # 1 A, 2 B, etc.
                r'^(\d+)\)\s*[A-D]',  # 1) A, 2) B, etc.
                r'^(\d+)\.\s*[A-D]',  # 1. A, 2. B, etc.
                r'(\d+)\s+[A-D]',     # Anywhere: 1 A, 2 B, etc.
                r'(\d+)\s*[A-D]',     # Anywhere: 1A, 2B, etc.
            ]
            
            for pattern in question_patterns:
                match = re.search(pattern, line)
                if match:
                    question_number = match.group(1)
                    
                    # Only accept valid question numbers (1-40 for this paper)
                    if question_number in self.valid_question_numbers:
                        # Get the question content (everything after the pattern)
                        question_content = line[match.end():].strip()
                        
                        # If question content is short, try to get more from next lines
                        if len(question_content) < 30 and i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if next_line and not re.match(r'^\d+[A-D]?[\)\.]?', next_line):
                                question_content += " " + next_line
                        
                        if question_content:
                            questions.append({
                                "number": question_number,
                                "content": question_content,
                                "line_number": i,
                                "pattern_used": pattern,
                                "full_line": line
                            })
                            break
        
        return questions
    
    def find_multiple_choice_answers_fixed(self, text: str) -> List[Dict[str, str]]:
        """
        Fixed answer detection that properly reconstructs the mark scheme table
        """
        answers = []
        
        # Split text into lines
        lines = text.split('\n')
        
        # First, let's find the "Answer" header to locate the answer section
        answer_section_start = -1
        for i, line in enumerate(lines):
            if "Answer" in line:
                answer_section_start = i
                break
        
        if answer_section_start == -1:
            print("Could not find Answer section")
            return []
        
        print(f"Found Answer section starting at line {answer_section_start}")
        
        # Now look for the pattern: question number followed by answer letter
        # The structure should be: 1, C, 2, B, 3, C, etc.
        current_question = None
        
        for i in range(answer_section_start, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            
            # Look for question numbers (just numbers)
            if re.match(r'^\d+$', line):
                current_question = line
                print(f"Found question number: {current_question} at line {i}")
            
            # Look for answer options (just A, B, C, or D)
            elif re.match(r'^[A-D]$', line) and current_question:
                answer_option = line
                print(f"Found answer {answer_option} for question {current_question} at line {i}")
                
                # Only accept valid question numbers (1-40)
                if current_question in self.valid_question_numbers:
                    answers.append({
                        "number": current_question,
                        "option": answer_option,
                        "question_line": i,
                        "answer_line": i,
                        "pattern_used": "fixed_table_reconstruction",
                        "full_line": f"Q{current_question}: {answer_option}"
                    })
                
                # Reset current question
                current_question = None
        
        return answers
    
    def match_qa_pairs(self, questions: List[Dict], answers: List[Dict]) -> List[Dict]:
        """
        Match questions with their corresponding answers
        """
        qa_pairs = []
        
        for question in questions:
            question_num = question["number"]
            
            # Find matching answer
            matching_answer = next((a for a in answers if a["number"] == question_num), None)
            
            if matching_answer:
                qa_pairs.append({
                    "question_number": question_num,
                    "question_content": question["content"],
                    "answer_option": matching_answer["option"],
                    "question_line": question["line_number"],
                    "answer_line": matching_answer["answer_line"],
                    "confidence": "high"
                })
            else:
                # No matching answer found
                qa_pairs.append({
                    "question_number": question_num,
                    "question_content": question["content"],
                    "answer_option": "No matching answer found",
                    "question_line": question["line_number"],
                    "answer_line": None,
                    "confidence": "low"
                })
        
        return qa_pairs
    
    def test_winter_paper(self, qp_path: str, ms_path: str) -> Dict:
        """
        Test QA matching on the winter Paper 1 MCQ
        """
        print(f"Testing QA matching for WINTER PAPER:")
        print(f"  Question Paper: {qp_path}")
        print(f"  Mark Scheme: {ms_path}")
        print()
        
        # Extract text from both PDFs
        print("1. Extracting text from PDFs...")
        qp_text = self.extract_text_from_pdf(qp_path)
        ms_text = self.extract_text_from_pdf(ms_path)
        
        if not qp_text:
            print("✗ Failed to extract text from question paper")
            return {}
        
        if not ms_text:
            print("✗ Failed to extract text from mark scheme")
            return {}
        
        print(f"  ✓ Question paper text: {len(qp_text)} characters")
        print(f"  ✓ Mark scheme text: {len(ms_text)} characters")
        print()
        
        # Find questions and answers
        print("2. Finding Multiple Choice questions and answers...")
        questions = self.find_multiple_choice_questions(qp_text)
        answers = self.find_multiple_choice_answers_fixed(ms_text)
        
        print(f"  ✓ Found {len(questions)} questions")
        print(f"  ✓ Found {len(answers)} answers")
        print()
        
        # Show some examples
        if questions:
            print("Sample questions found:")
            for q in questions[:5]:
                print(f"  Q{q['number']}: {q['content'][:100]}...")
                print(f"     Line: {q['line_number']}, Pattern: {q['pattern_used']}")
            print()
        
        if answers:
            print("Sample answers found:")
            for a in answers[:10]:
                print(f"  A{a['number']}: {a['option']}")
                print(f"     Line: {a['answer_line']}, Pattern: {a['pattern_used']}")
            print()
        
        # Match questions with answers
        print("3. Matching questions with answers...")
        qa_pairs = self.match_qa_pairs(questions, answers)
        
        print(f"  ✓ Created {len(qa_pairs)} QA pairs")
        print()
        
        # Show matching results
        print("4. QA Matching Results:")
        for pair in qa_pairs[:10]:  # Show first 10
            print(f"  Q{pair['question_number']}: {pair['question_content'][:80]}...")
            if pair['answer_option'] != "No matching answer found":
                print(f"  A{pair['question_number']}: {pair['answer_option']}")
            else:
                print(f"  A{pair['question_number']}: No matching answer found")
            print(f"     Confidence: {pair['confidence']}")
            print()
        
        # Summary statistics
        high_confidence = len([p for p in qa_pairs if p['confidence'] == 'high'])
        low_confidence = len([p for p in qa_pairs if p['confidence'] == 'low'])
        
        print("5. Summary:")
        print(f"  Total QA pairs: {len(qa_pairs)}")
        print(f"  High confidence: {high_confidence}")
        print(f"  Low confidence: {low_confidence}")
        print(f"  Success rate: {(high_confidence / len(qa_pairs) * 100):.1f}%" if qa_pairs else "0%")
        
        return {
            "questions": questions,
            "answers": answers,
            "qa_pairs": qa_pairs,
            "summary": {
                "total_pairs": len(qa_pairs),
                "high_confidence": high_confidence,
                "low_confidence": low_confidence,
                "success_rate": (high_confidence / len(qa_pairs) * 100) if qa_pairs else 0
            }
        }

def main():
    """
    Test QA matching on Physics 9702 Winter Paper 1 Variant 2
    """
    tester = WinterPaperTester()
    
    # Test with Winter Paper 1 (Multiple Choice)
    qp_path = "physics_9702_winter_2022/9702_w22_qp_12.pdf"  # Winter Paper 1, Variant 2
    ms_path = "physics_9702_winter_2022/9702_w22_ms_12.pdf"  # Winter Mark Scheme 1, Variant 2
    
    print("=== Physics 9702 Winter Paper QA Matching Test ===")
    print("Testing Multiple Choice question-answer matching on WINTER papers...")
    print()
    
    result = tester.test_winter_paper(qp_path, ms_path)
    
    # Save results to file
    if result:
        with open("winter_qa_matching_results.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\n✓ Results saved to winter_qa_matching_results.json")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
