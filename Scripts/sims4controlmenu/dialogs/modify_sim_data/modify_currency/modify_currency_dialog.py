"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
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
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_currency.operations.add_simoleons import S4CMAddSimoleonsOp
from sims4controlmenu.dialogs.modify_sim_data.modify_currency.operations.remove_simoleons import S4CMRemoveSimoleonsOp
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMModifyCurrencyDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_currency_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMSimControlMenuStringId.MODIFY_CURRENCY

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

        option_dialog.add_option(
            CommonDialogButtonOption(
                'AddSimoleons',
                None,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.ADD_SIMOLEONS
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMAddSimoleonsOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'RemoveSimoleons',
                None,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.REMOVE_SIMOLEONS
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMRemoveSimoleonsOp())
            )
        )
        return True
