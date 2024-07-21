"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_whims.operations.add_whims import CMAddWhimsSimOp
from controlmenu.dialogs.modify_sim_data.modify_whims.operations.remove_whims import CMRemoveWhimsSimOp
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase


class CMModifyWhimsDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_whims_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.WHIMS

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

        if CMAddWhimsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'AddWhims',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.ADD_WHIMS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMAddWhimsSimOp())
                )
            )

        if CMRemoveWhimsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveWhims',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.REMOVE_WHIMS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMRemoveWhimsSimOp())
                )
            )

        return True
