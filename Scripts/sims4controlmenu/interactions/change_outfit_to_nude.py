"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu.settings.setting_utils import S4CMSettingUtils


class S4CMChangeOutfitToNudeInteraction(CommonImmediateSuperInteraction):
    """S4CMChangeOutfitToNudeInteraction(*_, **__)

    Show a dialog to change a Sim into their bathing outfit.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_change_outfit_to_nude'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not S4CMSettingUtils.is_sim_allowed_to_perform_adult_sim_operations(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is not enabled for interactions.')
            return TestResult.NONE
        if CommonOutfitUtils.is_wearing_bathing_outfit(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is already wearing their bathing outfit.')
            return TestResult.NONE
        cls.get_log().debug('Success, can Change Outfit To Nude.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        CommonOutfitUtils.set_current_outfit(target_sim_info, (OutfitCategory.BATHING, 0))
        return True
