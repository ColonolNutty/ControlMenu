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
from sims4controlmenu.dialogs.game_world_dialog.enums.string_identifiers import S4CMGameWorldControlMenuStringId
from sims4controlmenu.dialogs.game_world_dialog.game_clock.modify_game_clock_dialog import S4CMModifyGameClockDialog
from sims4controlmenu.dialogs.game_world_dialog.lots.modify_lot_data_dialog import S4CMModifyLotDataDialog
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
        reopen: Callable[[], None],
        **__
    ) -> bool:
        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyGameClock',
                None,
                CommonDialogResponseOptionContext(
                    S4CMGameWorldControlMenuStringId.MODIFY_GAME_CLOCK,
                ),
                on_chosen=lambda *_, **__: S4CMModifyGameClockDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyLotData',
                None,
                CommonDialogResponseOptionContext(
                    S4CMGameWorldControlMenuStringId.MODIFY_LOT_DATA,
                ),
                on_chosen=lambda *_, **__: S4CMModifyLotDataDialog(self._sim_info, on_previous=reopen).open()
            )
        )
        return True
