"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from event_testing.resolver import Resolver
from interactions.utils.loot import LootActions


class CommonLootActionUtils:
    """Utilities for applying Loot Actions."""
    @staticmethod
    def apply_loot_action(loot_action_id: int, resolver: Resolver) -> bool:
        """apply_loot_action(loot_action_id, resolver)

        Apply a loot action using the specified resolver.

        :param loot_action_id: The decimal identifier of a loot action.
        :type loot_action_id: int
        :param resolver: A resolver used in various ways by loot actions. One example of a resolver is a SingleSimResolver, which will attempt to apply the loot actions to a single Sim.
        :type resolver: Resolver
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        loot_action = CommonLootActionUtils.load_loot_action_by_id(loot_action_id)
        if loot_action is None:
            return False
        loot_action.apply_to_resolver(resolver)
        return True

    @staticmethod
    def load_loot_action_by_id(loot_action_id: int) -> Union[LootActions, None]:
        """load_loot_action_by_id(loot_action_id)

        Load an instance of a Loot Action by its decimal identifier.

        :param loot_action_id: The decimal identifier of a Loot Action.
        :type loot_action_id: int
        :return: An instance of a Loot Action matching the decimal identifier or None if not found.
        :rtype: Union[LootActions, None]
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.ACTION, loot_action_id)
