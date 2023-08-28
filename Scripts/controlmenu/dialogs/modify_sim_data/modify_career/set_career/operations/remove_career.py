"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from controlmenu.dialogs.modify_sim_data.modify_career.enums.string_ids import CMSimModifyCareerStringId
from controlmenu.enums.string_identifiers import CMStringId
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_career_utils import CommonSimCareerUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMRemoveCareerSimOp(CMSingleSimOperation):
    """Remove Career from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_remove_career_from_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_ok_selected(_: Any):
            CommonSimCareerUtils.remove_careers(sim_info, include_career_callback=lambda x: True)
            on_completed(True)

        def _on_cancel_selected(_: Any):
            on_completed(False)

        confirmation = CommonOkCancelDialog(
            CMStringId.CONFIRMATION,
            CMSimModifyCareerStringId.ARE_YOU_SURE_YOU_WANT_TO_REMOVE_ALL_CAREERS_FROM_SIM,
            description_tokens=(sim_info,)
        )
        confirmation.show(on_ok_selected=_on_ok_selected, on_cancel_selected=_on_cancel_selected)
        return True
