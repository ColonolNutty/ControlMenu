"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims.sim_info import SimInfo
from sims4.localization import LocalizationHelperTuning
from sims4.resources import Types
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_integer_option import \
    CommonDialogInputIntegerOption
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_skill_utils import CommonSkillUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_skills.enums.string_ids import S4CMSimModifySkillsStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from statistics.skill import Skill


class S4CMSetSkillLevelsSimOp(S4CMSingleSimOperation):
    """Set Skill Levels of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_set_skill_levels_of_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        option_dialog = CommonChooseObjectOptionDialog(
            S4CMSimModifySkillsStringId.SET_SKILL_LEVELS,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_input_setting_changed(_skill: Skill, new_skill_level: int, outcome: CommonChoiceOutcome):
            if new_skill_level is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen()
                return
            self.log.format_with_message('Setting skill level for Sim.', _skill=_skill, new_skill_level=new_skill_level)
            CommonSimSkillUtils.set_current_skill_level(sim_info, _skill, new_skill_level)
            if new_skill_level == 0:
                CommonSimSkillUtils.remove_skill(sim_info, _skill)
            _reopen()

        skill_manager = CommonResourceUtils.get_instance_manager(Types.STATISTIC)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        for skill in skill_manager.get_ordered_types(only_subclasses_of=Skill):
            skill: Skill = skill
            skill_id = CommonSkillUtils.get_skill_id(skill)
            try:
                self.verbose_log.format_with_message('Attempting to display skill', skill=skill, skill_id=skill_id, sim=sim_info)
                if not skill.can_add(sim):
                    self.verbose_log.format_with_message('Failed, Skill is not allowed for Sim.', skill=skill, skill_id=skill_id, sim=sim_info)
                    continue
                if not CommonSimSkillUtils.has_skill(sim_info, skill_id):
                    current_skill_level = 0
                else:
                    current_skill_level = int(CommonSimSkillUtils.get_current_skill_level(sim_info, skill_id, use_effective_skill_level=False))
                stat_name = getattr(skill, 'stat_name', None)
                # noinspection PyUnresolvedReferences
                if stat_name and skill.stat_name.hash is not 0:
                    # noinspection PyUnresolvedReferences
                    display_name = skill.stat_name
                else:
                    display_name = LocalizationHelperTuning.get_raw_text(skill.__name__)

                # noinspection PyUnresolvedReferences
                if skill.hidden:
                    display_name = CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(display_name, S4CMSimControlMenuStringId.HIDDEN))

                display_name = CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.STRING_COLON_SPACE_STRING, tokens=(display_name, str(current_skill_level)))
                # noinspection PyUnresolvedReferences
                description = CommonLocalizationUtils.create_localized_string(skill.skill_description, tokens=(sim_info,))
                # noinspection PyUnresolvedReferences
                icon = skill.icon or CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                option_dialog.add_option(
                    CommonDialogInputIntegerOption(
                        self.mod_identity,
                        skill,
                        current_skill_level,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=icon,
                            is_enabled=self._is_skill_allowed_for_modification(sim_info, skill)
                        ),
                        dialog_description_identifier=S4CMSimModifySkillsStringId.ENTER_A_VALE_BETWEEN_MIN_AND_MAX_FOR_SKILL,
                        dialog_description_tokens=(str(0), str(int(skill.max_level)), str(current_skill_level)),
                        min_value=0,
                        max_value=int(skill.max_level),
                        on_chosen=_on_input_setting_changed
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display skill.', skill=skill, skill_name=skill.__name__, skill_id=skill_id, exception=ex)

        if not option_dialog.has_options():
            self.log.format_with_message('No skills available for the Sim!')
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    def _is_skill_allowed_for_modification(self, sim_info: SimInfo, skill: Skill) -> bool:
        skill_id = CommonSkillUtils.get_skill_id(skill)
        return sim_info is not None and skill_id is not None
