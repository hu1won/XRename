# XRename

A Python script that batch renames all files in a specified directory path.

## Features

- ✅ Add prefix/suffix
- ✅ Auto-add sequential numbers
- ✅ Change file extensions
- ✅ Custom naming patterns
- ✅ Filter by specific extensions
- ✅ Recursive subdirectory processing
- ✅ Preview mode (dry-run)
- ✅ Safe file handling (prevents duplicate names)

## Installation

Python 3.7 or higher is required.

```bash
# Clone or download the repository
cd XRename

# Grant execute permission (optional)
chmod +x xrename.py
```

## Usage

### Basic Usage

```bash
python xrename.py /path/to/directory
```

### Main Options

#### Add Prefix
```bash
python xrename.py /path/to/directory --prefix "IMG_"
# Result: file.jpg -> IMG_file.jpg
```

#### Add Suffix
```bash
python xrename.py /path/to/directory --suffix "_backup"
# Result: file.jpg -> file_backup.jpg
```

#### Add Sequential Numbers
```bash
python xrename.py /path/to/directory --number
# Result: file1.jpg -> file1_001.jpg, file2.jpg -> file2_002.jpg
```

#### Change Extension
```bash
python xrename.py /path/to/directory --ext "jpg"
# Result: file.png -> file.jpg
```

#### Combine Multiple Options
```bash
python xrename.py /path/to/directory --prefix "PHOTO_" --number --ext "jpg"
# Result: image.png -> PHOTO_image_001.jpg
```

#### Custom Pattern
```bash
python xrename.py /path/to/directory --pattern "photo_{index:03d}"
# Result: file1.jpg -> photo_001.jpg, file2.jpg -> photo_002.jpg
```

#### Filter by Specific Extensions
```bash
python xrename.py /path/to/directory --filter ".jpg,.png" --prefix "IMG_"
# Result: Only processes .jpg and .png files
```

#### Recursive Processing (Subdirectories)
```bash
python xrename.py /path/to/directory --recursive --prefix "NEW_"
```

#### Preview Mode (No Actual Changes)
```bash
python xrename.py /path/to/directory --prefix "NEW_" --dry-run
```

#### Save Log File
```bash
python xrename.py /path/to/directory --prefix "NEW_" --log rename.log
```

### Complete Option List

```
positional arguments:
  path                  Directory path to rename files in

optional arguments:
  --prefix PREFIX       Prefix to add before filename
  --suffix SUFFIX       Suffix to add after filename (excluding extension)
  --number              Add sequential numbers to filenames
  --ext EXT             Change file extension
  --pattern PATTERN     Custom naming pattern
  --recursive, -r       Process subdirectories recursively
  --dry-run             Preview changes without actually renaming
  --filter FILTER       Filter by specific extensions (e.g., ".jpg,.png")
  --log LOG             Log file path
  -h, --help            Show help message
```

## Project Structure

```
XRename/
├── xrename.py          # Main script (CLI entry point)
├── renamer.py          # File renaming logic
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies list
└── README.md           # Project documentation
```

## Safety Features

- Duplicate name prevention: Won't rename to existing filenames
- Preview mode: Use `--dry-run` option to preview changes before applying
- Error handling: Continues processing even if individual files fail
- Logging: Records all operations

## Warning

⚠️ **Important**: File renaming cannot be undone. Always use the `--dry-run` option to preview changes before processing important files!

## Examples

### Add Date Prefix to Photo Files
```bash
python xrename.py ~/Pictures --prefix "2024_" --filter ".jpg,.png"
```

### Add Suffix to Backup Files
```bash
python xrename.py ~/Documents --suffix "_backup" --recursive
```

### Add Sequential Numbers to All Files
```bash
python xrename.py /path/to/files --number --dry-run  # Preview first
python xrename.py /path/to/files --number            # Execute
```

## License

This project is free to use.
