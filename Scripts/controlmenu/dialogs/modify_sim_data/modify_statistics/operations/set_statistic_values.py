"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId
from statistics.statistic_tracker import StatisticTracker


class CMSetStatisticValuesSimOp(CMSingleSimOperation):
    """Set the value of Statistics on a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_statistic_values_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop, current_page: int = 1) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed, current_page=option_dialog.current_page)

        def _on_close() -> None:
            on_completed(False)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.SET_STATISTIC_VALUES,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_input_setting_changed(_statistic_guid: int, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen()
                return
            self._set_statistic_level(sim_info, _statistic_guid, setting_value)
            _reopen()

        statistic_tracker: StatisticTracker = sim_info.statistic_tracker
        for statistic in statistic_tracker.all_statistics():
            statistic_guid = CommonStatisticUtils.get_statistic_id(statistic)
            if statistic_guid is None:
                self.log.format_with_message('Missing statistic id for Statistic.', statistic=statistic)
                continue
            try:
                # noinspection PyUnresolvedReferences
                display_name = statistic.stat_name
                if display_name.hash == 0:
                    statistic_name = statistic.stat_type.name or 'Unknown Statistic Name'
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(statistic_name, statistic.stat_type.name))
                else:
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(CommonLocalizationUtils.create_localized_string(display_name, tokens=(sim_info,)), statistic.stat_type.name))
                # description = CommonLocalizationUtils.create_localized_string(statistic..trait_description._string_id, tokens=(sim_info,))
                description = 0
                icon = CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                min_value = statistic.min_value
                max_value = statistic.max_value
                initial_value = statistic.initial_value
                current_value = CommonSimStatisticUtils.get_statistic_value(sim_info, statistic_guid)
                option_dialog.add_option(
                    CommonDialogInputFloatOption(
                        statistic_guid,
                        current_value,
                        CommonDialogOptionContext(
                            CommonStringId.STRING_COLON_SPACE_STRING,
                            CommonStringId.STRING_SPACE_STRING,
                            title_tokens=(
                                display_name,
                                str(current_value),
                            ),
                            description_tokens=(
                                description,
                                CommonLocalizationUtils.create_localized_string(
                                    CMStringId.DEFAULT_MIN_MAX,
                                    tokens=(
                                        str(initial_value),
                                        str(min_value),
                                        str(max_value)
                                    )
                                )
                            ),
                            icon=icon
                        ),
                        min_value=min_value,
                        max_value=max_value,
                        on_chosen=_on_input_setting_changed
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display statistic.', statistic=statistic, statistic_name=statistic.stat_type.name, statistic_id=statistic_guid, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True, page=current_page)
        return True

    def _set_statistic_level(self, sim_info: SimInfo, statistic: int, amount: float):
        CommonSimStatisticUtils.set_statistic_level(sim_info, statistic, amount)
