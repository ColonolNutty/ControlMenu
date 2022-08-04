"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from controlmenu.logging.has_cm_log import HasCMLog


class CMDoubleSimOperation(HasCMLog):
    """Perform an operation on using two Sims"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    def run(self, sim_info_a: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        """Apply the operation."""
        raise NotImplementedError()
