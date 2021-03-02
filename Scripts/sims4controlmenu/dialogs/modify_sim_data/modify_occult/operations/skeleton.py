"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4controlmenu.commonlib.utils.common_sim_loot_utils import CommonSimLootActionUtils
from sims4controlmenu.dialogs.modify_sim_data.sim_operation import S4CMSingleSimOperation


class S4CMSkeletonAddOp(S4CMSingleSimOperation):
    """Add the Skeleton Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo) -> bool:
        if CommonOccultUtils.is_skeleton(sim_info):
            return False
        # loot_Skeleton_Add
        add_loot_id = 175969
        return CommonSimLootActionUtils.apply_loot_action_to_sim(add_loot_id, sim_info)


class S4CMSkeletonRemoveOp(S4CMSingleSimOperation):
    """Remove the Skeleton Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo) -> bool:
        if not CommonOccultUtils.is_skeleton(sim_info):
            return False
        # loot_Skeleton_Remove
        remove_loot_id = 175975
        return CommonSimLootActionUtils.apply_loot_action_to_sim(remove_loot_id, sim_info)

