"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from careers.career_tuning import Career
from controlmenu.dialogs.modify_sim_data.modify_career.enums.string_ids import CMSimModifyCareerStringId
from controlmenu.dialogs.modify_sim_data.modify_career.operations.demote import CMDemoteSimOp
from controlmenu.dialogs.modify_sim_data.modify_career.operations.promote import CMPromoteSimOp
from controlmenu.dialogs.modify_sim_data.modify_career.operations.set_performance import CMSetPerformanceSimOp
from controlmenu.dialogs.modify_sim_data.modify_career.operations.single_sim_career_operation import \
    CMSingleSimCareerOperation
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CMModifyCareerDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_career_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> LocalizedString:
        start_track = self._career.start_track
        sim = CommonSimUtils.get_sim_instance(self._sim_info)
        display_name = CommonLocalizationUtils.combine_localized_strings(
            (start_track.get_career_name(sim), self._career.__class__.__name__),
            separator=CommonLocalizedStringSeparator.SPACE_PARENTHESIS_SURROUNDED
        )
        return display_name

    # noinspection PyMissingOrEmptyDocstring
    @property
    def description(self) -> Union[int, str, LocalizedString]:
        start_track = self._career.start_track
        sim = CommonSimUtils.get_sim_instance(self._sim_info)
        return start_track.get_career_description(sim)

    def __init__(
        self,
        sim_info: SimInfo,
        career: Career,
        on_close: Callable[[], None] = None,
        on_previous: Callable[[], None] = None
    ):
        self._career = career
        super().__init__(
            sim_info,
            on_close=on_close,
            on_previous=on_previous
        )

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: CMSingleSimCareerOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, self._career, on_completed=_on_operation_complete)

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Promote',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyCareerStringId.PROMOTE
                ),
                on_chosen=lambda *_, **__: _operation_run(CMPromoteSimOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Demote',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyCareerStringId.DEMOTE
                ),
                on_chosen=lambda *_, **__: _operation_run(CMDemoteSimOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetPerformance',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyCareerStringId.SET_PERFORMANCE
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetPerformanceSimOp())
            )
        )
        return True
