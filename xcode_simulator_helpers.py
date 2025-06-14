from pathlib import Path
import subprocess

def get_simulator_group():
    sim_dir = Path("~/Library/Developer/CoreSimulator/Devices").expanduser()
    if not sim_dir.exists():
        return []
    return [p for p in sim_dir.iterdir() if p.is_dir()]

def delete_all_simulators():
    print("\nDeleting ALL user-created and default simulators...")
    try:
        result = subprocess.run(['xcrun', 'simctl', 'list', 'devices', '-j'], capture_output=True, check=True, text=True)
        import json
        data = json.loads(result.stdout)
        udids = []
        for runtime, devices in data.get("devices", {}).items():
            for device in devices:
                if device.get("isAvailable"):
                    udids.append(device["udid"])
        for udid in udids:
            print(f"Deleting simulator {udid}")
            subprocess.run(['xcrun', 'simctl', 'delete', udid])
    except Exception as e:
        print(f"Error deleting simulators: {e}")
    print("\nCleaning up unavailable (ghost) devices, if any...")
    try:
        subprocess.run(['xcrun', 'simctl', 'delete', 'unavailable'])
    except Exception as e:
        print(f"Error deleting unavailable simulators: {e}")
    print("\nAll simulators deleted. Open Xcode to auto-recreate default simulators.")