import fitz  # PyMuPDF
import re
import json
import os

class MCQOptionsExtractorV2:
    def __init__(self):
        self.valid_question_numbers = set(str(i) for i in range(1, 41))
    
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
    
    def find_multiple_choice_questions_with_options(self, text):
        """Find MCQ questions with their embedded A, B, C, D options"""
        questions = []
        
        # Split text into lines for better processing
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Look for question numbers (1-40) followed by content
            question_match = re.match(r'^(\d+)\s+[A-D]', line.strip())
            if question_match:
                question_num = question_match.group(1)
                if question_num in self.valid_question_numbers:
                    # Start building the complete question text
                    question_text = line.strip()
                    options = {}
                    
                    # Look ahead to collect the complete question and options
                    current_line = i
                    while current_line < len(lines) - 1:
                        current_line += 1
                        next_line = lines[current_line].strip()
                        
                        if not next_line:
                            continue
                        
                        # If we hit another question number, stop
                        if re.match(r'^\d+\s+[A-D]', next_line):
                            break
                        
                        # Add this line to question text
                        question_text += " " + next_line
                        
                        # Look for option patterns within the accumulated text
                        # Pattern: A followed by text, then B, C, D
                        if 'A' in question_text and 'B' in question_text and 'C' in question_text and 'D' in question_text:
                            # Extract options using regex
                            self.extract_options_from_text(question_text, options)
                            break
                    
                    # Only add if we have at least 2 options
                    if len(options) >= 2:
                        questions.append({
                            'question_number': question_num,
                            'question_content': question_text,
                            'options': options,
                            'line_number': i + 1
                        })
        
        return questions
    
    def extract_options_from_text(self, text, options):
        """Extract A, B, C, D options from question text"""
        # Look for patterns like "A text B text C text D text"
        # or "A text B text C text D" (D might be empty)
        
        # Pattern 1: A followed by text, then B, C, D
        pattern1 = r'A\s+([^B]+?)\s+B\s+([^C]+?)\s+C\s+([^D]+?)(?:\s+D\s+([^A-Z]+)?)?'
        match1 = re.search(pattern1, text, re.DOTALL)
        
        if match1:
            options['A'] = match1.group(1).strip()
            options['B'] = match1.group(2).strip()
            options['C'] = match1.group(3).strip()
            if match1.group(4):
                options['D'] = match1.group(4).strip()
            else:
                options['D'] = ""  # D option might be empty
            return
        
        # Pattern 2: Look for individual options
        # A option
        a_match = re.search(r'A\s+([^B]+?)(?=\s+B)', text, re.DOTALL)
        if a_match:
            options['A'] = a_match.group(1).strip()
        
        # B option
        b_match = re.search(r'B\s+([^C]+?)(?=\s+C)', text, re.DOTALL)
        if b_match:
            options['B'] = b_match.group(1).strip()
        
        # C option
        c_match = re.search(r'C\s+([^D]+?)(?=\s+D)', text, re.DOTALL)
        if c_match:
            options['C'] = c_match.group(1).strip()
        
        # D option (might be at the end)
        d_match = re.search(r'D\s+([^A-Z]+)?$', text, re.DOTALL)
        if d_match:
            options['D'] = d_match.group(1).strip() if d_match.group(1) else ""
    
    def merge_qa_with_options(self, qa_pairs, questions_with_options):
        """Merge Q&A pairs with their MCQ options"""
        merged_data = []
        
        for qa_pair in qa_pairs:
            question_num = qa_pair['question_number']
            
            # Find matching question with options
            matching_question = None
            for q in questions_with_options:
                if q['question_number'] == question_num:
                    matching_question = q
                    break
            
            if matching_question:
                merged_item = {
                    'question_number': question_num,
                    'question_content': matching_question['question_content'],
                    'options': matching_question['options'],
                    'correct_answer': qa_pair['answer_option'],
                    'question_line': qa_pair['question_line'],
                    'answer_line': qa_pair['answer_line'],
                    'confidence': qa_pair['confidence']
                }
                merged_data.append(merged_item)
            else:
                # Fallback if no options found
                merged_item = {
                    'question_number': question_num,
                    'question_content': qa_pair['question_content'],
                    'options': {},
                    'correct_answer': qa_pair['answer_option'],
                    'question_line': qa_pair['question_line'],
                    'answer_line': qa_pair['answer_line'],
                    'confidence': qa_pair['confidence']
                }
                merged_data.append(merged_item)
        
        return merged_data
    
    def process_paper(self, qp_path, ms_path, output_file):
        """Process a complete paper to extract Q&A with MCQ options"""
        print(f"Processing question paper: {qp_path}")
        print(f"Processing mark scheme: {ms_path}")
        
        # Extract text from both PDFs
        qp_text = self.extract_text_from_pdf(qp_path)
        ms_text = self.extract_text_from_pdf(ms_path)
        
        if not qp_text or not ms_text:
            print("Failed to extract text from one or both PDFs")
            return
        
        # Find questions with options from question paper
        questions_with_options = self.find_multiple_choice_questions_with_options(qp_text)
        print(f"Found {len(questions_with_options)} questions with options")
        
        # Find answers from mark scheme (using existing logic)
        answers = self.find_multiple_choice_answers_fixed(ms_text)
        print(f"Found {len(answers)} answers")
        
        # Match Q&A pairs
        qa_pairs = self.match_qa_pairs(questions_with_options, answers)
        print(f"Matched {len(qa_pairs)} Q&A pairs")
        
        # Merge with options
        merged_data = self.merge_qa_with_options(qa_pairs, questions_with_options)
        
        # Create final result structure
        result = {
            'paper_info': {
                'question_paper': os.path.basename(qp_path),
                'mark_scheme': os.path.basename(ms_path),
                'total_questions': len(merged_data)
            },
            'mcq_data': merged_data,
            'summary': {
                'total_pairs': len(merged_data),
                'questions_with_options': len([m for m in merged_data if m['options']]),
                'questions_without_options': len([m for m in merged_data if not m['options']]),
                'success_rate': 100.0 if len(merged_data) == 40 else (len(merged_data) / 40) * 100
            }
        }
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {output_file}")
        return result
    
    def find_multiple_choice_answers_fixed(self, text):
        """Find MCQ answers from mark scheme (reusing existing logic)"""
        answers = []
        lines = text.split('\n')
        
        # Find the "Answer" section
        answer_section_start = -1
        for i, line in enumerate(lines):
            if 'Answer' in line and ('Mark' in line or 'Scheme' in line):
                answer_section_start = i
                break
        
        if answer_section_start == -1:
            # Look for just "Answer" if the above doesn't work
            for i, line in enumerate(lines):
                if 'Answer' in line:
                    answer_section_start = i
                    break
        
        if answer_section_start == -1:
            print("Could not find Answer section")
            return answers
        
        # Process lines after the Answer section
        current_line = answer_section_start + 1
        while current_line < len(lines):
            line = lines[current_line].strip()
            
            # Skip empty lines
            if not line:
                current_line += 1
                continue
            
            # Look for lines with only numbers (question numbers)
            if re.match(r'^\d+$', line):
                question_num = line
                
                # Look at the next line for the answer
                if current_line + 1 < len(lines):
                    next_line = lines[current_line + 1].strip()
                    
                    # Check if next line contains only a single letter (A, B, C, or D)
                    if re.match(r'^[A-D]$', next_line):
                        answers.append({
                            'question_number': question_num,
                            'answer_option': next_line,
                            'answer_line': current_line + 2  # +2 because we're 0-indexed
                        })
                        current_line += 2  # Skip both lines
                        continue
            
            current_line += 1
        
        return answers
    
    def match_qa_pairs(self, questions, answers):
        """Match questions with their answers"""
        qa_pairs = []
        
        for question in questions:
            question_num = question['question_number']
            
            # Find matching answer
            matching_answer = None
            for answer in answers:
                if answer['question_number'] == question_num:
                    matching_answer = answer
                    break
            
            if matching_answer:
                qa_pairs.append({
                    'question_number': question_num,
                    'question_content': question['question_content'],
                    'answer_option': matching_answer['answer_option'],
                    'question_line': question['line_number'],
                    'answer_line': matching_answer['answer_line'],
                    'confidence': 'high'
                })
            else:
                print(f"No matching answer found for question {question_num}")
        
        return qa_pairs

def main():
    extractor = MCQOptionsExtractorV2()
    
    # Process summer paper
    print("=== PROCESSING SUMMER PAPER (May-June 2022) ===")
    summer_result = extractor.process_paper(
        'physics_9702_variant_2/9702_s22_qp_12.pdf',
        'physics_9702_variant_2/9702_s22_ms_12.pdf',
        'summer_mcq_with_options_v2.json'
    )
    
    print("\n=== PROCESSING WINTER PAPER (October-November 2022) ===")
    winter_result = extractor.process_paper(
        'physics_9702_winter_2022/9702_w22_qp_12.pdf',
        'physics_9702_winter_2022/9702_w22_ms_12.pdf',
        'winter_mcq_with_options_v2.json'
    )
    
    print("\n=== EXTRACTION COMPLETE ===")
    if summer_result:
        print(f"Summer paper: {summer_result['summary']['questions_with_options']}/{summer_result['summary']['total_pairs']} questions have options")
    if winter_result:
        print(f"Winter paper: {winter_result['summary']['questions_with_options']}/{winter_result['summary']['total_pairs']} questions have options")

if __name__ == "__main__":
    main()
