import fitz

def examine_paper_structure(pdf_path):
    """Examine the structure of a PDF paper"""
    print(f"Examining: {pdf_path}")
    print("=" * 50)
    
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    for page_num in range(min(10, len(doc))):  # Check first 10 pages
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')
        
        print(f"\nPage {page_num + 1}: {len(lines)} lines")
        print("-" * 30)
        
        # Look for question patterns
        question_lines = []
        for i, line in enumerate(lines):
            line = line.strip()
            if (line.startswith('1 ') or line.startswith('2 ') or 
                line.startswith('3 ') or line.startswith('4 ') or 
                line.startswith('5 ') or line.startswith('6 ') or
                line.startswith('7 ') or line.startswith('8 ') or
                line.startswith('9 ') or line.startswith('10 ')):
                question_lines.append(f"Line {i+1}: {line}")
        
        if question_lines:
            print("Found potential questions:")
            for q in question_lines[:5]:  # Show first 5
                print(f"  {q}")
        else:
            print("No question patterns found")
    
    doc.close()

if __name__ == "__main__":
    # Examine AS Level Theory Paper 2
    print("=== AS LEVEL THEORY PAPER 2 ===")
    examine_paper_structure('physics_9702_variant_2/9702_s22_qp_22.pdf')
    
    print("\n" + "=" * 80 + "\n")
    
    # Examine A Level Theory Paper 4
    print("=== A LEVEL THEORY PAPER 4 ===")
    examine_paper_structure('physics_9702_variant_2/9702_s22_qp_42.pdf')
