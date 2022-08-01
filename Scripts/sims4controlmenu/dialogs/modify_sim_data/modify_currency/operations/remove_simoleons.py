"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from protocolbuffers import Consts_pb2
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMRemoveSimoleonsOp(S4CMSingleSimOperation):
    """Remove simoleons from the household of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_remove_simoleons'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonHouseholdUtils.has_household(sim_info):
            on_completed(False)
            return False

        def _on_submit(amount: int, outcome: CommonChoiceOutcome):
            if outcome == CommonChoiceOutcome.ERROR:
                self.run(sim_info, on_completed=on_completed)
                return
            elif CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(False)
                return
            CommonHouseholdUtils.get_household(sim_info).funds.try_remove(amount, Consts_pb2.FUNDS_MONEY_CHEAT, sim=CommonSimUtils.get_sim_instance(sim_info), require_full_amount=False)
            on_completed(True)
            return True

        from sims4communitylib.dialogs.common_input_integer_dialog import CommonInputIntegerDialog
        dialog = CommonInputIntegerDialog(
            S4CMSimControlMenuStringId.HOW_MANY_SIMOLEONS,
            0,
            1000,
            min_value=1,
            mod_identity=ModInfo.get_identity()
        )
        dialog.show(on_submit=_on_submit)
        return True
