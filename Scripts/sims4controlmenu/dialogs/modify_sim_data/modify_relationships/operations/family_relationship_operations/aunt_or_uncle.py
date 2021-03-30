"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from sims.genealogy_tracker import genealogy_caching
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsAuntOrUncleToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as an aunt or uncle of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_AUNT_UNCLE

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_NIECE_NEPHEW

    def _update_family_tree(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_selected(_: str, operation: Any):
            if operation is None:
                on_completed(False)
                return
            operation(new_aunt_or_uncle_sim_info, sim_info, on_completed=on_completed)

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            S4CMSimControlMenuStringId.WHOSE_SIDE_OF_THE_FAMILY,
            0,
            on_previous=lambda: on_completed(False),
            on_close=lambda: on_completed(False),
            include_previous_button=True
        )

        if CommonSimGenealogyUtils.has_mother(sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Mother',
                    self._mothers_side,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.MOTHER
                    ),
                    on_chosen=_on_selected
                )
            )

        if CommonSimGenealogyUtils.has_father(sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Father',
                    self._fathers_side,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.FATHER
                    ),
                    on_chosen=_on_selected
                )
            )

        if not option_dialog.has_options():
            return self._no_sides(new_aunt_or_uncle_sim_info, sim_info, on_completed=on_completed)

        option_dialog.show()
        return True

    def _no_sides(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as aunt/uncle of Sim B on neither parents side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            self._add_new_relation(sim_info, new_aunt_or_uncle_sim_info)
            self.log.format_with_message('Done setting Sim A as aunt/uncle of Sim B on neither parents side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as aunt/uncle on neither parents side.', exception=ex)
            on_completed(False)
            return False
        return True

    def _mothers_side(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as aunt/uncle of Sim B on mothers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
            self._update_parent_relation(new_aunt_or_uncle_sim_info, sim_info, mother_sim_info)
            self._add_new_relation(sim_info, new_aunt_or_uncle_sim_info)
            self.log.format_with_message('Done setting Sim A as aunt/uncle of Sim B on mothers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as aunt/uncle on mothers side.', exception=ex)
            on_completed(False)
            return False
        return True

    def _fathers_side(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as aunt/uncle of Sim B on fathers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
            self._update_parent_relation(new_aunt_or_uncle_sim_info, sim_info, father_sim_info)
            self._add_new_relation(sim_info, new_aunt_or_uncle_sim_info)
            self.log.format_with_message('Done setting Sim A as aunt/uncle of Sim B on fathers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as aunt/uncle on fathers side.', exception=ex)
            on_completed(False)
            return False
        return True

    def _update_parent_relation(self, sim_info: SimInfo, new_aunt_or_uncle_sim_info: SimInfo, parent_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding parent relation', sim=sim_info, new_sim=new_aunt_or_uncle_sim_info, parent_sim=parent_sim_info)
        self.log.format_with_message('Done adding parent relation', sim=sim_info, new_sim=new_aunt_or_uncle_sim_info, parent_sim=parent_sim_info)
        return True

    def _add_new_relation(self, sim_info: SimInfo, new_aunt_or_uncle_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding new aunt/uncle to Sim', sim=sim_info, new_sim=new_aunt_or_uncle_sim_info)
        # Add Aunts/Uncles
        uncle_aunt_sim_info_list = list()
        new_aunt_uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_aunt_or_uncle_sim_info)
        with genealogy_caching():
            for uncle_aunt_sim_info in new_aunt_uncle_genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found aunt/uncle. Adding them as an aunt/uncle to sim.', sim=sim_info, new_aunt_uncle=uncle_aunt_sim_info)
                uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
                CommonRelationshipUtils.add_relationship_bit(sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(uncle_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for uncle_aunt_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(new_aunt_or_uncle_sim_info, (CommonRelationshipBitId.FAMILY_BROTHER_SISTER, CommonRelationshipBitId.FAMILY_STEP_SIBLING), instanced_only=False):
            if uncle_aunt_sim_info in uncle_aunt_sim_info_list:
                continue
            self.log.format_with_message('Found aunt/uncle. Adding them as an aunt/uncle to sim.', sim=sim_info, new_aunt_uncle=uncle_aunt_sim_info)
            uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
            CommonRelationshipUtils.add_relationship_bit(sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(uncle_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Add Cousins
        for uncle_aunt_sim_info in uncle_aunt_sim_info_list:
            uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(uncle_aunt_sim_info)
            with genealogy_caching():
                for cousin_sim_info in uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found a cousin. Adding them as a cousin to sim.', sim=sim_info, new_cousin=cousin_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(cousin_sim_info, sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        with genealogy_caching():
            for cousin_sim_info in new_aunt_uncle_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found a cousin. Adding them as a cousin to sim.', sim=sim_info, new_cousin=cousin_sim_info)
                CommonRelationshipUtils.add_relationship_bit(sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(cousin_sim_info, sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        self.log.format_with_message('Done adding new aunt/uncle', sim=sim_info, new_sim=new_aunt_or_uncle_sim_info)
        return True
