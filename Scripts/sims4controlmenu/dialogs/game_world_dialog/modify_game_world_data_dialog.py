"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.dialogs.game_world_dialog.enums.string_identifiers import S4CMGameWorldControlMenuStringId
from sims4controlmenu.dialogs.game_world_dialog.game_clock.set_clock_speed_scale_multiplier import \
    S4CMSetClockSpeedScaleMultiplierOp
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.enums.string_identifiers import S4CMStringId


class S4CMModifyGameWorldDataDialog(S4CMSimControlDialogBase):
    """ The control dialog for the Game World. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_game_world_data_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMStringId.MODIFY_GAME_WORLD_DATA

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None]
    ) -> bool:
        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetClockSpeedScale',
                None,
                CommonDialogResponseOptionContext(
                    S4CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_SCALE,
                ),
                on_chosen=lambda *_, **__: None if S4CMSetClockSpeedScaleMultiplierOp().run(on_completed=lambda *_, **__: reopen()) else None
            )
        )
        return True
