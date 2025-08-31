import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin
import json
from typing import Dict, List, Optional

class WinterPapersDownloader:
    """
    Downloader for Physics 9702 A-Level October-November 2022 papers (winter session)
    """
    
    def __init__(self, base_url: str = "https://pastpapers.co"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Physics 9702 winter session URL
        self.winter_2022_url = f"{self.base_url}/cie/?dir=A-Level/Physics-9702/2022-Oct-Nov"
        
    def get_winter_2022_papers(self) -> List[Dict[str, str]]:
        """
        Get all papers for Physics 9702 October-November 2022
        """
        try:
            print(f"Fetching papers from: {self.winter_2022_url}")
            response = self.session.get(self.winter_2022_url)
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
        Example: 9702_w22_qp_21 -> subject: 9702, session: w, year: 22, type: qp, paper: 2, variant: 1
        """
        try:
            # Pattern: {subject_code}_{session}{year}_{type}_{paper_component}{variant}
            parts = filename.split('_')
            if len(parts) >= 4:
                subject_code = parts[0]  # 9702
                session_year = parts[1]  # w22 (w for winter)
                paper_type = parts[2]    # qp or ms
                paper_variant = parts[3] # 11, 12, 13, 21, 22, 23, 31, 32, 33, 34
                
                # Extract session and year
                if len(session_year) >= 3:
                    session = session_year[0]  # w for winter
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
    
    def download_paper(self, paper_url: str, output_dir: str = "physics_9702_winter_2022") -> Optional[str]:
        """
        Download a specific paper PDF
        """
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            response = self.session.get(paper_url, stream=True)
            response.raise_for_status()
            
            # Extract filename from URL
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
    
    def download_variant_2_papers(self, output_dir: str = "physics_9702_winter_2022") -> List[str]:
        """
        Download all Variant 2 papers for Physics 9702 October-November 2022
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        all_papers = self.get_winter_2022_papers()
        variant_2_papers = []
        
        for paper in all_papers:
            if paper["variant"] == "2":
                variant_2_papers.append(paper)
        
        print(f"\nFound {len(variant_2_papers)} Variant 2 papers:")
        for paper in variant_2_papers:
            print(f"  - {paper['filename']} ({paper['type']} - Paper {paper['paper_component']})")
        
        print(f"\nDownloading {len(variant_2_papers)} papers...")
        
        downloaded_files = []
        for i, paper in enumerate(variant_2_papers, 1):
            print(f"\n[{i}/{len(variant_2_papers)}] Downloading: {paper['filename']}")
            
            filepath = self.download_paper(paper['url'], output_dir)
            if filepath:
                downloaded_files.append(filepath)
            
            # Be nice to the server
            time.sleep(1)
        
        return downloaded_files

def main():
    """
    Download Physics 9702 A-Level October-November 2022 Variant 2 papers
    """
    downloader = WinterPapersDownloader()
    
    print("=== Physics 9702 A-Level October-November 2022 Papers Downloader ===")
    print("Downloading winter session papers to test QA matching on another MCQ paper...")
    print()
    
    # Download Variant 2 papers
    downloaded_files = downloader.download_variant_2_papers()
    
    print(f"\n✓ Download complete! Downloaded {len(downloaded_files)} files:")
    for filepath in downloaded_files:
        print(f"  - {filepath}")
    
    print("\nNow we can test our QA matcher on the winter papers!")

if __name__ == "__main__":
    main()
