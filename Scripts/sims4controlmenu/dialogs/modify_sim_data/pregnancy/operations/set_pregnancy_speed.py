"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.enums.string_identifiers import S4CMStringId
from sims4controlmenu.settings.settings import CMSetting


class S4CMSetPregnancySpeedOp(S4CMSingleSimOperation):
    """Set the speed of pregnancy."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_set_pregnancy_speed'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils

        def _on_input_setting_changed(setting_name: str, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            old_speed = data_store.get_value_by_key(setting_name)
            self._update_pregnancy_speed_for_all_sims(old_speed, setting_value)
            data_store.set_value_by_key(setting_name, setting_value)
            on_completed(True)

        data_store = CMMainDataManagerUtils().get_main_mod_settings_data_store()
        CommonDialogInputFloatOption(
            CMSetting.PREGNANCY_SPEED,
            data_store.get_value_by_key(
                CMSetting.PREGNANCY_SPEED
            ),
            CommonDialogOptionContext(
                CommonStringId.STRING_COLON_SPACE_STRING,
                CommonStringId.STRING_SPACE_STRING,
                title_tokens=(
                    S4CMSimControlMenuStringId.SET_PREGNANCY_SPEED,
                    str(data_store.get_value_by_key(CMSetting.PREGNANCY_SPEED)),
                ),
                description_tokens=(
                    S4CMSimControlMenuStringId.SET_PREGNANCY_SPEED_DESCRIPTION,
                    CommonLocalizationUtils.create_localized_string(
                        S4CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(data_store.get_default_value_by_key(CMSetting.PREGNANCY_SPEED)),
                            '0.0',
                            '9999.0'
                        )
                    )
                )
            ),
            min_value=0.0,
            max_value=99999.0,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True

    def _update_pregnancy_speed_for_all_sims(self, old_speed: float, new_speed: float):
        for _sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            pregnancy_commodity_type = PregnancyTracker.PREGNANCY_COMMODITY_MAP.get(_sim_info.species)
            tracker = _sim_info.get_tracker(pregnancy_commodity_type)
            if tracker is not None:
                stat = tracker.get_statistic(pregnancy_commodity_type, add=True)
                if stat is not None:
                    stat.remove_statistic_modifier(old_speed)
                    if CommonSimPregnancyUtils.is_pregnant(_sim_info):
                        stat.add_statistic_modifier(new_speed)
