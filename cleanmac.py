#!/usr/bin/env python3
from cleanup_groups import CLEANUP_GROUPS
from core import confirm, do_cleanup, show_report

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mac OS Cleaner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be deleted without actually deleting")
    parser.add_argument("--simple", action="store_true",
                        help="Perform safe cleanup without sensitive deletions")
    parser.add_argument("--complete", action="store_true",
                        help="Perform complete cleanup including sensitive deletions with confirmation")
    args = parser.parse_args()   

    if args.dry_run:
        reports = show_report(CLEANUP_GROUPS)
        print("\nDry run mode: no files will be deleted.")
    elif args.simple or args.complete:
        reports = show_report(CLEANUP_GROUPS, is_complete=args.complete)
        if confirm('Do you want to proceed with the cleanup? (y/N)'):
            do_cleanup(reports, is_complete=args.complete)
        else:
            print("\nOperation cancelled.")
    else:
        print("\nNo action specified. Use --dry-run, --simple, or --complete to perform actions.")
        print("Use --help for more information.")