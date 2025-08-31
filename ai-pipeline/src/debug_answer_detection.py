import fitz  # PyMuPDF
import re

def debug_answer_detection():
    """
    Debug script to see what's happening with answer detection
    """
    ms_path = "physics_9702_variant_2/9702_s22_ms_12.pdf"
    
    print(f"Debugging answer detection for: {ms_path}")
    print()
    
    # Extract text from mark scheme
    doc = fitz.open(ms_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    
    print(f"Total text length: {len(text)} characters")
    print()
    
    # Split into lines and show each line
    lines = text.split('\n')
    print(f"Total lines: {len(lines)}")
    print()
    
    print("All lines with potential answer patterns:")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Check if line contains a number followed by A, B, C, or D
        if re.search(r'\d+\s+[A-D]', line):
            print(f"Line {i}: '{line}'")
            
            # Try our patterns
            patterns = [
                r'^(\d+)\s+([A-D])\s+\d+',  # 1 C 1, 2 B 1, etc.
                r'^(\d+)\s+([A-D])',        # 1 C, 2 B, etc.
                r'(\d+)\s+([A-D])\s+\d+',   # Anywhere in line: 1 C 1
            ]
            
            for j, pattern in enumerate(patterns):
                match = re.search(pattern, line)
                if match:
                    print(f"  Pattern {j+1} matched: {match.groups()}")
                else:
                    print(f"  Pattern {j+1}: no match")
            print()
    
    print("=== End of debug ===")

if __name__ == "__main__":
    debug_answer_detection()
