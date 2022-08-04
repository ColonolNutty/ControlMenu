"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMSkeletonAddOp(CMSingleSimOperation):
    """Add the Skeleton Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_skeleton'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_skeleton(sim_info):
            on_completed(False)
            return False
        # loot_Skeleton_Add
        add_loot_id = 175969
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)
        on_completed(result)
        return result


class CMSkeletonRemoveOp(CMSingleSimOperation):
    """Remove the Skeleton Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_skeleton'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_skeleton(sim_info):
            on_completed(False)
            return False
        # loot_Skeleton_Remove
        remove_loot_id = 175975
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(remove_loot_id, sim_info)
        on_completed(result)
        return result

