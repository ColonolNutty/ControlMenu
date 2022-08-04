"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
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
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation


class CMSetSimAAsFatherToSimBOp(CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a father of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_father'

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
        return CMSimControlMenuStringId.FATHER

    # noinspection PyMissingOrEmptyDocstring
    def has_relation(self, new_parent_sim_info: SimInfo, child_sim_info: SimInfo) -> bool:
        return super().has_relation(new_parent_sim_info, child_sim_info) and CommonSimGenealogyUtils.is_father_of(new_parent_sim_info, child_sim_info)

    def _update_family_tree(self, parent_sim_info: SimInfo, child_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as father of Sim B', sim_a=parent_sim_info, sim_b=child_sim_info)
            if CommonSimGenealogyUtils.has_father(child_sim_info):
                previous_parent_sim_info = CommonSimGenealogyUtils.get_father_sim_info(child_sim_info)
                self._remove_old_relation(previous_parent_sim_info, child_sim_info)
            self._add_new_relation(parent_sim_info, child_sim_info)
            self.log.format_with_message('Done setting Sim A as father of Sim B', sim_a=parent_sim_info, sim_b=child_sim_info)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as father.', exception=ex)
            on_completed(False)
        return True

    def _remove_old_relation(self, previous_parent_sim_info: SimInfo, child_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Removing relations to old family', new_sim=previous_parent_sim_info)
        previous_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_sim_info)
        previous_other_parent_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(child_sim_info)

        previous_parent_alternate_parent_sim_info_list = list()
        previous_parent_remove_blood_children_sim_info_list = list()
        previous_parent_blood_children_sim_info_list = list()
        with genealogy_caching():
            for previous_child_sim_info in previous_parent_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found blood child on mother side.', parent=previous_parent_sim_info, child=previous_child_sim_info)
                if (previous_other_parent_sim_info is None and CommonSimGenealogyUtils.has_mother(previous_child_sim_info)) or CommonSimGenealogyUtils.is_mother_of(previous_other_parent_sim_info, previous_child_sim_info):
                    previous_parent_remove_blood_children_sim_info_list.append(previous_child_sim_info)
                    continue
                previous_child_alternate_father_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(previous_child_sim_info)
                if previous_child_alternate_father_sim_info is not None:
                    previous_parent_alternate_parent_sim_info_list.append(previous_child_alternate_father_sim_info)
                previous_parent_blood_children_sim_info_list.append(previous_child_sim_info)

        previous_parent_blood_siblings_sim_info_list = list()
        with genealogy_caching():
            for previous_sibling_sim_info in previous_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found blood sibling on mother side.', parent=previous_parent_sim_info, sibling=previous_sibling_sim_info)
                previous_parent_blood_siblings_sim_info_list.append(previous_sibling_sim_info)

        previous_parent_alternate_cousin_parent_sim_info_list = list()
        previous_parent_blood_cousins_sim_info_list = list()
        for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
            previous_parent_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_blood_siblings_sim_info)
            with genealogy_caching():
                for previous_parent_blood_cousin_sim_info in previous_parent_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found blood cousin on mother side.', parent=previous_parent_sim_info, cousin=previous_parent_blood_cousin_sim_info)
                    previous_parent_blood_cousins_sim_info_list.append(previous_parent_blood_cousin_sim_info)
                    if CommonSimGenealogyUtils.is_mother_of(previous_parent_blood_siblings_sim_info, previous_parent_blood_cousin_sim_info):
                        cousin_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(previous_parent_blood_cousin_sim_info)
                        if cousin_father_sim_info is not None:
                            previous_parent_alternate_cousin_parent_sim_info_list.append(cousin_father_sim_info)
                    if CommonSimGenealogyUtils.is_father_of(previous_parent_blood_siblings_sim_info, previous_parent_blood_cousin_sim_info):
                        cousin_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(previous_parent_blood_cousin_sim_info)
                        if cousin_mother_sim_info is not None:
                            previous_parent_alternate_cousin_parent_sim_info_list.append(cousin_mother_sim_info)

        previous_parent_step_children_sim_info_list = list()
        for previous_step_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(previous_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
            if previous_step_child_sim_info in previous_parent_blood_children_sim_info_list or previous_step_child_sim_info in previous_parent_remove_blood_children_sim_info_list:
                continue
            self.log.format_with_message('Found step child on mother side.', parent=previous_parent_sim_info, child=previous_step_child_sim_info)
            previous_parent_step_children_sim_info_list.append(previous_step_child_sim_info)

        previous_parent_blood_parent_sim_info_list = list()
        with genealogy_caching():
            for previous_other_parent_parent_parent_sim_info in previous_parent_genealogy_tracker.get_parent_sim_infos_gen():
                self.log.format_with_message('Found blood parent on mother side.', mother=previous_parent_sim_info, parent=previous_other_parent_parent_parent_sim_info)
                previous_parent_blood_parent_sim_info_list.append(previous_other_parent_parent_parent_sim_info)

        # Remove Father Grandparent Relations with Previous Step Children
        for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
            for previous_parent_step_children_sim_info in previous_parent_step_children_sim_info_list:
                self.log.format_with_message('Removing Grandparent.', grandchild=previous_parent_step_children_sim_info, grandparent=previous_parent_blood_parent_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_step_children_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_parent_step_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Remove Blood Relations
        if previous_other_parent_sim_info is not None:
            # Remove Father relations to Mother
            for previous_parent_blood_children_sim_info in previous_parent_blood_children_sim_info_list:
                self.log.format_with_message('Found step child on mothers side.', parent=previous_other_parent_sim_info, step_child=previous_parent_blood_children_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            # Remove Father relations to Mother Parents
            for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                self.log.format_with_message('Found step parent on mothers side.', parent=previous_other_parent_sim_info, step_parent=previous_parent_blood_parent_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

            # Remove Father Sibling Step Sibling Relations with Mother One
            for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                self.log.format_with_message('Found step sibling on mothers side.', parent=previous_other_parent_sim_info, step_sibling=previous_parent_blood_siblings_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            # Remove Father Siblings Children Relations with Mother One
            for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                self.log.format_with_message('Found cousin on mothers side.', parent=previous_other_parent_sim_info, cousin=previous_parent_blood_cousins_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            previous_father_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_other_parent_sim_info)
            with genealogy_caching():
                for previous_other_parent_parent_parent_sim_info in previous_father_genealogy_tracker.get_parent_sim_infos_gen():
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_other_parent_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_parent_parent_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                    # Remove Father Sibling Uncle/Aunt Relations with Mother Parent
                    for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                        self.log.format_with_message('Found step parent on fathers side.', parent=previous_parent_blood_siblings_sim_info, step_parent=previous_other_parent_parent_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_parent_parent_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_other_parent_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

                    # Remove Father Cousin Relations with Mother Parent
                    for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                        self.log.format_with_message('Found step grandparent on fathers side.', parent=previous_parent_blood_cousins_sim_info, step_parent=previous_other_parent_parent_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_parent_parent_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_other_parent_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

                    # Remove Father Children Relations with Mother Parent
                    for previous_parent_blood_children_sim_info in previous_parent_blood_children_sim_info_list:
                        self.log.format_with_message('Found step grandparent on fathers side.', parent=previous_parent_blood_children_sim_info, step_parent=previous_other_parent_parent_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_parent_parent_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_other_parent_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            previous_father_blood_children_sim_info_list = list()
            with genealogy_caching():
                for previous_child_sim_info in previous_father_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found blood children on father side.', parent=previous_other_parent_sim_info, child=previous_child_sim_info)
                    previous_father_blood_children_sim_info_list.append(previous_child_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                    # Remove Father Child Sibling Relations with Mother Children
                    for previous_parent_blood_children_sim_info in previous_parent_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                    # Remove Father Sibling Uncle/Aunt Relations with Mother Children
                    for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    # Remove Father Cousin Relations with Mother Children
                    for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                    # Remove Father Parent Relations with Mother Children
                    for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            previous_father_step_children_sim_info_list = list()
            for previous_step_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                if previous_step_child_sim_info in previous_father_blood_children_sim_info_list or previous_step_child_sim_info in previous_father_step_children_sim_info_list:
                    continue
                previous_father_step_children_sim_info_list.append(previous_step_child_sim_info)
                self.log.format_with_message('Found step child on fathers side.', parent=previous_other_parent_sim_info, child=previous_step_child_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_step_child_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_step_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                    self.log.format_with_message('Removing Step Grandparent.', grandchild=previous_step_child_sim_info, grandparent=previous_parent_blood_parent_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_step_child_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_step_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            previous_father_blood_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_sibling_sim_info in previous_father_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found blood sibling on father side.', parent=previous_other_parent_sim_info, sibling=previous_sibling_sim_info)
                    previous_father_blood_siblings_sim_info_list.append(previous_sibling_sim_info)

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Children
                    for previous_parent_blood_children_sim_info in previous_parent_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Cousins
                    for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                    # Remove Father Sibling Step Sibling Relations with Mother Siblings
                    for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                    # Remove Father Sibling relations to Mother Parents
                    for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

            previous_father_blood_parent_sim_info_list = list()
            with genealogy_caching():
                for previous_other_parent_parent_parent_sim_info in previous_father_genealogy_tracker.get_parent_sim_infos_gen():
                    self.log.format_with_message('Found blood grandparent on father side.', parent=previous_other_parent_sim_info, grandparent=previous_other_parent_parent_parent_sim_info)
                    previous_father_blood_parent_sim_info_list.append(previous_other_parent_parent_parent_sim_info)

            # Remove Father Parent Relations with Mother One Children
            for previous_father_blood_children_sim_info in previous_father_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_father_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            # Remove Father Sibling Step Sibling Relations with Mother One Siblings
            previous_father_blood_cousins_sim_info_list = list()
            for previous_father_blood_siblings_sim_info in previous_father_blood_siblings_sim_info_list:
                previous_father_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_father_blood_siblings_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_father_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_siblings_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                with genealogy_caching():
                    for previous_cousin_sim_info in previous_father_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        previous_father_blood_cousins_sim_info_list.append(previous_cousin_sim_info)

            for previous_father_blood_cousins_sim_info in previous_father_blood_cousins_sim_info_list:
                for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                    self.log.format_with_message('Found step grandparent on mother side.', cousin=previous_father_blood_cousins_sim_info, grandparent=previous_parent_blood_parent_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_father_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_cousins_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Father Parent Relations with Mother One Children
            for previous_father_blood_parent_sim_info in previous_father_blood_parent_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_parent_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_father_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
        else:
            previous_parent_step_children_sim_info_list = list()
            for previous_step_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING, instanced_only=False):
                if previous_step_child_sim_info in previous_parent_remove_blood_children_sim_info_list or previous_step_child_sim_info in previous_parent_blood_children_sim_info_list:
                    continue
                previous_parent_step_children_sim_info_list.append(previous_step_child_sim_info)
                self.log.format_with_message('Found step sibling.', parent=child_sim_info, child=previous_step_child_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_step_child_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_step_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                    self.log.format_with_message('Removing Step Grandparent.', grandchild=previous_step_child_sim_info, grandparent=previous_parent_blood_parent_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_step_child_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_step_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                self.log.format_with_message('Found blood children on mother side.', parent=previous_parent_sim_info, child=previous_parent_remove_blood_children_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                # Remove Father Child Sibling Relations with Mother Children
                for previous_parent_blood_children_sim_info in previous_parent_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                # Remove Father Sibling Uncle/Aunt Relations with Mother Children
                for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                # Remove Father Cousin Relations with Mother Children
                for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # ------------------------Remove Fathers Parent Blood Relations With Previous Children------------------------
        for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
            for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                self.log.format_with_message('Removing Blood Grandparent.', grandchild=previous_parent_remove_blood_children_sim_info, grandparent=previous_parent_blood_parent_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                if CommonSimGenealogyUtils.is_father_of(previous_parent_blood_parent_sim_info, previous_parent_sim_info):
                    CommonSimGenealogyUtils.remove_fathers_father_relation(previous_parent_remove_blood_children_sim_info)
                if CommonSimGenealogyUtils.is_mother_of(previous_parent_blood_parent_sim_info, previous_parent_sim_info):
                    CommonSimGenealogyUtils.remove_fathers_mother_relation(previous_parent_remove_blood_children_sim_info)

            previous_parent_remove_blood_children_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_remove_blood_children_sim_info)
            with genealogy_caching():
                for previous_parent_remove_blood_grandchildren in previous_parent_remove_blood_children_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Removing Blood Grandchild', grandchild=previous_parent_remove_blood_grandchildren, grandmother=previous_parent_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_grandchildren, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_parent_remove_blood_grandchildren, CommonRelationshipBitId.FAMILY_GRANDCHILD)

                    if CommonSimGenealogyUtils.is_mother_of(previous_parent_remove_blood_children_sim_info, previous_parent_remove_blood_grandchildren):
                        CommonSimGenealogyUtils.remove_mothers_father_relation(previous_parent_remove_blood_grandchildren)
                    if CommonSimGenealogyUtils.is_father_of(previous_parent_remove_blood_children_sim_info, previous_parent_remove_blood_grandchildren):
                        CommonSimGenealogyUtils.remove_fathers_father_relation(previous_parent_remove_blood_grandchildren)

        # Remove Father Parent Relations with Previous Children
        for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
            self.log.format_with_message('Removing Blood parent.', child=previous_parent_remove_blood_children_sim_info, parent=previous_parent_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_father_relation(previous_parent_remove_blood_children_sim_info)

        # Remove Father Parent Relations with Previous Step Children
        for previous_parent_step_children_sim_info in previous_parent_step_children_sim_info_list:
            self.log.format_with_message('Removing Step parent.', step_child=previous_parent_step_children_sim_info, parent=previous_parent_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_step_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_parent_step_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        # ------------------------Remove Step Parent on Father Side Relations With Previous Children------------------------

        for previous_parent_alternate_parent_sim_info in previous_parent_alternate_parent_sim_info_list:
            self.log.format_with_message('Removing step step parent.', child=previous_parent_alternate_parent_sim_info, parent=previous_parent_sim_info)
            previous_parent_alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_alternate_parent_sim_info)

            previous_parent_alternate_parent_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_sibling_sim_info in previous_parent_alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found step parent sibling on mother side.', parent=previous_parent_alternate_parent_sim_info, sibling=previous_sibling_sim_info)
                    previous_parent_alternate_parent_siblings_sim_info_list.append(previous_sibling_sim_info)

                    # Remove Mother Sibling Aunt/Uncle Relations with Father Children
                    for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

            for previous_parent_alternate_parent_siblings_sim_info in previous_parent_alternate_parent_siblings_sim_info_list:
                previous_parent_alternate_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_alternate_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_cousin_sim_info in previous_parent_alternate_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                            CommonRelationshipUtils.remove_relationship_bit(previous_cousin_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                            CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            previous_parent_alternate_parent_parent_sim_info_list = list()
            with genealogy_caching():
                for previous_other_parent_parent_parent_sim_info in previous_parent_alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    self.log.format_with_message('Found step grandparent on mother side.', parent=previous_parent_alternate_parent_sim_info, grandparent=previous_other_parent_parent_parent_sim_info)
                    previous_parent_alternate_parent_parent_sim_info_list.append(previous_other_parent_parent_parent_sim_info)

            # Remove Father Parent Relations with Mother One Children
            for previous_parent_alternate_parent_parent_sim_info in previous_parent_alternate_parent_parent_sim_info_list:
                for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_alternate_parent_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_alternate_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Alternate Parent Relation with Mother One Children
            for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_alternate_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_alternate_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

        # ------------------------Remove Step Parent on Mother Blood Side Relations With Previous Children------------------------

        for previous_parent_alternate_cousin_parent_sim_info in previous_parent_alternate_cousin_parent_sim_info_list:
            self.log.format_with_message('Removing step uncle/aunt.', parent=previous_parent_alternate_cousin_parent_sim_info)
            previous_parent_alternate_cousin_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_alternate_cousin_parent_sim_info)

            previous_parent_alternate_cousin_parent_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_sibling_sim_info in previous_parent_alternate_cousin_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found step parent sibling on mother side.', parent=previous_parent_alternate_cousin_parent_sim_info, sibling=previous_sibling_sim_info)
                    previous_parent_alternate_cousin_parent_siblings_sim_info_list.append(previous_sibling_sim_info)

                    # Remove Mother Sibling Aunt/Uncle Relations with Father Children
                    for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

            for previous_parent_alternate_cousin_parent_siblings_sim_info in previous_parent_alternate_cousin_parent_siblings_sim_info_list:
                previous_parent_alternate_cousin_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_alternate_cousin_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_cousin_sim_info in previous_parent_alternate_cousin_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                            CommonRelationshipUtils.remove_relationship_bit(previous_cousin_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                            CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            previous_parent_alternate_cousin_parent_parent_sim_info_list = list()
            with genealogy_caching():
                for previous_other_parent_parent_parent_sim_info in previous_parent_alternate_cousin_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    self.log.format_with_message('Found step grandparent on mother side.', parent=previous_parent_alternate_cousin_parent_sim_info, grandparent=previous_other_parent_parent_parent_sim_info)
                    previous_parent_alternate_cousin_parent_parent_sim_info_list.append(previous_other_parent_parent_parent_sim_info)

            # Remove Father Alternate Uncle/Aunt Relations with Mother One Children
            for previous_parent_alternate_cousin_parent_parent_sim_info in previous_parent_alternate_cousin_parent_parent_sim_info_list:
                for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_alternate_cousin_parent_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_alternate_cousin_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Alternate Uncle/Aunt Relation with Mother One Children
            for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_alternate_cousin_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        self.log.format_with_message('Done removing relations to old family', new_sim=previous_parent_sim_info)
        return True

    def _add_new_relation(self, new_parent_sim_info: SimInfo, child_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding relation to Sim', child=child_sim_info, parent=new_parent_sim_info)

        child_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(child_sim_info)
        new_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_parent_sim_info)

        new_parent_blood_siblings_sim_info_list = list()
        with genealogy_caching():
            for new_sibling_sim_info in new_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                if new_sibling_sim_info in new_parent_blood_siblings_sim_info_list:
                    self.log.debug('Duplicate 1')
                    continue
                self.log.format_with_message('Found blood sibling on mother side.', parent=new_parent_sim_info, sibling=new_sibling_sim_info)
                new_parent_blood_siblings_sim_info_list.append(new_sibling_sim_info)

        new_parent_alternate_parent_sim_info_list = list()
        new_parent_blood_children_sim_info_list = list()
        with genealogy_caching():
            for new_child_sim_info in new_parent_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found blood child on mother side.', parent=new_parent_sim_info, child=new_child_sim_info)
                if new_child_sim_info not in new_parent_blood_children_sim_info_list:
                    new_parent_blood_children_sim_info_list.append(new_child_sim_info)
                else:
                    self.log.debug('Duplicate 2')
                if CommonSimGenealogyUtils.is_father_of(new_parent_sim_info, new_child_sim_info):
                    new_child_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_child_sim_info)
                    if new_child_mother_sim_info is not None and new_child_mother_sim_info not in new_parent_alternate_parent_sim_info_list:
                        self.log.format_with_message('Found alternative mother', child=new_child_sim_info, mother=new_child_mother_sim_info)
                        new_parent_alternate_parent_sim_info_list.append(new_child_mother_sim_info)
                if CommonSimGenealogyUtils.is_mother_of(new_parent_sim_info, new_child_sim_info):
                    new_child_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_child_sim_info)
                    if new_child_father_sim_info is not None and new_child_father_sim_info not in new_parent_alternate_parent_sim_info_list:
                        self.log.format_with_message('Found alternative father', child=new_child_sim_info, father=new_child_father_sim_info)
                        new_parent_alternate_parent_sim_info_list.append(new_child_father_sim_info)

        new_parent_alternate_parent_parent_sim_info_list = list()
        new_parent_alternate_parent_siblings_sim_info_list = list()
        new_parent_alternate_parent_children_sim_info_list = list()
        for new_parent_alternate_parent_sim_info in new_parent_alternate_parent_sim_info_list:
            self.log.format_with_message('Alternative parent', alt_parent=new_parent_alternate_parent_sim_info)
            new_parent_alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_parent_alternate_parent_sim_info)
            with genealogy_caching():
                for new_sibling_sim_info in new_parent_alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    if new_sibling_sim_info in new_parent_alternate_parent_siblings_sim_info_list:
                        self.log.debug('Duplicate 3')
                        continue
                    new_parent_alternate_parent_siblings_sim_info_list.append(new_sibling_sim_info)

            with genealogy_caching():
                for new_step_sibling_sim_info in new_parent_alternate_parent_genealogy_tracker.get_child_sim_infos_gen():
                    if new_step_sibling_sim_info in new_parent_blood_children_sim_info_list or new_step_sibling_sim_info in new_parent_alternate_parent_children_sim_info_list:
                        self.log.debug('Duplicate 4')
                        continue
                    new_parent_alternate_parent_children_sim_info_list.append(new_step_sibling_sim_info)
            with genealogy_caching():
                for new_grandparent_sim_info in new_parent_alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    if new_grandparent_sim_info in new_parent_alternate_parent_parent_sim_info_list:
                        self.log.debug('Duplicate 5')
                        continue
                    new_parent_alternate_parent_parent_sim_info_list.append(new_grandparent_sim_info)

        new_parent_alternate_parent_cousin_sim_info_list = list()
        for new_parent_alternate_parent_siblings_sim_info in new_parent_alternate_parent_siblings_sim_info_list:
            new_parent_alternate_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_parent_alternate_parent_siblings_sim_info)
            with genealogy_caching():
                for new_step_sibling_sim_info in new_parent_alternate_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                    if new_step_sibling_sim_info in new_parent_alternate_parent_cousin_sim_info_list:
                        self.log.debug('Duplicate 6')
                        continue
                    new_parent_alternate_parent_cousin_sim_info_list.append(new_step_sibling_sim_info)

        new_parent_alternate_cousin_parent_sim_info_list = list()
        new_parent_blood_cousins_sim_info_list = list()
        for new_parent_blood_siblings_sim_info in new_parent_blood_siblings_sim_info_list:
            new_parent_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_parent_blood_siblings_sim_info)
            with genealogy_caching():
                for new_cousin_sim_info in new_parent_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found blood cousin on mother side.', parent=new_parent_sim_info, cousin=new_cousin_sim_info)
                    if new_cousin_sim_info not in new_parent_blood_cousins_sim_info_list:
                        new_parent_blood_cousins_sim_info_list.append(new_cousin_sim_info)
                    else:
                        self.log.debug('Duplicate 7')
                    if CommonSimGenealogyUtils.is_father_of(new_parent_blood_siblings_sim_info, new_cousin_sim_info):
                        new_cousin_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_cousin_sim_info)
                        if new_cousin_mother_sim_info is not None and new_cousin_mother_sim_info not in new_parent_alternate_cousin_parent_sim_info_list:
                            new_parent_alternate_cousin_parent_sim_info_list.append(new_cousin_mother_sim_info)
                    if CommonSimGenealogyUtils.is_mother_of(new_parent_blood_siblings_sim_info, new_cousin_sim_info):
                        new_cousin_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_cousin_sim_info)
                        if new_cousin_father_sim_info is not None and new_cousin_father_sim_info not in new_parent_alternate_cousin_parent_sim_info_list:
                            new_parent_alternate_cousin_parent_sim_info_list.append(new_cousin_father_sim_info)

        new_parent_alternate_cousin_parent_parent_sim_info_list = list()
        new_parent_alternate_cousin_parent_siblings_sim_info_list = list()
        new_parent_alternate_cousin_parent_children_sim_info_list = list()
        for new_parent_alternate_cousin_parent_sim_info in new_parent_alternate_cousin_parent_sim_info_list:
            new_parent_alternate_cousin_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_parent_alternate_cousin_parent_sim_info)
            with genealogy_caching():
                for new_cousin_sim_info in new_parent_alternate_cousin_parent_genealogy_tracker.get_child_sim_infos_gen():
                    if new_cousin_sim_info in new_parent_alternate_cousin_parent_children_sim_info_list:
                        self.log.debug('Duplicate 8')
                        continue
                    new_parent_alternate_cousin_parent_children_sim_info_list.append(new_cousin_sim_info)
            with genealogy_caching():
                for new_uncle_aunt_sim_info in new_parent_alternate_cousin_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    if new_uncle_aunt_sim_info in new_parent_alternate_cousin_parent_siblings_sim_info_list:
                        self.log.debug('Duplicate 9')
                        continue
                    new_parent_alternate_cousin_parent_siblings_sim_info_list.append(new_uncle_aunt_sim_info)
            with genealogy_caching():
                for new_grandparent_sim_info in new_parent_alternate_cousin_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    if new_grandparent_sim_info in new_parent_alternate_cousin_parent_parent_sim_info_list:
                        self.log.debug('Duplicate 10')
                        continue
                    new_parent_alternate_cousin_parent_parent_sim_info_list.append(new_grandparent_sim_info)

        # Mother One New as Mother of New Child
        new_parent_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_parent_sim_info)
        new_parent_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_parent_sim_info)

        new_parent_grandparents_sim_info_list = (
            new_parent_father_sim_info,
            new_parent_mother_sim_info
        )

        previous_other_parent_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(child_sim_info)

        children_sim_info_list = list()
        step_children_sim_info_list = list()
        if previous_other_parent_sim_info is not None:
            previous_other_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_other_parent_sim_info)
            # Grandparents
            previous_other_parent_blood_parents_sim_info_list = list()
            # Uncle/Aunt
            previous_other_parent_blood_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_other_parent_blood_sibling_sim_info in previous_other_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    if previous_other_parent_blood_sibling_sim_info in previous_other_parent_blood_siblings_sim_info_list:
                        self.log.debug('Duplicate 11')
                        continue
                    previous_other_parent_blood_siblings_sim_info_list.append(previous_other_parent_blood_sibling_sim_info)
            with genealogy_caching():
                for previous_other_parent_blood_parents_sim_info in previous_other_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    if previous_other_parent_blood_parents_sim_info in previous_other_parent_blood_parents_sim_info_list:
                        self.log.debug('Duplicate 12')
                        continue
                    previous_other_parent_blood_parents_sim_info_list.append(previous_other_parent_blood_parents_sim_info)

            # Uncle/Aunt
            previous_other_parent_blood_alternate_cousin_parent_sim_info_list = list()
            # Cousin
            previous_other_parent_blood_sibling_cousin_sim_info_list = list()
            for previous_other_parent_blood_siblings_sim_info in previous_other_parent_blood_siblings_sim_info_list:
                previous_other_parent_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_other_parent_blood_siblings_sim_info)
                with genealogy_caching():
                    for previous_other_parent_blood_sibling_cousin_sim_info in previous_other_parent_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        if previous_other_parent_blood_sibling_cousin_sim_info not in previous_other_parent_blood_sibling_cousin_sim_info_list:
                            previous_other_parent_blood_sibling_cousin_sim_info_list.append(previous_other_parent_blood_sibling_cousin_sim_info)
                        else:
                            self.log.debug('Duplicate 13')
                        if CommonSimGenealogyUtils.is_father_of(previous_other_parent_blood_siblings_sim_info, previous_other_parent_blood_sibling_cousin_sim_info):
                            previous_other_parent_blood_sibling_cousin_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(previous_other_parent_blood_sibling_cousin_sim_info)
                            if previous_other_parent_blood_sibling_cousin_mother_sim_info is not None and previous_other_parent_blood_sibling_cousin_mother_sim_info not in previous_other_parent_blood_alternate_cousin_parent_sim_info_list:
                                previous_other_parent_blood_alternate_cousin_parent_sim_info_list.append(previous_other_parent_blood_sibling_cousin_mother_sim_info)
                        if CommonSimGenealogyUtils.is_mother_of(previous_other_parent_blood_siblings_sim_info, previous_other_parent_blood_sibling_cousin_sim_info):
                            previous_other_parent_blood_sibling_cousin_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(previous_other_parent_blood_sibling_cousin_sim_info)
                            if previous_other_parent_blood_sibling_cousin_father_sim_info is not None and previous_other_parent_blood_sibling_cousin_father_sim_info not in previous_other_parent_blood_alternate_cousin_parent_sim_info_list:
                                previous_other_parent_blood_alternate_cousin_parent_sim_info_list.append(previous_other_parent_blood_sibling_cousin_father_sim_info)

            # Grandparents
            previous_other_parent_blood_alternate_cousin_parent_parents_sim_info_list = list()
            # Uncle/Aunt
            previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info_list = list()
            # Cousin
            previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info_list = list()
            for previous_other_parent_blood_alternate_cousin_parent_sim_info in previous_other_parent_blood_alternate_cousin_parent_sim_info_list:
                previous_other_parent_blood_alternate_cousin_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_other_parent_blood_alternate_cousin_parent_sim_info)
                with genealogy_caching():
                    for previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info in previous_other_parent_blood_alternate_cousin_parent_genealogy_tracker.get_child_sim_infos_gen():
                        if previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info in previous_other_parent_blood_sibling_cousin_sim_info_list or previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info in previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info_list:
                            self.log.debug('Duplicate 14')
                            continue
                        previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info_list.append(previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info)
                with genealogy_caching():
                    for previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info in previous_other_parent_blood_alternate_cousin_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                        if previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info in previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info_list:
                            self.log.debug('Duplicate 15')
                            continue
                        previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info_list.append(previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_other_parent_blood_alternate_cousin_parent_parents_sim_info in previous_other_parent_blood_alternate_cousin_parent_genealogy_tracker.get_parent_sim_infos_gen():
                        if previous_other_parent_blood_alternate_cousin_parent_parents_sim_info in previous_other_parent_blood_alternate_cousin_parent_parents_sim_info_list:
                            self.log.debug('Duplicate 16')
                            continue
                        previous_other_parent_blood_alternate_cousin_parent_parents_sim_info_list.append(previous_other_parent_blood_alternate_cousin_parent_parents_sim_info)

            # Cousin
            previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info_list = list()
            for previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info in previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info_list:
                previous_other_parent_blood_alternate_cousin_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info in previous_other_parent_blood_alternate_cousin_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        if previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info in previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info_list:
                            self.log.debug('Duplicate 17')
                            continue
                        previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info_list.append(previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info)

            # Previous Father To New Mother
            for previous_other_parent_blood_siblings_sim_info in previous_other_parent_blood_siblings_sim_info_list:
                self.log.format_with_message('Setting as step sibling 1', step_sibling=previous_other_parent_blood_siblings_sim_info, parent=new_parent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_siblings_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, previous_other_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            for previous_other_parent_blood_parents_sim_info in previous_other_parent_blood_parents_sim_info_list:
                self.log.format_with_message('Setting as step parent 1', step_parent=previous_other_parent_blood_parents_sim_info, parent=new_parent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_parents_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, previous_other_parent_blood_parents_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

            for previous_other_parent_blood_sibling_cousin_sim_info in previous_other_parent_blood_sibling_cousin_sim_info_list:
                self.log.format_with_message('Setting as step niece/nephew 4', step_niece_nephew=previous_other_parent_blood_sibling_cousin_sim_info, parent=new_parent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_sibling_cousin_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, previous_other_parent_blood_sibling_cousin_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            # Previous Father Family To New Mother Children
            for new_parent_child_sim_info in new_parent_blood_children_sim_info_list:
                self.log.format_with_message('Setting as step parent 3', parent=previous_other_parent_sim_info, child=new_parent_child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_other_parent_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

                for previous_other_parent_blood_parents_sim_info in previous_other_parent_blood_parents_sim_info_list:
                    self.log.format_with_message('Setting as step grandparent 3', grandparent=previous_other_parent_blood_parents_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_parents_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_parents_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

                for previous_other_parent_blood_alternate_cousin_parent_parents_sim_info in previous_other_parent_blood_alternate_cousin_parent_parents_sim_info_list:
                    self.log.format_with_message('Setting as step grandparent 4', grandparent=previous_other_parent_blood_alternate_cousin_parent_parents_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_alternate_cousin_parent_parents_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_alternate_cousin_parent_parents_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

                for previous_other_parent_blood_siblings_sim_info in previous_other_parent_blood_siblings_sim_info_list:
                    self.log.format_with_message('Setting as step aunt/uncle 4', aunt_uncle=previous_other_parent_blood_siblings_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_siblings_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                for previous_other_parent_blood_alternate_cousin_parent_sim_info in previous_other_parent_blood_alternate_cousin_parent_sim_info_list:
                    self.log.format_with_message('Setting as step aunt/uncle 5', aunt_uncle=previous_other_parent_blood_alternate_cousin_parent_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_alternate_cousin_parent_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                for previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info in previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info_list:
                    self.log.format_with_message('Setting as step aunt/uncle 6', aunt_uncle=previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_alternate_cousin_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                for previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info in previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info_list:
                    self.log.format_with_message('Setting as step cousin 6', cousin=previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_alternate_cousin_parent_siblings_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for previous_other_parent_blood_sibling_cousin_sim_info in previous_other_parent_blood_sibling_cousin_sim_info_list:
                    self.log.format_with_message('Setting as step cousin 4', cousin=previous_other_parent_blood_sibling_cousin_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_sibling_cousin_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_sibling_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info in previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info_list:
                    self.log.format_with_message('Setting as step cousin 5', cousin=previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info, child=new_parent_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, previous_other_parent_blood_alternate_cousin_parent_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            with genealogy_caching():
                for new_blood_child_sim_info in child_genealogy_tracker.get_siblings_sim_infos_gen():
                    if new_blood_child_sim_info in children_sim_info_list:
                        self.log.debug('Duplicate 18')
                        continue
                    children_sim_info_list.append(new_blood_child_sim_info)

            for previous_step_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                if previous_step_child_sim_info in children_sim_info_list or previous_step_child_sim_info in step_children_sim_info_list or previous_step_child_sim_info is child_sim_info or previous_step_child_sim_info in new_parent_blood_children_sim_info_list:
                    continue
                self.log.format_with_message('Adding Step Child', step_child=previous_step_child_sim_info)
                step_children_sim_info_list.append(previous_step_child_sim_info)
        else:
            # Mother One New as Mother of New Child Siblings
            for new_blood_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER, instanced_only=False):
                if new_blood_child_sim_info in children_sim_info_list:
                    self.log.debug('Duplicate 19')
                    continue
                children_sim_info_list.append(new_blood_child_sim_info)

            for previous_step_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING, instanced_only=False):
                if previous_step_child_sim_info in children_sim_info_list or previous_step_child_sim_info in step_children_sim_info_list or previous_step_child_sim_info is child_sim_info or previous_step_child_sim_info in new_parent_blood_children_sim_info_list:
                    continue
                self.log.format_with_message('Adding Step Child', step_child=previous_step_child_sim_info)
                step_children_sim_info_list.append(previous_step_child_sim_info)

        if child_sim_info not in children_sim_info_list:
            children_sim_info_list.append(child_sim_info)
        else:
            self.log.debug('Duplicate 20')

        children_children_sim_info_list = list()
        for new_blood_child_sim_info in children_sim_info_list:
            self.log.format_with_message('Setting as mother', child=new_blood_child_sim_info, mother=new_parent_sim_info)
            CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonSimGenealogyUtils.set_as_father_of(new_parent_sim_info, new_blood_child_sim_info)

            for new_parent_blood_siblings_sim_info in new_parent_blood_siblings_sim_info_list:
                self.log.format_with_message('Setting as aunt/uncle', child=new_blood_child_sim_info, aunt_uncle=new_parent_blood_siblings_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(new_parent_blood_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_parent_alternate_cousin_parent_sim_info in new_parent_alternate_cousin_parent_sim_info_list:
                self.log.format_with_message('Setting as aunt/uncle 2', child=new_blood_child_sim_info, aunt_uncle=new_parent_alternate_cousin_parent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_cousin_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_parent_alternate_cousin_parent_siblings_sim_info in new_parent_alternate_cousin_parent_siblings_sim_info_list:
                self.log.format_with_message('Setting as aunt/uncle 3', child=new_blood_child_sim_info, aunt_uncle=new_parent_alternate_cousin_parent_siblings_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_cousin_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_cousin_parent_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_parent_alternate_cousin_parent_children_sim_info in new_parent_alternate_cousin_parent_children_sim_info_list:
                self.log.format_with_message('Setting as cousin', child=new_blood_child_sim_info, cousin=new_parent_alternate_cousin_parent_children_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_cousin_parent_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_cousin_parent_children_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            for new_parent_alternate_cousin_parent_parent_sim_info in new_parent_alternate_cousin_parent_parent_sim_info_list:
                self.log.format_with_message('Setting as step grandparent', child=new_blood_child_sim_info, grandparent=new_parent_alternate_cousin_parent_parent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_cousin_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_cousin_parent_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            for new_parent_child_sim_info in new_parent_blood_children_sim_info_list:
                self.log.format_with_message('Setting as sibling', child=new_blood_child_sim_info, sibling=new_parent_child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                CommonRelationshipUtils.add_relationship_bit(new_parent_child_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

            for new_parent_blood_cousins_sim_info in new_parent_blood_cousins_sim_info_list:
                self.log.format_with_message('Setting as cousin 2', child=new_blood_child_sim_info, cousin=new_parent_blood_cousins_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(new_parent_blood_cousins_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            for new_parent_alternate_parent_sim_info in new_parent_alternate_parent_sim_info_list:
                self.log.format_with_message('Setting as step parent', child=new_blood_child_sim_info, parent=new_parent_alternate_parent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            for new_parent_alternate_parent_parent_sim_info in new_parent_alternate_parent_parent_sim_info_list:
                self.log.format_with_message('Setting as step grandparent', child=new_blood_child_sim_info, grandparent=new_parent_alternate_parent_parent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_parent_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            for new_parent_alternate_parent_siblings_sim_info in new_parent_alternate_parent_siblings_sim_info_list:
                self.log.format_with_message('Setting as step aunt/uncle', child=new_blood_child_sim_info, uncle_aunt=new_parent_alternate_parent_siblings_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_parent_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_parent_alternate_parent_children_sim_info in new_parent_alternate_parent_children_sim_info_list:
                self.log.format_with_message('Setting as step sibling', child=new_blood_child_sim_info, step_sibling=new_parent_alternate_parent_children_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_parent_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_parent_children_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            for new_parent_alternate_parent_cousin_sim_info in new_parent_alternate_parent_cousin_sim_info_list:
                self.log.format_with_message('Setting as step cousin', child=new_blood_child_sim_info, cousin=new_parent_alternate_parent_cousin_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_alternate_parent_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(new_parent_alternate_parent_cousin_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            if new_parent_father_sim_info is not None:
                self.log.format_with_message('Setting as grandfather', child=new_blood_child_sim_info, grandfather=new_parent_father_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_father_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_parent_father_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                CommonSimGenealogyUtils.set_as_fathers_father_of(new_parent_father_sim_info, new_blood_child_sim_info)

            if new_parent_mother_sim_info is not None:
                self.log.format_with_message('Setting as grandfather', child=new_blood_child_sim_info, grandfather=new_parent_mother_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_parent_mother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_parent_mother_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                CommonSimGenealogyUtils.set_as_fathers_mother_of(new_parent_mother_sim_info, new_blood_child_sim_info)

            new_blood_child_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_blood_child_sim_info)
            with genealogy_caching():
                for new_grandchild_sim_info in new_blood_child_genealogy_tracker.get_child_sim_infos_gen():
                    if new_grandchild_sim_info in children_children_sim_info_list:
                        continue
                    self.log.format_with_message('Setting as grandmother', grandchild=new_grandchild_sim_info, grandmother=new_parent_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    if CommonSimGenealogyUtils.is_mother_of(new_blood_child_sim_info, new_grandchild_sim_info):
                        CommonSimGenealogyUtils.set_as_mothers_father_of(new_parent_sim_info, new_grandchild_sim_info)
                    if CommonSimGenealogyUtils.is_father_of(new_blood_child_sim_info, new_grandchild_sim_info):
                        CommonSimGenealogyUtils.set_as_fathers_father_of(new_parent_sim_info, new_grandchild_sim_info)

        for step_child_sim_info in step_children_sim_info_list:
            self.log.format_with_message('Setting as step mother.', step_mother=child_sim_info, child=step_child_sim_info)
            CommonRelationshipUtils.add_relationship_bit(step_child_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, step_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            for new_blood_child_sim_info in children_sim_info_list:
                self.log.format_with_message('Setting as step sibling.', step_sibling=new_blood_child_sim_info, child=step_child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(step_child_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, step_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            for new_parent_grandparents_sim_info in new_parent_grandparents_sim_info_list:
                self.log.format_with_message('Setting as Step Grandparent.', grandchild=step_child_sim_info, grandparent=new_parent_grandparents_sim_info)
                CommonRelationshipUtils.add_relationship_bit(step_child_sim_info, new_parent_grandparents_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_parent_grandparents_sim_info, step_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            step_child_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(step_child_sim_info)
            with genealogy_caching():
                for new_grandchild_sim_info in step_child_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Setting as grandmother', grandchild=new_grandchild_sim_info, grandmother=new_parent_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_parent_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

                    for new_blood_child_sim_info in children_sim_info_list:
                        self.log.format_with_message('Setting as step uncle/aunt.', uncle_aunt=new_blood_child_sim_info, niece_nephew=new_grandchild_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    for children_children_sim_info in children_children_sim_info_list:
                        self.log.format_with_message('Setting as step uncle/aunt.', cousin=children_children_sim_info, cousin_two=new_grandchild_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, children_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.add_relationship_bit(children_children_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        self.log.format_with_message('Done adding relation', child=child_sim_info, mother=new_parent_sim_info)
        return True
