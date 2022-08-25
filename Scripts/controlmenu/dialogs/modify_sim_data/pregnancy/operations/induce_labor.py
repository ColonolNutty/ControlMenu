"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMInduceLaborOp(CMSingleSimOperation):
    """Induce a pregnant Sim to give birth."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_induce_labor'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonSimPregnancyUtils.is_pregnant(sim_info):
            on_completed(CommonExecutionResult(False, reason=f'{sim_info} is not pregnant.'))
            return False
        result = CommonSimPregnancyUtils.induce_labor_in_sim(sim_info)
        if result:
            on_completed(CommonExecutionResult.TRUE)
        else:
            on_completed(CommonExecutionResult(False, reason=f'Failed to induce labor in {sim_info}'))
        return result
