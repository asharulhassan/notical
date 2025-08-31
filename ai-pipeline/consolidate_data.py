#!/usr/bin/env python3
"""
Data Consolidation Script
Consolidates all redundant data files into one clean training dataset
"""

import json
import os
from pathlib import Path

def load_json_file(file_path):
    """Load and return JSON data from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def clean_qa_pair(qa_pair):
    """Clean and standardize a QA pair"""
    # Remove redundant fields and clean up the data
    cleaned = {
        "question": qa_pair.get("question", "").strip(),
        "answer": qa_pair.get("answer", "").strip(),
        "subject": qa_pair.get("subject", "").strip(),
        "topic": qa_pair.get("topic", "").strip(),
        "level": qa_pair.get("level", "").strip(),
        "difficulty": qa_pair.get("difficulty", "medium"),
        "qa_type": qa_pair.get("qa_type", "general")
    }
    
    # Remove empty or invalid entries
    if not cleaned["question"] or not cleaned["answer"]:
        return None
    
    # Clean up the answer text (remove excessive whitespace, headers, etc.)
    answer = cleaned["answer"]
    # Remove common PDF artifacts
    answer = answer.replace("*P", "").replace("*", "")
    answer = answer.replace("Question Scheme Marks AOs", "")
    answer = answer.replace("DO NOT WRITE IN THIS AREA", "")
    
    # Clean up excessive whitespace
    answer = " ".join(answer.split())
    
    if len(answer) < 10:  # Skip very short answers
        return None
    
    cleaned["answer"] = answer
    return cleaned

def consolidate_data():
    """Main consolidation function"""
    data_dir = Path("data")
    
    # Load all data files
    all_qa_pairs = []
    
    # 1. Load extracted_qa_pairs.json
    print("Loading extracted_qa_pairs.json...")
    extracted_data = load_json_file(data_dir / "extracted_qa_pairs.json")
    if extracted_data and "extracted_qa_pairs" in extracted_data:
        all_qa_pairs.extend(extracted_data["extracted_qa_pairs"])
        print(f"Loaded {len(extracted_data['extracted_qa_pairs'])} pairs from extracted_qa_pairs.json")
    
    # 2. Load comprehensive_qa_pairs.json
    print("Loading comprehensive_qa_pairs.json...")
    comprehensive_data = load_json_file(data_dir / "comprehensive_qa_pairs.json")
    if comprehensive_data and "comprehensive_qa_pairs" in comprehensive_data:
        all_qa_pairs.extend(comprehensive_data["comprehensive_qa_pairs"])
        print(f"Loaded {len(comprehensive_data['comprehensive_qa_pairs'])} pairs from comprehensive_qa_pairs.json")
    
    # 3. Load real_pmt_content.json if it has QA pairs
    print("Loading real_pmt_content.json...")
    real_pmt_data = load_json_file(data_dir / "real_pmt_content.json")
    if real_pmt_data:
        # Check if it has QA structure
        if isinstance(real_pmt_data, list):
            for item in real_pmt_data:
                if isinstance(item, dict) and "question" in item and "answer" in item:
                    all_qa_pairs.append(item)
        elif isinstance(real_pmt_data, dict):
            # Look for QA pairs in nested structure
            for key, value in real_pmt_data.items():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and "question" in item and "answer" in item:
                            all_qa_pairs.append(item)
        print(f"Loaded additional pairs from real_pmt_content.json")
    
    print(f"Total QA pairs loaded: {len(all_qa_pairs)}")
    
    # Clean and deduplicate the data
    print("Cleaning and deduplicating data...")
    cleaned_pairs = []
    seen_questions = set()
    
    for qa_pair in all_qa_pairs:
        cleaned = clean_qa_pair(qa_pair)
        if cleaned:
            # Create a simple hash for deduplication
            question_hash = cleaned["question"].lower().strip()
            if question_hash not in seen_questions:
                seen_questions.add(question_hash)
                cleaned_pairs.append(cleaned)
    
    print(f"After cleaning and deduplication: {len(cleaned_pairs)} pairs")
    
    # Create the consolidated dataset
    consolidated_data = {
        "metadata": {
            "total_qa_pairs": len(cleaned_pairs),
            "subjects": list(set(pair["subject"] for pair in cleaned_pairs if pair["subject"])),
            "topics": list(set(pair["topic"] for pair in cleaned_pairs if pair["topic"])),
            "levels": list(set(pair["level"] for pair in cleaned_pairs if pair["level"])),
            "difficulties": list(set(pair["difficulty"] for pair in cleaned_pairs if pair["difficulty"])),
            "qa_types": list(set(pair["qa_type"] for pair in cleaned_pairs if pair["qa_type"])),
            "consolidation_date": "2025-08-27",
            "source_files": ["extracted_qa_pairs.json", "comprehensive_qa_pairs.json", "real_pmt_content.json"]
        },
        "training_data": cleaned_pairs
    }
    
    # Save consolidated data
    output_file = data_dir / "consolidated_training_data.json"
    print(f"Saving consolidated data to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
    
    print(f"Consolidated data saved successfully!")
    print(f"Output file size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
    
    # Print summary statistics
    print("\n=== SUMMARY STATISTICS ===")
    print(f"Total QA pairs: {len(cleaned_pairs)}")
    
    # Subject distribution
    subjects = {}
    for pair in cleaned_pairs:
        subject = pair.get("subject", "Unknown")
        subjects[subject] = subjects.get(subject, 0) + 1
    
    print(f"\nSubject distribution:")
    for subject, count in sorted(subjects.items(), key=lambda x: x[1], reverse=True):
        print(f"  {subject}: {count}")
    
    # Difficulty distribution
    difficulties = {}
    for pair in cleaned_pairs:
        diff = pair.get("difficulty", "medium")
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    print(f"\nDifficulty distribution:")
    for diff, count in sorted(difficulties.items(), key=lambda x: x[1], reverse=True):
        print(f"  {diff}: {count}")
    
    return output_file

def cleanup_redundant_files():
    """Remove redundant data files after consolidation"""
    data_dir = Path("data")
    
    files_to_remove = [
        "extracted_qa_pairs.json",
        "comprehensive_qa_pairs.json", 
        "comprehensive_pdf_scraper_results.json",
        "real_pmt_content.json",
        "simple_subject_finder_results.json"
    ]
    
    print("\n=== CLEANING UP REDUNDANT FILES ===")
    for filename in files_to_remove:
        file_path = data_dir / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Removed: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")
        else:
            print(f"File not found: {filename}")
    
    print("Cleanup completed!")

if __name__ == "__main__":
    print("=== DATA CONSOLIDATION SCRIPT ===")
    print("This script will consolidate all redundant data files into one clean training dataset.")
    print()
    
    # Consolidate the data
    output_file = consolidate_data()
    
    # Ask user if they want to clean up redundant files
    print("\n" + "="*50)
    response = input("Do you want to remove the redundant data files? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        cleanup_redundant_files()
        print(f"\n✅ Consolidation complete! All data is now in: {output_file}")
        print("You can now use this file for training your model.")
    else:
        print(f"\n✅ Consolidation complete! All data is now in: {output_file}")
        print("Redundant files were kept. You can manually remove them later.")

