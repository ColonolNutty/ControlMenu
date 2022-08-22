"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.manage_death.operations.revive_ghost_sim import CMReviveGhostSimOp
from sims.sim_info import SimInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMReviveAllGhostSimsOp(CMSingleSimOperation):
    """Revive ghost Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_revive_ghost_sims'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        revived_count = 0
        for _sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=CommonOccultUtils.is_ghost):
            if CMReviveGhostSimOp().run(_sim_info):
                revived_count += 1

        CommonBasicNotification(
            CMSimControlMenuStringId.REVIVED_COUNT_GHOSTS,
            0,
            title_tokens=(
                str(revived_count),
            )
        )
        on_completed(True)
        return True
