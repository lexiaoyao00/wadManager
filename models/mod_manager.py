from pathlib import Path
from schemas.mod_info import ModInfo
from utils import judge_file_type,FileType
from typing import List,Dict
import json

class ModManager:
    """从mod目录中加载信息，将需要安装的mod加入到输出目录中"""
    def __init__(self):
        self._installed_mods : List[ModInfo] = []
        self.mods : Dict[str, ModInfo]= {}

    def load_mods(self,mod_dir: str|Path):
        """加载mod信息，mod目录中必须每个按照META和WAD存放，与cslol一致"""
        mod_path = Path(mod_dir)
        if not mod_path.exists():
            raise FileNotFoundError(f"Mod目录{mod_path}不存在")
        for d in mod_path.rglob('*'):
            if not d.is_dir():
                continue
            meta_path = d / 'META'
            wad_path = d / 'WAD'
            if not meta_path.exists() or not wad_path.exists():
                continue
            mod_info = self._load_wad(wad_path)
            if mod_info is None:
                continue
            self._load_meta(meta_path, mod_info)

            self.mods[mod_info.file_path] = mod_info


    def _load_meta(self,meta_path: Path, mod_info: ModInfo):
        for f in meta_path.iterdir():
            # print(f)
            if f.name == 'info.json':
                with open(f, 'r', encoding='utf-8') as file:
                    info : Dict = json.load(file)
                    mod_info.name = info.get('Name', None)
                    mod_info.author = info.get('Author', None)
                    mod_info.version = info.get('Version', None)
                    mod_info.description = info.get('Description', '无描述')

            if judge_file_type(f) == FileType.IMAGE:
                mod_info.cover = str(f)

    def _load_wad(self,wad_path: Path):
        mod_files_path = [str(f) for f in wad_path.iterdir() if f.is_file()]
        if len(mod_files_path) == 0:
            return None
        if len(mod_files_path) > 1:
            raise ValueError(f"Mod目录{wad_path}中包含多个wad文件")
        return ModInfo(file_path=mod_files_path[0])

    def add_mods(self):
        pass

if __name__ == '__main__':
    mm = ModManager()
    mm.load_mods('mods')