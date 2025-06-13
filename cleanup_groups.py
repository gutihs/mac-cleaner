from pathlib import Path

HOME = Path.home()

def get_safe_subfolders(base, names):
    folders = []
    for name in names:
        candidate = base / name
        if candidate.exists() and candidate.is_dir():
            folders.append(candidate)
    return folders

CLEANUP_GROUPS = [
    {
        "name": "User Caches",
        "paths": [HOME / "Library" / "Caches"]
    },
    {
        "name": "User Logs",
        "paths": [HOME / "Library" / "Logs"]
    },
    {
        "name": "Application Containers: Caches & Logs",
        "get_paths": lambda: [
            subdir
            for cont in (HOME / "Library" / "Containers").iterdir() if cont.is_dir()
            for subdir in get_safe_subfolders(cont / "Data" / "Library", ["Caches", "Logs"])
        ] if (HOME / "Library" / "Containers").exists() else []
    },
    {
        "name": "Application Support: Caches & Logs",
        "get_paths": lambda: [
            subdir
            for subdir in get_safe_subfolders(HOME / "Library" / "Application Support", ["Caches", "Logs"])
        ] if (HOME / "Library" / "Application Support").exists() else []
    },
    {
        "name": "System Temporary Files",
        "paths": [
            Path("/private/tmp"),
            Path("/var/tmp"),
            Path("/private/var/folders"),
        ]
    },
    {
        "name": "Invisible System Files (.DS_Store, .AppleDouble, .Spotlight-V100, .TemporaryItems)",
        "find_patterns": [".DS_Store", ".AppleDouble", ".Spotlight-V100", ".TemporaryItems"],
        "base_dirs": [HOME]
    },
    {
        "name": "Trash",
        "paths": [HOME / ".Trash"]
    },
    {
        "name": "Browser Caches",
        "paths": [
            HOME / "Library" / "Caches" / "com.apple.Safari",
            HOME / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Cache",
            HOME / "Library" / "Caches" / "Firefox",
        ]
    },
    {
        "name": "iTunes/Music Cache",
        "paths": [
            HOME / "Library" / "Caches" / "com.apple.iTunes",
            HOME / "Library" / "Caches" / "com.apple.Music"
        ]
    },
    {
        "name": "Xcode/Final Cut/iMovie Cache",
        "paths": [
            HOME / "Library" / "Developer" / "Xcode" / "DerivedData",
            HOME / "Movies" / "Final Cut Backups",
        ]
    }
]
