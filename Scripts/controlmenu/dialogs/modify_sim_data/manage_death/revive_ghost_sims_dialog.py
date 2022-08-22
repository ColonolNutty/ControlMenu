"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from controlmenu.dialogs.modify_sim_data.manage_death.operations.revive_all_ghost_sims import CMReviveAllGhostSimsOp
from controlmenu.dialogs.modify_sim_data.manage_death.operations.revive_specific_ghost_sims import CMReviveSpecificGhostSimsOp
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CMReviveGhostSimsDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_revive_ghost_sims'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.REVIVE_GHOSTS

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_previous_button(self) -> bool:
        return False

    # noinspection PyMissingOrEmptyDocstring
    @property
    def description(self) -> Union[int, str, LocalizedString]:
        number_of_ghosts = len(tuple(CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=CommonOccultUtils.is_ghost)))
        return CommonLocalizationUtils.create_localized_string(
            CMSimControlMenuStringId.CURRENT_NUMBER_OF_GHOSTS_STRING,
            tokens=(
                str(number_of_ghosts),
            )
        )

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
                on_close()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        option_dialog.add_option(
            CommonDialogButtonOption(
                'AllSims',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.ALL_GHOST_SIMS,
                ),
                on_chosen=lambda *_, **__: _operation_run(CMReviveAllGhostSimsOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'SpecificSims',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.SPECIFIC_GHOST_SIMS,
                ),
                on_chosen=lambda *_, **__: _operation_run(CMReviveSpecificGhostSimsOp())
            )
        )
        return True
