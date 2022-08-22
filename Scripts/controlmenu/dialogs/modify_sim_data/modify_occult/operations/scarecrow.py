"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId


class CMScarecrowAddOp(CMSingleSimOperation):
    """Add the Scarecrow Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_scarecrow'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_scarecrow(sim_info):
            on_completed(CommonExecutionResult(False, reason=f'{sim_info} is already a Scarecrow.'))
            return False

        def _on_ok_selected(_: Any):
            result = CommonOccultUtils.add_scarecrow_occult(sim_info)
            on_completed(result)

        def _on_cancel_selected(_: Any):
            on_completed(CommonExecutionResult(False, reason='Cancelled to change.'))

        confirmation = CommonOkCancelDialog(
            CMStringId.CONFIRMATION,
            CMSimControlMenuStringId.BECOME_SCARECROW_CONFIRMATION_DESCRIPTION,
        )
        confirmation.show(on_ok_selected=_on_ok_selected, on_cancel_selected=_on_cancel_selected)
        return True


class CMScarecrowRemoveOp(CMSingleSimOperation):
    """Remove the Scarecrow Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_scarecrow'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        result = CommonOccultUtils.remove_scarecrow_occult(sim_info)
        on_completed(result)
        return result.result
