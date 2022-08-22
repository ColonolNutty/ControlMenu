"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.game_world_dialog.enums.string_identifiers import CMGameWorldControlMenuStringId
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_integer_option import \
    CommonDialogInputIntegerOption
from sims4communitylib.enums.common_weather_event_ids import CommonWeatherEventId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_weather_utils import CommonWeatherUtils
from controlmenu.logging.has_cm_log import HasCMLog


class CMChangeWeatherOp(HasCMLog):
    """Change the current weather."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_change_weather'

    def __init__(self, weather_event_id: CommonWeatherEventId) -> None:
        super().__init__()
        self._weather_event_id = weather_event_id
        self._weather_event = CommonWeatherUtils.load_weather_event_by_id(weather_event_id)

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_input_setting_changed(_: str, duration_in_hours: int, outcome: CommonChoiceOutcome):
            if duration_in_hours is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            CommonWeatherUtils.start_weather_event(self._weather_event, duration_in_hours)
            on_completed(True)

        CommonDialogInputIntegerOption(
            self.mod_identity,
            'DurationInHours',
            24,
            CommonDialogOptionContext(
                CMGameWorldControlMenuStringId.HOW_LONG_SHOULD_THE_WEATHER_LAST,
                0
            ),
            min_value=1,
            max_value=999,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True
