#!/usr/bin/env python3
import argparse
from cleanup_groups import CLEANUP_GROUPS
from core import confirm, do_cleanup, show_report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mac OS Cleaner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be deleted without actually deleting")
    parser.add_argument("--detailed", action="store_true",
                        help="Show detailed report of files to be deleted")
    args = parser.parse_args()
    
    if confirm('Start safe clean analysis? (y/N)'):
        print("\n--- SAFE CLEANUP ANALYSIS ---\n")
        reports = show_report(pick_auto_delete=True, show_details=args.detailed)
        if args.dry_run:
            print("\nDry run mode: no files will be deleted.")
        else:
            if confirm('Do you want to delete this files? (y/N)'):
                do_cleanup(reports, pick_auto_delete=True)
        
    if confirm('Start sensitive clean analysis? (y/N)'):
        print("\n--- SENSITIVE CLEANUP ANALYSIS ---\n")
        reports = show_report(pick_auto_delete=False, show_details=args.detailed)
        if args.dry_run:
            print("\nDry run mode: no files will be deleted.")
        else :
            if confirm('Do you want to delete this files (checking each one)? (y/N)'):
                do_cleanup(reports, pick_auto_delete=False)