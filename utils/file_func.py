
from pathlib import Path
from utils.enums import FileType
import subprocess
import sys
import os

def judge_file_type(file_path : str|Path):
    """判断文件类型，当前只支持图片和视频"""
    path = Path(file_path)
    if not path.is_file():
        raise ValueError(f"{str(path)} 不是一个文件")

    file_suffix = path.suffix.lower()

    if file_suffix in ['.jpg', '.png', '.jpeg', '.bmp', 'webp']:
        return FileType.IMAGE
    elif file_suffix in ['.mp4', '.avi', '.mov', '.mkv', '.flv']:
        return FileType.VIDEO
    else:
        return FileType.UNKNOWN


def open_folder(path: str|Path):

    path = Path(path)
    if not path.is_dir():
        raise ValueError(f"{str(path)} 不是一个文件夹")
    path_str = str(path)

    if sys.platform.startswith('darwin'):  # macOS
        subprocess.run(['open', path_str])
    elif sys.platform.startswith('win'):   # Windows
        os.startfile(path_str)
    elif sys.platform.startswith('linux'):  # Linux
        subprocess.run(['xdg-open', path_str])
    else:
        raise NotImplementedError("Unsupported platform")
