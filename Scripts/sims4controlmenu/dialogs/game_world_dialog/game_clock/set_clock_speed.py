"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

import date_and_time
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_input_integer_dialog import CommonInputIntegerDialog
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4controlmenu.dialogs.game_world_dialog.enums.string_identifiers import S4CMGameWorldControlMenuStringId
from sims4controlmenu.logging.has_s4cm_log import HasS4CMLog


class S4CMSetClockSpeedOp(CommonService, HasS4CMLog):
    """Set the clock speed for the Game Clock."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_set_clock_speed'

    _DEFAULT_CLOCK_SPEED = date_and_time.REAL_MILLISECONDS_PER_SIM_SECOND
    _DEFAULT_CLOCK_SPEED_MIN = 1
    _DEFAULT_CLOCK_SPEED_MAX = 9999

    def __init__(self) -> None:
        super().__init__()
        HasS4CMLog.__init__(self)
        self._current_clock_speed_in_milliseconds = S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_submit(_new_milliseconds: int, outcome: CommonChoiceOutcome):
            if _new_milliseconds is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(False)
                return
            from sims4.commands import execute
            execute('clock._set_milliseconds_per_sim_second {0}'.format(_new_milliseconds), None)
            self._current_clock_speed_in_milliseconds = _new_milliseconds
            on_completed(True)

        dialog = CommonInputIntegerDialog(
            S4CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_STRING,
            S4CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_DESCRIPTION,
            self._current_clock_speed_in_milliseconds,
            title_tokens=(
                str(self._current_clock_speed_in_milliseconds),
            ),
            description_tokens=(
                str(S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MIN),
                str(S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MAX),
                str(S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED)
            ),
            min_value=S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MIN,
            max_value=S4CMSetClockSpeedOp._DEFAULT_CLOCK_SPEED_MAX,
            mod_identity=self.mod_identity
        )

        dialog.show(on_submit=_on_submit)
        return True
