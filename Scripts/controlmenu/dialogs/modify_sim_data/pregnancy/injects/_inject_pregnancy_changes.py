"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from controlmenu.modinfo import ModInfo
from controlmenu.settings.setting_utils import CMSettingUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PregnancyTracker, PregnancyTracker.enable_pregnancy.__name__)
def _cm_adjust_pregnancy_duration_on_pregnancy_start(original, self, *_, **__) -> Any:
    original_result = original(self, *_, **__)
    pregnancy_commodity_type = self.PREGNANCY_COMMODITY_MAP.get(self._sim_info.species)
    tracker = self._sim_info.get_tracker(pregnancy_commodity_type)
    pregnancy_commodity = tracker.get_statistic(pregnancy_commodity_type, add=True)
    pregnancy_commodity.remove_statistic_modifier(PregnancyTracker.PREGNANCY_RATE)
    pregnancy_commodity.add_statistic_modifier(CMSettingUtils.get_pregnancy_speed_modifier())
    return original_result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PregnancyTracker, PregnancyTracker.clear_pregnancy.__name__)
def _cm_adjust_pregnancy_duration_on_pregnancy_end(original, self, *_, **__) -> Any:
    pregnancy_commodity_type = self.PREGNANCY_COMMODITY_MAP.get(self._sim_info.species)
    tracker = self._sim_info.get_tracker(pregnancy_commodity_type)
    if tracker is not None:
        stat = tracker.get_statistic(pregnancy_commodity_type, add=True)
        if stat is not None:
            stat.remove_statistic_modifier(CMSettingUtils.get_pregnancy_speed_modifier())
            stat.add_statistic_modifier(PregnancyTracker.PREGNANCY_RATE)
    return original(self, *_, **__)
