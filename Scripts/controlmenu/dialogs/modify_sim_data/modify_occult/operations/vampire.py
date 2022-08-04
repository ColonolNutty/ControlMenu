"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Callable

from sims.sim_info import SimInfo
from sims4communitylib.enums.common_bucks_types import CommonBucksType
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_bucks_utils import CommonSimBucksUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMVampireAddOp(CMSingleSimOperation):
    """Add the Vampire Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_vampire'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_vampire(sim_info):
            on_completed(False)
            return False
        # loot_VampireCreation_NewVampire
        add_loot_id = 149538
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)
        on_completed(result)
        return result


class CMVampireRemoveOp(CMSingleSimOperation):
    """Remove the Vampire Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_vampire'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_vampire(sim_info):
            on_completed(False)
            return False
        loot_action_ids: Tuple[int, ...] = (
            # loot_VampireCure_RemoveVampirism
            150170,
            # loot_Life_ResetProgress
            31238
        )
        result = CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)
        if result:
            CommonSimBucksUtils.remove_all_perks(sim_info, CommonBucksType.VAMPIRE_POWER, reason='Vampirism removed', remove_perk_points=True)
            CommonSimBucksUtils.remove_all_perks(sim_info, CommonBucksType.VAMPIRE_WEAKNESS, reason='Vampirism removed', remove_perk_points=True)
        on_completed(result)
        return result
