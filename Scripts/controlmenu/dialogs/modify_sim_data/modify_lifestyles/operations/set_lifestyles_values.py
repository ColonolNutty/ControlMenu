"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.trait_statistic import TraitStatistic, TraitStatisticGroup
from statistics.trait_statistic_tracker import TraitStatisticTracker


class CMSetLifestyleValuesSimOp(CMSingleSimOperation):
    """Set the value of Lifestyles on a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_lifestyle_values_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop, current_page: int = 1) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed, current_page=option_dialog.current_page)

        def _on_close() -> None:
            on_completed(False)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.SET_LIFESTYLE_VALUES,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_input_setting_changed(_statistic_guid: int, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen()
                return
            trait_tracker: TraitStatisticTracker = sim_info.trait_statistic_tracker
            _statistic = CommonStatisticUtils.load_statistic_by_id(_statistic_guid)
            trait_statistic: TraitStatistic = trait_tracker.get_statistic(_statistic, add=True)
            # Daily caps prevent setting the proper value, so we ignore the daily lifestyle caps.
            trait_statistic.set_value(setting_value, ignore_caps=True)
            trait_statistic.reset_daily_caps()
            _reopen()

        sim = CommonSimUtils.get_sim_instance(sim_info)
        for statistic in CommonResourceUtils.load_all_instance_values(Types.STATISTIC, return_type=TraitStatistic):
            if not hasattr(statistic, 'group'):
                continue
            if statistic.group != TraitStatisticGroup.Lifestyle:
                self.log.format_with_message('Group is not Lifestyle')
                continue
            statistic_guid = CommonStatisticUtils.get_statistic_id(statistic)
            if statistic_guid is None:
                self.log.format_with_message('Missing statistic id for Lifestyle.', statistic=statistic)
                continue
            if not statistic.can_add(sim):
                self.verbose_log.format_with_message('Failed, Lifestyle is not allowed for Sim.', statistic=statistic, sim=sim_info)
                continue

            def _get_trait_display_name(_trait) -> LocalizedString:
                # noinspection PyUnresolvedReferences
                return _trait.display_name(sim_info)

            try:
                trait_display_name = _get_trait_display_name(statistic.trait_data.trait)
                current_value = CommonSimStatisticUtils.get_statistic_value(sim_info, statistic_guid)
                if current_value > 0:
                    trait_display_name = CommonLocalizationUtils.colorize(trait_display_name, text_color=CommonLocalizedStringColor.GREEN)

                if hasattr(statistic, 'opposing_trait_data') and statistic.opposing_trait_data:
                    opposing_display_name = _get_trait_display_name(statistic.opposing_trait_data.trait)
                    if current_value < 0:
                        opposing_display_name = CommonLocalizationUtils.colorize(opposing_display_name, text_color=CommonLocalizedStringColor.GREEN)
                    display_name = CommonLocalizationUtils.create_localized_string(CommonStringId.STRING_HYPHEN_STRING, tokens=(opposing_display_name, trait_display_name))
                    description = CMSimControlMenuStringId.TWO_LIFESTYLE_TYPES_DESCRIPTION
                else:
                    display_name = trait_display_name
                    description = CMSimControlMenuStringId.ONE_LIFESTYLE_TYPE_DESCRIPTION
                icon = CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                min_value = statistic.min_value
                max_value = statistic.max_value
                initial_value = 0
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
                self.log.format_error_with_message('Failed to display lifestyle.', statistic=statistic, statistic_name=statistic.stat_type, statistic_id=statistic_guid, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=False, page=current_page)
        return True
