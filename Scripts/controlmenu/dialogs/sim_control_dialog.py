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
from controlmenu.dialogs.game_world_dialog.modify_game_world_data_dialog import CMModifyGameWorldDataDialog
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.modify_sim_data_dialog import CMModifySimDataDialog
from controlmenu.enums.string_identifiers import CMStringId


class CMSimControlDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_sim_control_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMStringId.CONTROL_MENU

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_previous_button(self) -> bool:
        return False

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
                'ModifySimData',
                None,
                CommonDialogResponseOptionContext(
                    CMStringId.MODIFY_SIM_DATA
                ),
                on_chosen=lambda *_, **__: CMModifySimDataDialog(self._sim_info, on_previous=reopen).open()
            )
        )
        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyGameWorldData',
                None,
                CommonDialogResponseOptionContext(
                    CMStringId.MODIFY_GAME_WORLD_DATA
                ),
                on_chosen=lambda *_, **__: CMModifyGameWorldDataDialog(self._sim_info, on_previous=reopen).open()
            )
        )
        return True
