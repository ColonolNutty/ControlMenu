"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4controlmenu.commonlib.utils.common_location_utils import S4CMCommonLocationUtils
from sims4controlmenu.logging.has_s4cm_log import HasS4CMLog


class S4CMClearLotChangesOp(HasS4CMLog):
    """Clear lot changes."""
    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'clear_lot_changes'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        S4CMCommonLocationUtils.clear_lot_capacity_overrides()
        on_completed(True)
        return True
