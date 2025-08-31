import PyPDF2
import fitz  # PyMuPDF
import re
import json
from typing import List, Dict, Tuple, Optional

class QAMatcher:
    """
    Test class to match questions and answers from Physics 9702 papers
    """
    
    def __init__(self):
        self.question_patterns = [
            r'(\d+)\s*[a-z]\)',  # 1a), 2b), etc.
            r'(\d+)\s*[A-Z]\)',  # 1A), 2B), etc.
            r'Question\s*(\d+)',  # Question 1, Question 2, etc.
            r'(\d+)\)',           # 1), 2), etc.
            r'(\d+)\.',           # 1., 2., etc.
            r'(\d+)\s+[A-Z]',    # 1 A, 2 B, etc.
            r'(\d+)\s+[a-z]',    # 1 a, 2 b, etc.
        ]
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF (more reliable than PyPDF2)
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
    
    def find_questions(self, text: str) -> List[Dict[str, str]]:
        """
        Find questions in the text and extract their content
        """
        questions = []
        
        # Split text into lines for better processing
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Try different question patterns
            for pattern in self.question_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    question_number = match.group(1)
                    
                    # Get the question content (next few lines)
                    question_content = line[match.end():].strip()
                    
                    # If question content is short, try to get more from next lines
                    if len(question_content) < 20 and i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not re.match(r'^\d+[a-zA-Z]?\)', next_line):
                            question_content += " " + next_line
                    
                    if question_content:
                        questions.append({
                            "number": question_number,
                            "content": question_content,
                            "line_number": i,
                            "pattern_used": pattern
                        })
                        break  # Only use first pattern that matches
        
        return questions
    
    def find_answers(self, text: str) -> List[Dict[str, str]]:
        """
        Find answers in the mark scheme text
        """
        answers = []
        
        # Split text into lines
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Look for answer patterns
            answer_patterns = [
                r'(\d+)\s*[a-z]\)\s*(.+)',  # 1a) answer content
                r'(\d+)\s*[A-Z]\)\s*(.+)',  # 1A) answer content
                r'(\d+)\)\s*(.+)',           # 1) answer content
                r'(\d+)\.\s*(.+)',           # 1. answer content
                r'Answer\s*(\d+)[:\s]+(.+)', # Answer 1: content
            ]
            
            for pattern in answer_patterns:
                match = re.search(pattern, line)
                if match:
                    answer_number = match.group(1)
                    answer_content = match.group(2).strip()
                    
                    if answer_content:
                        answers.append({
                            "number": answer_number,
                            "content": answer_content,
                            "line_number": i,
                            "pattern_used": pattern
                        })
                        break
        
        return answers
    
    def match_qa_pairs(self, questions: List[Dict], answers: List[Dict]) -> List[Dict]:
        """
        Match questions with their corresponding answers
        """
        qa_pairs = []
        
        for question in questions:
            question_num = question["number"]
            
            # Find matching answer(s)
            matching_answers = [a for a in answers if a["number"] == question_num]
            
            if matching_answers:
                for answer in matching_answers:
                    qa_pairs.append({
                        "question_number": question_num,
                        "question_content": question["content"],
                        "answer_content": answer["content"],
                        "question_line": question["line_number"],
                        "answer_line": answer["line_number"],
                        "confidence": "high" if len(matching_answers) == 1 else "medium"
                    })
            else:
                # No matching answer found
                qa_pairs.append({
                    "question_number": question_num,
                    "question_content": question["content"],
                    "answer_content": "No matching answer found",
                    "question_line": question["line_number"],
                    "answer_line": None,
                    "confidence": "low"
                })
        
        return qa_pairs
    
    def test_single_paper(self, qp_path: str, ms_path: str) -> Dict:
        """
        Test QA matching on a single question paper and mark scheme
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
        
        # Show first 500 characters of question paper for debugging
        print(f"  Sample question paper text:")
        print(f"    {qp_text[:500]}...")
        print()
        
        # Show first 500 characters of mark scheme for debugging
        print(f"  Sample mark scheme text:")
        print(f"    {ms_text[:500]}...")
        print()
        
        # Find questions and answers
        print("2. Finding questions and answers...")
        questions = self.find_questions(qp_text)
        answers = self.find_answers(ms_text)
        
        print(f"  ✓ Found {len(questions)} questions")
        print(f"  ✓ Found {len(answers)} answers")
        print()
        
        # Show some examples
        if questions:
            print("Sample questions found:")
            for q in questions[:3]:
                print(f"  Q{q['number']}: {q['content'][:100]}...")
            print()
        
        if answers:
            print("Sample answers found:")
            for a in answers[:3]:
                print(f"  A{a['number']}: {a['content'][:100]}...")
            print()
        
        # Match questions with answers
        print("3. Matching questions with answers...")
        qa_pairs = self.match_qa_pairs(questions, answers)
        
        print(f"  ✓ Created {len(qa_pairs)} QA pairs")
        print()
        
        # Show matching results
        print("4. QA Matching Results:")
        for pair in qa_pairs[:5]:  # Show first 5
            print(f"  Q{pair['question_number']}: {pair['question_content'][:80]}...")
            if pair['answer_content'] != "No matching answer found":
                print(f"  A{pair['question_number']}: {pair['answer_content'][:80]}...")
            else:
                print(f"  A{pair['question_number']}: No matching answer found")
            print(f"     Confidence: {pair['confidence']}")
            print()
        
        # Summary statistics
        high_confidence = len([p for p in qa_pairs if p['confidence'] == 'high'])
        medium_confidence = len([p for p in qa_pairs if p['confidence'] == 'medium'])
        low_confidence = len([p for p in qa_pairs if p['confidence'] == 'low'])
        
        print("5. Summary:")
        print(f"  Total QA pairs: {len(qa_pairs)}")
        print(f"  High confidence: {high_confidence}")
        print(f"  Medium confidence: {medium_confidence}")
        print(f"  Low confidence: {low_confidence}")
        print(f"  Success rate: {((high_confidence + medium_confidence) / len(qa_pairs) * 100):.1f}%" if qa_pairs else "0%")
        
        return {
            "questions": questions,
            "answers": answers,
            "qa_pairs": qa_pairs,
            "summary": {
                "total_pairs": len(qa_pairs),
                "high_confidence": high_confidence,
                "medium_confidence": medium_confidence,
                "low_confidence": low_confidence,
                "success_rate": ((high_confidence + medium_confidence) / len(qa_pairs) * 100) if qa_pairs else 0
            }
        }

def main():
    """
    Test QA matching on Physics 9702 Paper 1 Variant 2
    """
    matcher = QAMatcher()
    
    # Test with Paper 1 (usually has the most straightforward Q&A format)
    qp_path = "physics_9702_variant_2/9702_s22_qp_12.pdf"  # Paper 1, Variant 2
    ms_path = "physics_9702_variant_2/9702_s22_ms_12.pdf"  # Mark Scheme 1, Variant 2
    
    print("=== Physics 9702 QA Matching Test ===")
    print("Testing question-answer matching on a single paper...")
    print()
    
    result = matcher.test_single_paper(qp_path, ms_path)
    
    # Save results to file
    if result:
        with open("qa_matching_test_results.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\n✓ Results saved to qa_matching_test_results.json")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
