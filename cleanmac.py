#!/usr/bin/env python3
from cleanup_groups import CLEANUP_GROUPS
from core import confirm, do_cleanup, show_report

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mac OS Cleaner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be deleted without actually deleting")
    args = parser.parse_args()   

    reports = show_report(CLEANUP_GROUPS)

    if args.dry_run:
        print("\nDry run mode: no files will be deleted.")
    else:
        if confirm():
            do_cleanup(reports)
        else:
            print("\nOperation cancelled.")