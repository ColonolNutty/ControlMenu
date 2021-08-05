"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Callable

from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMAlienAddOp(S4CMSingleSimOperation):
    """Add the Alien Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_modify_alien'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_alien(sim_info):
            on_completed(False)
            return False
        loot_action_ids: Tuple[int] = (
            # loot_Occult_AlienAdd
            103256,
            # loot_Occult_AlienSwitch
            103254
        )
        # noinspection PyPropertyAccess
        physique = sim_info.physique
        # noinspection PyPropertyAccess
        facial_attributes = sim_info.facial_attributes
        # noinspection PyPropertyAccess
        voice_pitch = sim_info.voice_pitch
        # noinspection PyPropertyAccess
        voice_actor = sim_info.voice_actor
        # noinspection PyPropertyAccess
        voice_effect = sim_info.voice_effect
        # noinspection PyPropertyAccess
        skin_tone = sim_info.skin_tone
        flags = sim_info.flags
        pelt_layers = None
        if hasattr(sim_info, 'pelt_layers'):
            # noinspection PyPropertyAccess
            pelt_layers = sim_info.pelt_layers
        base_trait_ids = None
        if hasattr(sim_info, 'base_trait_ids'):
            base_trait_ids = list(sim_info.base_trait_ids)
        # noinspection PyPropertyAccess
        genetic_data_b = sim_info.genetic_data
        if hasattr(genetic_data_b, 'SerializeToString'):
            genetic_data_b = genetic_data_b.SerializeToString()
        result = CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)
        human_sim_info = sim_info.occult_tracker.get_occult_sim_info(OccultType.HUMAN)
        human_sim_info.physique = physique
        human_sim_info.facial_attributes = facial_attributes
        human_sim_info.voice_pitch = voice_pitch
        human_sim_info.voice_actor = voice_actor
        human_sim_info.voice_effect = voice_effect
        human_sim_info.skin_tone = skin_tone
        human_sim_info.flags = flags
        if pelt_layers is not None:
            human_sim_info.pelt_layers = pelt_layers
        if base_trait_ids is not None:
            human_sim_info.base_trait_ids = list(base_trait_ids)
        if hasattr(human_sim_info.genetic_data, 'MergeFromString'):
            human_sim_info.genetic_data.MergeFromString(genetic_data_b)
        else:
            human_sim_info.genetic_data = genetic_data_b
        on_completed(True)
        return result


class S4CMAlienRemoveOp(S4CMSingleSimOperation):
    """Remove the Alien Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_modify_alien'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_alien(sim_info):
            on_completed(False)
            return False
        sim_info.occult_tracker.remove_occult_type(OccultType.ALIEN)
        on_completed(True)
        return True
