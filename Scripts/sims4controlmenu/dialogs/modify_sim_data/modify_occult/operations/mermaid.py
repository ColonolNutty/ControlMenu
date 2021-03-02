"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4controlmenu.commonlib.utils.common_sim_loot_utils import CommonSimLootActionUtils
from sims4controlmenu.dialogs.modify_sim_data.sim_operation import S4CMSingleSimOperation


class S4CMMermaidAddOp(S4CMSingleSimOperation):
    """Add the Mermaid Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo) -> bool:
        if CommonOccultUtils.is_mermaid(sim_info):
            return False
        # loot_Mermaid_DebugAdd
        add_loot_id = 205399
        return CommonSimLootActionUtils.apply_loot_action_to_sim(add_loot_id, sim_info)


class S4CMMermaidRemoveOp(S4CMSingleSimOperation):
    """Remove the Mermaid Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo) -> bool:
        if not CommonOccultUtils.is_mermaid(sim_info):
            return False
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        trait_ids: Tuple[int] = (
            CommonTraitId.OCCULT_MERMAID_MERMAID_FORM,
            CommonTraitId.OCCULT_MERMAID_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TEMPORARY_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TYAE,
            CommonTraitId.OCCULT_MERMAID,
        )
        CommonTraitUtils.remove_trait(sim_info, *trait_ids)
        return True
