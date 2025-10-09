#!/usr/bin/env python3
"""
Undo MD Files Organization
Moves all .md files from subdirectories back to the main MD folder
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

def undo_md_organization(repo_path: str, dry_run: bool = True):
    """
    Move all markdown files from subdirectories back to the main MD folder
    
    Args:
        repo_path: Path to the repository
        dry_run: If True, only show what would be moved
    """
    repo_path = Path(repo_path)
    md_folder = repo_path / "MD"
    
    if not md_folder.exists():
        logging.error(f"MD folder not found at: {md_folder}")
        return
    
    moved_count = 0
    skipped_count = 0
    error_count = 0
    
    # Find all .md and .markdown files in subdirectories
    md_files = []
    for ext in ['.md', '.markdown']:
        md_files.extend(md_folder.rglob(f"*{ext}"))
    
    logging.info(f"Found {len(md_files)} markdown files in subdirectories")
    
    for md_file in md_files:
        # Skip if already in the main MD folder
        if md_file.parent == md_folder:
            logging.debug(f"Skipping {md_file.name} - already in main folder")
            skipped_count += 1
            continue
        
        # Destination in main MD folder
        dest_path = md_folder / md_file.name
        
        # Handle existing files
        if dest_path.exists():
            stem = md_file.stem
            suffix = md_file.suffix
            counter = 1
            while dest_path.exists():
                dest_path = md_folder / f"{stem}_{counter}{suffix}"
                counter += 1
        
        relative_source = md_file.relative_to(md_folder)
        
        if dry_run:
            logging.info(f"[DRY RUN] Would move: {relative_source} -> {md_file.name}")
            moved_count += 1
        else:
            try:
                shutil.move(str(md_file), str(dest_path))
                logging.info(f"Moved: {relative_source} -> {dest_path.name}")
                moved_count += 1
            except Exception as e:
                logging.error(f"Error moving {md_file}: {str(e)}")
                error_count += 1
    
    # Summary
    logging.info("-" * 50)
    if dry_run:
        logging.info(f"[DRY RUN] Would move {moved_count} files back to main MD folder")
        logging.info(f"Skipped {skipped_count} files already in main folder")
    else:
        logging.info(f"Moved {moved_count} files back to main MD folder")
        logging.info(f"Skipped {skipped_count} files already in main folder")
        if error_count > 0:
            logging.warning(f"Encountered {error_count} errors during the process")
        
        # Remove empty directories
        if moved_count > 0:
            remove_empty_dirs(md_folder)

def remove_empty_dirs(md_folder: Path):
    """Remove empty directories after moving files"""
    removed_count = 0
    
    # Get all subdirectories (excluding the main MD folder)
    subdirs = [d for d in md_folder.rglob("*") if d.is_dir() and d != md_folder]
    
    # Sort by depth (deepest first) to remove from bottom up
    subdirs.sort(key=lambda x: len(x.parts), reverse=True)
    
    for dirpath in subdirs:
        # Check if directory is empty
        if not any(dirpath.iterdir()):
            try:
                dirpath.rmdir()
                logging.info(f"Removed empty directory: {dirpath.relative_to(md_folder)}")
                removed_count += 1
            except Exception as e:
                logging.warning(f"Could not remove directory {dirpath}: {str(e)}")
    
    if removed_count > 0:
        logging.info(f"Removed {removed_count} empty directories")

def generate_undo_report(repo_path: Path, moved_count: int, skipped_count: int, error_count: int):
    """Generate a report of the undo operation"""
    report = []
    report.append("=" * 70)
    report.append("MD FILES UNDO ORGANIZATION REPORT")
    report.append("=" * 70)
    report.append(f"\nRepository: {repo_path}")
    report.append(f"MD folder: {repo_path / 'MD'}")
    report.append(f"\nFiles moved back to main folder: {moved_count}")
    report.append(f"Files already in main folder: {skipped_count}")
    report.append(f"Errors encountered: {error_count}")
    report.append("\nAll markdown files have been moved back to the main MD folder.")
    
    report_text = "\n".join(report)
    
    # Save report to file
    report_path = repo_path / "md_undo_organization_report.txt"
    with open(report_path, "w") as f:
        f.write(report_text)
    
    logging.info(f"\nReport saved to: {report_path}")
    return report_text

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Undo MD file organization - move all markdown files back to main MD folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would be moved
  python undo_md_organization.py /path/to/repo --dry-run
  
  # Actually move files back
  python undo_md_organization.py /path/to/repo
  
  # Keep empty directories after moving
  python undo_md_organization.py /path/to/repo --keep-dirs
        """
    )
    parser.add_argument("repo_path", help="Path to the repository root")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be moved without actually moving")
    parser.add_argument("--keep-dirs", action="store_true",
                       help="Keep empty directories after moving files")
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    
    logging.info(f"Undoing MD file organization")
    logging.info(f"Repository path: {args.repo_path}")
    logging.info(f"Mode: {'DRY RUN' if args.dry_run else 'ACTUAL MOVE'}")
    logging.info("-" * 50)
    
    # Track counts manually for report
    moved_count = 0
    skipped_count = 0
    error_count = 0
    
    md_folder = repo_path / "MD"
    if not md_folder.exists():
        logging.error(f"MD folder not found at: {md_folder}")
        return 1
    
    # Count files
    md_files = []
    for ext in ['.md', '.markdown']:
        md_files.extend(md_folder.rglob(f"*{ext}"))
    
    for md_file in md_files:
        if md_file.parent == md_folder:
            skipped_count += 1
        else:
            moved_count += 1
    
    # Run the undo
    undo_md_organization(args.repo_path, dry_run=args.dry_run)
    
    if not args.dry_run:
        # Generate report
        report = generate_undo_report(repo_path, moved_count, skipped_count, error_count)
        print("\n" + report)
    else:
        print(f"\n⚠️  This was a DRY RUN. Would move {moved_count} files.")
        print("Remove --dry-run flag to perform actual undo.")

if __name__ == "__main__":
    main()