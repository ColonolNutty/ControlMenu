"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

import date_and_time
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_integer_option import \
    CommonDialogInputIntegerOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4controlmenu.dialogs.game_world_dialog.enums.string_identifiers import S4CMGameWorldControlMenuStringId
from sims4controlmenu.enums.string_identifiers import S4CMStringId
from sims4controlmenu.logging.has_s4cm_log import HasS4CMLog
from sims4controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils
from sims4controlmenu.settings.settings import CMSetting


class S4CMSetClockSpeedOp(HasS4CMLog):
    """Set the clock speed for the Game Clock."""
    _DEFAULT_CLOCK_SPEED_MIN = 1
    _DEFAULT_CLOCK_SPEED_MAX = 9999

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_input_setting_changed(setting_name: str, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            # from sims4.commands import execute
            # execute('clock._set_milliseconds_per_sim_second {0}'.format(setting_value), None)
            date_and_time.REAL_MILLISECONDS_PER_SIM_SECOND = setting_value
            data_store.set_value_by_key(setting_name, setting_value)
            on_completed(True)

        data_store = CMMainDataManagerUtils().get_main_mod_settings_data_store()
        CommonDialogInputIntegerOption(
            self.mod_identity,
            CMSetting.REAL_MILLISECONDS_PER_SIM_SECOND,
            data_store.get_value_by_key(
                CMSetting.REAL_MILLISECONDS_PER_SIM_SECOND
            ),
            CommonDialogOptionContext(
                CommonStringId.STRING_COLON_SPACE_STRING,
                CommonStringId.STRING_SPACE_STRING,
                title_tokens=(
                    S4CMGameWorldControlMenuStringId.SET_REAL_MILLISECONDS_PER_SIM_SECOND,
                    str(data_store.get_value_by_key(CMSetting.REAL_MILLISECONDS_PER_SIM_SECOND)),
                ),
                description_tokens=(
                    S4CMGameWorldControlMenuStringId.SET_REAL_MILLISECONDS_PER_SIM_SECOND_DESCRIPTION,
                    CommonLocalizationUtils.create_localized_string(
                        S4CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(data_store.get_default_value_by_key(CMSetting.REAL_MILLISECONDS_PER_SIM_SECOND)),
                            str(S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MIN),
                            str(S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MAX)
                        )
                    )
                )
            ),
            min_value=S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MIN,
            max_value=S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MAX,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True
