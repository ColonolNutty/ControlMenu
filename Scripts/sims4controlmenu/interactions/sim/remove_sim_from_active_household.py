"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4controlmenu.modinfo import ModInfo


class S4CMDebugRemoveSimFromActiveHouseholdInteraction(CommonImmediateSuperInteraction):
    """ Handle the interaction to Remove Sim From Active Household. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_debug_remove_sim_from_active_household'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Target is not a Sim.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not CommonHouseholdUtils.is_part_of_active_household(target_sim_info):
            cls.get_log().format_with_message('Failed, Target Sim is not a part of the Active Household.', target_sim=target_sim_info)
            return TestResult.NONE
        if CommonHouseholdUtils.get_number_of_sims_in_household_of_sim(CommonSimUtils.get_active_sim_info()) <= 1:
            cls.get_log().format_with_message('Failed, Target Sim is the last Sim in their household. They cannot be removed!', target_sim=target_sim_info)
            return TestResult.NONE
        cls.get_log().debug('Success, can remove Target Sim from the Active Household.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        return CommonHouseholdUtils.move_sim_to_household(target_sim_info)
