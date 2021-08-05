"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Callable

from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMVampireAddOp(S4CMSingleSimOperation):
    """Add the Vampire Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_modify_vampire'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_vampire(sim_info):
            on_completed(False)
            return False
        # loot_VampireCreation_NewVampire
        add_loot_id = 149538
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)
        on_completed(result)
        return result


class S4CMVampireRemoveOp(S4CMSingleSimOperation):
    """Remove the Vampire Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_modify_vampire'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_vampire(sim_info):
            on_completed(False)
            return False
        loot_action_ids: Tuple[int] = (
            # loot_VampireCure_RemoveVampirism
            150170,
            # loot_Life_ResetProgress
            31238
        )
        result = CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)
        on_completed(result)
        return result
