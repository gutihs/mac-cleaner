from pathlib import Path
import subprocess

# Cache for installed bundle IDs to avoid repeated calls to lsregister
_lsregister_bundle_ids_cache = None

def get_all_registered_bundle_ids():
    global _lsregister_bundle_ids_cache
    if _lsregister_bundle_ids_cache is not None:
        return _lsregister_bundle_ids_cache
    try:
        output = subprocess.check_output(
            ["/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister",
             "-dump"],
            universal_newlines=True
        )
        bundle_ids = set()
        for line in output.splitlines():
            if "bundle identifier:" in line:
                parts = line.strip().split("bundle identifier:")
                if len(parts) > 1:
                    bundle_id = parts[1].strip()
                    bundle_ids.add(bundle_id)
        _lsregister_bundle_ids_cache = bundle_ids
        return bundle_ids
    except Exception as e:
        print(f"Error extracting bundle IDs from lsregister: {e}")
        return set()

def is_bundle_related_to_installed_app(bundle_id):
    # Check lsregister
    bundle_ids = get_all_registered_bundle_ids()
    if bundle_id in bundle_ids:
        return True
    # Check prefix or suffix match
    if any(bundle_id.startswith(bid) or bid.startswith(bundle_id) for bid in bundle_ids):
        return True
    # Heuristic: look for .app folders with matching name
    app_name = bundle_id.split('.')[-2] if '.' in bundle_id else bundle_id
    applications_dirs = [
        Path("/Applications"),
        Path.home() / "Applications"
    ]
    for apps_dir in applications_dirs:
        if not apps_dir.exists():
            continue
        for app in apps_dir.glob("*.app"):
            if app_name.lower() in app.name.lower():
                return True
    return False

def get_unused_containers():
    containers_dir = Path.home() / "Library" / "Containers"
    if not containers_dir.exists():
        return []
    unused = []
    for container in containers_dir.iterdir():
        if not container.is_dir():
            continue
        bundle_id = container.name
        # Exclude Apple system containers
        if bundle_id.startswith("com.apple."):
            continue
        if not is_bundle_related_to_installed_app(bundle_id):
            unused.append(container)
    return unused