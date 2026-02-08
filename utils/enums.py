from enum import Enum


class FileType(Enum):
    """文件类型"""
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    DOC = 'doc'
    UNKNOWN = 'unknown'
