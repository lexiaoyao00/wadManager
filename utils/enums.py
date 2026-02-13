from enum import Enum


class FileType(Enum):
    """文件类型"""
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    DOC = 'doc'
    MOD = 'mod'
    UNKNOWN = 'unknown'

class EventTopic(Enum):
    """事件主题"""
    MOD_INSTALL = 'mod_install'
    MOD_INSTALL_MUTIPLE = 'mod_install_multiple'

    MOD_INSTALL_SUCCEED = 'mod_install_success'
    MOD_INSTALL_FAILED = 'mod_install_faild'

    MOD_INSTALL_EXIST = 'mod_install_exist'

    MOD_UNINSTALL = 'mod_uninstall'
    MOD_UNINSTALL_MUTIPLE = 'mod_uninstall_multiple'

    MOD_INSTALL_OR_UNINSTALL = 'mod_install_or_uninstall'

    MOD_INFO_UPDATE = 'mod_info_update'

    LOAD_MOD = 'load_mod'
    INSTALL_SELECTED_MOD = 'install_selected_mod'
    UNINSTALL_SELECTED_MOD = 'uninstall_selected_mod'

    SEARCH_MOD = 'search_mod'
    SERACH_FINISHED = 'search_finished'
