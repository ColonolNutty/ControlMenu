"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Callable, Any, Tuple

from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4.localization import LocalizationHelperTuning
from sims4.resources import Types
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_objects_option_dialog import CommonChooseObjectsOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import \
    CommonDialogObjectOption
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_skill_utils import CommonSkillUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.modify_skills.enums.string_ids import CMSimModifySkillsStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId
from statistics.skill import Skill


class CMRandomizeSelectedSkillsSimOp(CMSingleSimOperation):
    """Set All Skills of a Sim to a random level."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_selected_skills_random_for_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        option_dialog = CommonChooseObjectsOptionDialog(
            CMSimModifySkillsStringId.UNSELECT_SKILLS_YOU_DO_NOT_WANT_RANDOMIZED,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_submit(choices: Tuple[Skill]):
            if not choices:
                _on_close()
                return
            self._display_select_skills_dialog(sim_info, choices, on_completed=_reopen)

        from controlmenu.dialogs.modify_sim_data.modify_skills.operations.set_skill_level import \
            CMSetSkillLevelsSimOp
        skill_manager = CommonResourceUtils.get_instance_manager(Types.STATISTIC)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        for skill in skill_manager.get_ordered_types(only_subclasses_of=Skill):
            skill: Skill = skill
            skill_id = CommonSkillUtils.get_skill_id(skill)
            if skill_id is None:
                self.log.format_with_message('Missing skill id for Skill.', skill=skill)
                continue
            try:
                if not CMSetSkillLevelsSimOp()._is_skill_allowed_for_modification(sim_info, skill):
                    continue
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
                    skill_name = skill.__name__ or 'Unknown Skill Name'
                    skill_name = skill_name[0].upper() + skill_name[1:]
                    display_name = LocalizationHelperTuning.get_raw_text(skill_name)

                # noinspection PyUnresolvedReferences
                if skill.hidden:
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(display_name, CMSimControlMenuStringId.HIDDEN))

                display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_COLON_SPACE_STRING, tokens=(display_name, str(current_skill_level)))
                # noinspection PyUnresolvedReferences
                description = CommonLocalizationUtils.create_localized_string(skill.skill_description, tokens=(sim_info,))

                option_dialog.add_option(
                    CommonDialogObjectOption(
                        f'{skill}',
                        skill,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=CommonIconUtils.load_checked_square_icon(),
                            is_selected=True
                        )
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display skill.', skill=skill, skill_name=skill.__name__, skill_id=skill_id, exception=ex)

        if not option_dialog.has_options():
            self.log.format_with_message('No skills available for the Sim!')
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True, on_submit=_on_submit, max_selectable=option_dialog.option_count)
        return True

    def _display_select_skills_dialog(self, sim_info: SimInfo, selected_skills: Tuple[Skill], on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_close() -> None:
            on_completed(False)

        def _on_yes_selected(_: Any):
            sim = CommonSimUtils.get_sim_instance(sim_info)
            for skill in selected_skills:
                skill: Skill = skill
                skill_levels = tuple(range(0, skill.max_level + 1))
                chosen_skill_level = random.choice(skill_levels)
                if chosen_skill_level == 0:
                    if CommonSimSkillUtils.has_skill(sim_info, skill):
                        CommonSimSkillUtils.remove_skill(sim_info, skill)
                else:
                    CommonSimSkillUtils.set_current_skill_level(sim_info, skill, int(chosen_skill_level))

            CommonBasicNotification(
                CMSimModifySkillsStringId.RANDOMIZED_SKILL_LEVELS_OF_SIM_TITLE,
                CMSimModifySkillsStringId.RANDOMIZED_SKILL_LEVELS_OF_SIM_DESCRIPTION,
                title_tokens=(sim,),
                description_tokens=(sim,)
            ).show(icon=IconInfoData(obj_instance=sim))
            _on_close()

        def _on_no_selected(_: Any):
            _on_close()

        confirmation = CommonOkCancelDialog(
            CMStringId.CONFIRMATION,
            CMSimModifySkillsStringId.ARE_YOU_SURE_YOU_WANT_TO_RANDOMIZE_SELECTED_SKILLS_FOR_SIM,
            description_tokens=(CommonSimUtils.get_sim_instance(sim_info),),
            ok_text_identifier=CMStringId.YES,
            cancel_text_identifier=CMStringId.NO,
            mod_identity=self.mod_identity
        )
        confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)
        return True
