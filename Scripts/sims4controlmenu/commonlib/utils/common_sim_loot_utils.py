"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from event_testing.resolver import SingleSimResolver, DoubleSimResolver
from sims.sim_info import SimInfo
from sims4controlmenu.commonlib.utils.common_loot_utils import CommonLootActionUtils


class CommonSimLootActionUtils:
    """Utilities for applying Loot Actions."""
    @staticmethod
    def apply_loot_action_to_sim(loot_action_id: int, sim_info: SimInfo) -> bool:
        """apply_loot_action_to_sim(loot_action_id, sim_info)

        Apply a loot action to a Sim.

        :param loot_action_id: The decimal identifier of a loot action.
        :type loot_action_id: int
        :param sim_info: The Sim to apply loot actions to.
        :type sim_info: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        return CommonLootActionUtils.apply_loot_action(loot_action_id, SingleSimResolver(sim_info))

    @staticmethod
    def apply_loot_actions_to_sim(loot_action_ids: Tuple[int], sim_info: SimInfo) -> bool:
        """apply_loot_actions_to_sim(loot_action_ids, sim_info)

        Apply loot actions to a Sim.

        :param loot_action_ids: A collection of decimal identifier for loot actions.
        :type loot_action_ids: Tuple[int]
        :param sim_info: The Sim to apply loot actions to.
        :type sim_info: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        all_success = True
        for loot_action_id in loot_action_ids:
            if not CommonSimLootActionUtils.apply_loot_action_to_sim(loot_action_id, sim_info):
                all_success = False
        return all_success

    @staticmethod
    def apply_loot_action_to_sims_duo(loot_action_id: int, source_sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """apply_loot_action_to_sims_duo(loot_action_id, source_sim_info, target_sim_info)

        Apply a loot action using two Sims.

        :param loot_action_id: The decimal identifier of a loot action.
        :type loot_action_id: int
        :param source_sim_info: The Sim to be considered as the Actor for the loot action.
        :type source_sim_info: SimInfo
        :param target_sim_info: The Sim to be considered as the TargetSim for the loot action.
        :type target_sim_info: SimInfo
        :return: True, if the loot action applied successfully. False, if not.
        :rtype: bool
        """
        return CommonLootActionUtils.apply_loot_action(loot_action_id, DoubleSimResolver(source_sim_info, target_sim_info))

    @staticmethod
    def apply_loot_actions_to_sims_duo(loot_action_ids: Tuple[int], source_sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """apply_loot_actions_to_sims_duo(loot_action_ids, source_sim_info, target_sim_info)

        Apply loot actions using two Sims.

        :param loot_action_ids: A collection of decimal identifier for loot actions.
        :type loot_action_ids: Tuple[int]
        :param source_sim_info: The Sim to be considered as the Actor for the loot action.
        :type source_sim_info: SimInfo
        :param target_sim_info: The Sim to be considered as the TargetSim for the loot action.
        :type target_sim_info: SimInfo
        :return: True, if all loot actions applied successfully. False, if not.
        :rtype: bool
        """
        all_success = True
        for loot_action_id in loot_action_ids:
            if not CommonLootActionUtils.apply_loot_action(loot_action_id, DoubleSimResolver(source_sim_info, target_sim_info)):
                all_success = False
        return all_success
