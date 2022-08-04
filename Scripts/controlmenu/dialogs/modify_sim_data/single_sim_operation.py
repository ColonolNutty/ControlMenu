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


class CMSingleSimOperation(HasCMLog):
    """Perform an operation on a Sim"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        """Apply the operation."""
        raise NotImplementedError()

    def run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        """Apply the operation while using a specified Sim."""
        return False

    def can_run_with_sim(self, sim_info: SimInfo) -> bool:
        """Determine if this operation can run using the specified Sim."""
        return sim_info is not None

    def can_run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """Determine if this operation can run using the specified Sims."""
        return self.can_run_with_sim(sim_info_a) and self.can_run_with_sim(sim_info_b)
