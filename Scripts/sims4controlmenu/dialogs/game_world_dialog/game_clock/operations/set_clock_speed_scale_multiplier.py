"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4controlmenu.dialogs.game_world_dialog.enums.string_identifiers import S4CMGameWorldControlMenuStringId
from sims4controlmenu.enums.string_identifiers import S4CMStringId
from sims4controlmenu.settings.settings import CMSetting


class S4CMSetClockSpeedScaleMultiplierOp:
    """Set the clock speed scale multiplier of the Game Clock."""
    _DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER = 1.0
    _DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MIN = 0.1
    _DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MAX = 9999.0

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils

        def _on_input_setting_changed(setting_name: str, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            data_store.set_value_by_key(setting_name, setting_value)
            on_completed(True)

        data_store = CMMainDataManagerUtils().get_main_mod_settings_data_store()
        CommonDialogInputFloatOption(
            CMSetting.CLOCK_SPEED_MULTIPLIER,
            data_store.get_value_by_key(
                CMSetting.CLOCK_SPEED_MULTIPLIER
            ),
            CommonDialogOptionContext(
                CommonStringId.STRING_COLON_SPACE_STRING,
                CommonStringId.STRING_SPACE_STRING,
                title_tokens=(
                    S4CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_SCALE,
                    str(data_store.get_value_by_key(CMSetting.CLOCK_SPEED_MULTIPLIER)),
                ),
                description_tokens=(
                    S4CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_SCALE_DESCRIPTION,
                    CommonLocalizationUtils.create_localized_string(
                        S4CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(data_store.get_default_value_by_key(CMSetting.CLOCK_SPEED_MULTIPLIER)),
                            '0.0',
                            '9999.0'
                        )
                    )
                )
            ),
            min_value=S4CMSetClockSpeedScaleMultiplierOp._DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MIN,
            max_value=S4CMSetClockSpeedScaleMultiplierOp._DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MAX,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True
