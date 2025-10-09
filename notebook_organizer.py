#!/usr/bin/env python3
"""
Repository Notebook Organizer for INFO 7390
Organizes Python notebooks (.ipynb) from a flat Notebooks folder into a structured hierarchy
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

class NotebookOrganizer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.notebooks_folder = self.repo_path / "Notebooks"
        self.moved_files = []
        self.skipped_files = []
        self.errors = []
        
        # Verify Notebooks folder exists
        if not self.notebooks_folder.exists():
            raise ValueError(f"Notebooks folder not found at: {self.notebooks_folder}")
        
        # Define folder structure and naming patterns
        self.folder_patterns = {
            'Botspeak_Framework': {
                'patterns': [
                    r'.*nine[_\s]?pillars.*',
                    r'.*strategic[_\s]?delegation.*',
                    r'.*effective[_\s]?communication.*',
                    r'.*critical[_\s]?evaluation.*',
                    r'.*technical[_\s]?understanding.*',
                    r'.*ethical[_\s]?reasoning.*',
                    r'.*stochastic[_\s]?reasoning.*',
                    r'.*learning[_\s]?by[_\s]?doing.*',
                    r'.*rapid[_\s]?prototyping.*',
                    r'.*theoretical[_\s]?foundation.*',
                    r'.*botspeak.*'
                ],
                'subfolders': [
                    'Nine_Pillars',
                    'Strategic_Delegation',
                    'Effective_Communication',
                    'Critical_Evaluation',
                    'Technical_Understanding',
                    'Ethical_Reasoning',
                    'Stochastic_Reasoning',
                    'Learning_by_Doing',
                    'Rapid_Prototyping',
                    'Theoretical_Foundation'
                ]
            },
            'Computational_Skepticism': {
                'patterns': [
                    r'.*computational[_\s]?skepticism.*',
                    r'.*philosophical[_\s]?foundations.*',
                    r'.*systematic[_\s]?doubt.*',
                    r'.*black[_\s]?box[_\s]?problem.*'
                ],
                'subfolders': [
                    'Philosophical_Foundations',
                    'Practical_Applications',
                    'Systematic_Doubt',
                    'Black_Box_Problem'
                ]
            },
            'Data_Understanding_and_Preprocessing': {
                'patterns': [
                    r'.*data[_\s]?types.*',
                    r'.*data[_\s]?quality.*',
                    r'.*missing[_\s]?data.*',
                    r'.*imputation.*',
                    r'.*data[_\s]?cleaning.*',
                    r'.*feature[_\s]?selection.*',
                    r'.*normalization.*',
                    r'.*data[_\s]?encoding.*',
                    r'.*imbalanced[_\s]?data.*',
                    r'.*preprocessing.*',
                    r'.*data[_\s]?understanding.*',
                    r'.*understanding[_\s]?data.*',
                    r'.*eda.*',
                    r'.*exploratory[_\s]?data.*',
                    r'.*data[_\s]?exploration.*',
                    r'.*data[_\s]?analysis.*',
                    r'.*feature[_\s]?engineering.*',
                    r'.*feature[_\s]?scaling.*',
                    r'.*dimensionality[_\s]?reduction.*',
                    r'.*pca.*',
                    r'.*data[_\s]?sampling.*',
                    r'.*sampling[_\s]?technique.*',
                    r'.*cross[_\s]?validation.*',
                    r'.*data[_\s]?size.*',
                    r'.*pre[_\s]?processing.*',
                    r'.*time[_\s]?series[_\s]?data.*',
                    r'.*audio[_\s]?data.*',
                    r'.*text[_\s]?data.*',
                    r'.*stock[_\s]?price.*understanding.*'  # Specific pattern for Stock_Price_Understanding_Data
                ],
                'subfolders': [
                    'Data_Types',
                    'Data_Quality_Assessment',
                    'Missing_Data_Handling',
                    'Imputation_Techniques',
                    'Data_Cleaning',
                    'Feature_Selection',
                    'Normalization_Methods',
                    'Data_Encoding',
                    'Imbalanced_Data'
                ]
            },
            'Data_Visualization': {
                'patterns': [
                    r'.*visual[_\s]?design.*',
                    r'.*comparison[_\s]?technique.*',
                    r'.*distribution[_\s]?visual.*',
                    r'.*relationship[_\s]?visual.*',
                    r'.*hierarchical[_\s]?visual.*',
                    r'.*spatiotemporal.*',
                    r'.*interactive[_\s]?visual.*',
                    r'.*data[_\s]?viz.*',
                    r'.*visualization.*',
                    r'.*plotting.*',
                    r'.*graphs?.*'
                ],
                'subfolders': [
                    'Visual_Design_Principles',
                    'Comparison_Techniques',
                    'Distribution_Visualization',
                    'Relationship_Visualization',
                    'Hierarchical_Visualization',
                    'Spatiotemporal_Visualization',
                    'Interactive_Visualization'
                ]
            },
            'Generative_AI': {
                'patterns': [
                    r'.*generative[_\s]?ai.*',
                    r'.*synthetic[_\s]?data.*',
                    r'.*system[_\s]?building.*',
                    r'.*evaluation[_\s]?methods.*',
                    r'.*bias[_\s]?detection.*',
                    r'.*gen[_\s]?ai.*',
                    r'.*llm.*',
                    r'.*gpt.*',
                    r'.*transformer.*',
                    r'.*gan.*',
                    r'.*generative.*',
                    r'.*text[_\s]?generation.*',
                    r'.*image[_\s]?generation.*',
                    r'.*diffusion[_\s]?model.*',
                    r'.*bert.*',
                    r'.*text[_\s]?summarization.*',
                    r'.*synthetic[_\s]?.*data.*',
                    r'.*fake[_\s]?face.*',
                    r'.*deep[_\s]?convolutional.*',
                    r'.*adversarial[_\s]?network.*',
                    r'.*prompt[_\s]?engineering.*',
                    r'.*rag.*',
                    r'.*embeddings.*',
                    r'.*multimodal.*',
                    r'.*text[_\s]?to[_\s]?image.*',  # For Text_to_Image_Generation
                    r'.*image[_\s]?to[_\s]?text.*'
                ],
                'subfolders': [
                    'Fundamentals',
                    'System_Building',
                    'Synthetic_Data',
                    'Evaluation_Methods',
                    'Bias_Detection'
                ]
            },
            'Causal_Inference': {
                'patterns': [
                    r'.*causal[_\s]?inference.*',
                    r'.*dag[s]?.*',
                    r'.*observational[_\s]?stud.*',
                    r'.*causal.*',
                    r'.*counterfactual.*',
                    r'.*causality.*',
                    r'.*casuality.*',  # Common misspelling
                    r'.*confounding[_\s]?variable.*',
                    r'.*crash[_\s]?course.*causal.*',
                    r'.*crash[_\s]?course.*casuality.*',
                    r'.*causation.*correlation.*',
                    r'.*\d{6}_\d{8}_.*confounding.*',  # Pattern for student ID files with confounding
                    r'.*part\d+.*crash.*course.*',  # Part2_Crash Course pattern
                    r'.*part\d+.*casuality.*'  # Part2 with casuality
                ],
                'subfolders': [
                    'Fundamentals',
                    'Visual_Techniques',
                    'DAGs',
                    'Advanced_Analysis',
                    'Observational_Studies'
                ]
            },
            'Statistical_Methods': {
                'patterns': [
                    r'.*hypothesis[_\s]?test.*',
                    r'.*probability[_\s]?distribution.*',
                    r'.*normality[_\s]?test.*',
                    r'.*feature[_\s]?importance.*',
                    r'.*time[_\s]?series.*',
                    r'.*clustering.*',
                    r'.*statistical.*',
                    r'.*statistics.*',
                    r'.*anova.*',
                    r'.*regression.*'
                ],
                'subfolders': [
                    'Hypothesis_Testing',
                    'Probability_Distributions',
                    'Normality_Testing',
                    'Feature_Importance',
                    'Time_Series_Analysis',
                    'Clustering'
                ]
            },
            'Weekly_Assignments': {
                'patterns': [
                    r'.*week[_\s]?\d{1,2}.*',
                    r'.*assignment[_\s]?\d{1,2}.*',
                    r'.*hw[_\s]?\d{1,2}.*',
                    r'.*homework[_\s]?\d{1,2}.*',
                    r'.*lab[_\s]?\d{1,2}.*'
                ],
                'subfolders': [f'Week_{i:02d}' for i in range(1, 14)]
            },
            'Projects': {
                'patterns': [
                    r'.*final[_\s]?project.*',
                    r'.*presentation.*',
                    r'.*project[_\s]?proposal.*',
                    r'.*project[_\s]?\d+.*',
                    r'.*capstone.*',
                    r'.*group[_\s]?\d+.*',
                    r'.*team[_\s]?\d+.*',
                    r'.*model[_\s]?development.*',
                    r'.*evaluation[_\s]?and[_\s]?deployment.*',
                    r'.*fifa.*',
                    r'.*titanic.*',
                    r'.*stock[_\s]?price.*',
                    r'.*bitcoin.*',
                    r'.*heart[_\s]?rate.*',
                    r'.*heart[_\s]?disease.*',
                    r'.*churn[_\s]?prediction.*',
                    r'.*recommender[_\s]?system.*',
                    r'.*netflix.*',
                    r'.*hbo.*',
                    r'.*spotify.*',
                    r'.*chess.*',
                    r'.*boston[_\s]?house.*',
                    r'.*apple.*',
                    r'.*tesla.*',
                    r'.*mental[_\s]?health.*',
                    r'.*smoking[_\s]?cessation.*',
                    r'.*air[_\s]?pollution.*',
                    r'.*product[_\s]?recommendation.*',
                    r'.*job[_\s]?posting.*',
                    r'.*bone[_\s]?fracture.*',
                    r'.*digit.*',
                    r'.*face.*',
                    r'.*worked[_\s]?exp.*',
                    r'.*worked[_\s]?example.*',
                    r'^\d{9}.*'  # Files starting with student ID
                ],
                'subfolders': [
                    'Final_Projects',
                    'Presentations'
                ]
            },
            'GIGO_Reference': {
                'patterns': [
                    r'.*gigo.*',
                    r'.*textbook[_\s]?example.*',
                    r'.*case[_\s]?stud.*',
                    r'.*practice[_\s]?problem.*',
                    r'.*reference[_\s]?material.*'
                ],
                'subfolders': [
                    'Textbook_Examples',
                    'Case_Studies',
                    'Practice_Problems',
                    'Additional_Resources'
                ]
            },
            'Misc': {
                'patterns': [
                    r'.*template.*',
                    r'.*dataset.*',
                    r'.*utilit.*',
                    r'.*reference.*',
                    r'.*misc.*',
                    r'.*test.*',
                    r'.*demo.*',
                    r'.*example.*',
                    r'.*scratch.*',
                    r'.*draft.*',
                    r'.*untitled.*',
                    r'.*todo.*',
                    r'.*main\.ipynb',
                    r'.*v-\d+.*',
                    r'.*checkpoint.*',
                    r'.*twitter.*',
                    r'.*updated[_\s]?labs.*',
                    r'.*shap.*',
                    r'.*pdf[_\s]?bot.*',
                    r'.*part\d+.*',
                    r'.*notes.*'
                ],
                'subfolders': [
                    'Templates',
                    'Datasets',
                    'Utilities',
                    'Reference_Materials'
                ]
            }
        }
    
    def create_folder_structure(self):
        """Create all necessary folders in the Notebooks directory"""
        for folder_name, folder_info in self.folder_patterns.items():
            # Create main category folder
            main_folder = self.notebooks_folder / folder_name
            main_folder.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created/verified main folder: {main_folder}")
            
            # Create subfolders
            for subfolder in folder_info.get('subfolders', []):
                subfolder_path = main_folder / subfolder
                subfolder_path.mkdir(parents=True, exist_ok=True)
                logging.debug(f"  Created subfolder: {subfolder}")
    
    def find_matching_folder(self, filename: str) -> Tuple[str, str, str]:
        """
        Find the appropriate folder for a notebook based on its name
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
        
        # Special handling for week assignments
        if folder_name == 'Weekly_Assignments':
            week_match = re.search(r'week[_\s]?(\d{1,2})', filename_lower)
            if week_match:
                week_num = int(week_match.group(1))
                week_folder = f'Week_{week_num:02d}'
                if week_folder in subfolders:
                    return week_folder
            # Default to Week_01 if no week number found
            return 'Week_01'
        
        # Special handling for Causal Inference
        if folder_name == 'Causal_Inference':
            if 'crash' in filename_lower and 'course' in filename_lower:
                return 'Fundamentals'
            elif 'dag' in filename_lower:
                return 'DAGs'
            elif 'confound' in filename_lower:
                return 'Advanced_Analysis'
            elif 'observational' in filename_lower:
                return 'Observational_Studies'
            else:
                return 'Fundamentals'
        
        # Special handling for Data Understanding
        if folder_name == 'Data_Understanding_and_Preprocessing':
            if 'eda' in filename_lower or 'exploratory' in filename_lower:
                return 'Data_Quality_Assessment'
            elif 'clean' in filename_lower:
                return 'Data_Cleaning'
            elif 'missing' in filename_lower:
                return 'Missing_Data_Handling'
            elif 'imputation' in filename_lower:
                return 'Imputation_Techniques'
            elif 'feature' in filename_lower and 'select' in filename_lower:
                return 'Feature_Selection'
            elif 'encoding' in filename_lower or 'encode' in filename_lower:
                return 'Data_Encoding'
            elif 'scaling' in filename_lower or 'normalization' in filename_lower:
                return 'Normalization_Methods'
            elif 'type' in filename_lower:
                return 'Data_Types'
            elif 'imbalanced' in filename_lower:
                return 'Imbalanced_Data'
            else:
                return 'Data_Quality_Assessment'
        
        # Special handling for Generative AI
        if folder_name == 'Generative_AI':
            if 'gan' in filename_lower:
                return 'Fundamentals'
            elif 'synthetic' in filename_lower:
                return 'Synthetic_Data'
            elif 'evaluation' in filename_lower or 'eval' in filename_lower:
                return 'Evaluation_Methods'
            elif 'bias' in filename_lower:
                return 'Bias_Detection'
            else:
                return 'System_Building'
        
        # Try to match subfolder names for other categories
        for subfolder in subfolders:
            subfolder_pattern = subfolder.lower().replace('_', r'[_\s]?')
            if re.search(subfolder_pattern, filename_lower):
                return subfolder
        
        # Return first subfolder as default
        return subfolders[0] if subfolders else None
    
    def organize_notebooks(self, dry_run: bool = True):
        """
        Organize notebooks into appropriate folders
        
        Args:
            dry_run: If True, only show what would be moved without actually moving
        """
        # Create folder structure
        if not dry_run:
            self.create_folder_structure()
        
        # Find all .ipynb files in the Notebooks folder (only at root level)
        notebooks = [f for f in self.notebooks_folder.iterdir() 
                    if f.is_file() and f.suffix.lower() == '.ipynb']
        
        logging.info(f"Found {len(notebooks)} notebooks in {self.notebooks_folder}")
        
        for notebook in notebooks:
            # Find matching folder - try each pattern category
            main_folder, subfolder, pattern = self.find_matching_folder(notebook.name)
            
            # If still no match, try more aggressive matching
            if not main_folder:
                # Check for any student ID pattern (6-10 digits at start)
                if re.match(r'^\d{6,10}[_\s]', notebook.name):
                    # Look for keywords in the rest of the filename
                    if any(keyword in notebook.name.lower() for keyword in ['causal', 'casuality', 'confound']):
                        main_folder = 'Causal_Inference'
                        subfolder = 'Fundamentals'
                        pattern = 'student_id_causal'
                    elif any(keyword in notebook.name.lower() for keyword in ['gan', 'generative', 'synthetic']):
                        main_folder = 'Generative_AI'
                        subfolder = 'Fundamentals'
                        pattern = 'student_id_generative'
                    elif any(keyword in notebook.name.lower() for keyword in ['understanding', 'eda', 'data']):
                        main_folder = 'Data_Understanding_and_Preprocessing'
                        subfolder = 'Data_Quality_Assessment'
                        pattern = 'student_id_data'
                    else:
                        main_folder = 'Projects'
                        subfolder = 'Final_Projects'
                        pattern = 'student_id_project'
            
            if main_folder:
                # Construct destination path
                if subfolder:
                    dest_folder = self.notebooks_folder / main_folder / subfolder
                else:
                    dest_folder = self.notebooks_folder / main_folder
                
                dest_path = dest_folder / notebook.name
                
                # Handle existing files
                if dest_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    stem = notebook.stem
                    suffix = notebook.suffix
                    dest_path = dest_folder / f"{stem}_{timestamp}{suffix}"
                
                if dry_run:
                    relative_path = dest_path.relative_to(self.notebooks_folder)
                    logging.info(f"[DRY RUN] Would move: {notebook.name}")
                    logging.info(f"          To: {relative_path}")
                    logging.info(f"          Pattern: {pattern}")
                    if subfolder:
                        logging.info(f"          Subfolder: {subfolder}")
                else:
                    try:
                        shutil.move(str(notebook), str(dest_path))
                        logging.info(f"Moved: {notebook.name} -> {dest_path.relative_to(self.notebooks_folder)}")
                        self.moved_files.append((notebook, dest_path))
                    except Exception as e:
                        logging.error(f"Error moving {notebook}: {str(e)}")
                        self.errors.append((notebook, str(e)))
            else:
                # Final catch-all: put remaining files in Misc
                logging.warning(f"No matching folder for: {notebook.name} - moving to Misc")
                main_folder = 'Misc'
                subfolder = 'Reference_Materials'
                pattern = 'catch_all'
                
                # Construct destination path for Misc
                dest_folder = self.notebooks_folder / main_folder / subfolder
                dest_path = dest_folder / notebook.name
                
                # Handle existing files
                if dest_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    stem = notebook.stem
                    suffix = notebook.suffix
                    dest_path = dest_folder / f"{stem}_{timestamp}{suffix}"
                
                if dry_run:
                    relative_path = dest_path.relative_to(self.notebooks_folder)
                    logging.info(f"[DRY RUN] Would move: {notebook.name}")
                    logging.info(f"          To: {relative_path}")
                    logging.info(f"          Pattern: {pattern} (catch-all)")
                else:
                    try:
                        shutil.move(str(notebook), str(dest_path))
                        logging.info(f"Moved: {notebook.name} -> {dest_path.relative_to(self.notebooks_folder)}")
                        self.moved_files.append((notebook, dest_path))
                    except Exception as e:
                        logging.error(f"Error moving {notebook}: {str(e)}")
                        self.errors.append((notebook, str(e)))
    
    def generate_report(self):
        """Generate a summary report of the organization process"""
        report = []
        report.append("=" * 70)
        report.append("INFO 7390 NOTEBOOK ORGANIZATION REPORT")
        report.append("=" * 70)
        report.append(f"\nRepository: {self.repo_path}")
        report.append(f"Notebooks folder: {self.notebooks_folder}")
        report.append(f"\nTotal notebooks processed: {len(self.moved_files) + len(self.skipped_files)}")
        report.append(f"Notebooks moved: {len(self.moved_files)}")
        report.append(f"Notebooks skipped: {len(self.skipped_files)}")
        report.append(f"Errors encountered: {len(self.errors)}")
        
        if self.moved_files:
            report.append("\n\nMOVED FILES:")
            report.append("-" * 50)
            for src, dst in self.moved_files:
                rel_path = dst.relative_to(self.notebooks_folder)
                report.append(f"  {src.name} -> {rel_path}")
        
        if self.skipped_files:
            report.append("\n\nSKIPPED FILES (no pattern match):")
            report.append("-" * 50)
            for notebook in self.skipped_files:
                report.append(f"  {notebook.name}")
            report.append("\nConsider adding patterns for these files or moving them manually.")
        
        if self.errors:
            report.append("\n\nERRORS:")
            report.append("-" * 50)
            for notebook, error in self.errors:
                report.append(f"  {notebook.name}: {error}")
        
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
        report_path = self.repo_path / "notebook_organization_report.txt"
        with open(report_path, "w") as f:
            f.write(report_text)
        
        logging.info(f"\nReport saved to: {report_path}")
        return report_text


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Organize Python notebooks in INFO 7390 repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would be moved
  python notebook_organizer.py /path/to/repo --dry-run
  
  # Actually organize the notebooks
  python notebook_organizer.py /path/to/repo
  
  # With verbose output
  python notebook_organizer.py /path/to/repo --dry-run --verbose
        """
    )
    parser.add_argument("repo_path", help="Path to the repository root (contains Notebooks folder)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be moved without actually moving files")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create organizer instance
        organizer = NotebookOrganizer(args.repo_path)
        
        # Run organization
        logging.info(f"Starting notebook organization")
        logging.info(f"Repository path: {args.repo_path}")
        logging.info(f"Mode: {'DRY RUN' if args.dry_run else 'ACTUAL MOVE'}")
        logging.info("-" * 50)
        
        organizer.organize_notebooks(dry_run=args.dry_run)
        
        # Generate report
        report = organizer.generate_report()
        print("\n" + report)
        
        if args.dry_run:
            print("\n⚠️  This was a DRY RUN. No files were actually moved.")
            print("Remove --dry-run flag to perform actual organization.")
            
    except ValueError as e:
        logging.error(f"Error: {e}")
        print(f"\n❌ Error: {e}")
        print("Make sure the repository contains a 'Notebooks' folder.")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())