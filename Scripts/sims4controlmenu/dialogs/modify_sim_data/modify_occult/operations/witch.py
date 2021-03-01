"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.resolver import SingleSimResolver, DoubleSimResolver
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.sim_operation import S4CMSimOperation


class S4CMWitchOp(S4CMSimOperation):
    """Turn a Sim into a Witch."""

    # noinspection PyMissingOrEmptyDocstring
    def add(self, sim_info: SimInfo) -> bool:
        if CommonOccultUtils.is_witch(sim_info):
            return False
        # loot_WitchOccult_AddOccult
        add_loot_id = 215080
        add_loot_action = CommonResourceUtils.load_instance(Types.ACTION, add_loot_id)
        if add_loot_action is None:
            return False
        add_loot_action.apply_to_resolver(SingleSimResolver(sim_info))
        return True

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, sim_info: SimInfo) -> bool:
        if not CommonOccultUtils.is_witch(sim_info):
            return False
        # loot_WitchOccult_RemoveOccult
        remove_loot_id = 215274
        remove_loot_action = CommonResourceUtils.load_instance(Types.ACTION, remove_loot_id)
        if remove_loot_action is None:
            return False
        remove_loot_action.apply_to_resolver(DoubleSimResolver(sim_info, sim_info))
        return True

