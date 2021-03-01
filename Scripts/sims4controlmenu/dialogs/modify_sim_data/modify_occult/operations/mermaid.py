"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from event_testing.resolver import SingleSimResolver
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.sim_operation import S4CMSimOperation


class S4CMMermaidOp(S4CMSimOperation):
    """Turn a Sim into a Mermaid."""

    # noinspection PyMissingOrEmptyDocstring
    def add(self, sim_info: SimInfo) -> bool:
        if CommonOccultUtils.is_mermaid(sim_info):
            return False
        # loot_Mermaid_DebugAdd
        add_loot_id = 205399
        add_loot_action = CommonResourceUtils.load_instance(Types.ACTION, add_loot_id)
        if add_loot_action is None:
            return False
        add_loot_action.apply_to_resolver(SingleSimResolver(sim_info))
        return True

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, sim_info: SimInfo) -> bool:
        if not CommonOccultUtils.is_mermaid(sim_info):
            return False
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        trait_ids: Tuple[int] = (
            CommonTraitId.OCCULT_MERMAID_MERMAID_FORM,
            CommonTraitId.OCCULT_MERMAID_TYAE,
            CommonTraitId.OCCULT_MERMAID,
        )
        CommonTraitUtils.remove_trait(sim_info, *trait_ids)
        return True

