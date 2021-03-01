"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.resolver import SingleSimResolver
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils


class S4CMBecomeVampireOp:
    """Turn a Sim into a Vampire."""
    def run(self, sim_info: SimInfo) -> bool:
        """Run the operation."""
        if CommonOccultUtils.is_vampire(sim_info):
            return False
        # loot_VampireCreation_NewVampire
        vampire_creation_loot_id = 149538
        loot_action = CommonResourceUtils.load_instance(Types.ACTION, vampire_creation_loot_id)
        if loot_action is None:
            return False
        loot_action.apply_to_resolver(SingleSimResolver(sim_info))
        return True
