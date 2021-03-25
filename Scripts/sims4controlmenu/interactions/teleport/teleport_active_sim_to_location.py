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
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.modinfo import ModInfo


class S4CMTeleportActiveSimToLocationInteraction(CommonImmediateSuperInteraction):
    """S4CMTeleportActiveSimToLocationInteraction(*_, **__)

    Teleport the active Sim to the target location.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_teleport_active_sim_to_location'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None:
            cls.get_log().debug('Failed, Target was invalid.')
            return TestResult.NONE
        location = CommonObjectLocationUtils.get_location(interaction_target)
        if location is None:
            cls.get_log().debug('Failed, No Location for target.')
            return TestResult.NONE
        cls.get_log().debug('Success, can teleport.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        location = CommonObjectLocationUtils.get_location(interaction_target)
        CommonSimSpawnUtils.hard_reset(sim_info, ResetReason.RESET_EXPECTED, source=interaction_sim, cause='S4CM: Teleporting Sim')
        return CommonSimLocationUtils.set_location(sim_info, location)
