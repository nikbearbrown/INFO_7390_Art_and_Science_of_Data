#!/usr/bin/env python3
"""
Simple Notebook Renamer - More robust version
"""

import os
import json
import re
from pathlib import Path
import shutil

def safe_read_notebook(filepath):
    """Safely read a notebook and extract title"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            notebook = json.loads(content)
        
        # Look through cells for a title
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                
                # Skip empty cells
                if not source.strip():
                    continue
                
                # Look for headers
                lines = source.split('\n')
                for line in lines:
                    # Check for markdown headers
                    if line.strip().startswith('#'):
                        title = line.strip().lstrip('#').strip()
                        # Skip generic titles
                        if title.lower() not in ['title', '', 'untitled', 'notebook']:
                            # Skip if it looks like just a name (First Last - Numbers)
                            if not re.match(r'^[A-Za-z]+\s+[A-Za-z]+\s*[-–]\s*\d+$', title):
                                return title
                
                # Look for specific keywords in the content
                if any(word in source.lower() for word in ['analysis', 'prediction', 'inference', 'causal']):
                    # Extract first meaningful sentence
                    sentences = re.split(r'[.!?]\s+', source)
                    for sent in sentences:
                        if len(sent) > 20 and any(word in sent.lower() for word in ['analysis', 'prediction', 'study', 'explore']):
                            return sent.strip()[:80]
        
        # Fallback: clean the original filename
        original = Path(filepath).stem
        # Remove common patterns
        cleaned = original
        cleaned = re.sub(r'fundamentals_\d+_', '', cleaned)
        cleaned = re.sub(r'^\d+_', '', cleaned)
        cleaned = re.sub(r'_\d{6,}', '', cleaned)  # Remove student IDs
        cleaned = cleaned.replace('_', ' ').strip()
        
        if len(cleaned) > 5:
            return cleaned.title()
        
        return "Notebook"
        
    except Exception as e:
        print(f"  Warning: Could not read {filepath}: {e}")
        # Return cleaned filename as fallback
        return Path(filepath).stem.replace('_', ' ').title()

def clean_for_filename(text):
    """Convert text to valid filename"""
    # Remove invalid characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace spaces with underscores
    text = re.sub(r'\s+', '_', text)
    # Remove multiple underscores
    text = re.sub(r'_+', '_', text)
    # Convert to lowercase
    text = text.lower()
    # Trim length
    if len(text) > 60:
        text = text[:60].rsplit('_', 1)[0]
    return text.strip('_')

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_rename.py <directory> [--execute]")
        sys.exit(1)
    
    directory = Path(sys.argv[1])
    execute = '--execute' in sys.argv
    
    if not directory.exists():
        print(f"Error: Directory {directory} does not exist")
        sys.exit(1)
    
    print(f"Scanning directory: {directory}")
    print(f"Mode: {'EXECUTE' if execute else 'DRY RUN'}")
    print("-" * 60)
    
    # Find all .ipynb files
    notebooks = list(directory.rglob('*.ipynb'))
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)]
    
    if not notebooks:
        print("No notebook files found!")
        return
    
    print(f"Found {len(notebooks)} notebooks")
    print()
    
    # Group by parent directory
    from collections import defaultdict
    by_dir = defaultdict(list)
    for nb in notebooks:
        by_dir[nb.parent].append(nb)
    
    # Process each directory
    changes = []
    for dir_path, files in sorted(by_dir.items()):
        print(f"\n📁 {dir_path.relative_to(directory.parent)}:")
        
        # Sort files for consistent numbering
        files.sort(key=lambda x: x.name.lower())
        
        for idx, filepath in enumerate(files, 1):
            # Extract title
            title = safe_read_notebook(filepath)
            
            # Create new filename
            clean_title = clean_for_filename(title)
            new_name = f"{idx:02d}_{clean_title}.ipynb"
            new_path = filepath.parent / new_name
            
            # Skip if already has correct name
            if filepath.name == new_name:
                print(f"  ✓ {filepath.name} (already correct)")
                continue
            
            # Handle duplicates
            if new_path.exists() and new_path != filepath:
                counter = 2
                while new_path.exists():
                    new_name = f"{idx:02d}_{clean_title}_{counter}.ipynb"
                    new_path = filepath.parent / new_name
                    counter += 1
            
            print(f"  • {filepath.name}")
            print(f"    → {new_name}")
            
            if execute:
                try:
                    filepath.rename(new_path)
                    changes.append((str(filepath), str(new_path)))
                except Exception as e:
                    print(f"    ERROR: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary: {len(changes)} files {'renamed' if execute else 'would be renamed'}")
    
    if not execute:
        print("\nTo execute these changes, run with --execute flag:")
        print(f"  python {sys.argv[0]} {sys.argv[1]} --execute")

if __name__ == '__main__':
    main()