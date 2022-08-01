"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sims_option_dialog import \
    CommonPremadeChooseSimsOptionDialog
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMAddHasMetSimsOp(S4CMSingleSimOperation):
    """Add the 'Has Met' Relationship Bit between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_has_met'

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
            S4CMSimControlMenuStringId.ADD_HAS_MET,
            S4CMSimControlMenuStringId.CHOOSE_SIMS_TO_ADD_HAS_MET,
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
        return sim_info_a is not sim_info_b and not CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a, sim_info_b, CommonRelationshipBitId.HAS_MET)

    # noinspection PyMissingOrEmptyDocstring
    def run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        on_completed(self._run_with_sims(sim_info_a, (sim_info_b,)))
        return True

    def _run_with_sims(self, sim_info: SimInfo, sim_info_list: Tuple[SimInfo]) -> bool:
        for other_sim_info in sim_info_list:
            CommonRelationshipUtils.add_relationship_bit(sim_info, other_sim_info, CommonRelationshipBitId.HAS_MET)
            CommonRelationshipUtils.add_relationship_bit(other_sim_info, sim_info, CommonRelationshipBitId.HAS_MET)
        return True


class S4CMRemoveHasMetSimsOp(S4CMSingleSimOperation):
    """Remove the 'Has Met' Relationship Bit between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_has_met'

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
            S4CMSimControlMenuStringId.REMOVE_HAS_MET,
            S4CMSimControlMenuStringId.CHOOSE_SIMS_TO_REMOVE_HAS_MET,
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
        return sim_info_a is not sim_info_b and CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a, sim_info_b, CommonRelationshipBitId.HAS_MET)

    # noinspection PyMissingOrEmptyDocstring
    def run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        on_completed(self._run_with_sims(sim_info_a, (sim_info_b,)))
        return True

    def _run_with_sims(self, sim_info: SimInfo, sim_info_list: Tuple[SimInfo]) -> bool:
        for other_sim_info in sim_info_list:
            CommonRelationshipUtils.remove_relationship_bit(sim_info, other_sim_info, CommonRelationshipBitId.HAS_MET)
            CommonRelationshipUtils.remove_relationship_bit(other_sim_info, sim_info, CommonRelationshipBitId.HAS_MET)
        return True
