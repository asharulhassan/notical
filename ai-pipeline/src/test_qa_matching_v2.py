import fitz  # PyMuPDF
import re
import json
from typing import List, Dict, Tuple, Optional

class ImprovedQAMatcher:
    """
    Improved QA matcher specifically for Multiple Choice papers
    """
    
    def __init__(self):
        # For Multiple Choice papers, questions are usually numbered 1-40
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
    
    def find_multiple_choice_answers(self, text: str) -> List[Dict[str, str]]:
        """
        Find Multiple Choice answers in mark scheme
        """
        answers = []
        
        # Split text into lines
        lines = text.split('\n')
        
        # The text extraction breaks up the table structure
        # We need to reconstruct it by looking for the pattern:
        # - Lines with just numbers (question numbers)
        # - Lines with just letters (answers)
        # - Lines with "Answer" header
        
        question_numbers = []
        answer_options = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Look for question numbers (just numbers)
            if re.match(r'^\d+$', line):
                question_numbers.append((i, line))
            
            # Look for answer options (just A, B, C, or D)
            if re.match(r'^[A-D]$', line):
                answer_options.append((i, line))
        
        # Match question numbers with answers
        # They should be in the same order
        for i, (q_line, q_num) in enumerate(question_numbers):
            if i < len(answer_options):
                a_line, a_option = answer_options[i]
                
                # Only accept valid question numbers (1-40)
                if q_num in self.valid_question_numbers:
                    answers.append({
                        "number": q_num,
                        "option": a_option,
                        "question_line": q_line,
                        "answer_line": a_line,
                        "pattern_used": "reconstructed_table",
                        "full_line": f"Q{q_num}: {a_option}"
                    })
        
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
    
    def test_single_paper(self, qp_path: str, ms_path: str) -> Dict:
        """
        Test QA matching on a single Multiple Choice paper
        """
        print(f"Testing QA matching for:")
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
        answers = self.find_multiple_choice_answers(ms_text)
        
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
            for a in answers[:5]:
                print(f"  A{a['number']}: {a['option']}")
                print(f"     Q Line: {a['question_line']}, A Line: {a['answer_line']}, Pattern: {a['pattern_used']}")
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
    Test improved QA matching on Physics 9702 Paper 1 Variant 2
    """
    matcher = ImprovedQAMatcher()
    
    # Test with Paper 1 (Multiple Choice)
    qp_path = "physics_9702_variant_2/9702_s22_qp_12.pdf"  # Paper 1, Variant 2
    ms_path = "physics_9702_variant_2/9702_s22_ms_12.pdf"  # Mark Scheme 1, Variant 2
    
    print("=== Physics 9702 Improved QA Matching Test ===")
    print("Testing Multiple Choice question-answer matching...")
    print()
    
    result = matcher.test_single_paper(qp_path, ms_path)
    
    # Save results to file
    if result:
        with open("improved_qa_matching_results.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\n✓ Results saved to improved_qa_matching_results.json")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
