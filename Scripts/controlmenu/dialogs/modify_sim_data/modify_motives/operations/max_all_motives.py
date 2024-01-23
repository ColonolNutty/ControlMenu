"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_motive_utils import CommonSimMotiveUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMMaxAllMotivesSimOp(CMSingleSimOperation):
    """Max the Motives of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_max_all_motives_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        CommonSimMotiveUtils.set_all_motives_max(sim_info)
        on_completed(True)
        return True
