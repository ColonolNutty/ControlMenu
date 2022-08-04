"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Type, Union, Dict, Any

from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from controlmenu.logging.has_cm_log import HasCMLog
from controlmenu.modinfo import ModInfo
from controlmenu.persistence.cm_data_manager import CMMainDataManager
from controlmenu.settings.data.data_store import CMMainSettingsDataStore


class CMMainDataManagerUtils(CommonService, HasCMLog):
    """ Utilities for accessing data stores """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_main_data_manager'

    def __init__(self) -> None:
        super().__init__()
        self._data_manager: Union[CMMainDataManager, None] = None

    @property
    def data_manager(self) -> CMMainDataManager:
        """ The data manager containing data. """
        if self._data_manager is None:
            # noinspection PyTypeChecker
            self._data_manager: CMMainDataManager = CommonDataManagerRegistry().locate_data_manager(self.mod_identity, identifier=CMMainDataManager.IDENTIFIER)
        return self._data_manager

    def get_main_mod_settings_data_store(self) -> CMMainSettingsDataStore:
        """ Retrieve the Main Mod Settings Data Store. """
        # noinspection PyTypeChecker
        data_store: CMMainSettingsDataStore = self._get_data_store(CMMainSettingsDataStore)
        return data_store

    def _get_data_store(self, data_store_type: Type[CommonDataStore]) -> Union[CommonDataStore, None]:
        return self.data_manager.get_data_store_by_type(data_store_type)

    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """ Get all data. """
        return self.data_manager._data_store_data

    def save(self) -> bool:
        """ Save data. """
        return self.data_manager.save()

    def reset(self, prevent_save: bool = False) -> bool:
        """ Reset data. """
        return self.data_manager.remove_all_data(prevent_save=prevent_save)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'cm.print_mod_global_data')


@CommonConsoleCommand(ModInfo.get_identity(), 'cm.print_main_mod_data', 'Print Mod Data', show_with_help_command=False)
def _cm_command_print_mod_data(output: CommonConsoleCommandOutput):
    output('Printing CKM Mod Main Data to Messages.txt file. This may take a little bit, be patient.')
    log.enable()
    log.format(data_store_data=CMMainDataManagerUtils().get_all_data())
    log.disable()
    return True
