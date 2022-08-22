"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from controlmenu.modinfo import ModInfo


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PregnancyTracker, PregnancyTracker.create_offspring_data.__name__)
def _cm_prevent_loss_of_offspring_data_on_birth(original, self, *_, **__) -> None:
    if self._offspring_data:
        return
    return original(self, *_, **__)
