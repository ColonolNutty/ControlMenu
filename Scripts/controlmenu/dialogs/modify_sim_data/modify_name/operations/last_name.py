"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_input_text_dialog import CommonInputTextDialog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMChangeLastNameOp(CMSingleSimOperation):
    """Change the last name of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_change_last_name'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_chosen(input_value: str, outcome: CommonChoiceOutcome):
            if outcome == CommonChoiceOutcome.ERROR:
                self.run(sim_info, on_completed=on_completed)
                return
            elif CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(False)
                return
            CommonSimNameUtils.set_last_name(sim_info, input_value)
            on_completed(True)
            return True

        first_name = CommonSimNameUtils.get_last_name(sim_info)

        dialog = CommonInputTextDialog(
            ModInfo.get_identity(),
            CMSimControlMenuStringId.LAST_NAME,
            0,
            first_name,
        )
        dialog.show(on_submit=_on_chosen)
        return True
