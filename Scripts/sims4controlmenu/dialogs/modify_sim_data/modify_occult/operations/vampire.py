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
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.sim_operation import S4CMSimOperation


class S4CMVampireOp(S4CMSimOperation):
    """Turn a Sim into a Vampire."""

    # noinspection PyMissingOrEmptyDocstring
    def add(self, sim_info: SimInfo) -> bool:
        if CommonOccultUtils.is_vampire(sim_info):
            return False
        # loot_VampireCreation_NewVampire
        vampire_creation_loot_id = 149538
        loot_action = CommonResourceUtils.load_instance(Types.ACTION, vampire_creation_loot_id)
        if loot_action is None:
            return False
        loot_action.apply_to_resolver(SingleSimResolver(sim_info))
        return True

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, sim_info: SimInfo) -> bool:
        if not CommonOccultUtils.is_vampire(sim_info):
            return False
        # loot_VampireCure_RemoveVampirism
        vampire_remove_loot_id = 150170
        remove_loot_action = CommonResourceUtils.load_instance(Types.ACTION, vampire_remove_loot_id)
        if remove_loot_action is None:
            return False
        remove_loot_action.apply_to_resolver(SingleSimResolver(sim_info))
        # loot_Life_ResetProgress
        reset_life_progress_loot_id = 31238
        reset_life_loot_action = CommonResourceUtils.load_instance(Types.ACTION, reset_life_progress_loot_id)
        if reset_life_loot_action is not None:
            reset_life_loot_action.apply_to_resolver(SingleSimResolver(sim_info))
        return True
