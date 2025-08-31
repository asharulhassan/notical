import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse
import json
from typing import Dict, List, Optional, Tuple
import re

class PastPapersCoScraper:
    """
    Scraper for pastpapers.co website with clean URL structure
    """
    
    def __init__(self, base_url: str = "https://pastpapers.co"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_exam_levels(self) -> List[Dict[str, str]]:
        """
        Get all available exam levels (IGCSE, A-Level, O-Level, Pre-U)
        """
        levels = [
            {"name": "IGCSE", "url": f"{self.base_url}/cie/?dir=IGCSE"},
            {"name": "A-Level", "url": f"{self.base_url}/cie/?dir=A-Level"},
            {"name": "O-Level", "url": f"{self.base_url}/cie/?dir=O-Level"},
            {"name": "Pre-U", "url": f"{self.base_url}/cie/?dir=Pre-U"}
        ]
        return levels
    
    def get_subjects_for_level(self, level_url: str) -> List[Dict[str, str]]:
        """
        Get all subjects available for a specific exam level
        """
        try:
            response = self.session.get(level_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            subjects = []
            # Look for folder links that contain subject codes
            folder_links = soup.find_all('a', href=True)
            
            for link in folder_links:
                href = link.get('href')
                if href and 'dir=' in href:
                    # Extract subject info from URL
                    dir_part = href.split('dir=')[-1]
                    if '/' in dir_part:
                        level, subject_part = dir_part.split('/', 1)
                        if '-' in subject_part:
                            subject_name, code = subject_part.rsplit('-', 1)
                            subjects.append({
                                "name": subject_name.replace('-', ' ').title(),
                                "code": code,
                                "url": urljoin(self.base_url, href),
                                "full_path": f"{level}/{subject_part}"
                            })
            
            return subjects
            
        except Exception as e:
            print(f"Error getting subjects for {level_url}: {e}")
            return []
    
    def get_years_for_subject(self, subject_url: str) -> List[Dict[str, str]]:
        """
        Get all available years/sessions for a specific subject
        """
        try:
            response = self.session.get(subject_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            years = []
            # Look for folder links that contain year patterns
            folder_links = soup.find_all('a', href=True)
            
            for link in folder_links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                if href and 'dir=' in href and text:
                    # Check if it's a year folder (e.g., "2022-May-June")
                    if re.match(r'\d{4}-[A-Za-z-]+', text):
                        years.append({
                            "name": text,
                            "url": urljoin(self.base_url, href),
                            "year": text.split('-')[0],
                            "session": '-'.join(text.split('-')[1:])
                        })
            
            return years
            
        except Exception as e:
            print(f"Error getting years for {subject_url}: {e}")
            return []
    
    def get_papers_for_year(self, year_url: str) -> List[Dict[str, str]]:
        """
        Get all available papers for a specific year/session
        """
        try:
            response = self.session.get(year_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            papers = []
            # Look for PDF files and their associated mark schemes
            file_links = soup.find_all('a', href=True)
            
            for link in file_links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                if href and text and (href.endswith('.pdf') or 'pdf' in href.lower()):
                    # Parse filename to extract paper info
                    filename = text.strip()
                    if filename.endswith('.pdf'):
                        filename = filename[:-4]
                    
                    # Extract paper type and variant
                    paper_info = self._parse_paper_filename(filename)
                    if paper_info:
                        papers.append({
                            "filename": filename,
                            "url": urljoin(self.base_url, href),
                            "paper_type": paper_info["type"],
                            "variant": paper_info["variant"],
                            "full_url": urljoin(self.base_url, href)
                        })
            
            return papers
            
        except Exception as e:
            print(f"Error getting papers for {year_url}: {e}")
            return []
    
    def _parse_paper_filename(self, filename: str) -> Optional[Dict[str, str]]:
        """
        Parse paper filename to extract type and variant
        Example: 9702_s22_qp_22 -> type: qp, variant: 22
        """
        try:
            # Pattern: {code}_{session}_{type}_{variant}
            parts = filename.split('_')
            if len(parts) >= 4:
                code = parts[0]
                session = parts[1]
                paper_type = parts[2]
                variant = parts[3]
                
                return {
                    "code": code,
                    "session": session,
                    "type": paper_type,
                    "variant": variant
                }
        except:
            pass
        return None
    
    def download_paper(self, paper_url: str, output_dir: str = "downloads") -> Optional[str]:
        """
        Download a specific paper PDF
        """
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            response = self.session.get(paper_url, stream=True)
            response.raise_for_status()
            
            # Extract filename from URL or content-disposition
            filename = paper_url.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error downloading {paper_url}: {e}")
            return None
    
    def get_physics_9702_2022_may_june_variant_2(self) -> Dict[str, str]:
        """
        Specifically get Physics 9702 A-Level May-June 2022 Variant 2 papers
        """
        # Navigate through the structure
        a_level_url = f"{self.base_url}/cie/?dir=A-Level"
        physics_url = f"{self.base_url}/cie/?dir=A-Level/Physics-9702"
        year_2022_url = f"{self.base_url}/cie/?dir=A-Level/Physics-9702/2022-May-June"
        
        # Get papers for 2022 May-June
        papers = self.get_papers_for_year(year_2022_url)
        
        # Filter for variant 2 papers
        variant_2_papers = []
        for paper in papers:
            if paper["variant"] == "2":
                variant_2_papers.append(paper)
        
        return {
            "year_url": year_2022_url,
            "papers": variant_2_papers,
            "total_variant_2_papers": len(variant_2_papers)
        }
    
    def scrape_full_structure(self) -> Dict:
        """
        Scrape the complete structure of pastpapers.co
        """
        structure = {
            "exam_levels": [],
            "subjects": {},
            "years": {},
            "papers": {}
        }
        
        # Get exam levels
        levels = self.get_exam_levels()
        structure["exam_levels"] = levels
        
        # For each level, get subjects
        for level in levels:
            level_name = level["name"]
            print(f"Scraping subjects for {level_name}...")
            
            subjects = self.get_subjects_for_level(level["url"])
            structure["subjects"][level_name] = subjects
            
            # For each subject, get years
            for subject in subjects:
                subject_key = f"{level_name}_{subject['code']}"
                print(f"  Scraping years for {subject['name']} ({subject['code']})...")
                
                years = self.get_years_for_subject(subject["url"])
                structure["years"][subject_key] = years
                
                # For each year, get papers
                for year in years:
                    year_key = f"{subject_key}_{year['name']}"
                    print(f"    Scraping papers for {year['name']}...")
                    
                    papers = self.get_papers_for_year(year["url"])
                    structure["papers"][year_key] = papers
                    
                    # Be nice to the server
                    time.sleep(1)
        
        return structure

def main():
    """
    Main function to test the scraper
    """
    scraper = PastPapersCoScraper()
    
    print("=== PastPapers.co Scraper ===")
    print("\n1. Getting exam levels...")
    levels = scraper.get_exam_levels()
    for level in levels:
        print(f"  - {level['name']}: {level['url']}")
    
    print("\n2. Getting Physics 9702 subjects...")
    physics_url = f"{scraper.base_url}/cie/?dir=A-Level/Physics-9702"
    years = scraper.get_years_for_subject(physics_url)
    print(f"  Found {len(years)} years/sessions:")
    for year in years:
        print(f"    - {year['name']}")
    
    print("\n3. Getting 2022 May-June papers...")
    year_2022_url = f"{scraper.base_url}/cie/?dir=A-Level/Physics-9702/2022-May-June"
    papers = scraper.get_papers_for_year(year_2022_url)
    print(f"  Found {len(papers)} papers:")
    for paper in papers:
        print(f"    - {paper['filename']} (Type: {paper['paper_type']}, Variant: {paper['variant']})")
    
    print("\n4. Filtering for Variant 2 papers...")
    variant_2_papers = [p for p in papers if p["variant"] == "2"]
    print(f"  Found {len(variant_2_papers)} Variant 2 papers:")
    for paper in variant_2_papers:
        print(f"    - {paper['filename']} ({paper['paper_type']})")
    
    # Save structure to file
    print("\n5. Saving structure to file...")
    structure = scraper.scrape_full_structure()
    with open("pastpapers_structure.json", "w") as f:
        json.dump(structure, f, indent=2)
    print("  Structure saved to pastpapers_structure.json")

if __name__ == "__main__":
    main()
