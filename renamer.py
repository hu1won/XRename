import logging
from pathlib import Path
from typing import Optional, List, Dict
import re


logger = logging.getLogger(__name__)


class FileRenamer:
    """A class that batch renames files"""
    
    def __init__(
        self,
        prefix: str = '',
        suffix: str = '',
        add_number: bool = False,
        new_ext: str = '',
        pattern: str = '',
        recursive: bool = False,
        filter_ext: Optional[List[str]] = None,
        dry_run: bool = False
    ):
        """
        Args:
            prefix: Prefix to add before filename
            suffix: Suffix to add after filename (excluding extension)
            add_number: Whether to add sequential numbers
            new_ext: New extension
            pattern: Custom naming pattern (e.g., "file_{index:03d}")
            recursive: Whether to process subdirectories recursively
            filter_ext: List of extensions to filter (e.g., ['.jpg', '.png'])
            dry_run: Whether to preview changes without actually renaming
        """
        self.prefix = prefix
        self.suffix = suffix
        self.add_number = add_number
        self.new_ext = new_ext.lower().lstrip('.') if new_ext else None
        self.pattern = pattern
        self.recursive = recursive
        self.filter_ext = [ext.lower().lstrip('.') for ext in filter_ext] if filter_ext else None
        self.dry_run = dry_run
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Check if the file should be processed"""
        if not file_path.is_file():
            return False
        
        if self.filter_ext:
            file_ext = file_path.suffix.lower().lstrip('.')
            if file_ext not in self.filter_ext:
                return False
        
        return True
    
    def _generate_new_name(
        self,
        original_name: str,
        index: int,
        total: int
    ) -> str:
        """
        Generate a new file name
        
        Args:
            original_name: Original file name (including extension)
            index: File index (starting from 0)
            total: Total number of files
        
        Returns:
            New file name (including extension)
        """
        # Separate the extension
        stem = Path(original_name).stem
        ext = Path(original_name).suffix
        
        # Use the custom pattern if it exists
        if self.pattern:
            try:
                new_name = self.pattern.format(
                    index=index,
                    original=stem,
                    total=total
                )
                # Add the extension
                if self.new_ext:
                    return f"{new_name}.{self.new_ext}"
                return f"{new_name}{ext}"
            except (KeyError, ValueError) as e:
                logger.warning(f"Pattern processing error: {e}. Using default method.")
        
        # Generate the default name
        new_stem = stem
        
        # Add the prefix
        if self.prefix:
            new_stem = f"{self.prefix}{new_stem}"
        
        # Add the number
        if self.add_number:
            # Calculate the number of digits based on the total number of files
            digits = len(str(total))
            number_format = f"_{index+1:0{digits}d}"
            new_stem = f"{new_stem}{number_format}"
        
        # Add the suffix
        if self.suffix:
            new_stem = f"{new_stem}{self.suffix}"
        
        # Handle the extension
        if self.new_ext:
            new_ext = f".{self.new_ext}"
        else:
            new_ext = ext
        
        return f"{new_stem}{new_ext}"
    
    def _rename_file(self, file_path: Path, new_name: str) -> bool:
        """
        Rename the file
        
        Args:
            file_path: Original file path
            new_name: New file name
        
        Returns:
            Success status
        """
        try:
            new_path = file_path.parent / new_name
            
            # Skip if the name is the same
            if file_path.name == new_name:
                logger.debug(f"Skip (name is the same): {file_path.name}")
                return False
            
            # Skip if the file with the same name already exists
            if new_path.exists():
                logger.warning(f"Skip (file already exists): {new_name}")
                return False
            
            if self.dry_run:
                logger.info(f"[Preview] {file_path.name} -> {new_name}")
            else:
                file_path.rename(new_path)
                logger.info(f"Change completed: {file_path.name} -> {new_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"File name change failed ({file_path.name}): {e}")
            return False
    
    def rename_files(self, target_path: Path) -> Dict[str, int]:
        """
        Rename all files in the specified path
        
        Args:
            target_path: Target directory path
        
        Returns:
            Result statistics dictionary
        """
        if not target_path.is_dir():
            raise ValueError(f"Path is not a directory: {target_path}")
        
        # Collect the list of files
        if self.recursive:
            files = [
                f for f in target_path.rglob('*')
                if self._should_process_file(f)
            ]
        else:
            files = [
                f for f in target_path.iterdir()
                if self._should_process_file(f)
            ]
        
        # Sort (ensure consistent order)
        files.sort()
        
        total = len(files)
        renamed = 0
        skipped = 0
        errors = 0
        
        logger.info(f"Total {total} files to process...")
        
        for index, file_path in enumerate(files):
            try:
                new_name = self._generate_new_name(
                    file_path.name,
                    index,
                    total
                )
                
                if self._rename_file(file_path, new_name):
                    renamed += 1
                else:
                    skipped += 1
                    
            except Exception as e:
                logger.error(f"Error processing file ({file_path.name}): {e}")
                errors += 1
        
        return {
            'total': total,
            'renamed': renamed,
            'skipped': skipped,
            'errors': errors
        }

