"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService
from sims4controlmenu.modinfo import ModInfo


@CommonDataManagerRegistry.common_data_manager(identifier='main_data')
class CMMainDataManager(CommonDataManager):
    """ Manage a storage of main data. """
    IDENTIFIER = 'main_data'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_main_data_manager'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def persistence_services(self) -> Tuple[CommonPersistenceService]:
        from sims4communitylib.persistence.persistence_services.common_file_persistence_service import \
            CommonFilePersistenceService
        result: Tuple[CommonPersistenceService] = (
            CommonFilePersistenceService(per_save=False),
        )
        return result
