"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

import date_and_time
from sims.household import Household
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from controlmenu.settings.settings import CMSetting


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
        from sims.sim_spawner_service import SimSpawnerService
        return {
            CMSetting.VERSION: self._version,

            CMSetting.PREGNANCY_SPEED: PregnancyTracker.PREGNANCY_RATE,
            CMSetting.MAXIMUM_HOUSEHOLD_SIZE: Household.MAXIMUM_SIZE,
            CMSetting.REAL_MILLISECONDS_PER_SIM_SECOND: date_and_time.REAL_MILLISECONDS_PER_SIM_SECOND,
            CMSetting.CLOCK_SPEED_MULTIPLIER: 1.0,
            CMSetting.MAXIMUM_SIMS_PER_LOT: SimSpawnerService.NPC_SOFT_CAP
        }.copy()
