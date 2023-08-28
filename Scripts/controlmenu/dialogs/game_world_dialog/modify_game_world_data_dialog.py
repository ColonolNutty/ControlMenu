"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.game_world_dialog.weather.manage_weather_dialog import CMManageWeatherDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.game_world_dialog.enums.string_identifiers import CMGameWorldControlMenuStringId
from controlmenu.dialogs.game_world_dialog.game_clock.modify_game_clock_dialog import CMModifyGameClockDialog
from controlmenu.dialogs.game_world_dialog.lots.modify_lot_data_dialog import CMModifyLotDataDialog
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.enums.string_identifiers import CMStringId


class CMModifyGameWorldDataDialog(CMSimControlDialogBase):
    """ The control dialog for the Game World. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_game_world_data_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMStringId.GAME_WORLD

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
                    CMGameWorldControlMenuStringId.GAME_CLOCK,
                ),
                on_chosen=lambda *_, **__: CMModifyGameClockDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyLotData',
                None,
                CommonDialogResponseOptionContext(
                    CMGameWorldControlMenuStringId.LOT_DATA,
                ),
                on_chosen=lambda *_, **__: CMModifyLotDataDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Weather',
                None,
                CommonDialogResponseOptionContext(
                    CMGameWorldControlMenuStringId.WEATHER,
                ),
                on_chosen=lambda *_, **__: CMManageWeatherDialog(self._sim_info, on_previous=reopen).open()
            )
        )
        return True
