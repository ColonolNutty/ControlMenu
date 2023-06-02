"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Any
from controlmenu.modinfo import ModInfo
from server.client import Client
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class CMDebugRemoveControlOfSimInteraction(CommonImmediateSuperInteraction):
    """ Handles the Remove Control of Sim interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_debug_remove_control_of_sim'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Target is not a Sim.')
            return CommonTestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        client = services.get_first_client()
        if target_sim_info not in client.selectable_sims:
            cls.get_log().format_with_message('Failed, Target Sim is not selectable.', target_sim=target_sim_info)
            return CommonTestResult.NONE
        if CommonHouseholdUtils.is_part_of_active_household(target_sim_info):
            cls.get_log().format_with_message('Failed, Target Sim is part of the active household. We do not want to remove them via this function.', target_sim=target_sim_info)
            return CommonTestResult.NONE
        cls.get_log().debug('Success, can remove control of the Target Sim.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        client: Client = services.get_first_client()
        client.remove_selectable_sim_info(target_sim_info)
        return True
