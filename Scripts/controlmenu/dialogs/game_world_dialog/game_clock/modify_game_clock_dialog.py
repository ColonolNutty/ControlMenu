"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.game_world_dialog.enums.string_identifiers import CMGameWorldControlMenuStringId
from controlmenu.dialogs.game_world_dialog.game_clock.operations.set_clock_speed import CMSetClockSpeedOp
from controlmenu.dialogs.game_world_dialog.game_clock.operations.set_clock_speed_scale_multiplier import \
    CMSetClockSpeedScaleMultiplierOp
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase


class CMModifyGameClockDialog(CMSimControlDialogBase):
    """ The control dialog for the Game Clock. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_game_clock_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMGameWorldControlMenuStringId.GAME_CLOCK

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: Any):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(on_completed=_on_operation_complete)

        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetClockSpeed',
                None,
                CommonDialogResponseOptionContext(
                    CMGameWorldControlMenuStringId.SET_CLOCK_SPEED,
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetClockSpeedOp())
            )
        )
        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetClockSpeedScale',
                None,
                CommonDialogResponseOptionContext(
                    CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_SCALE,
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetClockSpeedScaleMultiplierOp())
            )
        )
        return True
