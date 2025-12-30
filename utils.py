import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(log_file: Optional[str] = None):
    """
    Setup logging
    
    Args:
        log_file: Log file path (None for console only)
    """
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )


def validate_path(path: Path) -> bool:
    """
    Validate the path
    
    Args:
        path: Path to validate
    
    Returns:
        Whether the path is valid
    """
    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        return False
    
    if not path.is_dir():
        print(f"Error: Not a directory: {path}", file=sys.stderr)
        return False
    
    # Check read permission
    if not path.is_dir() or not (path.stat().st_mode & 0o444):
        print(f"Warning: Path may not have read permission: {path}", file=sys.stderr)
    
    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename by removing or replacing special characters
    
    Args:
        filename: Original file name
    
    Returns:
        Sanitized file name
    """
    # Remove characters that are not allowed on Windows
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Combine consecutive spaces into one
    filename = ' '.join(filename.split())
    
    return filename

