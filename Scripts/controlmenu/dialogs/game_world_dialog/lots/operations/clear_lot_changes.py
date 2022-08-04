"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from controlmenu.commonlib.utils.common_location_utils import CMCommonLocationUtils
from controlmenu.logging.has_cm_log import HasCMLog


class CMClearLotCapacityOverridesOp(HasCMLog):
    """Clear lot capacity overrides."""
    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_clear_lot_capacity_overrides'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        CMCommonLocationUtils.clear_lot_capacity_overrides()
        on_completed(True)
        return True
