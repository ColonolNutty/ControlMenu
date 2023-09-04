"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sims_option_dialog import \
    CommonPremadeChooseSimsOptionDialog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMRemoveFamilyRelationsBitOp(CMSingleSimOperation):
    """Remove a family relationship between a Sim and many Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_remove_family_relations'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_submit(chosen_sim_info_list: Tuple[SimInfo]) -> None:
            if chosen_sim_info_list is None or not chosen_sim_info_list:
                on_completed(False)
                return
            self.run_with_sims(sim_info, *chosen_sim_info_list, on_completed=on_completed)

        def _is_allowed(target_sim_info: SimInfo):
            return self.can_run_with_sims(sim_info, target_sim_info)

        dialog = CommonPremadeChooseSimsOptionDialog(
            CMSimControlMenuStringId.REMOVE_FAMILY_RELATIONS,
            0,
            title_tokens=(sim_info,),
            include_sim_callback=_is_allowed,
            instanced_sims_only=False,
            mod_identity=ModInfo.get_identity(),
            on_close=lambda: on_completed(False)
        )
        if not dialog.has_options():
            on_completed(False)
            return False
        # Sort the Sims in the dialog by their name.
        dialog._internal_dialog._rows = tuple(sorted(dialog._internal_dialog._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
        dialog.show(sim_info=sim_info, on_submit=_on_submit, max_selectable=dialog.option_count)
        return True

    # noinspection PyMissingOrEmptyDocstring
    def can_run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        return super().can_run_with_sims(sim_info_a, sim_info_b) and sim_info_a is not sim_info_b and CommonRelationshipUtils.are_blood_relatives(sim_info_a, sim_info_b)

    # noinspection PyMissingOrEmptyDocstring
    def run_with_sims(self, sim_info: SimInfo, *chosen_sim_info_list: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop):
        for chosen_sim_info in chosen_sim_info_list:
            try:
                CommonSimGenealogyUtils.remove_family_relations_with(sim_info, chosen_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(chosen_sim_info, sim_info)
            except Exception as ex:
                self.log.error('Failed to remove family relations', exception=ex)

        on_completed(True)
