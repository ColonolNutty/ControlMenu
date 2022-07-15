"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.household import Household
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu.settings.setting_utils import S4CMSettingUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Household, 'free_slot_count')
def _cm_override_free_slot_count(original, self, *_, **__) -> int:
    self.MAXIMUM_SIZE = S4CMSettingUtils.get_maximum_household_size()
    return original(self, *_, **__)
