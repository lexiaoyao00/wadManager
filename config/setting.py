from pydantic import Field,BaseModel
from pathlib import Path
from typing import Any
import toml

PRO_PATH = Path(__file__).parent.parent



class BaseSettings(BaseModel):
    # 通用配置
    debug: bool = Field(default=False, description="是否开启调试模式")

    # 路径配置
    log_dir: str = Field(default=str(PRO_PATH / "logs"))    # 日志目录
    data_dir: str = Field(default=str(PRO_PATH / "data"))    # 数据目录
    temp_dir: str = Field(default=str(PRO_PATH / "temp"))    # 临时目录
    download_dir: str = Field(default=str(PRO_PATH / "download"))    # 下载目录
    output_dir: str = Field(default=str(Path('E:/GeziSkin/Wads')))  # 输出目录

    mod_dir: str = Field(default=str(PRO_PATH / "mods"))    # mod 存放目录，整理后的mod会存放在这里
    load_mod_dir: str = Field(default=str(PRO_PATH / "load_mods"))    # 加载mod目录，从该目录中加载mod整理到mod_dir中

class Settings(BaseSettings, frozen=True):
    pass

CONFIG_PATH = PRO_PATH / "config" / "settings.toml"

def load_settings() -> Settings:
    if CONFIG_PATH.exists():
        data: dict[str, Any] = toml.load(CONFIG_PATH)
        return Settings(**data)
    else:
        s = BaseSettings()
        save_settings(s)
        return s

def save_settings(settings: BaseSettings):
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_PATH, "w") as f:
        toml.dump(settings.model_dump(), f)
