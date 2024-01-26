"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_name.operations.first_name import CMChangeFirstNameOp
from controlmenu.dialogs.modify_sim_data.modify_name.operations.last_name import CMChangeLastNameOp
from controlmenu.dialogs.modify_sim_data.modify_name.operations.pronouns_dialog import CMModifyPronounsOp
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifyNameDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_name_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.NAME

    # noinspection PyMissingOrEmptyDocstring
    @property
    def description(self) -> int:
        return CMSimControlMenuStringId.CHANGE_THE_NAME_OF_A_SIM

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
                'ChangeFirstName',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.FIRST_NAME
                ),
                on_chosen=lambda *_, **__: _operation_run(CMChangeFirstNameOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ChangeLastName',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.LAST_NAME
                ),
                on_chosen=lambda *_, **__: _operation_run(CMChangeLastNameOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ChangePronouns',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.PRONOUNS
                ),
                on_chosen=lambda *_, **__: _operation_run(CMModifyPronounsOp())
            )
        )
        return True
