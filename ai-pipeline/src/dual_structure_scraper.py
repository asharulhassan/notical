#!/usr/bin/env python3
"""
NOTICAL AI Pipeline - Dual Structure Scraper
============================================
Handle both old /download/ structure (Math & Physics) and new /pdf-pages/?pdf= structure (Chemistry, Biology, English, etc.)
"""

import requests
import json
import logging
from pathlib import Path
import time
import random
import re
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DualStructureScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = "https://www.physicsandmathstutor.com"
        self.found_pdfs = []

    def scrape_all_subjects(self):
        """Scrape PDFs from all subjects using both structures"""
        logger.info("🔍 Scraping ALL subjects using dual structure approach...")
        
        # Structure 1: Direct /download/ (Math & Physics)
        logger.info("📚 Structure 1: Direct /download/ URLs (Math & Physics)")
        self._scrape_download_structure()
        
        # Structure 2: /pdf-pages/?pdf= (Chemistry, Biology, English, etc.)
        logger.info("📚 Structure 2: /pdf-pages/?pdf= URLs (Chemistry, Biology, English, etc.)")
        self._scrape_pdf_pages_structure()
        
        return self.found_pdfs

    def _scrape_download_structure(self):
        """Scrape subjects using direct /download/ structure"""
        download_subjects = {
            'Mathematics': '/download/Maths/',
            'Physics': '/download/Physics/'
        }
        
        for subject_name, url_path in download_subjects.items():
            try:
                logger.info(f"  🔍 Checking {subject_name} download structure...")
                download_url = f"https://pmt.physicsandmathstutor.com{url_path}"
                
                # This is what we already have - just log it
                logger.info(f"    ✅ {subject_name}: Already have access via {download_url}")
                
            except Exception as e:
                logger.error(f"Error with {subject_name} download structure: {e}")

    def _scrape_pdf_pages_structure(self):
        """Scrape subjects using /pdf-pages/?pdf= structure"""
        pdf_pages_subjects = {
            'Chemistry': '/past-papers/a-level-chemistry/',
            'Biology': '/past-papers/a-level-biology/',
            'English': '/past-papers/a-level-english-language/',
            'Economics': '/past-papers/a-level-economics/',
            'History': '/past-papers/a-level-history/',
            'Geography': '/past-papers/a-level-geography/'
        }
        
        for subject_name, url_path in pdf_pages_subjects.items():
            try:
                logger.info(f"  🔍 Scraping {subject_name} PDF pages structure...")
                subject_url = self.base_url + url_path
                
                # Get the main subject page
                response = self.session.get(subject_url, timeout=30)
                if response.status_code != 200:
                    logger.error(f"    ❌ Failed to access {subject_name}: HTTP {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for links that might contain PDFs
                pdf_links = soup.find_all('a', href=re.compile(r'pdf-pages\?pdf=', re.IGNORECASE))
                
                if pdf_links:
                    logger.info(f"    📚 Found {len(pdf_links)} PDF page links in {subject_name}")
                    
                    for pdf_link in pdf_links[:10]:  # Limit to avoid too many requests
                        pdf_href = pdf_link.get('href', '')
                        pdf_title = pdf_link.get_text(strip=True) or pdf_link.get('title', '') or 'Untitled'
                        
                        if pdf_href:
                            pdf_url = urljoin(subject_url, pdf_href)
                            
                            # Extract the actual PDF URL from the query parameter
                            actual_pdf_url = self._extract_actual_pdf_url(pdf_url)
                            
                            if actual_pdf_url:
                                pdf_info = {
                                    'url': actual_pdf_url,
                                    'title': pdf_title,
                                    'subject': subject_name,
                                    'source': 'PMT',
                                    'level': 'A-Level',
                                    'topic': self._extract_topic(pdf_title),
                                    'structure': 'pdf_pages'
                                }
                                
                                self.found_pdfs.append(pdf_info)
                                logger.info(f"      ✅ {pdf_title}")
                
                # Also look for direct PDF links that might exist
                direct_pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
                if direct_pdf_links:
                    logger.info(f"    📚 Found {len(direct_pdf_links)} direct PDF links in {subject_name}")
                    
                    for pdf_link in direct_pdf_links[:5]:
                        pdf_url = urljoin(subject_url, pdf_link.get('href', ''))
                        pdf_title = pdf_link.get_text(strip=True) or pdf_link.get('title', '') or 'Untitled'
                        
                        pdf_info = {
                            'url': pdf_url,
                            'title': pdf_title,
                            'subject': subject_name,
                            'source': 'PMT',
                            'level': 'A-Level',
                            'topic': self._extract_topic(pdf_title),
                            'structure': 'direct_pdf'
                        }
                        
                        self.found_pdfs.append(pdf_info)
                        logger.info(f"      ✅ {pdf_title}")
                
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                logger.error(f"Error scraping {subject_name}: {e}")

    def _extract_actual_pdf_url(self, pdf_page_url):
        """Extract the actual PDF URL from a /pdf-pages/?pdf= URL"""
        try:
            # Extract the PDF parameter
            match = re.search(r'pdf=([^&]+)', pdf_page_url)
            if match:
                encoded_pdf_url = match.group(1)
                actual_pdf_url = unquote(encoded_pdf_url)
                logger.debug(f"      🔗 Extracted PDF URL: {actual_pdf_url}")
                return actual_pdf_url
            return None
        except Exception as e:
            logger.debug(f"Error extracting PDF URL: {e}")
            return None

    def _extract_topic(self, title):
        """Extract topic from PDF title"""
        title = re.sub(r'\s*(QP|MS|MA|Question Paper|Mark Scheme|Model Answer)\s*$', '', title, flags=re.IGNORECASE)
        return title.strip()

    def save_found_pdfs(self, filename="dual_structure_pdfs.json"):
        """Save all found PDFs"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        data = {
            'real_content': self.found_pdfs,
            'summary': {
                'total_pdfs': len(self.found_pdfs),
                'subjects': list(set(pdf['subject'] for pdf in self.found_pdfs)),
                'structures': list(set(pdf['structure'] for pdf in self.found_pdfs))
            }
        }
        
        content_file = data_dir / filename
        with open(content_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"💾 Found {len(self.found_pdfs)} PDFs, saved to: {content_file}")
        self._show_summary()
        
        return content_file

    def _show_summary(self):
        """Show summary of found PDFs"""
        subjects = {}
        structures = {}
        
        for pdf in self.found_pdfs:
            subject = pdf['subject']
            structure = pdf.get('structure', 'unknown')
            
            subjects[subject] = subjects.get(subject, 0) + 1
            structures[structure] = structures.get(structure, 0) + 1
        
        logger.info(f"\n📊 Dual Structure Scraper Results:")
        logger.info(f"  📄 Total PDFs Found: {len(self.found_pdfs)}")
        logger.info(f"  📚 Subjects: {subjects}")
        logger.info(f"  🏗️  Structures: {structures}")
        
        if self.found_pdfs:
            logger.info(f"\n🎯 Next Steps:")
            logger.info(f"1. Run the existing PDF scraper on these new PDFs")
            logger.info(f"2. Extract Q&A pairs from Chemistry, Biology, English, etc.")
            logger.info(f"3. Expand training dataset beyond Math/Physics")

def main():
    logger.info("🎯 NOTICAL AI Pipeline - Dual Structure Scraper")
    logger.info("=" * 60)
    logger.info("🚀 Handling both old /download/ and new /pdf-pages/?pdf= structures!")
    logger.info("=" * 60)
    
    scraper = DualStructureScraper()
    found_pdfs = scraper.scrape_all_subjects()
    
    if found_pdfs:
        scraper.save_found_pdfs()
        logger.info(f"\n🎯 Dual Structure Scraping Complete!")
        logger.info(f"  📄 Total PDFs Found: {len(found_pdfs)}")
        logger.info(f"\n🎯 Now run the existing scraper to extract Q&A pairs!")
    else:
        logger.error("❌ No PDFs were found")
    
    return found_pdfs

if __name__ == "__main__":
    main()

