"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_motives.enums.string_ids import CMSimModifyMotivesStringId
from controlmenu.dialogs.modify_sim_data.modify_motives.operations.max_all_motives import CMMaxAllMotivesSimOp
from controlmenu.dialogs.modify_sim_data.modify_motives.operations.max_world_motives import CMMaxWorldMotivesSimOp
from controlmenu.dialogs.modify_sim_data.modify_motives.operations.modify_motives import CMModifyMotivesSimOp
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifyMotivesDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_motives_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimModifyMotivesStringId.MOTIVES

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

        option_dialog.add_option(
            CommonDialogButtonOption(
                'MaxAllMotives',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyMotivesStringId.MAX_ALL_MOTIVES,
                    subtext_identifier=CMSimModifyMotivesStringId.MAX_ALL_MOTIVES_DESCRIPTION
                ),
                on_chosen=lambda *_, **__: _operation_run(CMMaxAllMotivesSimOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'MaxWorldMotives',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyMotivesStringId.MAX_WORLD_MOTIVES,
                    subtext_identifier=CMSimModifyMotivesStringId.MAX_ALL_MOTIVES_DESCRIPTION
                ),
                on_chosen=lambda *_, **__: _operation_run(CMMaxWorldMotivesSimOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyMotives',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyMotivesStringId.MODIFY_MOTIVES
                ),
                on_chosen=lambda *_, **__: _operation_run(CMModifyMotivesSimOp())
            )
        )
        return True
