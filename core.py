import os
import shutil
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

def confirm(msg="\nDo you want to delete all the above files and folders? (y/N)"):
    print(msg)
    return input("> ").strip().lower() == "y"

def show_report(groups):
    print("\n--- SAFE CLEANUP ANALYSIS ---\n")
    reports = []
    for idx, group in enumerate(groups):
        auto_delete_status = " (with user confirmation)" if not group.get("auto_delete", False) else ""
        print(f"{idx+1}. {group['name']}{auto_delete_status}:")
        group_size = 0
        details = [] # tuples of (path, size)
        
        # Dynamic paths
        if "get_paths" in group:
            paths = group["get_paths"]()
        else:
            paths = group.get("paths", [])
        for path in paths:
            size = get_size(path)
            if size > 0:
                details.append((str(path), size))
                group_size += size
                
        # Pattern finders
        for base_dir in group.get("base_dirs", []):
            size, matches = find_and_size(base_dir, group.get("find_patterns", []))
            if size > 0:
                for match in matches:
                    details.append(match)
                group_size += size
                
        print(f"    {format_to_human_readable(group_size)}")
        
        # for d, s in details[:5]:
        for d, s in details:
            print(f"        {d} ({format_to_human_readable(s)})")
        # if len(details) > 5:
        #     print(f"        ... and {len(details)-5} more")
        reports.append({"name": group["name"], "details": details, "total": group_size, "group": group})
        
    total_cleanup = sum(r["total"] for r in reports)
    print(f"\nTOTAL: {format_to_human_readable(total_cleanup)}\n")
    return reports

def do_cleanup(reports):
    print("\nDeleting files...\n")
    for report in reports:
        auto_delete = report["group"].get("auto_delete", False)
        should_delete = auto_delete or confirm(f"Do you want to delete {report['name']}? (y/N)")
        if not should_delete:
            print(f"Skipping {report['name']}.")
            continue
        print(f"Deleting {report['name']}...")
        if report['name'] == "Xcode Simulators":
            delete_all_simulators()
            continue
        for path_str, _ in report["details"]:
            path = Path(path_str)
            try:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
            except Exception as e:
                print(f"    [!] Could not delete {path}: {e}")
    print("\nCleanup completed.")