"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.enums.string_identifiers import CMStringId
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.utils.sims.common_sim_body_utils import CommonSimBodyUtils


class CMSetFitLevelOp(CMSingleSimOperation):
    """Set the Fit level of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_fit_level'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_submit(level: float, outcome: CommonChoiceOutcome):
            if outcome == CommonChoiceOutcome.ERROR:
                self.run(sim_info, on_completed=on_completed)
                return
            elif CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(False)
                return
            CommonSimBodyUtils.set_fit_level(sim_info, level)
            on_completed(True)
            return True

        current_level = CommonSimBodyUtils.get_fit_level(sim_info)

        from sims4communitylib.dialogs.common_input_float_dialog import CommonInputFloatDialog
        dialog = CommonInputFloatDialog(
            CMSimControlMenuStringId.WHAT_LEVEL,
            CommonLocalizationUtils.combine_localized_strings(
                (
                    CMSimControlMenuStringId.WHAT_LEVEL_OF_FIT_DESCRIPTION,
                    CommonLocalizationUtils.create_localized_string(
                        CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(0),
                            str(-100.0),
                            str(100.0)
                        )
                    )
                ),
                separator=CommonLocalizedStringSeparator.SPACE
            ),
            current_level,
            min_value=-100.0,
            max_value=100.0,
            mod_identity=ModInfo.get_identity()
        )
        dialog.show(on_submit=_on_submit)
        return True
