"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.dialogs.game_world_dialog.enums.string_identifiers import S4CMGameWorldControlMenuStringId
from sims4controlmenu.dialogs.game_world_dialog.lots.operations.clear_lot_changes import S4CMClearLotChangesOp
from sims4controlmenu.dialogs.game_world_dialog.lots.operations.set_maximum_sims_per_lot import \
    S4CMSetMaximumSimsPerLotOp
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.settings.setting_utils import S4CMSettingUtils


class S4CMModifyLotDataDialog(S4CMSimControlDialogBase):
    """ The control dialog for Lots. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_lot_data_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMGameWorldControlMenuStringId.MODIFY_LOT_DATA

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
                'SetMaximumSimsPerLot',
                None,
                CommonDialogResponseOptionContext(
                    CommonStringId.STRING_COLON_SPACE_STRING,
                    text_tokens=(
                        S4CMGameWorldControlMenuStringId.MAXIMUM_SIMS_PER_LOT_NAME,
                        str(S4CMSettingUtils.get_maximum_number_of_sims_per_lot()),
                    )
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMSetMaximumSimsPerLotOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ClearLotChanges',
                None,
                CommonDialogResponseOptionContext(
                    S4CMGameWorldControlMenuStringId.CLEAR_LOT_CHANGES
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMClearLotChangesOp())
            )
        )
        return True
