"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.genealogy_tracker import genealogy_caching
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsFatherToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a father of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_PARENT

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_SON_DAUGHTER

    @property
    def _display_name(self) -> int:
        return S4CMSimControlMenuStringId.FATHER

    # noinspection PyMissingOrEmptyDocstring
    def has_relation(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        parent_sim_info_b = CommonSimGenealogyUtils.get_father_sim_info(sim_info_b)
        if parent_sim_info_b is None:
            return False
        if sim_info_a is not parent_sim_info_b:
            return False
        return super().has_relation(sim_info_a, sim_info_b)

    def _update_family_tree(self, new_parent_sim_info: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        self.log.format_with_message('Setting Sim A as father of Sim B', sim_a=new_parent_sim_info, sim_b=sim_info_b)
        try:
            self._set_as_parent(new_parent_sim_info, sim_info_b)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as father.', exception=ex)
            on_completed(False)
        return True

    def _set_as_parent(self, new_parent_sim_info: SimInfo, sim_info_b: SimInfo):
        self.log.format_with_message('Setting Sim A as father of Sim B', sim_a=new_parent_sim_info, sim_b=sim_info_b)
        self._remove_old_parent(sim_info_b)
        self._add_new_parent(sim_info_b, new_parent_sim_info)
        self.log.format_with_message('Done setting Sim A as father of Sim B', sim_a=new_parent_sim_info, sim_b=sim_info_b)
        return True

    def _remove_old_parent(self, sim_info: SimInfo) -> bool:
        self.log.format_with_message('Removing old father from Sim', sim=sim_info)

        # Remove old father.
        old_father_sim_info: SimInfo = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
        if old_father_sim_info is not None:
            self.log.format_with_message('Found an old father. Removing them.', sim=old_father_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, old_father_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(old_father_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_father_relation(sim_info)

            # Remove old Uncles/Aunts
            uncle_aunt_sim_info_list = list()
            old_father_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(old_father_sim_info)
            with genealogy_caching():
                for uncle_aunt_sim_info in old_father_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found an uncle/aunt. Removing them.', sim=uncle_aunt_sim_info)
                    uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(uncle_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            # Remove Cousins
            for uncle_aunt_sim_info in uncle_aunt_sim_info_list:
                uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(uncle_aunt_sim_info)
                with genealogy_caching():
                    for cousin_sim_info in uncle_genealogy_tracker.get_child_sim_infos_gen():
                        self.log.format_with_message('Found a cousin. Removing them.', sim=cousin_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.remove_relationship_bit(cousin_sim_info, sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
            genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(old_father_sim_info)
            with genealogy_caching():
                for brother_sister_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

                    old_brother_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(brother_sister_sim_info)
                    if mother_sim_info is not None and old_brother_mother_sim_info is mother_sim_info:
                        self.log.format_with_message('Found a brother/sister. Changing them to Step Siblings.', sim=brother_sister_sim_info, mother_sim_info=mother_sim_info, old_brother_mother_sim=old_brother_mother_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.add_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    else:
                        self.log.format_with_message('Found a brother/sister. Removing them as Siblings.', sim=brother_sister_sim_info, mother_sim_info=mother_sim_info, old_brother_mother_sim=old_brother_mother_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
            with genealogy_caching():
                for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    CommonRelationshipUtils.remove_relationship_bit(child_sim_info, old_father_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(old_father_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonSimGenealogyUtils.remove_mothers_father_relation(child_sim_info)

        # Remove old grandmother
        old_grandmother_sim_info = CommonSimGenealogyUtils.get_sim_info_of_grandmother_of_sim_on_fathers_side(sim_info)
        if old_grandmother_sim_info is not None:
            self.log.format_with_message('Found an old grandmother on mothers side. Removing them.', sim=old_grandmother_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, old_grandmother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.remove_relationship_bit(old_grandmother_sim_info, sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.remove_fathers_mother_relation(sim_info)

        # Remove old grandfather
        old_grandfather_sim_info = CommonSimGenealogyUtils.get_sim_info_of_grandfather_of_sim_on_fathers_side(sim_info)
        if old_grandfather_sim_info is not None:
            self.log.format_with_message('Found an old grandfather on mothers side. Removing them.', sim=old_grandfather_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, old_grandfather_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.remove_relationship_bit(old_grandfather_sim_info, sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.remove_fathers_father_relation(sim_info)

        self.log.debug('Done removing old father')
        return True

    def _add_new_parent(self, sim_info: SimInfo, new_parent_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding new father to Sim', sim=sim_info, new_parent_sim=new_parent_sim_info)
        # Add new father
        CommonSimGenealogyUtils.set_as_father_of(new_parent_sim_info, sim_info)

        # Add new Uncles/Aunts
        uncle_aunt_sim_info_list = list()
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_parent_sim_info)
        with genealogy_caching():
            for uncle_aunt_sim_info in genealogy_tracker.get_siblings_sim_infos_gen():
                uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
                CommonRelationshipUtils.add_relationship_bit(sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(uncle_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Remove Cousins
        for uncle_aunt_sim_info in uncle_aunt_sim_info_list:
            uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(uncle_aunt_sim_info)
            with genealogy_caching():
                for cousin_sim_info in uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found a cousin. Adding them as cousins to sim.', sim=sim_info, new_cousin=cousin_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(cousin_sim_info, sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_parent_sim_info)
        with genealogy_caching():
            for brother_sister_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                if brother_sister_sim_info is sim_info:
                    continue
                new_brother_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(brother_sister_sim_info)
                if new_brother_mother_sim_info is mother_sim_info:
                    self.log.format_with_message('Found a brother/sister. Adding them as brother/sister to Sim.', sim=sim_info, brother_sister_sim=brother_sister_sim_info, mother=mother_sim_info, new_brother_mother=new_brother_mother_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.add_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.add_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                else:
                    self.log.format_with_message('Found a step brother/step sister. Adding them as step brother/step sister to Sim.', sim=sim_info, brother_sister_sim=brother_sister_sim_info, mother=mother_sim_info, new_brother_mother=new_brother_mother_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.add_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.add_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        with genealogy_caching():
            for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                CommonSimGenealogyUtils.set_as_mothers_father_of(new_parent_sim_info, child_sim_info)

        # Add new grandmother
        new_grandmother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_parent_sim_info)
        if new_grandmother_sim_info is not None:
            self.log.format_with_message('Found grandmother, adding them as grandmother to sim.', sim=sim_info, new_grandmother=new_grandmother_sim_info)
            CommonRelationshipUtils.add_relationship_bit(sim_info, new_grandmother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandmother_sim_info, sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(new_grandmother_sim_info, sim_info)

        # Add new grandfather
        new_grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_parent_sim_info)
        if new_grandfather_sim_info is not None:
            self.log.format_with_message('Found grandfather, adding them as grandfather to sim.', sim=sim_info, new_grandfather=new_grandfather_sim_info)
            CommonRelationshipUtils.add_relationship_bit(sim_info, new_grandfather_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandfather_sim_info, sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_father_of(new_grandfather_sim_info, sim_info)

        self.log.format_with_message('Done adding new father', sim=sim_info, new_father_sim=new_parent_sim_info)
        return True
