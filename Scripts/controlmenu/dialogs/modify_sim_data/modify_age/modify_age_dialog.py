"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.set_age_length_multipliers_dialog import \
    CMSetAgeLengthMultipliersDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.set_age_dialog import CMSetAgeDialog


class CMModifyAgeDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_age_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.AGE

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
                'SetAge',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.SET_AGE
                ),
                on_chosen=lambda *_, **__: CMSetAgeDialog(self._sim_info, on_previous=reopen).open()
            )
        )
        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetAgeLengthMultipliers',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.SET_AGE_LENGTH_MULTIPLIERS
                ),
                on_chosen=lambda *_, **__: CMSetAgeLengthMultipliersDialog(self._sim_info, on_previous=reopen).open()
            )
        )
        return True
