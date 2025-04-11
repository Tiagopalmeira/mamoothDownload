import os
import platform
from pathlib import Path
import os


def get_download_folder():
    return str(Path.home() / "Downloads")

def obter_diretorio_download():
    sistema = platform.system()

    # Windows
    if sistema == "Windows":
        return str(Path.home() / "Downloads")

    # Linux/macOS
    elif sistema in ["Linux", "Darwin"]:
        return str(Path.home() / "Downloads")

    # Termux ou fallback
    else:
        if "ANDROID_ROOT" in os.environ:
            return "/sdcard/Download"
        return str(Path.home() / "Downloads")
