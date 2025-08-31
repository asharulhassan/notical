import fitz  # PyMuPDF
import re

def debug_specific_questions(pdf_path, question_numbers):
    """Debug specific questions to see their exact structure"""
    print(f"=== DEBUGGING SPECIFIC QUESTIONS IN: {pdf_path} ===")
    
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
            
            print(f"Question starts at line {question_start + 1}")
            
            # Show the question and next 15 lines
            print(f"Question and context:")
            for j in range(question_start, min(question_start + 15, len(lines))):
                line = lines[j].strip()
                if line:
                    # Highlight option lines
                    if re.match(r'^[A-D]', line):
                        print(f"  >>> OPTION: {line}")
                    elif re.match(r'^\d+\s+[A-D]', line) and j != question_start:
                        print(f"  >>> NEXT QUESTION: {line}")
                        break
                    else:
                        print(f"  {line}")
            
            # Now look specifically for A, B, C, D options
            print(f"\n  Looking for A, B, C, D options:")
            found_options = {}
            
            for i in range(question_start, min(question_start + 20, len(lines))):
                line = lines[i].strip()
                
                # If we hit another question, stop
                if i != question_start and re.match(r'^\d+\s+[A-D]', line):
                    break
                
                # Look for option patterns
                if re.match(r'^A\s', line):
                    found_options['A'] = line
                    print(f"    A: {line}")
                elif re.match(r'^B\s', line):
                    found_options['B'] = line
                    print(f"    B: {line}")
                elif re.match(r'^C\s', line):
                    found_options['C'] = line
                    print(f"    C: {line}")
                elif re.match(r'^D\s', line):
                    found_options['D'] = line
                    print(f"    D: {line}")
                
                # Also look for lines that are just A, B, C, D
                elif re.match(r'^[A-D]$', line):
                    option_letter = line
                    print(f"    {option_letter}: (just letter)")
                    # Look at next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not re.match(r'^[A-D]', next_line):
                            print(f"      Next line: {next_line}")
                            found_options[option_letter] = next_line
                        else:
                            found_options[option_letter] = ""
                    else:
                        found_options[option_letter] = ""
            
            print(f"  Found {len(found_options)} options: {list(found_options.keys())}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Debug specific questions from summer paper
    print("SUMMER PAPER DEBUG:")
    debug_specific_questions('physics_9702_variant_2/9702_s22_qp_12.pdf', [1, 2, 3, 4, 5])
    
    print("\n" + "="*80 + "\n")
    
    # Debug specific questions from winter paper
    print("WINTER PAPER DEBUG:")
    debug_specific_questions('physics_9702_winter_2022/9702_w22_qp_12.pdf', [1, 2, 3, 4, 5])

if __name__ == "__main__":
    main()
