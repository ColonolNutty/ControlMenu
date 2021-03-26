"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple

import services
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sims_option_dialog import \
    CommonPremadeChooseSimsOptionDialog
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMForgetSimsOp(S4CMSingleSimOperation):
    """Cause a Sim to forget their relationship with other Sims."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        sim_id = CommonSimUtils.get_sim_id(sim_info)

        def _on_submit(chosen_sim_info_list: Tuple[SimInfo]) -> None:
            if chosen_sim_info_list is None or not chosen_sim_info_list:
                return
            for chosen_sim_info in chosen_sim_info_list:
                chosen_sim_id = CommonSimUtils.get_sim_id(chosen_sim_info)
                # noinspection PyBroadException
                try:
                    services.relationship_service().destroy_relationship(sim_id, chosen_sim_id, notify_client=True)
                    services.relationship_service().destroy_relationship(chosen_sim_id, sim_id, notify_client=True)
                except:
                    pass

        def _has_relationship(_sim_info: SimInfo) -> bool:
            target_sim_id = CommonSimUtils.get_sim_id(_sim_info)
            return any(services.relationship_service().get_all_bits(sim_id, target_sim_id=target_sim_id)) or any(services.relationship_service().get_all_bits(target_sim_id, target_sim_id=sim_id))

        dialog = CommonPremadeChooseSimsOptionDialog(
            S4CMSimControlMenuStringId.FORGET_SIMS,
            S4CMSimControlMenuStringId.CHOOSE_SIMS_FOR_SIM_TO_FORGET,
            include_sim_callback=_has_relationship,
            description_tokens=(sim_info,),
            instanced_sims_only=False,
            mod_identity=self.mod_identity
        )
        if not dialog.has_options():
            return False
        # Sort the Sims in the dialog by their name.
        dialog._internal_dialog._rows = tuple(sorted(dialog._internal_dialog._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
        dialog.show(on_submit=_on_submit, max_selectable=dialog.option_count)
