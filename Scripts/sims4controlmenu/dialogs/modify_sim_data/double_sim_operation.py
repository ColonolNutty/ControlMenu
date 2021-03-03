"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class S4CMDoubleSimOperation:
    """Perform an operation on using two Sims"""
    def run(self, sim_info_one: SimInfo, sim_info_two: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        """Apply the operation."""
        raise NotImplementedError()
