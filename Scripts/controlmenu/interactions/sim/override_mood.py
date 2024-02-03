"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from controlmenu.enums.buff_ids import CMBuffId
from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.moods_enum import CommonMoodId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class CMDebugOverrideMoodInteraction(CommonImmediateSuperInteraction):
    """ Handles the Override Mood interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_debug_override_mood'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Target is not a Sim.')
            return CommonTestResult.NONE
        cls.get_log().debug('Success, can gain control of Target Sim.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        self._show_mood_override_menu(target_sim_info)
        return True

    def _show_mood_override_menu(self, sim_info: SimInfo):
        def _reopen() -> None:
            self._show_mood_override_menu(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CMStringId.CHOOSE_MOOD_OVERRIDE,
            CMStringId.CHOOSE_MOOD_OVERRIDE_DESCRIPTION,
            title_tokens=(sim_info,),
            description_tokens=(sim_info,),
            mod_identity=self.mod_identity,
            per_page=20000
        )

        scared_mood_id = CMBuffId.MOOD_OVERRIDE_SCARED
        if CommonSpeciesUtils.is_dog(sim_info):
            scared_mood_id = CMBuffId.MOOD_OVERRIDE_SCARED_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            scared_mood_id = CMBuffId.MOOD_OVERRIDE_SCARED_CAT

        moods = {
            CommonMoodId.CONFIDENT: CMBuffId.MOOD_OVERRIDE_CONFIDENT,
            CommonMoodId.SLEEPING: CMBuffId.MOOD_OVERRIDE_SLEEPING,
            CommonMoodId.STRESSED: CMBuffId.MOOD_OVERRIDE_STRESSED,
            CommonMoodId.EMBARRASSED: CMBuffId.MOOD_OVERRIDE_EMBARRASSED,
            CommonMoodId.FLIRTY: CMBuffId.MOOD_OVERRIDE_FLIRTY,
            CommonMoodId.ENERGIZED: CMBuffId.MOOD_OVERRIDE_ENERGIZED,
            CommonMoodId.ANGRY: CMBuffId.MOOD_OVERRIDE_ANGRY,
            CommonMoodId.FOCUSED: CMBuffId.MOOD_OVERRIDE_FOCUSED,
            CommonMoodId.HAPPY: CMBuffId.MOOD_OVERRIDE_HAPPY,
            CommonMoodId.UNCOMFORTABLE: CMBuffId.MOOD_OVERRIDE_UNCOMFORTABLE,
            CommonMoodId.BORED: CMBuffId.MOOD_OVERRIDE_BORED,
            CommonMoodId.DAZED: CMBuffId.MOOD_OVERRIDE_DAZED,
            CommonMoodId.PLAYFUL: CMBuffId.MOOD_OVERRIDE_PLAYFUL,
            CommonMoodId.SAD: CMBuffId.MOOD_OVERRIDE_SAD,
            CommonMoodId.FINE: CMBuffId.MOOD_OVERRIDE_FINE,
            CommonMoodId.INSPIRED: CMBuffId.MOOD_OVERRIDE_INSPIRED,
            CommonMoodId.POSSESSED: CMBuffId.MOOD_OVERRIDE_POSSESSED,
            CommonMoodId.SCARED: scared_mood_id,
        }

        def _on_mood_chosen(____: str, mood_override: int):
            for buff_id in moods.values():
                CommonBuffUtils.remove_buff(sim_info, buff_id)

            if mood_override == 0:
                _reopen()
                return

            chosen_mood_buff_id = moods.get(mood_override, None)
            if chosen_mood_buff_id is None:
                _reopen()
                return

            CommonBuffUtils.add_buff(sim_info, chosen_mood_buff_id, buff_reason=CommonStringId.S4CL_BUFF_REASON_FROM_DEBUG)

        option_dialog.add_option(
            CommonDialogSelectOption(
                'None',
                0,
                CommonDialogOptionContext(
                    CommonStringId.S4CL_NONE,
                    0,
                ),
                on_chosen=_on_mood_chosen
            )
        )

        for mood_id in moods.keys():
            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(mood_id),
                    mood_id,
                    CommonDialogOptionContext(
                        mood_id.name,
                        0,
                    ),
                    on_chosen=_on_mood_chosen
                )
            )

        option_dialog.show(
            sim_info=sim_info
        )
