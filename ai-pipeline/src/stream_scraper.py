#!/usr/bin/env python3
"""
NOTICAL AI Pipeline - Streaming PDF Scraper
==========================================
Stream PDFs and extract Q&A pairs without downloading
"""

import requests
import json
import logging
from pathlib import Path
import time
import random
import re
import PyPDF2
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensivePDFScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.extracted_qa_pairs = []

    def load_pdf_links(self, filename="all_subjects_pdf_links.json"):
        """Load PDF links from our comprehensive scraping"""
        try:
            data_file = Path("data") / filename
            if data_file.exists():
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    # Get all content and filter for PDFs
                    all_content = data.get('real_content', [])
                    
                    # Filter for PDF links only
                    pdf_links = []
                    for item in all_content:
                        url = item.get('url', '')
                        if url and url.endswith('.pdf'):
                            pdf_links.append(item)
                    
                    logger.info(f"Found {len(pdf_links)} PDF links from {len(all_content)} total items")
                    return pdf_links
            else:
                # If file doesn't exist, create sample links for new subjects
                logger.info("Creating sample PDF links for new subjects...")
                return self._create_sample_subject_links()
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return self._create_sample_subject_links()
    
    def _create_sample_subject_links(self):
        """Create sample PDF links for new subjects"""
        accessible_subjects = {
            'Chemistry': '/a-level-chemistry/',
            'Biology': '/a-level-biology/',
            'English': '/a-level-english/',
            'Economics': '/a-level-economics/',
            'History': '/a-level-history/',
            'Geography': '/a-level-geography/'
        }
        
        all_pdf_links = []
        
        for subject_name, url_path in accessible_subjects.items():
            logger.info(f"🔍 Creating links for {subject_name}")
            
            # Create sample structure for each subject
            subject_pdfs = [
                {
                    'url': f'https://www.physicsandmathstutor.com{url_path}past-papers/topic-1.pdf',
                    'title': f'{subject_name} Topic 1 QP',
                    'subject': subject_name,
                    'topic': 'Topic 1',
                    'source': 'PMT',
                    'level': 'A-Level'
                },
                {
                    'url': f'https://www.physicsandmathstutor.com{url_path}past-papers/topic-1-ms.pdf',
                    'title': f'{subject_name} Topic 1 MS',
                    'subject': subject_name,
                    'topic': 'Topic 1',
                    'source': 'PMT',
                    'level': 'A-Level'
                }
            ]
            
            all_pdf_links.extend(subject_pdfs)
            logger.info(f"  ✅ {subject_name}: {len(subject_pdfs)} PDFs created")
        
        return all_pdf_links

    def stream_and_extract_pdf(self, pdf_info):
        """Stream PDF and extract ALL content"""
        try:
            url = pdf_info.get('url')
            title = pdf_info.get('title')
            logger.info(f"📄 Streaming: {title}")
            
            response = self.session.get(url, stream=True, timeout=30)
            if response.status_code != 200:
                return []
            
            pdf_content = response.content
            extracted_text = self._extract_text_from_pdf_content(pdf_content, title)
            
            if extracted_text and len(extracted_text) > 100:
                qa_pairs = self._create_comprehensive_qa_pairs(extracted_text, pdf_info)
                return qa_pairs
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error processing {pdf_info.get('title', 'Unknown')}: {e}")
            return []

    def _extract_text_from_pdf_content(self, pdf_content, title):
        """Extract ALL text from PDF content"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            logger.info(f"  📖 PDF has {len(pdf_reader.pages)} pages")
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- PAGE {page_num + 1} ---\n{page_text}\n"
            
            return text.strip()
            
        except Exception as e:
            logger.debug(f"PyPDF2 extraction failed for {title}: {e}")
            return ""

    def _create_comprehensive_qa_pairs(self, text, pdf_info):
        """Create COMPREHENSIVE Q&A pairs from ALL content"""
        qa_pairs = []
        try:
            title = pdf_info.get('title', 'Unknown')
            subject = pdf_info.get('subject', 'Unknown')
            topic = pdf_info.get('topic', 'Unknown')
            
            # Split text into sections (by pages, paragraphs, etc.)
            sections = self._split_text_into_sections(text)
            
            logger.info(f"  📝 Processing {len(sections)} sections from {title}")
            
            for section_num, section in enumerate(sections):
                if len(section.strip()) < 20:  # Skip very short sections
                    continue
                
                # Extract ALL possible Q&A from this section
                section_qa_pairs = self._extract_all_qa_from_section(section, pdf_info, section_num)
                qa_pairs.extend(section_qa_pairs)
            
            logger.info(f"  ✅ Generated {len(qa_pairs)} Q&A pairs from {title}")
            
        except Exception as e:
            logger.error(f"Error creating Q&A from {pdf_info.get('title', 'Unknown')}: {e}")
        
        return qa_pairs

    def _split_text_into_sections(self, text):
        """Split text into meaningful sections for processing"""
        sections = []
        
        # Split by page markers first
        page_splits = text.split('--- PAGE')
        
        for page_split in page_splits:
            if not page_split.strip():
                continue
                
            # Further split by paragraphs within each page
            paragraphs = [p.strip() for p in page_split.split('\n\n') if len(p.strip()) > 20]
            
            for paragraph in paragraphs:
                # Split long paragraphs into smaller chunks
                if len(paragraph) > 500:
                    # Split by sentences for very long paragraphs
                    sentences = re.split(r'[.!?]+', paragraph)
                    for sentence in sentences:
                        if len(sentence.strip()) > 30:
                            sections.append(sentence.strip())
                else:
                    sections.append(paragraph)
        
        return sections

    def _extract_all_qa_from_section(self, section, pdf_info, section_num):
        """Extract ALL possible Q&A from a section"""
        qa_pairs = []
        title = pdf_info.get('title', 'Unknown')
        subject = pdf_info.get('subject', 'Unknown')
        topic = pdf_info.get('topic', 'Unknown')
        
        clean_text = section.strip()
        if len(clean_text) < 20:
            return qa_pairs
        
        # Extract multiple Q&A types from the same section
        qa_types = []
        
        # Type 1: Definition/Concept (look for "is", "are", "refers to", "defined as")
        if any(word in clean_text.lower() for word in ['is', 'are', 'refers to', 'defined as', 'means', 'consists of']):
            qa_types.append(('definition', f"What is the definition of {topic} in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # Type 2: Key Points/Explanation (look for "key", "important", "essential")
        if any(word in clean_text.lower() for word in ['key', 'important', 'essential', 'critical', 'main', 'primary']):
            qa_types.append(('key_points', f"What are the key points about {topic} in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # Type 3: Process/Steps (look for "step", "process", "method")
        if any(word in clean_text.lower() for word in ['step', 'process', 'method', 'procedure', 'approach', 'technique']):
            qa_types.append(('process', f"What is the process for {topic} in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # Type 4: Formula/Calculation (look for "formula", "equation", "calculate")
        if any(word in clean_text.lower() for word in ['formula', 'equation', 'calculate', 'solve', 'compute', 'evaluate']):
            qa_types.append(('formula', f"What is the formula for {topic} in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # Type 5: Comparison/Analysis (look for "compare", "difference", "similar")
        if any(word in clean_text.lower() for word in ['compare', 'difference', 'similar', 'versus', 'contrast', 'analyze']):
            qa_types.append(('comparison', f"How does {topic} compare in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # Type 6: Application/Example (look for "example", "application", "use")
        if any(word in clean_text.lower() for word in ['example', 'application', 'use', 'apply', 'instance', 'case']):
            qa_types.append(('application', f"What is an example of {topic} in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # Type 7: Properties/Characteristics (look for "properties", "characteristics", "features")
        if any(word in clean_text.lower() for word in ['properties', 'characteristics', 'features', 'attributes', 'qualities']):
            qa_types.append(('properties', f"What are the properties of {topic} in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # Type 8: Causes/Effects (look for "cause", "effect", "result", "impact")
        if any(word in clean_text.lower() for word in ['cause', 'effect', 'result', 'impact', 'consequence', 'outcome']):
            qa_types.append(('causes_effects', f"What are the causes and effects of {topic} in {subject}?", 
                           f"{clean_text[:300]}..."))
        
        # If no specific type detected, create multiple general questions
        if not qa_types:
            qa_types.extend([
                ('concept', f"Explain the concept of {topic} in {subject}.", f"{clean_text[:300]}..."),
                ('understanding', f"How do you understand {topic} in {subject}?", f"{clean_text[:300]}..."),
                ('overview', f"Give an overview of {topic} in {subject}.", f"{clean_text[:300]}...")
            ])
        
        # Create Q&A pairs for ALL detected types
        for qa_type, question, answer in qa_types:
            qa_pairs.append({
                'question': question,
                'answer': answer,
                'qa_type': qa_type,
                'difficulty': self._determine_difficulty(clean_text),
                'subject': subject,
                'level': pdf_info.get('level', 'Unknown'),
                'topic': topic,
                'source': pdf_info.get('source', 'Unknown'),
                'content_type': 'pdf_extraction',
                'url': pdf_info.get('url', ''),
                'section_num': section_num,
                'text_length': len(clean_text),
                'extracted_date': time.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return qa_pairs

    def _determine_difficulty(self, text):
        """Determine difficulty based on text complexity"""
        word_count = len(text.split())
        if word_count < 30:
            return 'easy'
        elif word_count < 80:
            return 'medium'
        elif word_count < 150:
            return 'hard'
        else:
            return 'extreme'

    def process_all_pdfs(self):
        """Process ALL PDFs and extract EVERYTHING"""
        logger.info(f"🚀 Starting COMPREHENSIVE PDF processing...")
        
        # Load PDF links
        pdf_links = self.load_pdf_links()
        if not pdf_links:
            logger.error("No PDF links found to process")
            return []
        
        logger.info(f"📚 Found {len(pdf_links)} PDF links to process")
        
        all_qa_pairs = []
        
        for i, pdf_info in enumerate(pdf_links):
            if i % 10 == 0:
                logger.info(f"📊 Progress: {i}/{len(pdf_links)}")
            
            # Process this PDF
            qa_pairs = self.stream_and_extract_pdf(pdf_info)
            
            if qa_pairs:
                all_qa_pairs.extend(qa_pairs)
                logger.info(f"  ✅ Extracted {len(qa_pairs)} Q&A pairs from {pdf_info['title']}")
            
            # Be respectful with delays
            time.sleep(random.uniform(0.5, 1))
        
        self.extracted_qa_pairs = all_qa_pairs
        
        logger.info(f"🎉 COMPREHENSIVE Processing complete!")
        logger.info(f"  ❓ Total Q&A pairs extracted: {len(all_qa_pairs)}")
        
        return all_qa_pairs

    def save_qa_data(self, filename="comprehensive_qa_pairs.json"):
        """Save extracted Q&A pairs"""
        if not self.extracted_qa_pairs:
            logger.warning("No Q&A pairs to save")
            return
        
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        content_file = data_dir / filename
        with open(content_file, 'w') as f:
            json.dump({
                'extracted_qa_pairs': self.extracted_qa_pairs,
                'extraction_summary': self._get_summary()
            }, f, indent=2)
        
        logger.info(f"💾 Q&A data saved to: {content_file}")
        self._show_summary()
        
        return content_file

    def _get_summary(self):
        """Get comprehensive summary of extracted data"""
        summary = {
            'total_qa_pairs': len(self.extracted_qa_pairs),
            'subjects': {},
            'qa_types': {},
            'difficulties': {},
            'pdfs_processed': len(set(qa.get('url', '') for qa in self.extracted_qa_pairs))
        }
        
        for qa in self.extracted_qa_pairs:
            summary['subjects'][qa.get('subject', 'Unknown')] = summary['subjects'].get(qa.get('subject', 'Unknown'), 0) + 1
            summary['qa_types'][qa.get('qa_type', 'Unknown')] = summary['qa_types'].get(qa.get('qa_type', 'Unknown'), 0) + 1
            summary['difficulties'][qa.get('difficulty', 'Unknown')] = summary['difficulties'].get(qa.get('difficulty', 'Unknown'), 0) + 1
        
        return summary

    def _show_summary(self):
        """Display comprehensive summary"""
        summary = self._get_summary()
        logger.info(f"\n📊 COMPREHENSIVE Q&A Extraction Summary:")
        logger.info(f"  ❓ Total Q&A Pairs: {summary['total_qa_pairs']}")
        logger.info(f"  📚 PDFs Processed: {summary['pdfs_processed']}")
        logger.info(f"  📖 Subjects: {summary['subjects']}")
        logger.info(f"  🏷️  Q&A Types: {summary['qa_types']}")
        logger.info(f"  📈 Difficulties: {summary['difficulties']}")

def main():
    logger.info("🎯 NOTICAL AI Pipeline - COMPREHENSIVE PDF Scraper")
    logger.info("=" * 60)
    logger.info("🚀 This will extract EVERY question and answer from ALL PDFs!")
    logger.info("=" * 60)
    
    scraper = ComprehensivePDFScraper()
    qa_pairs = scraper.process_all_pdfs()
    
    if qa_pairs:
        scraper.save_qa_data()
        logger.info(f"\n🎯 COMPREHENSIVE PDF Processing Summary:")
        logger.info(f"  ❓ Total Q&A Pairs Extracted: {len(qa_pairs)}")
        logger.info(f"  💾 Data saved to: data/comprehensive_qa_pairs.json")
        logger.info(f"\n🎯 Next Steps:")
        logger.info(f"1. Review comprehensive Q&A quality")
        logger.info(f"2. Expand to more subjects")
        logger.info(f"3. Create training dataset")
        logger.info(f"4. Train ML model")
    else:
        logger.error("❌ No Q&A pairs were extracted successfully")
    
    return qa_pairs

if __name__ == "__main__":
    main()
