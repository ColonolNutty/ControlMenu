"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from careers.career_tuning import Career
from controlmenu.dialogs.modify_sim_data.modify_career.operations.single_sim_career_operation import \
    CMSingleSimCareerOperation
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CMPromoteSimOp(CMSingleSimCareerOperation):
    """Promote a Sim in a career."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_promote'

    # noinspection PyMissingOrEmptyDocstring
    def run(
        self,
        sim_info: SimInfo,
        career: Career,
        on_completed: Callable[[bool], None] = CommonFunctionUtils.noop
    ) -> bool:
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            on_completed(False)
            return False
        sim_career = sim.sim_info.career_tracker.get_career_by_uid(career.guid64)
        if sim_career is not None:
            if sim_career.can_change_level(demote=False):
                sim_career.promote()
                on_completed(True)
                return True

        on_completed(False)
        return False
