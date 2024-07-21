"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from careers.career_tuning import Career
from controlmenu.dialogs.modify_sim_data.modify_career.enums.string_ids import CMSimModifyCareerStringId
from controlmenu.dialogs.modify_sim_data.modify_career.operations.single_sim_career_operation import \
    CMSingleSimCareerOperation
from controlmenu.enums.string_identifiers import CMStringId
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.misc.common_text_utils import CommonTextUtils
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CMSetPerformanceSimOp(CMSingleSimCareerOperation):
    """Set Career Performance of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_performance'

    # noinspection PyMissingOrEmptyDocstring
    def run(
        self,
        sim_info: SimInfo,
        career: Career,
        on_completed: Callable[[bool], None] = CommonFunctionUtils.noop
    ) -> bool:
        sim = CommonSimUtils.get_sim_instance(sim_info)
        sim_career = sim.sim_info.career_tracker.get_career_by_uid(career.guid64)
        statistic = sim_career.current_level_tuning.performance_stat

        def _on_input_setting_changed(_: str, new_amount: float, outcome: CommonChoiceOutcome):
            if new_amount is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            if sim_career is not None:
                performance_stat = sim.statistic_tracker.get_statistic(statistic)
                performance_stat.set_value(new_amount)
                sim.sim_info.career_tracker.resend_career_data()

        current_value = CommonSimStatisticUtils.get_statistic_value(sim_info, statistic)

        default_value = CommonStatisticUtils.get_statistic_initial_value(statistic)
        min_value = CommonStatisticUtils.get_statistic_min_value(statistic)
        max_value = CommonStatisticUtils.get_statistic_max_value(statistic)

        CommonDialogInputFloatOption(
            'Career',
            current_value,
            CommonDialogOptionContext(
                CommonStringId.STRING_COLON_SPACE_STRING,
                CommonStringId.STRING_SPACE_STRING,
                title_tokens=(
                    CMSimModifyCareerStringId.SET_PERFORMANCE,
                    str(CommonTextUtils.to_truncated_decimal(current_value)),
                ),
                description_tokens=(
                    CMSimModifyCareerStringId.SET_PERFORMANCE,
                    CommonLocalizationUtils.create_localized_string(
                        CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(default_value),
                            str(min_value),
                            str(max_value)
                        )
                    )
                )
            ),
            min_value=min_value,
            max_value=max_value,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True
