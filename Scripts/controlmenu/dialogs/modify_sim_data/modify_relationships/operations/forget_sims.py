"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
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
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMForgetSimsOp(CMSingleSimOperation):
    """Cause a Sim to forget their relationship with other Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_forget_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_submit(chosen_sim_info_list: Tuple[SimInfo]) -> None:
            if chosen_sim_info_list is None or not chosen_sim_info_list:
                on_completed(False)
                return
            on_completed(self._run_with_sims(sim_info, chosen_sim_info_list))

        def _has_relationship(target_sim_info: SimInfo) -> bool:
            return self.can_run_with_sims(sim_info, target_sim_info)

        dialog = CommonPremadeChooseSimsOptionDialog(
            CMSimControlMenuStringId.FORGET_SIMS,
            CMSimControlMenuStringId.CHOOSE_SIMS_FOR_SIM_TO_FORGET,
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

    # noinspection PyMissingOrEmptyDocstring
    def can_run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        if not super().can_run_with_sims(sim_info_a, sim_info_b):
            return False
        sim_a_id = CommonSimUtils.get_sim_id(sim_info_a)
        sim_b_id = CommonSimUtils.get_sim_id(sim_info_b)
        return sim_info_a is not sim_info_b and any(services.relationship_service().get_all_bits(sim_a_id, target_sim_id=sim_b_id)) or any(services.relationship_service().get_all_bits(sim_b_id, target_sim_id=sim_a_id))

    # noinspection PyMissingOrEmptyDocstring
    def run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        on_completed(self._run_with_sims(sim_info_a, (sim_info_b,)))
        return True

    def _run_with_sims(self, sim_info: SimInfo, sim_info_list: Tuple[SimInfo]) -> bool:
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        for other_sim_info in sim_info_list:
            other_sim_id = CommonSimUtils.get_sim_id(other_sim_info)
            # noinspection PyBroadException
            try:
                CommonSimGenealogyUtils.remove_family_relations_with(sim_info, other_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(other_sim_info, sim_info)
                services.relationship_service().destroy_relationship(sim_id, other_sim_id, notify_client=True)
                services.relationship_service().destroy_relationship(other_sim_id, sim_id, notify_client=True)
            except:
                pass
        return True
