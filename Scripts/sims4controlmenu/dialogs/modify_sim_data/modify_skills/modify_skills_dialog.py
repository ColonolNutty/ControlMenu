"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
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
from sims4controlmenu.dialogs.modify_sim_data.modify_skills.enums.string_ids import S4CMSimModifySkillsStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_skills.operations.max_all_skills import S4CMMaxAllSkillsSimOp
from sims4controlmenu.dialogs.modify_sim_data.modify_skills.operations.remove_all_skills import S4CMRemoveAllSkillsSimOp
from sims4controlmenu.dialogs.modify_sim_data.modify_skills.operations.set_skill_level import S4CMSetSkillLevelsSimOp
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMModifySkillsDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_skills_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMSimModifySkillsStringId.MODIFY_SKILLS

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: S4CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        if S4CMSetSkillLevelsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'SetSkillLevels',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimModifySkillsStringId.SET_SKILL_LEVELS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMSetSkillLevelsSimOp())
                )
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'MaxAllSkills',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimModifySkillsStringId.MAX_ALL_SKILLS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMMaxAllSkillsSimOp())
                )
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveAllSkills',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimModifySkillsStringId.REMOVE_ALL_SKILLS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMRemoveAllSkillsSimOp())
                )
            )
        return True
