from pydantic import BaseModel,model_validator
from enum import Enum
from pathlib import Path
from typing import Optional,List

# 安装状态
class InstallState(Enum):
    """安装状态"""
    INSTALLING = "安装中"
    INSTALLED = "已安装"
    UNINSTALLING = "卸载中"
    UNINSTALLED = "未安装"

class ModCategory(Enum):
    """mod分类"""
    SKIN = "皮肤"
    MAPS = "地图"
    MEMES = "表情包"
    TFT = "云顶"
    UI = "界面"
    AUDIO = "音效"
    VTUBER = "虚拟主播"
    OTHER = "其他"


"""{
    "Author": "554",
    "Description": "",
    "Heart": "",
    "Home": "",
    "Name": "Vex Nude",
    "Version": "2.2"
}
"""
class ModInfo(BaseModel):
    """MOD信息类，用于存储mod信息"""

    file_path: str      # 文件路径
    name: str = None      # 名称
    author: str = None  # 作者
    cover : str = None  # 封面
    description: str = '无描述' # 描述
    version: str = None # 版本
    category:Optional[List[ModCategory]]  = None # 分类
    state : InstallState = InstallState.UNINSTALLED # 安装状态

    @model_validator(mode='after')
    def check_file_path(self):
        if not Path(self.file_path).exists():
            raise ValueError(f"文件路径不存在: {self.file_path}")

        if not Path(self.file_path).is_file():
            raise ValueError(f"文件路径不是一个文件: {self.file_path}")

        self.name = self.name or Path(self.file_path).stem
        return self
