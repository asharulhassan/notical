#!/usr/bin/env python3
"""
NOTICAL AI Pipeline - Direct PDF Finder
=======================================
Go directly to past papers section to find PDFs
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

class DirectPDFFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = "https://www.physicsandmathstutor.com"
        self.found_pdfs = []

    def find_pdfs_directly(self):
        """Find PDFs directly from past papers section"""
        logger.info("🔍 Going directly to past papers section...")
        
        # Direct URLs to past papers sections
        direct_urls = [
            "https://www.physicsandmathstutor.com/past-papers/",
            "https://www.physicsandmathstutor.com/past-papers/a-level/",
            "https://www.physicsandmathstutor.com/past-papers/a-level-chemistry/",
            "https://www.physicsandmathstutor.com/past-papers/a-level-biology/",
            "https://www.physicsandmathstutor.com/past-papers/a-level-english/",
            "https://www.physicsandmathstutor.com/past-papers/a-level-economics/",
            "https://www.physicsandmathstutor.com/past-papers/a-level-history/",
            "https://www.physicsandmathstutor.com/past-papers/a-level-geography/"
        ]
        
        for url in direct_urls:
            try:
                logger.info(f"🔍 Checking: {url}")
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for PDF links
                    pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
                    
                    if pdf_links:
                        logger.info(f"  📚 Found {len(pdf_links)} PDFs on {url}")
                        
                        for pdf_link in pdf_links:
                            pdf_url = urljoin(url, pdf_link.get('href', ''))
                            pdf_title = pdf_link.get_text(strip=True) or pdf_link.get('title', '') or 'Untitled'
                            
                            # Determine subject from URL or title
                            subject = self._determine_subject_from_url(url, pdf_title)
                            
                            pdf_info = {
                                'url': pdf_url,
                                'title': pdf_title,
                                'subject': subject,
                                'source': 'PMT',
                                'level': 'A-Level',
                                'topic': self._extract_topic(pdf_title)
                            }
                            
                            self.found_pdfs.append(pdf_info)
                            logger.info(f"    ✅ {pdf_title} ({subject})")
                    else:
                        logger.info(f"  ⚠️  No PDFs found on {url}")
                        
                        # Look for links to other pages that might have PDFs
                        other_links = soup.find_all('a', href=re.compile(r'(past-papers|revision|notes)', re.IGNORECASE))
                        logger.info(f"    🔍 Found {len(other_links)} other links to explore")
                        
                        # Explore a few of these links
                        for link in other_links[:3]:
                            link_url = urljoin(url, link.get('href', ''))
                            link_text = link.get_text(strip=True)
                            logger.info(f"      🔗 {link_text} -> {link_url}")
                            
                            # Try to find PDFs on this sub-page
                            self._explore_sub_page(link_url, subject)
                            
                else:
                    logger.info(f"  ❌ Failed to access: HTTP {response.status_code}")
                
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                logger.error(f"Error checking {url}: {e}")
        
        return self.found_pdfs

    def _explore_sub_page(self, url, parent_subject):
        """Explore a sub-page for PDFs"""
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
                
                if pdf_links:
                    logger.info(f"        📚 Found {len(pdf_links)} PDFs on sub-page!")
                    
                    for pdf_link in pdf_links:
                        pdf_url = urljoin(url, pdf_link.get('href', ''))
                        pdf_title = pdf_link.get_text(strip=True) or pdf_link.get('title', '') or 'Untitled'
                        
                        subject = self._determine_subject_from_url(url, pdf_title) or parent_subject
                        
                        pdf_info = {
                            'url': pdf_url,
                            'title': pdf_title,
                            'subject': subject,
                            'source': 'PMT',
                            'level': 'A-Level',
                            'topic': self._extract_topic(pdf_title)
                        }
                        
                        self.found_pdfs.append(pdf_info)
                        logger.info(f"          ✅ {pdf_title} ({subject})")
                        
        except Exception as e:
            logger.debug(f"Error exploring sub-page {url}: {e}")

    def _determine_subject_from_url(self, url, title):
        """Determine subject from URL or title"""
        url_lower = url.lower()
        title_lower = title.lower()
        
        if 'chemistry' in url_lower or 'chemistry' in title_lower:
            return 'Chemistry'
        elif 'biology' in url_lower or 'biology' in title_lower:
            return 'Biology'
        elif 'english' in url_lower or 'english' in title_lower:
            return 'English'
        elif 'economics' in url_lower or 'economics' in title_lower:
            return 'Economics'
        elif 'history' in url_lower or 'history' in title_lower:
            return 'History'
        elif 'geography' in url_lower or 'geography' in title_lower:
            return 'Geography'
        elif 'math' in url_lower or 'math' in title_lower:
            return 'Mathematics'
        elif 'physics' in url_lower or 'physics' in title_lower:
            return 'Physics'
        else:
            return 'Unknown'

    def _extract_topic(self, title):
        """Extract topic from PDF title"""
        title = re.sub(r'\s*(QP|MS|MA|Question Paper|Mark Scheme|Model Answer)\s*$', '', title, flags=re.IGNORECASE)
        return title.strip()

    def save_found_pdfs(self, filename="direct_pdf_finder_results.json"):
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
        
        logger.info(f"\n📊 Direct PDF Finder Results:")
        logger.info(f"  📄 Total PDFs Found: {len(self.found_pdfs)}")
        logger.info(f"  📚 Subjects: {subjects}")
        
        if self.found_pdfs:
            logger.info(f"\n🎯 Next Steps:")
            logger.info(f"1. Run the existing PDF scraper on these PDFs")
            logger.info(f"2. Extract Q&A pairs from new subjects")
            logger.info(f"3. Expand training dataset beyond Math/Physics")

def main():
    logger.info("🎯 NOTICAL AI Pipeline - Direct PDF Finder")
    logger.info("=" * 50)
    logger.info("🚀 Going directly to past papers to find PDFs!")
    logger.info("=" * 50)
    
    finder = DirectPDFFinder()
    found_pdfs = finder.find_pdfs_directly()
    
    if found_pdfs:
        finder.save_found_pdfs()
        logger.info(f"\n🎯 PDF Discovery Complete!")
        logger.info(f"  📄 Total PDFs Found: {len(found_pdfs)}")
        logger.info(f"\n🎯 Now run the existing scraper to extract Q&A pairs!")
    else:
        logger.error("❌ No PDFs were found")
    
    return found_pdfs

if __name__ == "__main__":
    main()

