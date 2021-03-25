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
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.modinfo import ModInfo


class S4CMTeleportSimToActiveSimLocationInteraction(CommonImmediateSuperInteraction):
    """S4CMTeleportSimToActiveSimLocationInteraction(*_, **__)

    Teleport the Target Sim to the Active Sim location.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_teleport_sim_to_active_sim_location'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target was invalid.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_target)
        active_sim_location = CommonSimLocationUtils.get_location(sim_info)
        if active_sim_location is None:
            cls.get_log().debug('Failed, No location for active Sim.')
            return TestResult.NONE
        cls.get_log().debug('Success, can teleport.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        CommonSimSpawnUtils.hard_reset(target_sim_info, ResetReason.RESET_EXPECTED, source=interaction_sim, cause='S4CM: Teleporting Sim')
        active_sim_location = CommonSimLocationUtils.get_location(sim_info)
        return CommonSimLocationUtils.set_location(target_sim_info, active_sim_location)
