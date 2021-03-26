"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from clock import GameClock
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_input_float_dialog import CommonInputFloatDialog
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4controlmenu.dialogs.game_world_dialog.enums.string_identifiers import S4CMGameWorldControlMenuStringId
from sims4controlmenu.modinfo import ModInfo


class S4CMSetClockSpeedScaleMultiplierOp(CommonService):
    """Set the clock speed scale multiplier of the Game Clock."""
    _DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER = 1.0
    _DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MIN = 0.1
    _DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MAX = 9999.0

    def __init__(self) -> None:
        self._clock_speed_multiplier = 1.0

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_submit(_new_speed: float, outcome: CommonChoiceOutcome):
            if _new_speed is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(False)
                return
            self._clock_speed_multiplier = _new_speed
            on_completed(True)

        dialog = CommonInputFloatDialog(
            S4CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_SCALE,
            S4CMGameWorldControlMenuStringId.SET_CLOCK_SPEED_SCALE_DESCRIPTION,
            self._clock_speed_multiplier,
            description_tokens=(
                str(S4CMSetClockSpeedScaleMultiplierOp._DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MIN),
                str(S4CMSetClockSpeedScaleMultiplierOp._DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MAX),
                str(S4CMSetClockSpeedScaleMultiplierOp._DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER)
            ),
            min_value=S4CMSetClockSpeedScaleMultiplierOp._DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MIN,
            max_value=S4CMSetClockSpeedScaleMultiplierOp._DEFAULT_CLOCK_SPEED_SCALE_MULTIPLIER_MAX
        )

        dialog.show(on_submit=_on_submit)
        return True


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameClock, GameClock.current_clock_speed_scale.__name__)
def _s4cm_get_current_clock_speed_scale(original, self) -> Any:
    return original(self) * S4CMSetClockSpeedScaleMultiplierOp()._clock_speed_multiplier
