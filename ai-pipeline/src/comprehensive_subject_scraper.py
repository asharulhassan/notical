#!/usr/bin/env python3
"""
NOTICAL AI Pipeline - Comprehensive Subject Scraper
==================================================
Find and scrape ALL available subjects on PMT
"""

import requests
import json
import logging
from pathlib import Path
import time
import random
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveSubjectScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = "https://www.physicsandmathstutor.com"
        self.discovered_subjects = {}
        self.all_pdf_links = []

    def discover_all_subjects(self):
        """Discover ALL available subjects on PMT"""
        logger.info("🔍 Discovering ALL available subjects on PMT...")
        
        try:
            # Start with the main page
            response = self.session.get(self.base_url, timeout=30)
            if response.status_code != 200:
                logger.error("Failed to access main page")
                return {}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for subject navigation links
            subject_links = []
            
            # Common patterns for subject links
            patterns = [
                'a[href*="/a-level/"]',
                'a[href*="/gcse/"]',
                'a[href*="/igcse/"]',
                'a[href*="/ib/"]',
                'a[href*="/alevel/"]',
                'a[href*="/subjects/"]'
            ]
            
            for pattern in patterns:
                links = soup.select(pattern)
                for link in links:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    if href and text and len(text) > 2:
                        subject_links.append({
                            'url': urljoin(self.base_url, href),
                            'text': text,
                            'type': 'subject_link'
                        })
            
            # Also look for specific subject mentions
            subject_keywords = [
                'Mathematics', 'Maths', 'Math', 'Physics', 'Chemistry', 'Biology',
                'English', 'Literature', 'Language', 'Business', 'Economics',
                'Accounting', 'History', 'Geography', 'Psychology', 'Sociology',
                'Computer Science', 'ICT', 'Art', 'Music', 'Drama', 'PE',
                'Religious Studies', 'Philosophy', 'Politics', 'Law', 'Medicine'
            ]
            
            for keyword in subject_keywords:
                keyword_links = soup.find_all('a', string=re.compile(keyword, re.IGNORECASE))
                for link in keyword_links:
                    href = link.get('href', '')
                    if href:
                        subject_links.append({
                            'url': urljoin(self.base_url, href),
                            'text': keyword,
                            'type': 'keyword_match'
                        })
            
            logger.info(f"Found {len(subject_links)} potential subject links")
            
            # Explore each subject link to find actual subject pages
            for link_info in subject_links:
                self._explore_subject_link(link_info)
                time.sleep(random.uniform(1, 2))
            
            return self.discovered_subjects
            
        except Exception as e:
            logger.error(f"Error discovering subjects: {e}")
            return {}

    def _explore_subject_link(self, link_info):
        """Explore a subject link to find actual subject content"""
        try:
            url = link_info['url']
            text = link_info['text']
            
            logger.info(f"🔍 Exploring: {text} -> {url}")
            
            response = self.session.get(url, timeout=30)
            if response.status_code != 200:
                return
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for PDF links and educational content
            pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
            
            if pdf_links:
                logger.info(f"  📚 Found {len(pdf_links)} PDFs in {text}")
                
                subject_data = {
                    'name': text,
                    'url': url,
                    'pdf_links': [],
                    'subject_type': self._determine_subject_type(text)
                }
                
                for pdf_link in pdf_links:
                    pdf_url = urljoin(url, pdf_link.get('href', ''))
                    pdf_title = pdf_link.get_text(strip=True) or pdf_link.get('title', '') or 'Untitled'
                    
                    subject_data['pdf_links'].append({
                        'url': pdf_url,
                        'title': pdf_title,
                        'subject': text,
                        'source': 'PMT',
                        'level': self._determine_level(url),
                        'topic': self._extract_topic(pdf_title)
                    })
                
                self.discovered_subjects[text] = subject_data
                self.all_pdf_links.extend(subject_data['pdf_links'])
            
            # Look for sub-subjects or topics
            sub_links = soup.find_all('a', href=re.compile(r'/(a-level|gcse|igcse|ib)/', re.IGNORECASE))
            for sub_link in sub_links[:10]:  # Limit to avoid infinite loops
                sub_href = sub_link.get('href', '')
                sub_text = sub_link.get_text(strip=True)
                if sub_href and sub_text and len(sub_text) > 2:
                    sub_url = urljoin(url, sub_href)
                    self._explore_subject_link({
                        'url': sub_url,
                        'text': f"{text} - {sub_text}",
                        'type': 'sub_subject'
                    })
                    time.sleep(random.uniform(0.5, 1))
                    
        except Exception as e:
            logger.debug(f"Error exploring {link_info.get('text', 'Unknown')}: {e}")

    def _determine_subject_type(self, subject_name):
        """Determine the type of subject"""
        subject_lower = subject_name.lower()
        
        if any(word in subject_lower for word in ['math', 'algebra', 'calculus', 'geometry']):
            return 'Mathematics'
        elif any(word in subject_lower for word in ['physics', 'mechanics', 'electricity', 'waves']):
            return 'Physics'
        elif any(word in subject_lower for word in ['chemistry', 'organic', 'inorganic', 'physical']):
            return 'Chemistry'
        elif any(word in subject_lower for word in ['biology', 'cell', 'genetics', 'ecology']):
            return 'Biology'
        elif any(word in subject_lower for word in ['english', 'literature', 'language']):
            return 'English'
        elif any(word in subject_lower for word in ['business', 'economics', 'accounting', 'finance']):
            return 'Business'
        elif any(word in subject_lower for word in ['history', 'geography', 'politics']):
            return 'Humanities'
        elif any(word in subject_lower for word in ['computer', 'ict', 'programming']):
            return 'Computer Science'
        else:
            return 'Other'

    def _determine_level(self, url):
        """Determine the educational level from URL"""
        url_lower = url.lower()
        if 'a-level' in url_lower or 'alevel' in url_lower:
            return 'A-Level'
        elif 'gcse' in url_lower:
            return 'GCSE'
        elif 'igcse' in url_lower:
            return 'IGCSE'
        elif 'ib' in url_lower:
            return 'IB'
        else:
            return 'Unknown'

    def _extract_topic(self, title):
        """Extract topic from PDF title"""
        # Remove common suffixes
        title = re.sub(r'\s*(QP|MS|MA|Question Paper|Mark Scheme|Model Answer)\s*$', '', title, flags=re.IGNORECASE)
        return title.strip()

    def save_discovered_subjects(self, filename="all_pmt_subjects.json"):
        """Save all discovered subjects and PDF links"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        data = {
            'discovered_subjects': self.discovered_subjects,
            'all_pdf_links': self.all_pdf_links,
            'summary': self._get_summary()
        }
        
        content_file = data_dir / filename
        with open(content_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"💾 All subjects data saved to: {content_file}")
        self._show_summary()
        
        return content_file

    def _get_summary(self):
        """Get summary of discovered subjects"""
        summary = {
            'total_subjects': len(self.discovered_subjects),
            'total_pdfs': len(self.all_pdf_links),
            'subjects_by_type': {},
            'levels': {},
            'top_subjects': []
        }
        
        for subject_name, subject_data in self.discovered_subjects.items():
            subject_type = subject_data.get('subject_type', 'Unknown')
            summary['subjects_by_type'][subject_type] = summary['subjects_by_type'].get(subject_type, 0) + 1
            
            pdf_count = len(subject_data.get('pdf_links', []))
            summary['top_subjects'].append({
                'name': subject_name,
                'pdf_count': pdf_count,
                'type': subject_type
            })
        
        # Sort by PDF count
        summary['top_subjects'].sort(key=lambda x: x['pdf_count'], reverse=True)
        
        # Count levels
        for pdf_info in self.all_pdf_links:
            level = pdf_info.get('level', 'Unknown')
            summary['levels'][level] = summary['levels'].get(level, 0) + 1
        
        return summary

    def _show_summary(self):
        """Display summary of discovered subjects"""
        summary = self._get_summary()
        logger.info(f"\n📊 COMPREHENSIVE Subject Discovery Summary:")
        logger.info(f"  📚 Total Subjects Found: {summary['total_subjects']}")
        logger.info(f"  📄 Total PDFs Found: {summary['total_pdfs']}")
        logger.info(f"  🏷️  Subjects by Type: {summary['subjects_by_type']}")
        logger.info(f"  📈 Educational Levels: {summary['levels']}")
        logger.info(f"\n🏆 Top Subjects by PDF Count:")
        for i, subject in enumerate(summary['top_subjects'][:10]):
            logger.info(f"  {i+1}. {subject['name']}: {subject['pdf_count']} PDFs ({subject['type']})")

def main():
    logger.info("🎯 NOTICAL AI Pipeline - Comprehensive Subject Scraper")
    logger.info("=" * 60)
    logger.info("🚀 Discovering ALL available subjects on PMT!")
    logger.info("=" * 60)
    
    scraper = ComprehensiveSubjectScraper()
    discovered_subjects = scraper.discover_all_subjects()
    
    if discovered_subjects:
        scraper.save_discovered_subjects()
        logger.info(f"\n🎯 Subject Discovery Complete!")
        logger.info(f"  📚 Subjects Found: {len(discovered_subjects)}")
        logger.info(f"  📄 Total PDFs: {len(scraper.all_pdf_links)}")
        logger.info(f"\n🎯 Next Steps:")
        logger.info(f"1. Review discovered subjects")
        logger.info(f"2. Run comprehensive PDF scraper on new subjects")
        logger.info(f"3. Expand training dataset beyond Math/Physics")
    else:
        logger.error("❌ No subjects were discovered")
    
    return discovered_subjects

if __name__ == "__main__":
    main()

