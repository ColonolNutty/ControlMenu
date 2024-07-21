"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from careers.career_tuning import Career
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CMSingleSimCareerOperation(CMSingleSimOperation):
    """Perform an operation on a Sim and career"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring,PyMethodOverriding
    def run(self, sim_info: SimInfo, career: Career, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring,PyMethodOverriding
    def run_with_sims(self, sim_info_a: SimInfo, career_a: Career, sim_info_b: SimInfo, career_b: Career, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        return False

    # noinspection PyMissingOrEmptyDocstring,PyMethodOverriding
    def can_run_with_sim(self, sim_info: SimInfo, career: Career) -> bool:
        return sim_info is not None and career is not None

    # noinspection PyMissingOrEmptyDocstring,PyMethodOverriding
    def can_run_with_sims(self, sim_info_a: SimInfo, career_a: Career, sim_info_b: SimInfo, career_b: Career) -> bool:
        return self.can_run_with_sim(sim_info_a, career_a) and self.can_run_with_sim(sim_info_b, career_b)
