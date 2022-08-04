"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from bucks.bucks_enums import BucksType
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_bucks_types import CommonBucksType
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_bucks_utils import CommonSimBucksUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMWitchAddOp(CMSingleSimOperation):
    """Add the Witch Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_witch'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_witch(sim_info):
            on_completed(False)
            return False
        # loot_WitchOccult_AddOccult
        add_loot_id = 215080
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)
        on_completed(result)
        return result


class CMWitchRemoveOp(CMSingleSimOperation):
    """Remove the Witch Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_witch'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_witch(sim_info):
            on_completed(False)
            return False
        # loot_WitchOccult_RemoveOccult
        remove_loot_id = 215274
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_duo_sims(remove_loot_id, sim_info, sim_info)
        if result:
            CommonSimBucksUtils.remove_all_perks(sim_info, CommonBucksType.WITCH_PERK, reason='Witch removed', remove_perk_points=True)
        on_completed(result)
        return result

