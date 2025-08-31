#!/usr/bin/env python3
"""
NOTICAL AI Pipeline - Comprehensive PDF Scraper
===============================================
Follows the exact structure: Subject → Exam Board → Topic → PDFs
Handles both direct /download/ URLs and /pdf-pages/?pdf= wrapper URLs
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

class ComprehensivePDFScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = "https://www.physicsandmathstutor.com"
        self.found_pdfs = []

    def scrape_all_subjects(self):
        """Scrape PDFs from ALL subjects following the exact structure"""
        logger.info("🔍 Comprehensive PDF Scraper - Getting ALL subjects, ALL exam boards, ALL topics, ALL PDFs!")
        
        # All subjects to scrape
        subjects = {
            'Biology': {
                'papers': '/past-papers/a-level-biology/',
                'revision': '/biology-revision/'
            },
            'Chemistry': {
                'papers': '/past-papers/a-level-chemistry/',
                'revision': '/chemistry-revision/'
            },
            'Physics': {
                'papers': '/past-papers/a-level-physics/',
                'revision': '/physics-revision/'
            },
            'Mathematics': {
                'papers': '/a-level-maths-papers/',
                'revision': '/maths-revision/'
            },
            'English': {
                'papers': '/past-papers/a-level-english-language/',
                'revision': '/english-revision/'
            },
            'Economics': {
                'papers': '/past-papers/a-level-economics/',
                'revision': '/economics-revision/'
            },
            'History': {
                'papers': '/past-papers/a-level-history/',
                'revision': '/history-revision/'
            },
            'Geography': {
                'papers': '/past-papers/a-level-geography/',
                'revision': '/geography-revision/'
            }
        }
        
        for subject_name, subject_paths in subjects.items():
            try:
                logger.info(f"🔍 Scraping {subject_name}...")
                
                # Try both papers and revision paths
                for path_type, path in subject_paths.items():
                    logger.info(f"  📚 Checking {path_type}: {path}")
                    subject_url = self.base_url + path
                    
                    # Get exam boards from this subject page
                    exam_board_links = self._get_exam_board_links(subject_name, subject_url)
                    
                    if exam_board_links:
                        # For each exam board, get topic links
                        for exam_board, exam_board_url in exam_board_links.items():
                            logger.info(f"    🏛️  Exam Board: {exam_board}")
                            topic_links = self._get_topic_links(subject_name, exam_board, exam_board_url)
                            
                            if topic_links:
                                # For each topic, get PDF links
                                for topic_name, topic_url in topic_links.items():
                                    logger.info(f"      📖 Topic: {topic_name}")
                                    pdf_links = self._get_pdf_links(subject_name, exam_board, topic_name, topic_url)
                                    
                                    if pdf_links:
                                        self.found_pdfs.extend(pdf_links)
                                        logger.info(f"        ✅ Found {len(pdf_links)} PDFs")
                
                time.sleep(2)  # Be respectful between subjects
                
            except Exception as e:
                logger.error(f"Error scraping {subject_name}: {e}")
        
        return self.found_pdfs

    def _get_exam_board_links(self, subject_name, subject_url):
        """Get links to exam board pages from subject page"""
        try:
            response = self.session.get(subject_url, timeout=30)
            if response.status_code != 200:
                return {}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for exam board links (AQA, Edexcel, OCR, etc.)
            exam_board_patterns = ['aqa', 'edexcel', 'ocr', 'caie', 'wjec', 'eduqas']
            exam_board_links = {}
            
            for pattern in exam_board_patterns:
                links = soup.find_all('a', href=re.compile(pattern, re.IGNORECASE))
                for link in links:
                    href = link.get('href', '')
                    if href and ('past-papers' in href or 'revision' in href):
                        exam_board_name = pattern.upper()
                        exam_board_url = urljoin(subject_url, href)
                        exam_board_links[exam_board_name] = exam_board_url
                        logger.info(f"        🔍 Found exam board: {exam_board_name} -> {exam_board_url}")
                        break
            
            return exam_board_links
            
        except Exception as e:
            logger.error(f"Error getting exam board links for {subject_name}: {e}")
            return {}

    def _get_topic_links(self, subject_name, exam_board, exam_board_url):
        """Get links to topic pages from exam board page"""
        try:
            response = self.session.get(exam_board_url, timeout=30)
            if response.status_code != 200:
                return {}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for topic links (Cell Biology, Organic Chemistry, etc.)
            topic_links = {}
            
            # Look for links that might be topics
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                link_text = link.get_text(strip=True)
                
                # Check if this looks like a topic link
                if (href and 
                    ('revision' in href or 'topic' in href or 'cell' in href.lower() or 'organic' in href.lower()) and
                    len(link_text) < 100 and  # Topic names are usually reasonable length
                    not any(word in link_text.lower() for word in ['home', 'menu', 'contact', 'shop', 'tutor'])):
                    
                    topic_url = urljoin(exam_board_url, href)
                    topic_links[link_text] = topic_url
                    logger.info(f"          🔍 Found topic: {link_text} -> {topic_url}")
            
            return topic_links
            
        except Exception as e:
            logger.error(f"Error getting topic links for {exam_board}: {e}")
            return {}

    def _get_pdf_links(self, subject_name, exam_board, topic_name, topic_url):
        """Get PDF links from topic page"""
        try:
            response = self.session.get(topic_url, timeout=30)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            pdf_links = []
            
            # Look for PDF links in the /pdf-pages/?pdf= structure (new structure)
            pdf_page_links = soup.find_all('a', href=re.compile(r'pdf-pages\?pdf=', re.IGNORECASE))
            
            for link in pdf_page_links:
                href = link.get('href', '')
                if href:
                    # Extract the actual PDF URL from the query parameter
                    actual_pdf_url = self._extract_actual_pdf_url(href)
                    
                    if actual_pdf_url:
                        pdf_title = link.get_text(strip=True) or 'Untitled'
                        
                        pdf_info = {
                            'url': actual_pdf_url,
                            'title': pdf_title,
                            'subject': subject_name,
                            'exam_board': exam_board,
                            'topic': topic_name,
                            'source': 'PMT',
                            'level': 'A-Level/GCSE',
                            'structure': 'pdf_pages_wrapper'
                        }
                        
                        pdf_links.append(pdf_info)
                        logger.info(f"            📄 Found PDF (wrapper): {pdf_title}")
            
            # Also look for direct PDF links that might exist
            direct_pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
            
            for link in direct_pdf_links:
                href = link.get('href', '')
                if href:
                    pdf_url = href if href.startswith('http') else urljoin(topic_url, href)
                    pdf_title = link.get_text(strip=True) or 'Untitled'
                    
                    pdf_info = {
                        'url': pdf_url,
                        'title': pdf_title,
                        'subject': subject_name,
                        'exam_board': exam_board,
                        'topic': topic_name,
                        'source': 'PMT',
                        'level': 'A-Level/GCSE',
                        'structure': 'direct_pdf'
                    }
                    
                    pdf_links.append(pdf_info)
                    logger.info(f"            📄 Found PDF (direct): {pdf_title}")
            
            return pdf_links
            
        except Exception as e:
            logger.error(f"Error getting PDF links for {topic_name}: {e}")
            return []

    def _extract_actual_pdf_url(self, pdf_page_url):
        """Extract the actual PDF URL from a /pdf-pages/?pdf= URL"""
        try:
            # Extract the PDF parameter
            match = re.search(r'pdf=([^&]+)', pdf_page_url)
            if match:
                encoded_pdf_url = match.group(1)
                actual_pdf_url = unquote(encoded_pdf_url)
                logger.debug(f"            🔗 Extracted PDF URL: {actual_pdf_url}")
                return actual_pdf_url
            return None
        except Exception as e:
            logger.debug(f"Error extracting PDF URL: {e}")
            return None

    def save_found_pdfs(self, filename="comprehensive_pdf_scraper_results.json"):
        """Save all found PDFs"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        data = {
            'real_content': self.found_pdfs,
            'summary': {
                'total_pdfs': len(self.found_pdfs),
                'subjects': list(set(pdf['subject'] for pdf in self.found_pdfs)),
                'exam_boards': list(set(pdf['exam_board'] for pdf in self.found_pdfs)),
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
        exam_boards = {}
        structures = {}
        
        for pdf in self.found_pdfs:
            subject = pdf['subject']
            exam_board = pdf.get('exam_board', 'Unknown')
            structure = pdf.get('structure', 'unknown')
            
            subjects[subject] = subjects.get(subject, 0) + 1
            exam_boards[exam_board] = exam_boards.get(exam_board, 0) + 1
            structures[structure] = structures.get(structure, 0) + 1
        
        logger.info(f"\n📊 Comprehensive PDF Scraper Results:")
        logger.info(f"  📄 Total PDFs Found: {len(self.found_pdfs)}")
        logger.info(f"  📚 Subjects: {subjects}")
        logger.info(f"  🏛️  Exam Boards: {exam_boards}")
        logger.info(f"  🏗️  Structures: {structures}")
        
        if self.found_pdfs:
            logger.info(f"\n🎯 Next Steps:")
            logger.info(f"1. Run the existing PDF scraper on these new PDFs")
            logger.info(f"2. Extract Q&A pairs from Chemistry, Biology, English, etc.")
            logger.info(f"3. Expand training dataset beyond Math/Physics")
            logger.info(f"4. We should now have THOUSANDS of PDFs across all subjects!")

def main():
    logger.info("🎯 NOTICAL AI Pipeline - Comprehensive PDF Scraper")
    logger.info("=" * 70)
    logger.info("🚀 Getting ALL subjects, ALL exam boards, ALL topics, ALL PDFs!")
    logger.info("🚀 Following the EXACT structure: Subject → Exam Board → Topic → PDFs")
    logger.info("🚀 Handling both direct /download/ AND /pdf-pages/?pdf= wrapper URLs")
    logger.info("=" * 70)
    
    scraper = ComprehensivePDFScraper()
    found_pdfs = scraper.scrape_all_subjects()
    
    if found_pdfs:
        scraper.save_found_pdfs()
        logger.info(f"\n🎯 Comprehensive PDF Scraping Complete!")
        logger.info(f"  📄 Total PDFs Found: {len(found_pdfs)}")
        logger.info(f"\n🎯 Now run the existing scraper to extract Q&A pairs!")
        logger.info(f"🎯 We should have MASSIVE amounts of training data now!")
    else:
        logger.error("❌ No PDFs were found")
    
    return found_pdfs

if __name__ == "__main__":
    main()




