from pathlib import Path
from schemas.mod_info import ModInfo
from utils import judge_file_type,FileType
from typing import List,Dict
import json
from config import settings
import shutil

# 译名对照表
NAME_MAP = {
    'Vex': '薇古丝-熬夜波比',
    'Janna': '迦娜-风女',
    'Evelynn' : '伊芙琳-寡妇',
    'Morgana' : '莫甘娜',
    'Hecarim' : '赫卡里姆-人马',
    'Soraka' : '索拉卡-星妈',
    'Caitlyn' : '凯特琳-女警',
    'Briar' : '贝蕾亚-玉足',
}
class ModManager:
    """从mod目录中加载信息，将需要安装的mod加入到输出目录中"""
    def __init__(self):
        self._installed_mods : Dict[str, ModInfo] = {} # key为mod文件路径, 取modinfo中的file_path，便于查找
        self.mods : Dict[str, ModInfo]= {}  # key为mod目录

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

            self.mods[d] = mod_info


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


    """整理mod文件"""
    def organize_mods(self, output_dir: str|Path = None):
        if output_dir is None:
            output_dir = Path(settings.mod_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f'output dir = {str(output_dir)}')
        old_mos = self.mods.copy()
        self.mods.clear()
        for dir,mod in old_mos.items():
            mod_dir_name = Path(dir).name
            new_dir_name = NAME_MAP.get(mod.file_stem, mod.file_stem)
            # print(f'new_dir_name = {new_dir_name}')
            new_dir = output_dir / new_dir_name / mod_dir_name
            mod.file_path = str(new_dir / 'WAD' / mod.file_name)
            self.mods[new_dir] = mod
            if new_dir.exists():
                continue
            shutil.copytree(src=dir, dst=new_dir, dirs_exist_ok=True)


        # for dir,mod in self.mods.items():
        #     print(dir,mod.file_path)



if __name__ == '__main__':
    mm = ModManager()
    mm.load_mods('mods')