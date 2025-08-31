#!/usr/bin/env python3
"""
NOTICAL AI Pipeline - Real Subject PDF Scraper
==============================================
Find REAL PDF URLs from Chemistry, Biology, English, etc. pages
"""

import requests
import json
import logging
from pathlib import Path
import time
import random
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealSubjectScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = "https://www.physicsandmathstutor.com"
        self.found_pdfs = []

    def scrape_all_subjects(self):
        """Scrape REAL PDFs from all accessible subjects"""
        logger.info("🔍 Scraping REAL PDFs from all accessible subjects...")
        
        # The subjects we know are accessible
        accessible_subjects = {
            'Chemistry': '/a-level-chemistry/',
            'Biology': '/a-level-biology/',
            'English': '/a-level-english/',
            'Economics': '/a-level-economics/',
            'History': '/a-level-history/',
            'Geography': '/a-level-geography/'
        }
        
        for subject_name, url_path in accessible_subjects.items():
            logger.info(f"🔍 Scraping {subject_name}...")
            try:
                subject_url = self.base_url + url_path
                self._scrape_subject_page(subject_name, subject_url)
                time.sleep(random.uniform(1, 2))  # Be respectful
            except Exception as e:
                logger.error(f"Error scraping {subject_name}: {e}")
        
        return self.found_pdfs

    def _scrape_subject_page(self, subject_name, subject_url):
        """Scrape a subject page for PDFs"""
        try:
            logger.info(f"  📄 Accessing: {subject_url}")
            response = self.session.get(subject_url, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"  ❌ Failed to access {subject_name}: HTTP {response.status_code}")
                return
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for PDF links
            pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
            
            if pdf_links:
                logger.info(f"  📚 Found {len(pdf_links)} PDFs in {subject_name}")
                
                for pdf_link in pdf_links:
                    pdf_url = urljoin(subject_url, pdf_link.get('href', ''))
                    pdf_title = pdf_link.get_text(strip=True) or pdf_link.get('title', '') or 'Untitled'
                    
                    pdf_info = {
                        'url': pdf_url,
                        'title': pdf_title,
                        'subject': subject_name,
                        'source': 'PMT',
                        'level': 'A-Level',
                        'topic': self._extract_topic(pdf_title)
                    }
                    
                    self.found_pdfs.append(pdf_info)
                    logger.info(f"    ✅ {pdf_title}")
            else:
                logger.info(f"  ⚠️  No PDFs found on {subject_name} main page")
                
                # Try to find sub-pages with PDFs
                self._find_sub_pages_with_pdfs(subject_name, subject_url, soup)
                
        except Exception as e:
            logger.error(f"Error scraping {subject_name}: {e}")

    def _find_sub_pages_with_pdfs(self, subject_name, subject_url, soup):
        """Find sub-pages that might contain PDFs"""
        try:
            # Look for links to past papers, notes, etc.
            sub_page_patterns = [
                'past-papers', 'notes', 'revision', 'questions', 'worksheets',
                'exam-papers', 'mark-schemes', 'model-answers'
            ]
            
            for pattern in sub_page_patterns:
                sub_links = soup.find_all('a', href=re.compile(pattern, re.IGNORECASE))
                
                for sub_link in sub_links[:5]:  # Limit to avoid too many requests
                    sub_href = sub_link.get('href', '')
                    if sub_href:
                        sub_url = urljoin(subject_url, sub_href)
                        logger.info(f"    🔍 Checking sub-page: {sub_url}")
                        
                        try:
                            sub_response = self.session.get(sub_url, timeout=30)
                            if sub_response.status_code == 200:
                                sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
                                sub_pdfs = sub_soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
                                
                                if sub_pdfs:
                                    logger.info(f"      📚 Found {len(sub_pdfs)} PDFs on sub-page!")
                                    
                                    for pdf_link in sub_pdfs:
                                        pdf_url = urljoin(sub_url, pdf_link.get('href', ''))
                                        pdf_title = pdf_link.get_text(strip=True) or pdf_link.get('title', '') or 'Untitled'
                                        
                                        pdf_info = {
                                            'url': pdf_url,
                                            'title': pdf_title,
                                            'subject': subject_name,
                                            'source': 'PMT',
                                            'level': 'A-Level',
                                            'topic': self._extract_topic(pdf_title)
                                        }
                                        
                                        self.found_pdfs.append(pdf_info)
                                        logger.info(f"        ✅ {pdf_title}")
                                    
                                    break  # Found PDFs, no need to check more sub-pages
                            
                            time.sleep(0.5)  # Small delay between sub-page requests
                            
                        except Exception as e:
                            logger.debug(f"Error checking sub-page {sub_url}: {e}")
                            
        except Exception as e:
            logger.debug(f"Error finding sub-pages for {subject_name}: {e}")

    def _extract_topic(self, title):
        """Extract topic from PDF title"""
        # Remove common suffixes
        title = re.sub(r'\s*(QP|MS|MA|Question Paper|Mark Scheme|Model Answer)\s*$', '', title, flags=re.IGNORECASE)
        return title.strip()

    def save_found_pdfs(self, filename="real_subject_pdfs.json"):
        """Save all found PDFs"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        data = {
            'real_content': self.found_pdfs,
            'summary': {
                'total_pdfs': len(self.found_pdfs),
                'subjects': list(set(pdf['subject'] for pdf in self.found_pdfs))
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
        for pdf in self.found_pdfs:
            subject = pdf['subject']
            subjects[subject] = subjects.get(subject, 0) + 1
        
        logger.info(f"\n📊 Real Subject PDF Scraper Results:")
        logger.info(f"  📄 Total PDFs Found: {len(self.found_pdfs)}")
        logger.info(f"  📚 Subjects: {subjects}")
        
        if self.found_pdfs:
            logger.info(f"\n🎯 Next Steps:")
            logger.info(f"1. Run the existing PDF scraper on these REAL PDFs")
            logger.info(f"2. Extract Q&A pairs from Chemistry, Biology, English, etc.")
            logger.info(f"3. Expand training dataset beyond Math/Physics")

def main():
    logger.info("🎯 NOTICAL AI Pipeline - Real Subject PDF Scraper")
    logger.info("=" * 60)
    logger.info("🚀 Finding REAL PDFs from Chemistry, Biology, English, etc.!")
    logger.info("=" * 60)
    
    scraper = RealSubjectScraper()
    found_pdfs = scraper.scrape_all_subjects()
    
    if found_pdfs:
        scraper.save_found_pdfs()
        logger.info(f"\n🎯 PDF Discovery Complete!")
        logger.info(f"  📄 Total PDFs Found: {len(found_pdfs)}")
        logger.info(f"\n🎯 Now run the existing scraper to extract Q&A pairs!")
    else:
        logger.error("❌ No PDFs were found")
    
    return found_pdfs

if __name__ == "__main__":
    main()

