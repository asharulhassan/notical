import fitz  # PyMuPDF
import re

def debug_mcq_structure(pdf_path):
    """Debug the structure of MCQ questions in a PDF"""
    print(f"=== DEBUGGING MCQ STRUCTURE IN: {pdf_path} ===")
    
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        # Split into lines
        lines = text.split('\n')
        
        # Look for question patterns
        print("\n=== LOOKING FOR QUESTION PATTERNS ===")
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for lines that might be questions
            if re.search(r'\d+\s*[A-D]', line):
                print(f"Line {i+1}: {line[:100]}...")
                
                # Look at next few lines for options
                print(f"  Next 3 lines:")
                for j in range(1, 4):
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        if next_line:
                            print(f"    {i+j+1}: {next_line[:80]}...")
                print()
            
            # Also look for lines with just A), B), C), D)
            elif re.match(r'^[A-D]\)', line):
                print(f"Option line {i+1}: {line[:80]}...")
                print()
        
        # Look for specific question numbers
        print("\n=== LOOKING FOR SPECIFIC QUESTIONS ===")
        for i, line in enumerate(lines):
            line = line.strip()
            if re.match(r'^1\s*[A-D]', line) or re.match(r'^2\s*[A-D]', line) or re.match(r'^3\s*[A-D]', line):
                print(f"Question 1-3 pattern at line {i+1}: {line[:100]}...")
                print(f"  Next 5 lines:")
                for j in range(1, 6):
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        if next_line:
                            print(f"    {i+j+1}: {next_line[:80]}...")
                print()
                break
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Debug summer paper
    debug_mcq_structure('physics_9702_variant_2/9702_s22_qp_12.pdf')
    
    print("\n" + "="*80 + "\n")
    
    # Debug winter paper
    debug_mcq_structure('physics_9702_winter_2022/9702_w22_qp_12.pdf')

if __name__ == "__main__":
    main()
