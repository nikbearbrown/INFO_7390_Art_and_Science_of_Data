#!/usr/bin/env python3
"""
Undo Notebook Organization
Moves all .ipynb files from subdirectories back to the main Notebooks folder
"""

import os
import shutil
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def undo_organization(repo_path: str, dry_run: bool = True):
    """
    Move all notebooks from subdirectories back to the main Notebooks folder
    
    Args:
        repo_path: Path to the repository
        dry_run: If True, only show what would be moved
    """
    repo_path = Path(repo_path)
    notebooks_folder = repo_path / "Notbooks"
    
    if not notebooks_folder.exists():
        logging.error(f"Notebooks folder not found at: {notebooks_folder}")
        return
    
    moved_count = 0
    
    # Find all .ipynb files in subdirectories
    for notebook in notebooks_folder.rglob("*.ipynb"):
        # Skip if already in the main Notebooks folder
        if notebook.parent == notebooks_folder:
            continue
        
        # Destination in main Notebooks folder
        dest_path = notebooks_folder / notebook.name
        
        # Handle existing files
        if dest_path.exists():
            stem = notebook.stem
            suffix = notebook.suffix
            counter = 1
            while dest_path.exists():
                dest_path = notebooks_folder / f"{stem}_{counter}{suffix}"
                counter += 1
        
        relative_source = notebook.relative_to(notebooks_folder)
        
        if dry_run:
            logging.info(f"[DRY RUN] Would move: {relative_source} -> {notebook.name}")
        else:
            try:
                shutil.move(str(notebook), str(dest_path))
                logging.info(f"Moved: {relative_source} -> {notebook.name}")
                moved_count += 1
            except Exception as e:
                logging.error(f"Error moving {notebook}: {str(e)}")
    
    if dry_run:
        logging.info(f"\n[DRY RUN] Would move {moved_count} notebooks back to main folder")
    else:
        logging.info(f"\nMoved {moved_count} notebooks back to main folder")
        
        # Optional: Remove empty directories
        remove_empty_dirs(notebooks_folder)

def remove_empty_dirs(notebooks_folder: Path):
    """Remove empty directories after moving files"""
    removed_count = 0
    
    for dirpath, dirnames, filenames in os.walk(notebooks_folder, topdown=False):
        dirpath = Path(dirpath)
        
        # Skip the main Notebooks folder
        if dirpath == notebooks_folder:
            continue
        
        # Check if directory is empty (no files, and no subdirectories or all subdirectories are empty)
        if not any(dirpath.iterdir()):
            try:
                dirpath.rmdir()
                logging.info(f"Removed empty directory: {dirpath.relative_to(notebooks_folder)}")
                removed_count += 1
            except Exception as e:
                logging.warning(f"Could not remove directory {dirpath}: {str(e)}")
    
    if removed_count > 0:
        logging.info(f"Removed {removed_count} empty directories")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Undo notebook organization - move all notebooks back to main folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would be moved
  python undo_organization.py /path/to/repo --dry-run
  
  # Actually move files back
  python undo_organization.py /path/to/repo
  
  # Keep empty directories after moving
  python undo_organization.py /path/to/repo --keep-dirs
        """
    )
    parser.add_argument("repo_path", help="Path to the repository root")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be moved without actually moving")
    parser.add_argument("--keep-dirs", action="store_true",
                       help="Keep empty directories after moving files")
    
    args = parser.parse_args()
    
    logging.info(f"Undoing notebook organization")
    logging.info(f"Repository path: {args.repo_path}")
    logging.info(f"Mode: {'DRY RUN' if args.dry_run else 'ACTUAL MOVE'}")
    logging.info("-" * 50)
    
    undo_organization(args.repo_path, dry_run=args.dry_run)
    
    if args.dry_run:
        print("\n⚠️  This was a DRY RUN. No files were actually moved.")
        print("Remove --dry-run flag to perform actual undo.")

if __name__ == "__main__":
    main()