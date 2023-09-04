"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_statistics.operations.set_commodity_values import \
    CMSetCommodityValuesSimOp
from controlmenu.dialogs.modify_sim_data.modify_statistics.operations.set_statistic_values import \
    CMSetStatisticValuesSimOp
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifyStatisticsDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_statistics_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.STATISTICS

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
                'SetStatisticValues',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.SET_STATISTIC_VALUES
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetStatisticValuesSimOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetCommodityValues',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.SET_COMMODITY_VALUES
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetCommodityValuesSimOp())
            )
        )
        return True
