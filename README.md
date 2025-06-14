# Mac Cleaner

A simple command-line utility to clean up unnecessary files and free up space on macOS systems.

## Features

- **Dry Run Mode**: Preview what files would be deleted without making any changes
- **Simple Cleanup**: Safe cleanup of non-sensitive system files and caches
- **Complete Cleanup**: Full system cleanup including sensitive files (with confirmation)
- **User-Friendly**: Clear reporting and confirmation before any deletions

## Usage

The tool provides three main modes of operation:

```bash
# Show what would be deleted without making changes
./mac_cleaner.py --dry-run

# Perform safe cleanup of non-sensitive files
./mac_cleaner.py --simple

# Perform complete cleanup (includes sensitive files)
./mac_cleaner.py --complete

# Show help and available options
./mac_cleaner.py --help
```

## Requirements

- macOS 10.12 or later
- Python 3.6+
