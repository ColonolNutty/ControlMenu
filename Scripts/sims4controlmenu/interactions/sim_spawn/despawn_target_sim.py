"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from event_testing.results import TestResult
from interactions.context import InteractionContext
from objects.object_enums import ResetReason
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.modinfo import ModInfo


class S4CMDespawnTargetSimInteraction(CommonImmediateSuperInteraction):
    """S4CMDespawnTargetSimInteraction(*_, **__)

    Despawn the target Sim.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_despawn_sim'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target was invalid.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if CommonHouseholdUtils.get_household_id(target_sim_info) == CommonHouseholdUtils.get_active_household_id():
            cls.get_log().debug('Failed, cannot despawn active household Sims.')
            return TestResult.NONE
        cls.get_log().debug('Success, can despawn target Sim.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        CommonSimSpawnUtils.hard_reset(target_sim_info, reset_reason=ResetReason.RESET_EXPECTED, source=interaction_sim, cause='S4CM: Preparing To Despawn Sim')
        CommonSimSpawnUtils.despawn_sim(target_sim_info, source=CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(interaction_sim)), cause='S4CM: Despawn Sim')
        return True
