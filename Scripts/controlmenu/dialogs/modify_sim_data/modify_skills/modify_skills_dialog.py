"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.modify_skills.enums.string_ids import CMSimModifySkillsStringId
from controlmenu.dialogs.modify_sim_data.modify_skills.operations.max_all_skills import CMMaxAllSkillsSimOp
from controlmenu.dialogs.modify_sim_data.modify_skills.operations.randomize_all_skills import \
    CMRandomizeAllSkillsSimOp
from controlmenu.dialogs.modify_sim_data.modify_skills.operations.remove_all_skills import CMRemoveAllSkillsSimOp
from controlmenu.dialogs.modify_sim_data.modify_skills.operations.set_skill_level import CMSetSkillLevelsSimOp
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifySkillsDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_skills_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimModifySkillsStringId.MODIFY_SKILLS

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        if CMSetSkillLevelsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'SetSkillLevels',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimModifySkillsStringId.SET_SKILL_LEVELS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetSkillLevelsSimOp())
                )
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'MaxAllSkills',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimModifySkillsStringId.MAX_ALL_SKILLS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMMaxAllSkillsSimOp())
                )
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RandomizeAllSkills',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimModifySkillsStringId.RANDOMIZE_SKILL_LEVELS_TITLE
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMRandomizeAllSkillsSimOp())
                )
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveAllSkills',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimModifySkillsStringId.REMOVE_ALL_SKILLS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMRemoveAllSkillsSimOp())
                )
            )
        return True
