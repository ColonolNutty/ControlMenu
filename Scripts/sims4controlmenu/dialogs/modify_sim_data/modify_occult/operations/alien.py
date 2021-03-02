"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4controlmenu.commonlib.utils.common_sim_loot_utils import CommonSimLootActionUtils
from sims4controlmenu.dialogs.modify_sim_data.sim_operation import S4CMSingleSimOperation


class S4CMAlienAddOp(S4CMSingleSimOperation):
    """Add the Alien Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo) -> bool:
        if CommonOccultUtils.is_alien(sim_info):
            return False
        loot_action_ids: Tuple[int] = (
            # loot_Occult_AlienAdd
            103256,
            # loot_Occult_AlienSwitch
            103254
        )
        return CommonSimLootActionUtils.apply_loot_actions_to_sim(loot_action_ids, sim_info)


class S4CMAlienRemoveOp(S4CMSingleSimOperation):
    """Remove the Alien Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo) -> bool:
        if not CommonOccultUtils.is_alien(sim_info):
            return False
        loot_action_ids: Tuple[int] = (
            # loot_Occult_AlienSwitchOff
            103255,
            # loot_Occult_AlienRemove
            103257
        )
        return CommonSimLootActionUtils.apply_loot_actions_to_sim(loot_action_ids, sim_info)

