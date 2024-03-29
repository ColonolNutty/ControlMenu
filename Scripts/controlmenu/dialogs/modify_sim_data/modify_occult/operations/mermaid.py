"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Callable
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMMermaidAddOp(CMSingleSimOperation):
    """Add the Mermaid Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_mermaid'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_mermaid(sim_info):
            on_completed(CommonExecutionResult(False, reason=f'{sim_info} is already a mermaid.'))
            return False
        # loot_Mermaid_DebugAdd
        add_loot_id = 205399
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)
        on_completed(CommonExecutionResult(result))
        return result


class CMMermaidRemoveOp(CMSingleSimOperation):
    """Remove the Mermaid Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_mermaid'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_mermaid(sim_info):
            on_completed(CommonExecutionResult(False, reason=f'{sim_info} is not a mermaid.'))
            return False
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        trait_ids: Tuple[CommonTraitId, ...] = (
            CommonTraitId.OCCULT_MERMAID_MERMAID_FORM,
            CommonTraitId.OCCULT_MERMAID_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TEMPORARY_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TYAE,
            CommonTraitId.OCCULT_MERMAID,
        )
        result = CommonTraitUtils.remove_trait(sim_info, *trait_ids)
        on_completed(result)
        return result.result
