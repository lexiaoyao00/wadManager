from pathlib import Path
from schemas.mod_info import ModInfo,InstalledModInfo,InstallState,ModCategory
from utils import judge_file_type,FileType,EventTopic
from typing import List,Dict
import json
from config import settings
import shutil
from loguru import logger
import json
from pubsub import pub

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
    'Katarina' : '卡特琳娜-卡特',
    'Yunara' : '芸阿娜',
}

class ModManager:
    """从mod目录中加载信息，将需要安装的mod加入到输出目录中"""
    def __init__(self):
        self.installed_mods_info : InstalledModInfo = InstalledModInfo(install_path=settings.output_dir, installed_mods=[]) # 安装的mod的信息，保存为json
        self.mods : Dict[str, ModInfo]= {}  # key为mod目录
        self.name_map : Dict[str,str] = self._load_name_map()

        pub.subscribe(self.install_mod, EventTopic.MOD_INSTALL.value)
        pub.subscribe(self.install_mods, EventTopic.MOD_INSTALL_MUTIPLE.value)
        pub.subscribe(self.uninstall_mod, EventTopic.MOD_UNINSTALL.value)
        pub.subscribe(self.uninstall_mods, EventTopic.MOD_UNINSTALL_MUTIPLE.value)
        pub.subscribe(self.update_mod_info, EventTopic.MOD_INFO_UPDATE.value)

    def _load_name_map(self):
        """加载name_map"""
        name_map_file = Path(settings.config_dir) / settings.name_map_file
        if not name_map_file.exists():
            return NAME_MAP
        with open(name_map_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def init_load(self, load_mod_dir: str|Path):
        """初始化加载mod信息"""
        self.load_mods(load_mod_dir)
        self.load_installed_mods()

    def load_mods(self,load_mod_dir: str|Path):
        """加载mod信息，mod目录中必须每个按照META和WAD存放，与cslol一致"""
        self.mods.clear()
        mod_path = Path(load_mod_dir)
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

    def load_installed_mods(self):
        """加载已经安装的mod信息,从文件中获取"""
        installed_info_file = Path(settings.data_dir) / settings.installed_mod_info_file
        if not installed_info_file.exists():
            return

        with open(installed_info_file, 'r', encoding='utf-8') as file:
            self.installed_mods_info = InstalledModInfo(**json.load(file))


    def save_installed_mods(self):
        """保存已经安装的mod信息到文件中"""
        installed_info_file = Path(settings.data_dir) / settings.installed_mod_info_file
        installed_info_file.parent.mkdir(parents=True, exist_ok=True)
        with open(installed_info_file, 'w', encoding='utf-8') as file:
            json.dump(self.installed_mods_info.model_dump(exclude_none=True,mode='json'), file, ensure_ascii=False, indent=4)

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
                    mod_info.category = [ModCategory(tag) for tag in info.get('Category', [])]

            if mod_info.cover is None and judge_file_type(f) == FileType.IMAGE:
                mod_info.cover = str(f)

    def _load_wad(self,wad_path: Path):
        mod_files_path = [str(f) for f in wad_path.iterdir() if f.is_file()]
        if len(mod_files_path) == 0:
            return None
        if len(mod_files_path) > 1:
            raise ValueError(f"Mod目录{wad_path}中包含多个wad文件")
        return ModInfo(file_path=mod_files_path[0])


    def organize_mods(self, mod_dir: str|Path = None, move:bool = False):
        """整理mod文件到模型存放目录中，覆盖操作"""
        if mod_dir is None:
            mod_dir = Path(settings.mod_dir)
        mod_dir = Path(mod_dir)
        mod_dir.mkdir(parents=True, exist_ok=True)
        failed_organize = []
        old_mos = self.mods.copy()
        for dir,mod in old_mos.items():
            mod_dir_name = Path(dir).name
            new_dir_name = self.name_map.get(mod.file_stem, mod.file_stem)
            # print(f'new_dir_name = {new_dir_name}')
            new_dir = mod_dir / new_dir_name / mod_dir_name

            mod.file_path = str(new_dir / 'WAD' / mod.file_name)
            if mod.cover is not None:
                cover_name = Path(mod.cover).name
                mod.cover = str(new_dir / 'META' / cover_name)

            if new_dir.exists():
                failed_organize.append((dir,new_dir))
                continue

            if move:
                shutil.move(src=dir, dst=new_dir)
            else:
                shutil.copytree(src=dir, dst=new_dir,dirs_exist_ok=True)

        self.load_mods(mod_dir)
        return failed_organize


    def install_mod(self, mod_info : ModInfo):
        """安装mod"""
        if mod_info in self.installed_mods_info.installed_mods:
            logger.warning(f"Mod '{mod_info.name}' 已安装，跳过")
            return


        src_file = mod_info.file_path
        dst_file = Path(self.installed_mods_info.install_path) / mod_info.file_name

        if dst_file.exists():
            logger.warning(f"Mod '{mod_info.name}' 已安装，跳过")
            pub.sendMessage(EventTopic.MOD_INSTALL_EXIST.value, mod_info=mod_info, msg="模组已存在或冲突")
            return

        try:
            shutil.copyfile(src=src_file, dst=dst_file)
            self.installed_mods_info.installed_mods.append(mod_info)
            pub.sendMessage(EventTopic.MOD_INSTALL_SUCCEED.value, mod_info=mod_info)
        except Exception as e:
            logger.error(f"安装mod '{mod_info.name}' 失败，错误信息：{e}")
            pub.sendMessage(EventTopic.MOD_INSTALL_FAILED.value, mod_info=mod_info)

    def uninstall_mod(self, mod_info : ModInfo):
        """卸载mod"""
        installed_mod_file = Path(self.installed_mods_info.install_path) / mod_info.file_name
        if not installed_mod_file.exists():
            logger.warning(f"Mod '{mod_info.name}' 未安装，跳过")
            return
        installed_mod_file.unlink()
        self.installed_mods_info.installed_mods.remove(mod_info)


    def install_mods(self, mods: List[ModInfo]):
        """安装多个mod"""
        for mod in mods:
            self.install_mod(mod)


    def uninstall_mods(self, mods: List[ModInfo]):
        """卸载多个mod"""
        for mod in mods:
            self.uninstall_mod(mod)

    def update_mod_info(self, mod_path : str, mod_info : ModInfo):
        """更新mod信息"""
        logger.debug('mod manager 更新mod信息')
        self.mods[mod_path] = mod_info

