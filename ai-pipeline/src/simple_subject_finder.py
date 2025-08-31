#!/usr/bin/env python3
"""
NOTICAL AI Pipeline - Simple Subject Finder
==========================================
Simple, direct approach to find subjects on PMT
"""

import requests
import json
import logging
from pathlib import Path
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleSubjectFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = "https://www.physicsandmathstutor.com"
        self.found_subjects = {}

    def find_main_subjects(self):
        """Find main subjects directly from PMT"""
        logger.info("🔍 Finding main subjects on PMT...")
        
        # Direct subject URLs we know exist
        known_subjects = {
            'Mathematics': '/a-level-maths/',
            'Physics': '/a-level-physics/',
            'Chemistry': '/a-level-chemistry/',
            'Biology': '/a-level-biology/',
            'English': '/a-level-english/',
            'Business': '/a-level-business/',
            'Economics': '/a-level-economics/',
            'Accounting': '/a-level-accounting/',
            'History': '/a-level-history/',
            'Geography': '/a-level-geography/',
            'Psychology': '/a-level-psychology/',
            'Computer Science': '/a-level-computer-science/',
            'ICT': '/a-level-ict/',
            'Art': '/a-level-art/',
            'Music': '/a-level-music/',
            'Drama': '/a-level-drama/',
            'PE': '/a-level-physical-education/',
            'Religious Studies': '/a-level-religious-studies/',
            'Philosophy': '/a-level-philosophy/',
            'Politics': '/a-level-politics/',
            'Law': '/a-level-law/',
            'Medicine': '/a-level-medicine/'
        }
        
        logger.info(f"Checking {len(known_subjects)} known subject URLs...")
        
        for subject_name, url_path in known_subjects.items():
            try:
                full_url = self.base_url + url_path
                logger.info(f"🔍 Checking: {subject_name} -> {full_url}")
                
                response = self.session.get(full_url, timeout=30)
                if response.status_code == 200:
                    # Count PDF links on this page
                    pdf_count = len(re.findall(r'\.pdf', response.text))
                    logger.info(f"  ✅ {subject_name}: {pdf_count} PDFs found")
                    
                    self.found_subjects[subject_name] = {
                        'url': full_url,
                        'pdf_count': pdf_count,
                        'status': 'accessible'
                    }
                else:
                    logger.info(f"  ❌ {subject_name}: HTTP {response.status_code}")
                    self.found_subjects[subject_name] = {
                        'url': full_url,
                        'pdf_count': 0,
                        'status': f'HTTP_{response.status_code}'
                    }
                
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                logger.error(f"Error checking {subject_name}: {e}")
                self.found_subjects[subject_name] = {
                    'url': full_url,
                    'pdf_count': 0,
                    'status': f'Error: {str(e)}'
                }
        
        return self.found_subjects

    def save_results(self, filename="simple_subject_finder_results.json"):
        """Save the results"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        data = {
            'found_subjects': self.found_subjects,
            'summary': self._get_summary()
        }
        
        content_file = data_dir / filename
        with open(content_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"💾 Results saved to: {content_file}")
        self._show_summary()
        
        return content_file

    def _get_summary(self):
        """Get summary of found subjects"""
        accessible = [s for s in self.found_subjects.values() if s['status'] == 'accessible']
        total_pdfs = sum(s['pdf_count'] for s in accessible)
        
        return {
            'total_subjects': len(self.found_subjects),
            'accessible_subjects': len(accessible),
            'total_pdfs_found': total_pdfs,
            'accessible_subjects_list': [name for name, data in self.found_subjects.items() if data['status'] == 'accessible']
        }

    def _show_summary(self):
        """Show summary"""
        summary = self._get_summary()
        logger.info(f"\n📊 Simple Subject Finder Results:")
        logger.info(f"  📚 Total Subjects Checked: {summary['total_subjects']}")
        logger.info(f"  ✅ Accessible Subjects: {summary['accessible_subjects']}")
        logger.info(f"  📄 Total PDFs Found: {summary['total_pdfs_found']}")
        logger.info(f"\n✅ Accessible Subjects:")
        for subject in summary['accessible_subjects_list']:
            pdf_count = self.found_subjects[subject]['pdf_count']
            logger.info(f"  • {subject}: {pdf_count} PDFs")

def main():
    logger.info("🎯 NOTICAL AI Pipeline - Simple Subject Finder")
    logger.info("=" * 50)
    logger.info("🚀 Simple, direct subject discovery - no loops!")
    logger.info("=" * 50)
    
    finder = SimpleSubjectFinder()
    results = finder.find_main_subjects()
    
    if results:
        finder.save_results()
        logger.info(f"\n🎯 Subject Discovery Complete!")
        logger.info(f"  📚 Subjects Found: {len(results)}")
        logger.info(f"\n🎯 Next Steps:")
        logger.info(f"1. Review accessible subjects")
        logger.info(f"2. Run PDF scraper on new subjects")
        logger.info(f"3. Expand beyond Math/Physics")
    else:
        logger.error("❌ No subjects were found")
    
    return results

if __name__ == "__main__":
    main()

