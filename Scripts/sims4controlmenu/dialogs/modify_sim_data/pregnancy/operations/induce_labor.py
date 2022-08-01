"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.enums.string_identifiers import S4CMStringId


class S4CMInduceLaborOp(S4CMSingleSimOperation):
    """Induce a pregnant Sim to give birth."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_induce_labor'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonSimPregnancyUtils.is_pregnant(sim_info):
            on_completed(CommonExecutionResult(False, reason=f'{sim_info} is not pregnant.'))
            return False
        buff_id = CommonSimPregnancyUtils.get_in_labor_buff(sim_info)
        if buff_id == -1:
            on_completed(CommonExecutionResult(False, reason=f'No in labor buff found for {sim_info}'))
            return False
        result = CommonBuffUtils.add_buff(sim_info, buff_id, buff_reason=S4CMStringId.DEBUG_COMMAND)
        on_completed(result)
        return result.result
