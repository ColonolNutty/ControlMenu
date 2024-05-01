"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from interactions.context import InteractionContext
from objects.object_enums import ResetReason
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.objects.common_object_spawn_utils import CommonObjectSpawnUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.modinfo import ModInfo


class CMTeleportToActiveSimLocationInteraction(CommonImmediateSuperInteraction):
    """CMTeleportToActiveSimLocationInteraction(*_, **__)

    Teleport the Target to the Active Sim location.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_teleport_to_active_sim_location'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        if interaction_target is None:
            cls.get_log().debug('Failed, Target was invalid.')
            return CommonTestResult.NONE
        if CommonTypeUtils.is_land(interaction_target) or CommonTypeUtils.is_water(interaction_target):
            cls.get_log().format_with_message('Failed, Target was land or water.', target=interaction_target)
            return CommonTestResult.NONE

        source_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        source_location = CommonSimLocationUtils.get_location(source_sim_info)
        if source_location is None:
            cls.get_log().debug('Failed, No location for Source Sim.')
            return CommonTestResult.NONE

        if CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
            target_location = CommonSimLocationUtils.get_location(target_sim_info)
        else:
            target_location = CommonObjectLocationUtils.get_location(interaction_target)

        if target_location is None:
            cls.get_log().debug('Failed, No location for target Object.')
            return CommonTestResult.NONE
        cls.get_log().debug('Success, can teleport.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        source_sim_info = CommonSimUtils.get_sim_info(interaction_sim)

        if CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
            CommonSimSpawnUtils.hard_reset(target_sim_info, ResetReason.RESET_EXPECTED, source=interaction_sim, cause='CM: Teleporting Sim')
            source_sim_location = CommonSimLocationUtils.get_location(source_sim_info)
            return CommonSimLocationUtils.set_location(target_sim_info, source_sim_location)
        else:
            CommonObjectSpawnUtils.hard_reset(interaction_target, ResetReason.RESET_EXPECTED, source=interaction_sim, cause='CM: Teleporting Object')
            source_sim_location = CommonSimLocationUtils.get_location(source_sim_info)
            return CommonObjectLocationUtils.set_location(interaction_target, source_sim_location)
