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
from sims4controlmenu.commonlib.utils.common_sim_genealogy_utils import CommonSimGenealogyUtils
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
    def has_relation(self, new_parent_sim_info: SimInfo, child_sim_info: SimInfo) -> bool:
        return super().has_relation(new_parent_sim_info, child_sim_info) and CommonSimGenealogyUtils.is_father_of(new_parent_sim_info, child_sim_info)

    def _update_family_tree(self, parent_sim_info: SimInfo, child_sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
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
        previous_other_parent_sim_info = CommonSimGenealogyUtils.get_father_sim_info(child_sim_info)

        previous_parent_alternate_parent_sim_info_list = list()
        previous_parent_remove_blood_children_sim_info_list = list()
        previous_parent_blood_children_sim_info_list = list()
        with genealogy_caching():
            for previous_child_sim_info in previous_parent_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found blood child on mother side.', parent=previous_parent_sim_info, child=previous_child_sim_info)
                if (previous_other_parent_sim_info is None and CommonSimGenealogyUtils.has_father(previous_child_sim_info)) or CommonSimGenealogyUtils.is_father_of(previous_other_parent_sim_info, previous_child_sim_info):
                    previous_parent_remove_blood_children_sim_info_list.append(previous_child_sim_info)
                    continue
                previous_child_alternate_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(previous_child_sim_info)
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

        # Remove Mother Grandparent Relations with Previous Step Children
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

            # Remove Mother Sibling Step Sibling Relations with Father One
            for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                self.log.format_with_message('Found step sibling on mothers side.', parent=previous_other_parent_sim_info, step_sibling=previous_parent_blood_siblings_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            # Remove Mother Siblings Children Relations with Father One
            for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                self.log.format_with_message('Found cousin on mothers side.', parent=previous_other_parent_sim_info, cousin=previous_parent_blood_cousins_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_other_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            previous_father_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_other_parent_sim_info)
            with genealogy_caching():
                for previous_other_parent_parent_parent_sim_info in previous_father_genealogy_tracker.get_parent_sim_infos_gen():
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_other_parent_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_parent_parent_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                    # Remove Mother Sibling Uncle/Aunt Relations with Father Parent
                    for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                        self.log.format_with_message('Found step parent on fathers side.', parent=previous_parent_blood_siblings_sim_info, step_parent=previous_other_parent_parent_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_parent_parent_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_other_parent_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

                    # Remove Mother Cousin Relations with Father Parent
                    for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                        self.log.format_with_message('Found step grandparent on fathers side.', parent=previous_parent_blood_cousins_sim_info, step_parent=previous_other_parent_parent_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_other_parent_parent_parent_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_other_parent_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

                    # Remove Mother Children Relations with Father Parent
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

                    # Remove Mother Child Sibling Relations with Father Children
                    for previous_parent_blood_children_sim_info in previous_parent_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                    # Remove Mother Sibling Uncle/Aunt Relations with Father Children
                    for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    # Remove Mother Cousin Relations with Father Children
                    for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                    # Remove Mother Parent Relations with Father Children
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

                    # Remove Mother Sibling Step Sibling Relations with Father Siblings
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

            # Remove Mother Parent Relations with Father One Children
            for previous_father_blood_children_sim_info in previous_father_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_father_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            # Remove Mother Sibling Step Sibling Relations with Father One Siblings
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

            # Remove Mother Parent Relations with Father One Children
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

                # Remove Mother Child Sibling Relations with Father Children
                for previous_parent_blood_children_sim_info in previous_parent_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_children_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                # Remove Mother Sibling Uncle/Aunt Relations with Father Children
                for previous_parent_blood_siblings_sim_info in previous_parent_blood_siblings_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_siblings_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                # Remove Mother Cousin Relations with Father Children
                for previous_parent_blood_cousins_sim_info in previous_parent_blood_cousins_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_cousins_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # ------------------------Remove Mother Blood Relations With Previous Children------------------------

        # ------------------------Remove Mothers Parent Blood Relations With Previous Children------------------------
        for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
            for previous_parent_blood_parent_sim_info in previous_parent_blood_parent_sim_info_list:
                self.log.format_with_message('Removing Blood Grandparent.', grandchild=previous_parent_remove_blood_children_sim_info, grandparent=previous_parent_blood_parent_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_blood_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                if CommonSimGenealogyUtils.is_father_of(previous_parent_blood_parent_sim_info, previous_parent_sim_info):
                    CommonSimGenealogyUtils.remove_mothers_father_relation(previous_parent_remove_blood_children_sim_info)
                if CommonSimGenealogyUtils.is_mother_of(previous_parent_blood_parent_sim_info, previous_parent_sim_info):
                    CommonSimGenealogyUtils.remove_mothers_mother_relation(previous_parent_remove_blood_children_sim_info)

            previous_parent_remove_blood_children_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_remove_blood_children_sim_info)
            with genealogy_caching():
                for previous_parent_remove_blood_grandchildren in previous_parent_remove_blood_children_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Removing Blood Grandchild', grandchild=previous_parent_remove_blood_grandchildren, grandmother=previous_parent_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_grandchildren, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_parent_remove_blood_grandchildren, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    if CommonSimGenealogyUtils.is_mother_of(previous_parent_remove_blood_children_sim_info, previous_parent_remove_blood_grandchildren):
                        CommonSimGenealogyUtils.remove_mothers_mother_relation(previous_parent_remove_blood_grandchildren)
                    if CommonSimGenealogyUtils.is_father_of(previous_parent_remove_blood_children_sim_info, previous_parent_remove_blood_grandchildren):
                        CommonSimGenealogyUtils.remove_fathers_mother_relation(previous_parent_remove_blood_grandchildren)

        # Remove Mother Parent Relations with Previous Children
        for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
            self.log.format_with_message('Removing Blood parent.', child=previous_parent_remove_blood_children_sim_info, parent=previous_parent_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_mother_relation(previous_parent_remove_blood_children_sim_info)

        # Remove Mother Parent Relations with Previous Step Children
        for previous_parent_step_children_sim_info in previous_parent_step_children_sim_info_list:
            self.log.format_with_message('Removing Step parent.', step_child=previous_parent_step_children_sim_info, parent=previous_parent_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_step_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_parent_step_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        # ------------------------Remove Step Parent on Mother Side Relations With Previous Children------------------------

        for previous_parent_alternate_parent_sim_info in previous_parent_alternate_parent_sim_info_list:
            self.log.format_with_message('Removing step step parent.', child=previous_parent_alternate_parent_sim_info, parent=previous_parent_sim_info)
            previous_parent_alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_parent_alternate_parent_sim_info)

            previous_parent_alternate_parent_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_sibling_sim_info in previous_parent_alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found step parent sibling on mother side.', parent=previous_parent_alternate_parent_sim_info, sibling=previous_sibling_sim_info)
                    previous_parent_alternate_parent_siblings_sim_info_list.append(previous_sibling_sim_info)

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Children
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

            # Remove Mother Parent Relations with Father One Children
            for previous_parent_alternate_parent_parent_sim_info in previous_parent_alternate_parent_parent_sim_info_list:
                for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_alternate_parent_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_alternate_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Alternate Parent Relation with Father One Children
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

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Children
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

            # Remove Mother Alternate Uncle/Aunt Relations with Father One Children
            for previous_parent_alternate_cousin_parent_parent_sim_info in previous_parent_alternate_cousin_parent_parent_sim_info_list:
                for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_alternate_cousin_parent_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_alternate_cousin_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Alternate Uncle/Aunt Relation with Father One Children
            for previous_parent_remove_blood_children_sim_info in previous_parent_remove_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_alternate_cousin_parent_sim_info, previous_parent_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                CommonRelationshipUtils.remove_relationship_bit(previous_parent_remove_blood_children_sim_info, previous_parent_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        self.log.format_with_message('Done removing relations to old family', new_sim=previous_parent_sim_info)
        return True

    def _add_new_relation(self, parent_sim_info: SimInfo, sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding new father to Sim', sim=sim_info, new_parent_sim=parent_sim_info)
        # Add new father
        CommonSimGenealogyUtils.set_as_father_of(parent_sim_info, sim_info)

        # Add new Uncles/Aunts
        uncle_aunt_sim_info_list = list()
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(parent_sim_info)
        with genealogy_caching():
            for uncle_aunt_sim_info in genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found an uncle/aunt. Adding them.', sim=uncle_aunt_sim_info)
                uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
                CommonRelationshipUtils.add_relationship_bit(sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(uncle_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for uncle_aunt_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(parent_sim_info, (CommonRelationshipBitId.FAMILY_BROTHER_SISTER, CommonRelationshipBitId.FAMILY_STEP_SIBLING), instanced_only=False):
            if uncle_aunt_sim_info in uncle_aunt_sim_info_list:
                continue
            self.log.format_with_message('Found an uncle/aunt. Adding them as aunt/uncle to sim.', sim=sim_info, new_uncle=uncle_aunt_sim_info)
            uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
            CommonRelationshipUtils.add_relationship_bit(sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(uncle_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Add Cousins
        for uncle_aunt_sim_info in uncle_aunt_sim_info_list:
            uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(uncle_aunt_sim_info)
            with genealogy_caching():
                for cousin_sim_info in uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found a cousin. Adding them as cousins to sim.', sim=sim_info, new_cousin=cousin_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(cousin_sim_info, sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(parent_sim_info)
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
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                CommonSimGenealogyUtils.set_as_mothers_father_of(parent_sim_info, child_sim_info)

        # Add new grandmother
        new_grandmother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(parent_sim_info)
        if new_grandmother_sim_info is not None:
            self.log.format_with_message('Found grandmother, adding them as grandmother to sim.', sim=sim_info, new_grandmother=new_grandmother_sim_info)
            CommonRelationshipUtils.add_relationship_bit(sim_info, new_grandmother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandmother_sim_info, sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(new_grandmother_sim_info, sim_info)

        # Add new grandfather
        new_grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(parent_sim_info)
        if new_grandfather_sim_info is not None:
            self.log.format_with_message('Found grandfather, adding them as grandfather to sim.', sim=sim_info, new_grandfather=new_grandfather_sim_info)
            CommonRelationshipUtils.add_relationship_bit(sim_info, new_grandfather_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandfather_sim_info, sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_father_of(new_grandfather_sim_info, sim_info)

        self.log.format_with_message('Done adding new father', sim=sim_info, new_father_sim=parent_sim_info)
        return True
