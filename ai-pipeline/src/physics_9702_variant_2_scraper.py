import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin
import json
from typing import Dict, List, Optional

class Physics9702Variant2Scraper:
    """
    Focused scraper for Physics 9702 A-Level May-June 2022 Variant 2 papers
    """
    
    def __init__(self, base_url: str = "https://pastpapers.co"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Physics 9702 specific URLs
        self.physics_url = f"{self.base_url}/cie/?dir=A-Level/Physics-9702"
        self.may_june_2022_url = f"{self.base_url}/cie/?dir=A-Level/Physics-9702/2022-May-June"
        
    def get_may_june_2022_papers(self) -> List[Dict[str, str]]:
        """
        Get all papers for Physics 9702 May-June 2022
        """
        try:
            print(f"Fetching papers from: {self.may_june_2022_url}")
            response = self.session.get(self.may_june_2022_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            papers = []
            
            # Find all table rows that contain PDF files
            table_rows = soup.find_all('tr', attrs={'row-data-name': True})
            
            for row in table_rows:
                row_data_name = row.get('row-data-name', '')
                if not row_data_name.endswith('.pdf'):
                    continue
                
                # Extract filename without .pdf extension
                filename = row_data_name[:-4]
                
                # Parse the filename according to the convention
                paper_info = self._parse_physics_filename(filename)
                if paper_info:
                    # Find the download button (not the view button)
                    download_button = row.find('a', class_='btn btn-outline-primary bbx hidden-sm hidden-xs pull-right')
                    if download_button:
                        href = download_button.get('href')
                        # The download button has a direct file path, construct full URL
                        download_url = f"{self.base_url}/cie/{href}"
                        
                        papers.append({
                            "filename": filename,
                            "url": download_url,
                            "subject_code": paper_info["subject_code"],
                            "session": paper_info["session"],
                            "year": paper_info["year"],
                            "type": paper_info["type"],
                            "paper_component": paper_info["paper_component"],
                            "variant": paper_info["variant"],
                            "full_url": download_url
                        })
            
            return papers
            
        except Exception as e:
            print(f"Error getting papers: {e}")
            return []
    
    def _parse_physics_filename(self, filename: str) -> Optional[Dict[str, str]]:
        """
        Parse Physics 9702 filename according to the convention
        Example: 9702_s22_qp_21 -> subject: 9702, session: s, year: 22, type: qp, paper: 2, variant: 1
        """
        try:
            # Pattern: {subject_code}_{session}{year}_{type}_{paper_component}{variant}
            parts = filename.split('_')
            if len(parts) >= 4:
                subject_code = parts[0]  # 9702
                session_year = parts[1]  # s22
                paper_type = parts[2]    # qp or ms
                paper_variant = parts[3] # 11, 12, 13, 21, 22, 23, 31, 32, 33, 34
                
                # Extract session and year
                if len(session_year) >= 3:
                    session = session_year[0]  # s, w, or m
                    year = session_year[1:]    # 22
                else:
                    return None
                
                # Extract paper component and variant
                if len(paper_variant) >= 2:
                    paper_component = paper_variant[0]  # 1, 2, 3
                    variant = paper_variant[1:]         # 1, 2, 3, 4
                else:
                    return None
                
                return {
                    "subject_code": subject_code,
                    "session": session,
                    "year": year,
                    "type": paper_type,
                    "paper_component": paper_component,
                    "variant": variant
                }
        except:
            pass
        return None
    
    def get_variant_2_papers(self) -> List[Dict[str, str]]:
        """
        Get specifically Variant 2 papers for May-June 2022
        """
        all_papers = self.get_may_june_2022_papers()
        variant_2_papers = []
        
        for paper in all_papers:
            if paper["variant"] == "2":
                variant_2_papers.append(paper)
        
        return variant_2_papers
    
    def download_variant_2_papers(self, output_dir: str = "physics_9702_variant_2") -> List[str]:
        """
        Download all Variant 2 papers for Physics 9702 May-June 2022
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        variant_2_papers = self.get_variant_2_papers()
        downloaded_files = []
        
        print(f"\nFound {len(variant_2_papers)} Variant 2 papers:")
        for paper in variant_2_papers:
            print(f"  - {paper['filename']} ({paper['type']} - Paper {paper['paper_component']})")
        
        print(f"\nDownloading {len(variant_2_papers)} papers...")
        
        for i, paper in enumerate(variant_2_papers, 1):
            print(f"\n[{i}/{len(variant_2_papers)}] Downloading: {paper['filename']}")
            
            try:
                response = self.session.get(paper['url'], stream=True)
                response.raise_for_status()
                
                filename = f"{paper['filename']}.pdf"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"  ✓ Downloaded: {filepath}")
                downloaded_files.append(filepath)
                
                # Be nice to the server
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ Error downloading {paper['filename']}: {e}")
        
        return downloaded_files
    
    def analyze_paper_structure(self) -> Dict:
        """
        Analyze the structure of papers available for May-June 2022
        """
        all_papers = self.get_may_june_2022_papers()
        
        # Group by paper type
        question_papers = [p for p in all_papers if p["type"] == "qp"]
        mark_schemes = [p for p in all_papers if p["type"] == "ms"]
        
        # Group by paper component
        paper_components = {}
        for paper in all_papers:
            component = paper["paper_component"]
            if component not in paper_components:
                paper_components[component] = {"qp": [], "ms": []}
            
            if paper["type"] == "qp":
                paper_components[component]["qp"].append(paper)
            elif paper["type"] == "ms":
                paper_components[component]["ms"].append(paper)
        
        # Group by variant
        variants = {}
        for paper in all_papers:
            variant = paper["variant"]
            if variant not in variants:
                variants[variant] = []
            variants[variant].append(paper)
        
        return {
            "total_papers": len(all_papers),
            "question_papers": len(question_papers),
            "mark_schemes": len(mark_schemes),
            "paper_components": paper_components,
            "variants": variants,
            "all_papers": all_papers
        }

def main():
    """
    Main function to test the Physics 9702 Variant 2 scraper
    """
    scraper = Physics9702Variant2Scraper()
    
    print("=== Physics 9702 A-Level May-June 2022 Variant 2 Scraper ===")
    
    # Analyze the structure
    print("\n1. Analyzing paper structure...")
    structure = scraper.analyze_paper_structure()
    
    print(f"  Total papers found: {structure['total_papers']}")
    print(f"  Question papers: {structure['question_papers']}")
    print(f"  Mark schemes: {structure['mark_schemes']}")
    
    print("\n2. Paper components available:")
    for component, papers in structure["paper_components"].items():
        qp_count = len(papers["qp"])
        ms_count = len(papers["ms"])
        print(f"  Paper {component}: {qp_count} QP, {ms_count} MS")
    
    print("\n3. Variants available:")
    for variant, papers in structure["variants"].items():
        print(f"  Variant {variant}: {len(papers)} papers")
        for paper in papers:
            print(f"    - {paper['filename']} ({paper['type']})")
    
    # Get specifically Variant 2 papers
    print("\n4. Variant 2 papers:")
    variant_2_papers = scraper.get_variant_2_papers()
    for paper in variant_2_papers:
        print(f"  - {paper['filename']} ({paper['type']} - Paper {paper['paper_component']})")
    
    # Download Variant 2 papers
    print(f"\n5. Downloading Variant 2 papers...")
    downloaded_files = scraper.download_variant_2_papers()
    
    print(f"\n✓ Download complete! Downloaded {len(downloaded_files)} files:")
    for filepath in downloaded_files:
        print(f"  - {filepath}")
    
    # Save analysis to file
    print("\n6. Saving analysis to file...")
    with open("physics_9702_analysis.json", "w") as f:
        json.dump(structure, f, indent=2)
    print("  Analysis saved to physics_9702_analysis.json")

if __name__ == "__main__":
    main()
