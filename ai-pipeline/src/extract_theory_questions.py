import fitz  # PyMuPDF
import re
import json
import os

class TheoryQuestionExtractor:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using PyMuPDF"""
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
    
    def find_theory_questions(self, text):
        """Find theory questions in the paper"""
        questions = []
        
        # Split text into lines for better processing
        lines = text.split('\n')
        
        # Look for question patterns
        # Theory papers typically have questions like: "1 (a)", "2 (b)", "3 (c)", etc.
        question_patterns = [
            r'^(\d+)\s*\(([a-z])\)',  # 1 (a), 2 (b), etc.
            r'^(\d+)\s*[a-z]',       # 1 a, 2 b, etc.
            r'^(\d+)\s*[A-Z]',       # 1 A, 2 B, etc.
            r'^(\d+)\s*[ivx]+',      # 1 i, 1 ii, 1 iii, etc.
            r'^(\d+)\s*[IVX]+',      # 1 I, 1 II, 1 III, etc.
        ]
        
        current_question = None
        current_part = None
        question_text = ""
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check if this line starts a new question or part
            for pattern in question_patterns:
                match = re.match(pattern, line)
                if match:
                    question_num = match.group(1)
                    part_letter = match.group(2) if len(match.groups()) > 1 else ""
                    
                    # Save previous question if exists
                    if current_question and question_text.strip():
                        questions.append({
                            'question_number': current_question,
                            'part': current_part,
                            'question_text': question_text.strip(),
                            'line_number': i
                        })
                    
                    # Start new question
                    current_question = question_num
                    current_part = part_letter
                    question_text = line
                    break
            else:
                # Continue building current question text
                if current_question:
                    question_text += " " + line
        
        # Add the last question
        if current_question and question_text.strip():
            questions.append({
                'question_number': current_question,
                'part': current_part,
                'question_text': question_text.strip(),
                'line_number': len(lines)
            })
        
        return questions
    
    def find_mark_scheme_answers(self, text):
        """Find answers from the mark scheme"""
        answers = []
        lines = text.split('\n')
        
        # Look for answer patterns in mark schemes
        # Mark schemes typically have: "1 (a) answer", "2 (b) answer", etc.
        answer_patterns = [
            r'^(\d+)\s*\(([a-z])\)',  # 1 (a), 2 (b), etc.
            r'^(\d+)\s*[a-z]',       # 1 a, 2 b, etc.
            r'^(\d+)\s*[A-Z]',       # 1 A, 2 B, etc.
            r'^(\d+)\s*[ivx]+',      # 1 i, 1 ii, 1 iii, etc.
            r'^(\d+)\s*[IVX]+',      # 1 I, 1 II, 1 III, etc.
        ]
        
        current_answer = None
        current_part = None
        answer_text = ""
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check if this line starts a new answer
            for pattern in answer_patterns:
                match = re.match(pattern, line)
                if match:
                    question_num = match.group(1)
                    part_letter = match.group(2) if len(match.groups()) > 1 else ""
                    
                    # Save previous answer if exists
                    if current_answer and answer_text.strip():
                        answers.append({
                            'question_number': current_answer,
                            'part': current_part,
                            'answer_text': answer_text.strip(),
                            'line_number': i
                        })
                    
                    # Start new answer
                    current_answer = question_num
                    current_part = part_letter
                    answer_text = line
                    break
            else:
                # Continue building current answer text
                if current_answer:
                    answer_text += " " + line
        
        # Add the last answer
        if current_answer and answer_text.strip():
            answers.append({
                'question_number': current_answer,
                'part': current_part,
                'answer_text': answer_text.strip(),
                'line_number': len(lines)
            })
        
        return answers
    
    def match_qa_pairs(self, questions, answers):
        """Match questions with their answers"""
        qa_pairs = []
        
        for question in questions:
            question_num = question['question_number']
            part = question['part']
            
            # Find matching answer
            matching_answer = None
            for answer in answers:
                if (answer['question_number'] == question_num and 
                    answer['part'] == part):
                    matching_answer = answer
                    break
            
            if matching_answer:
                qa_pairs.append({
                    'question_number': question_num,
                    'part': part,
                    'question_text': question['question_text'],
                    'answer_text': matching_answer['answer_text'],
                    'question_line': question['line_number'],
                    'answer_line': matching_answer['line_number'],
                    'confidence': 'high'
                })
            else:
                print(f"No matching answer found for question {question_num} ({part})")
        
        return qa_pairs
    
    def process_theory_paper(self, qp_path, ms_path, output_file):
        """Process a theory paper to extract Q&A pairs"""
        print(f"Processing theory question paper: {qp_path}")
        print(f"Processing theory mark scheme: {ms_path}")
        
        # Extract text from both PDFs
        qp_text = self.extract_text_from_pdf(qp_path)
        ms_text = self.extract_text_from_pdf(ms_path)
        
        if not qp_text or not ms_text:
            print("Failed to extract text from one or both PDFs")
            return
        
        # Find theory questions from question paper
        questions = self.find_theory_questions(qp_text)
        print(f"Found {len(questions)} theory questions")
        
        # Find answers from mark scheme
        answers = self.find_mark_scheme_answers(ms_text)
        print(f"Found {len(answers)} mark scheme answers")
        
        # Match Q&A pairs
        qa_pairs = self.match_qa_pairs(questions, answers)
        print(f"Matched {len(qa_pairs)} Q&A pairs")
        
        # Create final result structure
        result = {
            'paper_info': {
                'question_paper': os.path.basename(qp_path),
                'mark_scheme': os.path.basename(ms_path),
                'total_questions': len(questions),
                'total_answers': len(answers),
                'matched_pairs': len(qa_pairs)
            },
            'theory_questions': questions,
            'mark_scheme_answers': answers,
            'qa_pairs': qa_pairs,
            'summary': {
                'success_rate': (len(qa_pairs) / len(questions) * 100) if questions else 0,
                'paper_type': 'Theory Paper (Structured Questions)'
            }
        }
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {output_file}")
        return result

def main():
    extractor = TheoryQuestionExtractor()
    
    # Process AS Level Theory Paper 2
    print("=== PROCESSING AS LEVEL THEORY PAPER 2 ===")
    as_theory_result = extractor.process_theory_paper(
        'physics_9702_variant_2/9702_s22_qp_22.pdf',
        'physics_9702_variant_2/9702_s22_ms_22.pdf',
        'as_level_theory_paper_2.json'
    )
    
    print("\n=== PROCESSING A LEVEL THEORY PAPER 4 ===")
    a_level_theory_result = extractor.process_theory_paper(
        'physics_9702_variant_2/9702_s22_qp_42.pdf',
        'physics_9702_variant_2/9702_s22_ms_42.pdf',
        'a_level_theory_paper_4.json'
    )
    
    print("\n=== EXTRACTION COMPLETE ===")
    if as_theory_result:
        print(f"AS Level Theory: {as_theory_result['summary']['matched_pairs']}/{as_theory_result['summary']['total_questions']} Q&A pairs matched")
    if a_level_theory_result:
        print(f"A Level Theory: {a_level_theory_result['summary']['matched_pairs']}/{a_level_theory_result['summary']['total_questions']} Q&A pairs matched")

if __name__ == "__main__":
    main()
