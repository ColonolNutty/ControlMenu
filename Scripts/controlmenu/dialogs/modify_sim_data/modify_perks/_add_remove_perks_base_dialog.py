"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple

from controlmenu.dialogs.modify_sim_data.modify_perks.operations._perk_modify_base import CMPerkModifyOp
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMAddRemovePerksDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_add_remove_perks_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def per_page(self) -> int:
        return 5

    def _get_operations(self) -> Tuple[CMPerkModifyOp]:
        raise NotImplementedError()

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(_operation: CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            _operation.run(self._sim_info, on_completed=_on_operation_complete)

        for operation in self._get_operations():
            if not operation.can_run_with_sim(self._sim_info):
                continue

            def _run_op(_operation_to_run) -> Callable[..., None]:
                return lambda *_, **__: _operation_run(_operation_to_run)

            option_dialog.add_option(
                CommonDialogButtonOption(
                    operation.title,
                    None,
                    CommonDialogResponseOptionContext(
                        operation.title,
                    ),
                    on_chosen=_run_op(operation)
                ),
            )
        return True
