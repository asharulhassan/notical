import fitz  # PyMuPDF
import re

def find_mcq_options(pdf_path):
    """Find where the actual A, B, C, D options are located in the PDF"""
    print(f"=== SEARCHING FOR MCQ OPTIONS IN: {pdf_path} ===")
    
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        # Split into lines
        lines = text.split('\n')
        
        # Look for lines that start with A), B), C), D)
        print("\n=== LOOKING FOR OPTION LINES ===")
        option_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for lines starting with A), B), C), D)
            if re.match(r'^[A-D]\)', line):
                option_lines.append((i+1, line))
                print(f"Line {i+1}: {line[:100]}...")
                
                # Show context around this option
                print(f"  Context (2 lines before and after):")
                for j in range(max(0, i-2), min(len(lines), i+3)):
                    if j != i:  # Skip the current line
                        context_line = lines[j].strip()
                        if context_line:
                            print(f"    {j+1}: {context_line[:80]}...")
                print()
        
        # Look for question numbers followed by options
        print("\n=== LOOKING FOR QUESTION + OPTIONS PATTERNS ===")
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for lines that might contain question + options
            if re.search(r'\d+\s+[A-D]', line):
                print(f"Potential Q+Option at line {i+1}: {line[:100]}...")
                
                # Look ahead for more options
                print(f"  Looking ahead for more options:")
                for j in range(1, 6):
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        if next_line and re.search(r'[A-D]', next_line):
                            print(f"    {i+j+1}: {next_line[:80]}...")
                print()
        
        # Look for specific patterns like "A ... B ... C ... D"
        print("\n=== LOOKING FOR A B C D SEQUENCES ===")
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for lines containing multiple options
            if line.count('A') > 0 and line.count('B') > 0 and line.count('C') > 0 and line.count('D') > 0:
                print(f"Line with all options at {i+1}: {line[:100]}...")
                print()
        
        print(f"\nTotal option lines found: {len(option_lines)}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Search summer paper
    find_mcq_options('physics_9702_variant_2/9702_s22_qp_12.pdf')
    
    print("\n" + "="*80 + "\n")
    
    # Search winter paper
    find_mcq_options('physics_9702_winter_2022/9702_w22_qp_12.pdf')

if __name__ == "__main__":
    main()
