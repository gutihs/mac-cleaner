from pathlib import Path
from app_containers_helpers import get_unused_containers
from xcode_simulator_helpers import get_simulator_group

HOME = Path.home()

def get_safe_subfolders(base, names):
    folders = []
    for name in names:
        candidate = base / name
        if candidate.exists() and candidate.is_dir():
            folders.append(candidate)
    return folders

CLEANUP_GROUPS = [
    # safe to delete automatically
    {
        "name": "User Caches & Logs",
        "paths": [
            HOME / "Library" / "Caches",
            HOME / "Library" / "Logs"
        ],
        "auto_delete": True
    },
    {
        "name": "Application Containers Caches & Logs",
        "get_paths": lambda: [
            subdir
            for cont in (HOME / "Library" / "Containers").iterdir() if cont.is_dir()
            for subdir in get_safe_subfolders(cont / "Data" / "Library", ["Caches", "Logs"])
        ] if (HOME / "Library" / "Containers").exists() else [],
        "auto_delete": True
    },
    {
        "name": "Application Support Caches & Logs",
        "get_paths": lambda: [
            subdir
            for subdir in get_safe_subfolders(HOME / "Library" / "Application Support", ["Caches", "Logs"])
        ] if (HOME / "Library" / "Application Support").exists() else [],
        "auto_delete": True
    },
    {
        "name": "System Temporary Files",
        "paths": [
            Path("/private/tmp"),
            Path("/var/tmp"),
            Path("/private/var/folders"),
        ],
        "auto_delete": True
    },
    {
        "name": "Trash",
        "paths": [HOME / ".Trash"],
        "auto_delete": True
    },
    {
        "name": "Browser Caches",
        "paths": [
            HOME / "Library" / "Caches" / "com.apple.Safari",
            HOME / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Cache",
            HOME / "Library" / "Caches" / "Firefox",
        ],
        "auto_delete": True
    },
    {
        "name": "iTunes/Music/iMovie Cache",
        "paths": [
            HOME / "Library" / "Caches" / "com.apple.iTunes",
            HOME / "Library" / "Caches" / "com.apple.Music",
            HOME / "Movies" / "Final Cut Backups",
        ],
        "auto_delete": True
    },
    {
        "name": "Dev Cache",
        "paths": [
            HOME / "Library" / "Developer" / "Xcode" / "DerivedData",
            HOME / "Library" / "Application Support" / "Code" / "Cache",
            HOME / "Library" / "Application Support" / "Code" / "CachedData",
            HOME / ".gradle",
            HOME / ".android" / "build-cache",
            HOME / "Library" / "Caches" / "CocoaPods",
        ],
        "auto_delete": True
    },
    {
        "name": "Diagnostic Reports",
        "paths": [
            HOME / "Library" / "Logs" / "DiagnosticReports"
        ],
        "auto_delete": True
    },
    {
        "name": "Invisible System Files",
        "find_patterns": [".DS_Store", ".AppleDouble", ".Spotlight-V100", ".TemporaryItems"],
        "base_dirs": [HOME],
        "auto_delete": True
    },

    # to be confirmed before deletion
    {
        "name": "Xcode Archives (manual builds)",
        "paths": [
            HOME / "Library" / "Developer" / "Xcode" / "Archives"
        ],
        "auto_delete": False
    },
    {
        "name": "Large Files in Downloads",
        "get_paths": lambda: [p for p in (HOME / "Downloads").rglob("*") if p.is_file() and p.stat().st_size > 100 * 1024 * 1024],
        "auto_delete": False
    },
    {
        "name": "Dropbox/Google Drive Cache",
        "paths": [
            HOME / "Library" / "Application Support" / "Dropbox",
            HOME / "Library" / "Application Support" / "Google" / "DriveFS"
        ],
        "auto_delete": False
    },
    {
        "name": "Xcode Simulators",
        "get_paths": get_simulator_group,
        "auto_delete": False
    },
    {
        "name": "Application Containers: Tmp Folders",
        "get_paths": lambda: [
            tmp for cont in (HOME / "Library" / "Containers").iterdir() if cont.is_dir()
            for tmp in get_safe_subfolders(cont / "Data", ["tmp"])
        ] if (HOME / "Library" / "Containers").exists() else [],
        "auto_delete": False
    },
    {
        "name": "Unused Application Containers",
        "get_paths": get_unused_containers,
        "auto_delete": False
    }
]
