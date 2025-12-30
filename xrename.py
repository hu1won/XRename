import argparse
import sys
from pathlib import Path
from renamer import FileRenamer
from utils import setup_logging, validate_path


def main():
    parser = argparse.ArgumentParser(
        description='Batch rename all files in the specified path.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  # Add prefix
  python xrename.py /path/to/directory --prefix "IMG_"
  
  # Add suffix
  python xrename.py /path/to/directory --suffix "_backup"
  
  # Add number (sequentially)
  python xrename.py /path/to/directory --number
  
  # Change extension
  python xrename.py /path/to/directory --ext "jpg"
  
  # Custom pattern
  python xrename.py /path/to/directory --pattern "file_{index:03d}"
  
  # Preview (no actual changes)
  python xrename.py /path/to/directory --prefix "NEW_" --dry-run
        """
    )
    
    parser.add_argument(
        'path',
        type=str,
        help='Path to the directory to rename files in'
    )
    
    parser.add_argument(
        '--prefix',
        type=str,
        default='',
        help='Prefix to add before filename'
    )
    
    parser.add_argument(
        '--suffix',
        type=str,
        default='',
        help='Suffix to add after filename (excluding extension)'
    )
    
    parser.add_argument(
        '--number',
        action='store_true',
        help='Add sequential numbers to filenames (e.g., file_001, file_002)'
    )
    
    parser.add_argument(
        '--ext',
        type=str,
        default='',
        help='Change file extension (e.g., jpg, png)'
    )
    
    parser.add_argument(
        '--pattern',
        type=str,
        default='',
        help='Custom filename pattern (e.g., "file_{index:03d}")'
    )
    
    parser.add_argument(
        '--recursive',
        '-r',
        action='store_true',
        help='Process subdirectories recursively'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without actually renaming'
    )
    
    parser.add_argument(
        '--filter',
        type=str,
        default='',
        help='Filter by specific extensions (e.g., ".jpg,.png")'
    )
    
    parser.add_argument(
        '--log',
        type=str,
        default='',
        help='Log file path (None for console only)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log)
    
    # Validate the path
    target_path = Path(args.path)
    if not validate_path(target_path):
        sys.exit(1)
    
    # Create the file renamer
    renamer = FileRenamer(
        prefix=args.prefix,
        suffix=args.suffix,
        add_number=args.number,
        new_ext=args.ext,
        pattern=args.pattern,
        recursive=args.recursive,
        filter_ext=args.filter.split(',') if args.filter else None,
        dry_run=args.dry_run
    )
    
    # Execute the file name change
    try:
        result = renamer.rename_files(target_path)
        
        if args.dry_run:
            print(f"\n[Preview mode] {result['total']} files are expected to be changed.")
        else:
            print(f"\nSuccessfully changed the names of {result['renamed']} files.")
            if result['skipped'] > 0:
                print(f"{result['skipped']} files were skipped.")
            if result['errors'] > 0:
                print(f"{result['errors']} files processing failed.")
        
        sys.exit(0 if result['errors'] == 0 else 1)
        
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

