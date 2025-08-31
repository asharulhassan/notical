import fitz  # PyMuPDF
import re

def examine_question_structure(pdf_path, question_numbers):
    """Examine the complete structure of specific MCQ questions"""
    print(f"=== EXAMINING QUESTION STRUCTURE IN: {pdf_path} ===")
    
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        # Split into lines
        lines = text.split('\n')
        
        for question_num in question_numbers:
            print(f"\n=== QUESTION {question_num} ===")
            
            # Find the question
            question_start = -1
            for i, line in enumerate(lines):
                line = line.strip()
                if re.match(rf'^{question_num}\s+[A-D]', line):
                    question_start = i
                    break
            
            if question_start == -1:
                print(f"Question {question_num} not found")
                continue
            
            # Show the question and look ahead for options
            print(f"Question starts at line {question_start + 1}")
            
            # Show the question text (current line and next few lines)
            current_line = question_start
            question_text = []
            
            while current_line < len(lines) and current_line < question_start + 10:
                line = lines[current_line].strip()
                if line:
                    question_text.append(line)
                    
                    # Check if this line contains an option marker
                    if re.search(r'^[A-D]\.\.\.', line) or re.search(r'^[A-D]\s', line):
                        print(f"  OPTION FOUND: {line}")
                    else:
                        print(f"  {line}")
                    
                    # If we hit another question number, stop
                    if current_line != question_start and re.match(r'^\d+\s+[A-D]', line):
                        break
                
                current_line += 1
            
            # Now look specifically for A, B, C, D options
            print(f"\n  Looking for A, B, C, D options after question {question_num}:")
            found_options = {}
            
            for i in range(question_start, min(question_start + 20, len(lines))):
                line = lines[i].strip()
                
                # Look for option patterns
                if re.match(r'^A[\.\s]', line):
                    found_options['A'] = line
                    print(f"    A: {line}")
                elif re.match(r'^B[\.\s]', line):
                    found_options['B'] = line
                    print(f"    B: {line}")
                elif re.match(r'^C[\.\s]', line):
                    found_options['C'] = line
                    print(f"    C: {line}")
                elif re.match(r'^D[\.\s]', line):
                    found_options['D'] = line
                    print(f"    D: {line}")
                
                # If we hit another question, stop
                if i != question_start and re.match(r'^\d+\s+[A-D]', line):
                    break
            
            print(f"  Found {len(found_options)} options: {list(found_options.keys())}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Examine specific questions from summer paper
    print("SUMMER PAPER EXAMINATION:")
    examine_question_structure('physics_9702_variant_2/9702_s22_qp_12.pdf', [20, 22, 24, 25])
    
    print("\n" + "="*80 + "\n")
    
    # Examine specific questions from winter paper
    print("WINTER PAPER EXAMINATION:")
    examine_question_structure('physics_9702_winter_2022/9702_w22_qp_12.pdf', [18, 20, 21, 24])

if __name__ == "__main__":
    main()
