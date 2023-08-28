"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_currency.operations.add_simoleons import CMAddSimoleonsOp
from controlmenu.dialogs.modify_sim_data.modify_currency.operations.remove_simoleons import CMRemoveSimoleonsOp
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifyCurrencyDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_currency_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.CURRENCY

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
                'AddSimoleons',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.ADD_SIMOLEONS
                ),
                on_chosen=lambda *_, **__: _operation_run(CMAddSimoleonsOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'RemoveSimoleons',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.REMOVE_SIMOLEONS
                ),
                on_chosen=lambda *_, **__: _operation_run(CMRemoveSimoleonsOp())
            )
        )
        return True
