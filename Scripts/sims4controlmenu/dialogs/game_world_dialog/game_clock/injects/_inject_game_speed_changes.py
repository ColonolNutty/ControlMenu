"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import date_and_time
import sims4.core_services
from typing import Any

from clock import GameClock
from scheduler import ScheduleEntry
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu.settings.setting_utils import S4CMSettingUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), sims4.core_services, 'start_services')
def _cm_adjust_game_clock_on_zone_load(original, self, *_, **__) -> Any:
    original_result = original(self, *_, **__)
    date_and_time.REAL_MILLISECONDS_PER_SIM_SECOND = S4CMSettingUtils.get_real_milliseconds_per_sim_second()
    ScheduleEntry.FACTORY_TUNABLES['start_time']._default = date_and_time.create_date_and_time(hours=9, minutes=0)
    return original_result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameClock, GameClock.current_clock_speed_scale.__name__)
def _cm_get_current_clock_speed_scale(original, self) -> Any:
    return original(self) * S4CMSettingUtils().get_clock_speed_multiplier()
