"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.sim_control_dialog import CMSimControlDialog
from controlmenu.modinfo import ModInfo


class CMOpenSimControlMenuFromRelPanelInteraction(CommonImmediateSuperInteraction):
    """CMOpenSimControlMenuFromRelPanelInteraction(*_, **__)

    Show a dialog to control aspects of a Sim.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_open_sim_control_menu_from_rel_panel'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        if 'picked_item_ids' not in kwargs:
            cls.get_log().format_with_message('Failed, No picked targets.', kwargles=kwargs)
            return CommonTestResult.NONE
        cls.get_log().debug('Success, can open Sim control menu from rel panel.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        # noinspection PyUnresolvedReferences
        picked_sim_info = CommonSimUtils.get_sim_info(self.get_participant(ParticipantType.PickedSim))
        if picked_sim_info is None:
            return False
        CMSimControlDialog(picked_sim_info).open()
        return True
