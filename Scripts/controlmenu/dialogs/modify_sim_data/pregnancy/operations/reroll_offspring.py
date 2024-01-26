"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims.sim_info import SimInfo
from sims4.math import MAX_UINT32
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMRerollOffspringOp(CMSingleSimOperation):
    """Reroll the offspring of a pregnant Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_reroll_offspring'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonSimPregnancyUtils.is_pregnant(sim_info):
            on_completed(False)
            return False

        pregnancy_tracker: PregnancyTracker = sim_info.pregnancy_tracker
        if not pregnancy_tracker:
            on_completed(False)
            return False
        import random
        pregnancy_tracker._seed = random.randint(1, MAX_UINT32)
        pregnancy_tracker._offspring_data = []
        on_completed(True)
        return True
