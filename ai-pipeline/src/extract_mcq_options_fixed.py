import fitz  # PyMuPDF
import re
import json
import os

class FixedMCQOptionsExtractor:
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
    
    def find_question_boundaries(self, lines):
        """Find the start and end boundaries of each question"""
        boundaries = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for question numbers (1-40) followed by content
            question_match = re.match(r'^(\d+)\s+[A-D]', line)
            if question_match:
                question_num = question_match.group(1)
                if question_num in self.valid_question_numbers:
                    start_line = i
                    
                    # Look ahead to find where this question ends
                    end_line = start_line
                    for j in range(start_line + 1, len(lines)):
                        next_line = lines[j].strip()
                        
                        # If we hit another question number, stop
                        if re.match(r'^\d+\s+[A-D]', next_line):
                            break
                        
                        end_line = j
                    
                    boundaries[question_num] = {
                        'start': start_line,
                        'end': end_line,
                        'lines': lines[start_line:end_line + 1]
                    }
        
        return boundaries
    
    def extract_options_for_question(self, question_lines):
        """Extract options from the lines of a specific question"""
        options = {}
        
        # Look for option patterns within the question's lines
        for i, line in enumerate(question_lines):
            line = line.strip()
            
            # Pattern 1: Lines starting with A, B, C, D followed by text
            option_match = re.match(r'^([A-D])\s+(.+)$', line)
            if option_match:
                option_letter = option_match.group(1)
                option_text = option_match.group(2).strip()
                options[option_letter] = option_text
            
            # Pattern 2: Lines that are just A, B, C, D (might be followed by text on next line)
            elif re.match(r'^([A-D])$', line):
                option_letter = line
                # Look at next line for the option text
                if i + 1 < len(question_lines):
                    next_line = question_lines[i + 1].strip()
                    if next_line and not re.match(r'^[A-D]', next_line):
                        options[option_letter] = next_line
                    else:
                        options[option_letter] = ""  # Empty option
                else:
                    options[option_letter] = ""
            
            # Pattern 3: Lines containing A, B, C, D with some text
            elif re.search(r'^[A-D]\s*[^A-Z]', line):
                # This might be an option with some formatting
                for option in ['A', 'B', 'C', 'D']:
                    if line.startswith(option):
                        # Extract text after the option letter
                        option_text = line[len(option):].strip()
                        if option_text:
                            options[option] = option_text
                        break
        
        return options
    
    def is_simple_mcq(self, question_text, options):
        """Check if this is a simple MCQ (text-based, no complex formatting)"""
        # Skip if we don't have all 4 options
        if len(options) < 4:
            return False
        
        # Skip if any option is empty
        if any(not opt.strip() for opt in options.values()):
            return False
        
        # Skip if question contains words that suggest diagrams/tables
        complex_keywords = ['diagram', 'graph', 'table', 'figure', 'shown', 'illustration', 'sketch']
        question_lower = question_text.lower()
        if any(keyword in question_lower for keyword in complex_keywords):
            return False
        
        # Skip if options are very short (likely incomplete)
        if any(len(opt.strip()) < 3 for opt in options.values()):
            return False
        
        return True
    
    def find_simple_multiple_choice_questions(self, text):
        """Find simple MCQ questions with their A, B, C, D options"""
        questions = []
        
        # Split text into lines for better processing
        lines = text.split('\n')
        
        # Find question boundaries first
        boundaries = self.find_question_boundaries(lines)
        
        print(f"Found {len(boundaries)} questions with boundaries")
        
        for question_num, boundary in boundaries.items():
            question_lines = boundary['lines']
            
            # Extract question text (everything before options)
            question_text = ""
            option_start = -1
            
            for i, line in enumerate(question_lines):
                line = line.strip()
                
                # If we hit an option line, stop collecting question text
                if re.match(r'^[A-D]', line):
                    option_start = i
                    break
                
                question_text += " " + line
            
            question_text = question_text.strip()
            
            # Extract options from the remaining lines
            if option_start != -1:
                option_lines = question_lines[option_start:]
                options = self.extract_options_for_question(option_lines)
                
                # Only add if we have all 4 options and it's a simple MCQ
                if len(options) == 4 and self.is_simple_mcq(question_text, options):
                    questions.append({
                        'question_number': question_num,
                        'question_content': question_text,
                        'options': options,
                        'line_number': boundary['start'] + 1
                    })
                    print(f"Found simple MCQ {question_num}: {len(options)} options")
                    print(f"  Options: {list(options.keys())}")
        
        return questions
    
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
        
        # Find simple questions with options from question paper
        questions_with_options = self.find_simple_multiple_choice_questions(qp_text)
        print(f"Found {len(questions_with_options)} simple MCQs with options")
        
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
                'simple_mcqs_with_options': len([m for m in merged_data if m['options']]),
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
    extractor = FixedMCQOptionsExtractor()
    
    # Process summer paper
    print("=== PROCESSING SUMMER PAPER (May-June 2022) ===")
    summer_result = extractor.process_paper(
        'physics_9702_variant_2/9702_s22_qp_12.pdf',
        'physics_9702_variant_2/9702_s22_ms_12.pdf',
        'summer_fixed_mcqs.json'
    )
    
    print("\n=== PROCESSING WINTER PAPER (October-November 2022) ===")
    winter_result = extractor.process_paper(
        'physics_9702_winter_2022/9702_w22_qp_12.pdf',
        'physics_9702_winter_2022/9702_w22_ms_12.pdf',
        'winter_fixed_mcqs.json'
    )
    
    print("\n=== EXTRACTION COMPLETE ===")
    if summer_result:
        print(f"Summer paper: {summer_result['summary']['simple_mcqs_with_options']}/{summer_result['summary']['total_pairs']} simple MCQs have options")
    if winter_result:
        print(f"Winter paper: {winter_result['summary']['simple_mcqs_with_options']}/{winter_result['summary']['total_pairs']} simple MCQs have options")

if __name__ == "__main__":
    main()
