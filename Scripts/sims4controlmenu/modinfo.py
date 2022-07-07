"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    """ Mod info for the Sims 4 Control Menu. """
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'ControlMenu'

    @property
    def _author(self) -> str:
        return 'ColonolNutty'

    @property
    def _base_namespace(self) -> str:
        return 'sims4controlmenu'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '1.4'
