"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from sims.household import Household
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4controlmenu.settings.settings import CMSetting


class CMMainSettingsDataStore(CommonDataStore):
    """ Manages main settings for CM. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 'cm_main_settings'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _version(self) -> int:
        return 7

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _default_data(self) -> Dict[str, Any]:
        return {
            CMSetting.VERSION: self._version,

            CMSetting.PREGNANCY_SPEED: PregnancyTracker.PREGNANCY_RATE,
            CMSetting.MAXIMUM_HOUSEHOLD_SIZE: Household.MAXIMUM_SIZE
        }.copy()
