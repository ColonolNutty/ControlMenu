"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4controlmenu.commonlib.utils.common_sim_loot_utils import CommonSimLootActionUtils
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMWitchAddOp(S4CMSingleSimOperation):
    """Add the Witch Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_witch(sim_info):
            on_completed(False)
            return False
        # loot_WitchOccult_AddOccult
        add_loot_id = 215080
        result = CommonSimLootActionUtils.apply_loot_action_to_sim(add_loot_id, sim_info)
        on_completed(result)
        return result


class S4CMWitchRemoveOp(S4CMSingleSimOperation):
    """Remove the Witch Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_witch(sim_info):
            on_completed(False)
            return False
        # loot_WitchOccult_RemoveOccult
        remove_loot_id = 215274
        result = CommonSimLootActionUtils.apply_loot_action_to_sims_duo(remove_loot_id, sim_info, sim_info)
        on_completed(result)
        return result

