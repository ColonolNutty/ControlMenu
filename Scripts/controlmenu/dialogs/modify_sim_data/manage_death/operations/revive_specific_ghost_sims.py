"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple

from controlmenu.dialogs.modify_sim_data.manage_death.operations.revive_ghost_sim import CMReviveGhostSimOp
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sims_option_dialog import \
    CommonPremadeChooseSimsOptionDialog
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMReviveSpecificGhostSimsOp(CMSingleSimOperation):
    """Revive ghost Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_revive_ghost_sims'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_submit(chosen_sim_info_list: Tuple[SimInfo]) -> None:
            if not chosen_sim_info_list:
                on_completed(False)
                return
            revived_count = 0
            for _sim_info in chosen_sim_info_list:
                if CMReviveGhostSimOp().run(_sim_info):
                    revived_count += 1
            CommonBasicNotification(
                CMSimControlMenuStringId.REVIVED_COUNT_GHOSTS,
                0,
                title_tokens=(
                    str(revived_count),
                )
            ).show()
            on_completed(True)

        def _is_dead(ghost_sim_info: SimInfo) -> bool:
            return CommonOccultUtils.is_ghost(ghost_sim_info).result

        dialog = CommonPremadeChooseSimsOptionDialog(
            CMSimControlMenuStringId.CHOOSE_GHOSTS_TO_REVIVE,
            0,
            title_tokens=(sim_info,),
            include_sim_callback=_is_dead,
            instanced_sims_only=False,
            mod_identity=self.mod_identity,
            on_close=lambda: on_completed(False)
        )
        if not dialog.has_options():
            on_completed(False)
            return False
        # Sort the Sims in the dialog by their name.
        dialog._internal_dialog._rows = tuple(sorted(dialog._internal_dialog._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
        dialog.show(sim_info=sim_info, on_submit=_on_submit)
        return True
