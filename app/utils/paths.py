from pathlib import Path

def get_download_folder():
    return str(Path.home() / "Downloads")
