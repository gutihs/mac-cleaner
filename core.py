import os
import sys
import time
import shutil
import threading
from pathlib import Path
from cleanup_groups import CLEANUP_GROUPS
from xcode_simulator_helpers import delete_all_simulators

def format_to_human_readable(size):
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

# Calculates the total size of a file or folder (recursively).
def get_size(path):
    total = 0
    if path.is_file():
        return path.stat().st_size
    if not path.exists():
        return 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
            except Exception:
                pass
    return total

# Searches for files or folders whose names contain certain patterns, and sums their sizes.
def find_and_size(base_dir, patterns):
    total = 0
    matches = []
    for root, dirs, files in os.walk(base_dir):
        for name in files + dirs:
            for pattern in patterns:
                if pattern in name:
                    full_path = os.path.join(root, name)
                    try:
                        size = os.path.getsize(full_path)
                    except Exception:
                        size = 0
                    total += size
                    matches.append((full_path, size))
    return total, matches

def confirm(msg):
    print(msg)
    return input("> ").strip().lower() == "y"

def show_progress(text, stop_event=None):
    chars = "/—\\|"
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r{text} {chars[i % len(chars)]}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    # Clear the progress line when the stop event is set
    sys.stdout.write('\r' + ' ' * (len(text) + 4) + '\r')
    sys.stdout.flush()

def show_report(pick_auto_delete, show_details):
    reports = []
    for group in CLEANUP_GROUPS:
        auto_delete = group.get("auto_delete", False)
        if (auto_delete != pick_auto_delete):
            continue
        print(f"* {group['name']}:")
        # show loading in another thread
        stop_event = threading.Event()
        t = threading.Thread(target=show_progress, args=("Analyzing files...", stop_event))
        t.start()
        try:
            # perform search and size calculation
            group_size = 0
            details = [] # tuples of (path, size)
            if "get_paths" in group:
                paths = group["get_paths"]()
            else:
                paths = group.get("paths", [])
            for path in paths:
                size = get_size(path)
                if size > 0:
                    details.append((str(path), size))
                    group_size += size
            for base_dir in group.get("base_dirs", []):
                size, matches = find_and_size(base_dir, group.get("find_patterns", []))
                if size > 0:
                    for match in matches:
                        details.append(match)
                    group_size += size
        finally:
            # stop the loading thread
            stop_event.set()
            t.join()
        print(f"    {format_to_human_readable(group_size)}")
        if show_details:
            for d, s in details:
                print(f"        {d} ({format_to_human_readable(s)})")
        reports.append({"name": group["name"], "details": details, "total": group_size, "group": group})
    total_cleanup = sum(r["total"] for r in reports)
    print(f"\nTOTAL: {format_to_human_readable(total_cleanup)}\n")
    return reports

def do_cleanup(reports, pick_auto_delete):
    for report in reports:
        auto_delete = report["group"].get("auto_delete", False)
        if (auto_delete != pick_auto_delete):
            continue
        if auto_delete:
            should_delete_group = True
        else:
            should_delete_group = confirm(f"Do you want to process {report['name']}? (y/N)")
        if not should_delete_group:
            print(f"Skipping {report['name']}.")
            continue
        print(f"Processing {report['name']}...")
        if report['name'] == "Xcode Simulators":
            delete_all_simulators()
            continue
        for path_str, _ in report["details"]:
            path = Path(path_str)
            if auto_delete:
                should_delete = True
            else:
                should_delete = confirm(f"Delete: {path}? (y/N)")
            if not should_delete:
                print(f"    Skipped {path}")
                continue
            try:
                if path.is_file():
                    path.unlink()
                    print(f"    Deleted file: {path}")
                elif path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"    Deleted folder: {path}")
            except Exception as e:
                print(f"    [!] Could not delete {path}: {e}")
    print("\nCleanup completed.")
