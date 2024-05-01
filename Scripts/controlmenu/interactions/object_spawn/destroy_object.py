"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from controlmenu.enums.string_identifiers import CMStringId
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_spawn_utils import CommonObjectSpawnUtils
from controlmenu.modinfo import ModInfo


class CMDestroyObjectInteraction(CommonImmediateSuperInteraction):
    """CMDestroyObjectInteraction(*_, **__)

    Destroy an Object.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_destroy_object'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        if interaction_target is None or CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().format_with_message('Failed, Target was invalid.', target=interaction_target)
            return CommonTestResult.NONE

        if not CommonTypeUtils.is_game_object(interaction_target)\
                or CommonTypeUtils.is_land(interaction_target)\
                or CommonTypeUtils.is_water(interaction_target):
            cls.get_log().format_with_message('Failed, Target was land, water, or not a game object.', target=interaction_target)
            return CommonTestResult.NONE
        cls.get_log().format_with_message('Success, can destroy Object.', target=interaction_target)
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        def _on_yes_selected(_: Any):
            CommonObjectSpawnUtils.schedule_object_for_destroy(interaction_target, source=self, cause='Destroying target of Control Menu Destroy.')

        def _on_no_selected(_: Any):
            return

        confirmation = CommonOkCancelDialog(
            CMStringId.CONFIRMATION,
            CMStringId.ARE_YOU_SURE_YOU_WANT_TO_DESTROY_THIS_OBJECT,
            ok_text_identifier=CMStringId.YES,
            cancel_text_identifier=CMStringId.NO,
            mod_identity=self.mod_identity
        )
        confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)
        return True
