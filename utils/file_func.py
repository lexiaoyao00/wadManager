
from pathlib import Path
from utils.enums import FileType

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