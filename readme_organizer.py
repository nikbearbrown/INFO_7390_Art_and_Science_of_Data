#!/usr/bin/env python3
"""
Repository MD Files Organizer for INFO 7390
Organizes Markdown/README files from the MD folder into a structured hierarchy
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MDOrganizer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.md_folder = self.repo_path / "MD"
        self.moved_files = []
        self.skipped_files = []
        self.errors = []
        
        # Verify MD folder exists
        if not self.md_folder.exists():
            raise ValueError(f"MD folder not found at: {self.md_folder}")
        
        # Define folder structure based on course content
        self.folder_patterns = {
            'Part_0_AI_Fluency': {
                'patterns': [
                    r'.*botspeak.*',
                    r'.*nine[_\s]?pillars.*',
                    r'.*ai[_\s]?fluency.*',
                    r'.*computational[_\s]?skepticism.*',
                    r'.*philosophical[_\s]?foundations.*',
                    r'.*week[_\s]?[1-3].*',
                    r'.*part[_\s]?0.*'
                ],
                'subfolders': [
                    'Week_1_Botspeak',
                    'Week_2_Philosophical_Foundations',
                    'Week_3_Practical_Applications'
                ]
            },
            'Part_I_Understanding_Data': {
                'patterns': [
                    r'.*data[_\s]?preprocessing.*',
                    r'.*data[_\s]?validation.*',
                    r'.*data[_\s]?analysis.*',
                    r'.*visual[_\s]?design.*',
                    r'.*understanding[_\s]?data.*',
                    r'.*week[_\s]?[4-6].*',
                    r'.*part[_\s]?i[_\s]?.*',
                    r'.*part[_\s]?1.*'
                ],
                'subfolders': [
                    'Week_4_Data_Preprocessing',
                    'Week_5_Data_Analysis',
                    'Week_6_Visual_Design'
                ]
            },
            'Part_II_Generative_AI': {
                'patterns': [
                    r'.*generative[_\s]?ai.*',
                    r'.*synthetic[_\s]?data.*',
                    r'.*week[_\s]?[7-9].*',
                    r'.*part[_\s]?ii.*',
                    r'.*part[_\s]?2.*'
                ],
                'subfolders': [
                    'Week_7_Understanding_GenAI',
                    'Week_8_Building_GenAI',
                    'Week_9_Synthetic_Data'
                ]
            },
            'Part_III_Causal_Inference': {
                'patterns': [
                    r'.*causal[_\s]?inference.*',
                    r'.*causality.*',
                    r'.*dag[s]?.*',
                    r'.*visual[_\s]?techniques.*causal.*',
                    r'.*week[_\s]?1[0-2].*',
                    r'.*part[_\s]?iii.*',
                    r'.*part[_\s]?3.*'
                ],
                'subfolders': [
                    'Week_10_Causal_Basics',
                    'Week_11_Visual_Causal',
                    'Week_12_Advanced_Causal'
                ]
            },
            'Week_13_Final_Projects': {
                'patterns': [
                    r'.*final[_\s]?project.*',
                    r'.*week[_\s]?13.*',
                    r'.*presentation.*'
                ],
                'subfolders': []
            },
            'Course_Materials': {
                'patterns': [
                    r'.*syllabus.*',
                    r'.*course[_\s]?outline.*',
                    r'.*readme.*',
                    r'.*index.*',
                    r'.*introduction.*',
                    r'.*overview.*'
                ],
                'subfolders': [
                    'Syllabus',
                    'Resources',
                    'Templates'
                ]
            },
            'Assignments': {
                'patterns': [
                    r'.*assignment.*',
                    r'.*homework.*',
                    r'.*hw[_\s]?\d+.*',
                    r'.*exercise.*',
                    r'.*lab[_\s]?\d+.*'
                ],
                'subfolders': [
                    'Weekly_Assignments',
                    'Projects',
                    'Solutions'
                ]
            },
            'Resources': {
                'patterns': [
                    r'.*resource.*',
                    r'.*reference.*',
                    r'.*guide.*',
                    r'.*tutorial.*',
                    r'.*documentation.*',
                    r'.*notes.*'
                ],
                'subfolders': [
                    'Guides',
                    'References',
                    'External_Resources'
                ]
            }
        }
    
    def create_folder_structure(self):
        """Create all necessary folders in the MD directory"""
        for folder_name, folder_info in self.folder_patterns.items():
            # Create main category folder
            main_folder = self.md_folder / folder_name
            main_folder.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created/verified main folder: {main_folder}")
            
            # Create subfolders
            for subfolder in folder_info.get('subfolders', []):
                subfolder_path = main_folder / subfolder
                subfolder_path.mkdir(parents=True, exist_ok=True)
                logging.debug(f"  Created subfolder: {subfolder}")
    
    def find_matching_folder(self, filename: str) -> Tuple[str, str, str]:
        """
        Find the appropriate folder for an MD file based on its name
        Returns: (main_folder, subfolder, matched_pattern) or (None, None, None)
        """
        filename_lower = filename.lower()
        
        for folder_name, folder_info in self.folder_patterns.items():
            for pattern in folder_info['patterns']:
                if re.match(pattern, filename_lower):
                    # Try to determine subfolder based on filename
                    subfolder = self.determine_subfolder(filename_lower, folder_name, folder_info.get('subfolders', []))
                    return folder_name, subfolder, pattern
        
        return None, None, None
    
    def determine_subfolder(self, filename: str, folder_name: str, subfolders: List[str]) -> str:
        """Determine the best subfolder match based on filename and folder category"""
        if not subfolders:
            return None
            
        filename_lower = filename.lower()
        
        # Week-based matching
        week_match = re.search(r'week[_\s]?(\d{1,2})', filename_lower)
        if week_match:
            week_num = int(week_match.group(1))
            
            # Part 0: Weeks 1-3
            if folder_name == 'Part_0_AI_Fluency':
                if week_num == 1:
                    return 'Week_1_Botspeak'
                elif week_num == 2:
                    return 'Week_2_Philosophical_Foundations'
                elif week_num == 3:
                    return 'Week_3_Practical_Applications'
            
            # Part I: Weeks 4-6
            elif folder_name == 'Part_I_Understanding_Data':
                if week_num == 4:
                    return 'Week_4_Data_Preprocessing'
                elif week_num == 5:
                    return 'Week_5_Data_Analysis'
                elif week_num == 6:
                    return 'Week_6_Visual_Design'
            
            # Part II: Weeks 7-9
            elif folder_name == 'Part_II_Generative_AI':
                if week_num == 7:
                    return 'Week_7_Understanding_GenAI'
                elif week_num == 8:
                    return 'Week_8_Building_GenAI'
                elif week_num == 9:
                    return 'Week_9_Synthetic_Data'
            
            # Part III: Weeks 10-12
            elif folder_name == 'Part_III_Causal_Inference':
                if week_num == 10:
                    return 'Week_10_Causal_Basics'
                elif week_num == 11:
                    return 'Week_11_Visual_Causal'
                elif week_num == 12:
                    return 'Week_12_Advanced_Causal'
        
        # Content-based matching for other categories
        if folder_name == 'Course_Materials':
            if 'syllabus' in filename_lower:
                return 'Syllabus'
            elif any(word in filename_lower for word in ['resource', 'template']):
                return 'Resources'
            else:
                return 'Templates'
        
        elif folder_name == 'Assignments':
            if 'solution' in filename_lower:
                return 'Solutions'
            elif 'project' in filename_lower:
                return 'Projects'
            else:
                return 'Weekly_Assignments'
        
        elif folder_name == 'Resources':
            if 'guide' in filename_lower:
                return 'Guides'
            elif 'reference' in filename_lower:
                return 'References'
            else:
                return 'External_Resources'
        
        # Try to match subfolder names
        for subfolder in subfolders:
            subfolder_pattern = subfolder.lower().replace('_', r'[_\s]?')
            if re.search(subfolder_pattern, filename_lower):
                return subfolder
        
        # Return first subfolder as default
        return subfolders[0] if subfolders else None
    
    def organize_md_files(self, dry_run: bool = True):
        """
        Organize MD files into appropriate folders
        
        Args:
            dry_run: If True, only show what would be moved without actually moving
        """
        # Create folder structure
        if not dry_run:
            self.create_folder_structure()
        
        # Find all .md files in the MD folder (only at root level)
        md_files = [f for f in self.md_folder.iterdir() 
                    if f.is_file() and f.suffix.lower() in ['.md', '.markdown']]
        
        logging.info(f"Found {len(md_files)} markdown files in {self.md_folder}")
        
        for md_file in md_files:
            # Find matching folder
            main_folder, subfolder, pattern = self.find_matching_folder(md_file.name)
            
            if main_folder:
                # Construct destination path
                if subfolder:
                    dest_folder = self.md_folder / main_folder / subfolder
                else:
                    dest_folder = self.md_folder / main_folder
                
                dest_path = dest_folder / md_file.name
                
                # Handle existing files
                if dest_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    stem = md_file.stem
                    suffix = md_file.suffix
                    dest_path = dest_folder / f"{stem}_{timestamp}{suffix}"
                
                if dry_run:
                    relative_path = dest_path.relative_to(self.md_folder)
                    logging.info(f"[DRY RUN] Would move: {md_file.name}")
                    logging.info(f"          To: {relative_path}")
                    logging.info(f"          Pattern: {pattern}")
                    if subfolder:
                        logging.info(f"          Subfolder: {subfolder}")
                else:
                    try:
                        shutil.move(str(md_file), str(dest_path))
                        logging.info(f"Moved: {md_file.name} -> {dest_path.relative_to(self.md_folder)}")
                        self.moved_files.append((md_file, dest_path))
                    except Exception as e:
                        logging.error(f"Error moving {md_file}: {str(e)}")
                        self.errors.append((md_file, str(e)))
            else:
                # Put unmatched files in Resources
                logging.warning(f"No matching folder for: {md_file.name} - moving to Resources")
                main_folder = 'Resources'
                subfolder = 'External_Resources'
                
                dest_folder = self.md_folder / main_folder / subfolder
                dest_path = dest_folder / md_file.name
                
                if dest_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    stem = md_file.stem
                    suffix = md_file.suffix
                    dest_path = dest_folder / f"{stem}_{timestamp}{suffix}"
                
                if dry_run:
                    relative_path = dest_path.relative_to(self.md_folder)
                    logging.info(f"[DRY RUN] Would move: {md_file.name}")
                    logging.info(f"          To: {relative_path}")
                    logging.info(f"          Pattern: (default to Resources)")
                else:
                    try:
                        shutil.move(str(md_file), str(dest_path))
                        logging.info(f"Moved: {md_file.name} -> {dest_path.relative_to(self.md_folder)}")
                        self.moved_files.append((md_file, dest_path))
                    except Exception as e:
                        logging.error(f"Error moving {md_file}: {str(e)}")
                        self.errors.append((md_file, str(e)))
    
    def generate_report(self):
        """Generate a summary report of the organization process"""
        report = []
        report.append("=" * 70)
        report.append("INFO 7390 MD FILES ORGANIZATION REPORT")
        report.append("=" * 70)
        report.append(f"\nRepository: {self.repo_path}")
        report.append(f"MD folder: {self.md_folder}")
        report.append(f"\nTotal files processed: {len(self.moved_files) + len(self.skipped_files)}")
        report.append(f"Files moved: {len(self.moved_files)}")
        report.append(f"Files skipped: {len(self.skipped_files)}")
        report.append(f"Errors encountered: {len(self.errors)}")
        
        if self.moved_files:
            report.append("\n\nMOVED FILES:")
            report.append("-" * 50)
            for src, dst in self.moved_files:
                rel_path = dst.relative_to(self.md_folder)
                report.append(f"  {src.name} -> {rel_path}")
        
        if self.skipped_files:
            report.append("\n\nSKIPPED FILES:")
            report.append("-" * 50)
            for md_file in self.skipped_files:
                report.append(f"  {md_file.name}")
        
        if self.errors:
            report.append("\n\nERRORS:")
            report.append("-" * 50)
            for md_file, error in self.errors:
                report.append(f"  {md_file.name}: {error}")
        
        # Add folder structure summary
        report.append("\n\nFOLDER STRUCTURE CREATED:")
        report.append("-" * 50)
        for folder_name in sorted(self.folder_patterns.keys()):
            report.append(f"  {folder_name}/")
            for subfolder in self.folder_patterns[folder_name].get('subfolders', [])[:5]:
                report.append(f"    └── {subfolder}/")
            if len(self.folder_patterns[folder_name].get('subfolders', [])) > 5:
                report.append(f"    └── ... and {len(self.folder_patterns[folder_name]['subfolders']) - 5} more")
        
        report_text = "\n".join(report)
        
        # Save report to file
        report_path = self.repo_path / "md_organization_report.txt"
        with open(report_path, "w") as f:
            f.write(report_text)
        
        logging.info(f"\nReport saved to: {report_path}")
        return report_text


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Organize Markdown files in INFO 7390 repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would be moved
  python md_organizer.py /path/to/repo --dry-run
  
  # Actually organize the MD files
  python md_organizer.py /path/to/repo
  
  # With verbose output
  python md_organizer.py /path/to/repo --dry-run --verbose
        """
    )
    parser.add_argument("repo_path", help="Path to the repository root (contains MD folder)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be moved without actually moving files")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create organizer instance
        organizer = MDOrganizer(args.repo_path)
        
        # Run organization
        logging.info(f"Starting MD file organization")
        logging.info(f"Repository path: {args.repo_path}")
        logging.info(f"Mode: {'DRY RUN' if args.dry_run else 'ACTUAL MOVE'}")
        logging.info("-" * 50)
        
        organizer.organize_md_files(dry_run=args.dry_run)
        
        # Generate report
        report = organizer.generate_report()
        print("\n" + report)
        
        if args.dry_run:
            print("\n⚠️  This was a DRY RUN. No files were actually moved.")
            print("Remove --dry-run flag to perform actual organization.")
            
    except ValueError as e:
        logging.error(f"Error: {e}")
        print(f"\n❌ Error: {e}")
        print("Make sure the repository contains an 'MD' folder.")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())