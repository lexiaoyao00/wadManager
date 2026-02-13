from pydantic import BaseModel,model_validator,ConfigDict
from enum import Enum
from pathlib import Path
from typing import Optional,List

# 安装状态
class InstallState(Enum):
    """安装状态"""
    INSTALLED = "已安装"
    INSTALLING = "安装中"
    UNINSTALLED = "未安装"

class ModCategory(Enum):
    """mod分类"""
    SKIN = "skin"   # 皮肤
    MAPS =  "maps"  # 地图
    MEMES = "memes" # 表情包
    TFT = "tft"     # 云顶
    UI =  "ui"      # 界面
    AUDIO = "audio" # 音效
    VTUBER = "vtuber"   # 虚拟主播
    OTHER = "other" # 其他


"""{
    "Author": "554",
    "Description": "",
    "Heart": "",
    "Home": "",
    "Name": "Vex Nude",
    "Version": "2.2"
}
"""
class ModState(BaseModel):
    """mod状态"""
    install_state: InstallState = InstallState.UNINSTALLED
    install_path: str = None

class ModInfo(BaseModel):
    """MOD信息类，用于存储mod信息"""

    file_path: str      # 文件路径，唯一
    file_name: str = None      # 文件名称，包含后缀
    file_stem : str = None      # 文件名，从path中去除后缀
    name: str = None      # 名称
    author: str = None  # 作者
    cover : str = None  # 封面
    description: str = '无描述' # 描述
    version: str = None # 版本
    category:Optional[List[ModCategory]]  = None # 分类

    @model_validator(mode='after')
    def check_file_path(self):
        if not Path(self.file_path).exists():
            raise ValueError(f"文件路径不存在: {self.file_path}")

        if not Path(self.file_path).is_file():
            raise ValueError(f"文件路径不是一个文件: {self.file_path}")

        self.file_name = self.file_name or Path(self.file_path).name
        self.file_stem = self.file_stem or self.file_name.split('.')[0]
        self.name = self.name or self.file_stem
        return self

    def __eq__(self, other):
        if not isinstance(other, ModInfo):
            return False
        return self.file_path == other.file_path

    def __hash__(self):
        return hash(self.file_path)

    model_config = ConfigDict(
        alias_generator=lambda s: s[0].upper() + s[1:],
        populate_by_name=True
)


class InstalledModInfo(BaseModel):
    """已安装的mod信息类，用于存储已安装的mod信息"""
    install_path: str = None # 安装路径
    installed_mods : List[ModInfo] = None