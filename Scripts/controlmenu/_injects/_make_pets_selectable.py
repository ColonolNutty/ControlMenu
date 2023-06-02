"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from controlmenu.modinfo import ModInfo
from server.client import SelectableSims
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SelectableSims, '__init__')
def _cm_make_pets_selectable_by_default(original, self: SelectableSims, *_, **__):
    original_result = original(self, *_, **__)
    self._can_select_pets = True
    return original_result
