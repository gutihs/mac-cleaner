# Mac Cleaner

A simple command-line utility to clean up unnecessary files and free up space on macOS systems.

## Features

- **Dry Run Mode**: Preview what files would be deleted without making any changes
- **Safe Cleanup**: Automatically clean non-sensitive system files and caches
- **Sensitive Cleanup**: Manual review and cleanup of sensitive files
- **Detailed Reports**: Option to show detailed file listings before deletion

## Usage

```bash
# Basic usage (will prompt for safe and sensitive cleanups)
./mac_cleaner.py

# Show detailed report of files to be deleted
./mac_cleaner.py --detailed

# Preview what would be deleted without making changes
./mac_cleaner.py --dry-run

# Show help and available options
./mac_cleaner.py --help
```

The tool will:
1. Prompt for safe cleanup analysis
2. Show report of files to be deleted
3. Ask for confirmation before deletion
4. Optionally proceed with sensitive file cleanup

## Requirements

- macOS 10.12 or later
- Python 3.6+
