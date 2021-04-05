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


class S4CMSetSimAAsMotherToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a mother of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_set_mother'

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
        return S4CMSimControlMenuStringId.MOTHER

    # noinspection PyMissingOrEmptyDocstring
    def has_relation(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        return super().has_relation(sim_info_a, sim_info_b) and CommonSimGenealogyUtils.is_mother_of(sim_info_a, sim_info_b)

    def _update_family_tree(self, parent_sim_info: SimInfo, child_sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as mother of Sim B', parent=parent_sim_info, sim_b=child_sim_info)
            if CommonSimGenealogyUtils.has_mother(child_sim_info):
                previous_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(child_sim_info)
                self._remove_old_relation(previous_mother_sim_info, child_sim_info)
            self._add_new_relation(parent_sim_info, child_sim_info)
            self.log.format_with_message('Done setting Sim A as mother of Sim B', parent=parent_sim_info, sim_b=child_sim_info)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as mother.', exception=ex)
            on_completed(False)
        return True

    def _remove_old_relation(self, previous_mother_sim_info: SimInfo, child_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Removing relations to old family', new_sim=previous_mother_sim_info)
        previous_mother_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_mother_sim_info)
        previous_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(child_sim_info)

        previous_mother_alternate_parent_sim_info_list = list()
        previous_mother_remove_blood_children_sim_info_list = list()
        previous_mother_blood_children_sim_info_list = list()
        with genealogy_caching():
            for previous_child_sim_info in previous_mother_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found blood child on mother side.', parent=previous_mother_sim_info, child=previous_child_sim_info)
                if (previous_father_sim_info is None and CommonSimGenealogyUtils.has_father(previous_child_sim_info)) or CommonSimGenealogyUtils.is_father_of(previous_father_sim_info, previous_child_sim_info):
                    previous_mother_remove_blood_children_sim_info_list.append(previous_child_sim_info)
                    continue
                previous_child_alternate_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(previous_child_sim_info)
                if previous_child_alternate_father_sim_info is not None:
                    previous_mother_alternate_parent_sim_info_list.append(previous_child_alternate_father_sim_info)
                previous_mother_blood_children_sim_info_list.append(previous_child_sim_info)

        previous_mother_blood_siblings_sim_info_list = list()
        with genealogy_caching():
            for previous_sibling_sim_info in previous_mother_genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found blood sibling on mother side.', parent=previous_mother_sim_info, sibling=previous_sibling_sim_info)
                previous_mother_blood_siblings_sim_info_list.append(previous_sibling_sim_info)

        previous_mother_alternate_cousin_parent_sim_info_list = list()
        previous_mother_blood_cousins_sim_info_list = list()
        for previous_mother_blood_siblings_sim_info in previous_mother_blood_siblings_sim_info_list:
            previous_mother_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_mother_blood_siblings_sim_info)
            with genealogy_caching():
                for previous_mother_blood_cousin_sim_info in previous_mother_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found blood cousin on mother side.', parent=previous_mother_sim_info, cousin=previous_mother_blood_cousin_sim_info)
                    previous_mother_blood_cousins_sim_info_list.append(previous_mother_blood_cousin_sim_info)
                    if CommonSimGenealogyUtils.is_mother_of(previous_mother_blood_siblings_sim_info, previous_mother_blood_cousin_sim_info):
                        cousin_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(previous_mother_blood_cousin_sim_info)
                        if cousin_father_sim_info is not None:
                            previous_mother_alternate_cousin_parent_sim_info_list.append(cousin_father_sim_info)
                    if CommonSimGenealogyUtils.is_father_of(previous_mother_blood_siblings_sim_info, previous_mother_blood_cousin_sim_info):
                        cousin_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(previous_mother_blood_cousin_sim_info)
                        if cousin_mother_sim_info is not None:
                            previous_mother_alternate_cousin_parent_sim_info_list.append(cousin_mother_sim_info)

        previous_mother_step_children_sim_info_list = list()
        for previous_step_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(previous_mother_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
            if previous_step_child_sim_info in previous_mother_blood_children_sim_info_list or previous_step_child_sim_info in previous_mother_remove_blood_children_sim_info_list:
                continue
            self.log.format_with_message('Found step child on mother side.', parent=previous_mother_sim_info, child=previous_step_child_sim_info)
            previous_mother_step_children_sim_info_list.append(previous_step_child_sim_info)

        previous_mother_blood_parent_sim_info_list = list()
        with genealogy_caching():
            for previous_parent_sim_info in previous_mother_genealogy_tracker.get_parent_sim_infos_gen():
                self.log.format_with_message('Found blood parent on mother side.', mother=previous_mother_sim_info, parent=previous_parent_sim_info)
                previous_mother_blood_parent_sim_info_list.append(previous_parent_sim_info)

        # Remove Blood Relations
        if previous_father_sim_info is not None:
            # Remove Father relations to Mother
            for previous_mother_blood_children_sim_info in previous_mother_blood_children_sim_info_list:
                self.log.format_with_message('Found step child on mothers side.', parent=previous_father_sim_info, step_child=previous_mother_blood_children_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_children_sim_info, previous_father_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_father_sim_info, previous_mother_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            # Remove Father relations to Mother Parents
            for previous_mother_blood_parent_sim_info in previous_mother_blood_parent_sim_info_list:
                self.log.format_with_message('Found step parent on mothers side.', parent=previous_father_sim_info, step_parent=previous_mother_blood_parent_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_parent_sim_info, previous_father_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.remove_relationship_bit(previous_father_sim_info, previous_mother_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

            # Remove Mother Sibling Step Sibling Relations with Father One
            for previous_mother_blood_siblings_sim_info in previous_mother_blood_siblings_sim_info_list:
                self.log.format_with_message('Found step sibling on mothers side.', parent=previous_father_sim_info, step_sibling=previous_mother_blood_siblings_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_father_sim_info, previous_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_siblings_sim_info, previous_father_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            # Remove Mother Siblings Children Relations with Father One
            for previous_mother_blood_cousins_sim_info in previous_mother_blood_cousins_sim_info_list:
                self.log.format_with_message('Found cousin on mothers side.', parent=previous_father_sim_info, cousin=previous_mother_blood_cousins_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_cousins_sim_info, previous_father_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.remove_relationship_bit(previous_father_sim_info, previous_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            previous_father_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_father_sim_info)
            with genealogy_caching():
                for previous_parent_sim_info in previous_father_genealogy_tracker.get_parent_sim_infos_gen():
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                    # Remove Mother Sibling Uncle/Aunt Relations with Father Parent
                    for previous_mother_blood_siblings_sim_info in previous_mother_blood_siblings_sim_info_list:
                        self.log.format_with_message('Found step parent on fathers side.', parent=previous_mother_blood_siblings_sim_info, step_parent=previous_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_siblings_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

                    # Remove Mother Cousin Relations with Father Parent
                    for previous_mother_blood_cousins_sim_info in previous_mother_blood_cousins_sim_info_list:
                        self.log.format_with_message('Found step grandparent on fathers side.', parent=previous_mother_blood_cousins_sim_info, step_parent=previous_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_cousins_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

                    # Remove Mother Children Relations with Father Parent
                    for previous_mother_blood_children_sim_info in previous_mother_blood_children_sim_info_list:
                        self.log.format_with_message('Found step grandparent on fathers side.', parent=previous_mother_blood_children_sim_info, step_parent=previous_parent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(previous_parent_sim_info, previous_mother_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_children_sim_info, previous_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            previous_father_blood_children_sim_info_list = list()
            with genealogy_caching():
                for previous_child_sim_info in previous_father_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found blood children on father side.', parent=previous_father_sim_info, child=previous_child_sim_info)
                    previous_father_blood_children_sim_info_list.append(previous_child_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                    # Remove Mother Child Sibling Relations with Father Children
                    for previous_mother_blood_children_sim_info in previous_mother_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_mother_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_children_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_mother_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_children_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                    # Remove Mother Sibling Uncle/Aunt Relations with Father Children
                    for previous_mother_blood_siblings_sim_info in previous_mother_blood_siblings_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_siblings_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    # Remove Mother Cousin Relations with Father Children
                    for previous_mother_blood_cousins_sim_info in previous_mother_blood_cousins_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_cousins_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                    # Remove Mother Parent Relations with Father Children
                    for previous_mother_blood_parent_sim_info in previous_mother_blood_parent_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_child_sim_info, previous_mother_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_parent_sim_info, previous_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            previous_father_blood_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_sibling_sim_info in previous_father_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found blood sibling on father side.', parent=previous_father_sim_info, sibling=previous_sibling_sim_info)
                    previous_father_blood_siblings_sim_info_list.append(previous_sibling_sim_info)

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Children
                    for previous_mother_blood_children_sim_info in previous_mother_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_mother_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_children_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Cousins
                    for previous_mother_blood_cousins_sim_info in previous_mother_blood_cousins_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_cousins_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                    # Remove Mother Sibling Step Sibling Relations with Father Siblings
                    for previous_mother_blood_siblings_sim_info in previous_mother_blood_siblings_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_siblings_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                    # Remove Father Sibling relations to Mother Parents
                    for previous_mother_blood_parent_sim_info in previous_mother_blood_parent_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_parent_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_mother_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

            previous_father_blood_parent_sim_info_list = list()
            with genealogy_caching():
                for previous_parent_sim_info in previous_father_genealogy_tracker.get_parent_sim_infos_gen():
                    self.log.format_with_message('Found blood grandparent on father side.', parent=previous_father_sim_info, grandparent=previous_parent_sim_info)
                    previous_father_blood_parent_sim_info_list.append(previous_parent_sim_info)

            # Remove Mother Parent Relations with Father One Children
            for previous_father_blood_children_sim_info in previous_father_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_children_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_father_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            # Remove Mother Sibling Step Sibling Relations with Father One Siblings
            previous_father_blood_cousins_sim_info_list = list()
            for previous_father_blood_siblings_sim_info in previous_father_blood_siblings_sim_info_list:
                previous_father_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_father_blood_siblings_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_father_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_siblings_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                with genealogy_caching():
                    for previous_cousin_sim_info in previous_father_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        previous_father_blood_cousins_sim_info_list.append(previous_cousin_sim_info)

            for previous_father_blood_cousins_sim_info in previous_father_blood_cousins_sim_info_list:
                for previous_mother_blood_parent_sim_info in previous_mother_blood_parent_sim_info_list:
                    self.log.format_with_message('Found step grandparent on mother side.', cousin=previous_father_blood_cousins_sim_info, grandparent=previous_mother_blood_parent_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_parent_sim_info, previous_father_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_cousins_sim_info, previous_mother_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Mother Parent Relations with Father One Children
            for previous_father_blood_parent_sim_info in previous_father_blood_parent_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_father_blood_parent_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_father_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
        else:
            for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                self.log.format_with_message('Found blood children on mother side.', parent=previous_mother_sim_info, child=previous_mother_remove_blood_children_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                # Remove Mother Child Sibling Relations with Father Children
                for previous_mother_blood_children_sim_info in previous_mother_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_children_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_children_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                # Remove Mother Sibling Uncle/Aunt Relations with Father Children
                for previous_mother_blood_siblings_sim_info in previous_mother_blood_siblings_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_siblings_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                # Remove Mother Cousin Relations with Father Children
                for previous_mother_blood_cousins_sim_info in previous_mother_blood_cousins_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_cousins_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for previous_mother_blood_parent_sim_info in previous_mother_blood_parent_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_parent_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # ------------------------Remove Mother Blood Relations With Previous Children------------------------

        # ------------------------Remove Mothers Parent Blood Relations With Previous Children------------------------
        for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
            for previous_mother_blood_parent_sim_info in previous_mother_blood_parent_sim_info_list:
                self.log.format_with_message('Removing Blood Grandparent.', grandchild=previous_mother_remove_blood_children_sim_info, grandparent=previous_mother_blood_parent_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_blood_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_blood_parent_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                if CommonSimGenealogyUtils.is_father_of(previous_mother_blood_parent_sim_info, previous_mother_sim_info):
                    CommonSimGenealogyUtils.remove_mothers_father_relation(previous_mother_remove_blood_children_sim_info)
                if CommonSimGenealogyUtils.is_mother_of(previous_mother_blood_parent_sim_info, previous_mother_sim_info):
                    CommonSimGenealogyUtils.remove_mothers_mother_relation(previous_mother_remove_blood_children_sim_info)

        # Remove Mother Parent Relations with Previous Children
        for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
            self.log.format_with_message('Removing Blood parent.', child=previous_mother_remove_blood_children_sim_info, parent=previous_mother_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_mother_relation(previous_mother_remove_blood_children_sim_info)

        # Remove Mother Parent Relations with Previous Step Children
        for previous_mother_step_children_sim_info in previous_mother_step_children_sim_info_list:
            self.log.format_with_message('Removing Step parent.', step_child=previous_mother_step_children_sim_info, parent=previous_mother_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(previous_mother_step_children_sim_info, previous_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(previous_mother_sim_info, previous_mother_step_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        # ------------------------Remove Step Parent on Mother Side Relations With Previous Children------------------------

        for previous_mother_alternate_parent_sim_info in previous_mother_alternate_parent_sim_info_list:
            self.log.format_with_message('Removing step step parent.', child=previous_mother_alternate_parent_sim_info, parent=previous_mother_sim_info)
            previous_mother_alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_mother_alternate_parent_sim_info)

            previous_mother_alternate_parent_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_sibling_sim_info in previous_mother_alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found step parent sibling on mother side.', parent=previous_mother_alternate_parent_sim_info, sibling=previous_sibling_sim_info)
                    previous_mother_alternate_parent_siblings_sim_info_list.append(previous_sibling_sim_info)

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Children
                    for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

            for previous_mother_alternate_parent_siblings_sim_info in previous_mother_alternate_parent_siblings_sim_info_list:
                previous_mother_alternate_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_mother_alternate_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_cousin_sim_info in previous_mother_alternate_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                            CommonRelationshipUtils.remove_relationship_bit(previous_cousin_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                            CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            previous_mother_alternate_parent_parent_sim_info_list = list()
            with genealogy_caching():
                for previous_parent_sim_info in previous_mother_alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    self.log.format_with_message('Found step grandparent on mother side.', parent=previous_mother_alternate_parent_sim_info, grandparent=previous_parent_sim_info)
                    previous_mother_alternate_parent_parent_sim_info_list.append(previous_parent_sim_info)

            # Remove Mother Parent Relations with Father One Children
            for previous_mother_alternate_parent_parent_sim_info in previous_mother_alternate_parent_parent_sim_info_list:
                for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_alternate_parent_parent_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_alternate_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Alternate Parent Relation with Father One Children
            for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_alternate_parent_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_alternate_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

        # ------------------------Remove Step Parent on Mother Blood Side Relations With Previous Children------------------------

        for previous_mother_alternate_cousin_parent_sim_info in previous_mother_alternate_cousin_parent_sim_info_list:
            self.log.format_with_message('Removing step uncle/aunt.', parent=previous_mother_alternate_cousin_parent_sim_info)
            previous_mother_alternate_cousin_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_mother_alternate_cousin_parent_sim_info)

            previous_mother_alternate_cousin_parent_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_sibling_sim_info in previous_mother_alternate_cousin_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Found step parent sibling on mother side.', parent=previous_mother_alternate_cousin_parent_sim_info, sibling=previous_sibling_sim_info)
                    previous_mother_alternate_cousin_parent_siblings_sim_info_list.append(previous_sibling_sim_info)

                    # Remove Father Sibling Aunt/Uncle Relations with Mother Children
                    for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                        CommonRelationshipUtils.remove_relationship_bit(previous_sibling_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                        CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_sibling_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

            for previous_mother_alternate_cousin_parent_siblings_sim_info in previous_mother_alternate_cousin_parent_siblings_sim_info_list:
                previous_mother_alternate_cousin_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_mother_alternate_cousin_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_cousin_sim_info in previous_mother_alternate_cousin_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                            CommonRelationshipUtils.remove_relationship_bit(previous_cousin_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                            CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            previous_mother_alternate_cousin_parent_parent_sim_info_list = list()
            with genealogy_caching():
                for previous_parent_sim_info in previous_mother_alternate_cousin_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    self.log.format_with_message('Found step grandparent on mother side.', parent=previous_mother_alternate_cousin_parent_sim_info, grandparent=previous_parent_sim_info)
                    previous_mother_alternate_cousin_parent_parent_sim_info_list.append(previous_parent_sim_info)

            # Remove Mother Alternate Uncle/Aunt Relations with Father One Children
            for previous_mother_alternate_cousin_parent_parent_sim_info in previous_mother_alternate_cousin_parent_parent_sim_info_list:
                for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_alternate_cousin_parent_parent_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_alternate_cousin_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            # Remove Alternate Uncle/Aunt Relation with Father One Children
            for previous_mother_remove_blood_children_sim_info in previous_mother_remove_blood_children_sim_info_list:
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_alternate_cousin_parent_sim_info, previous_mother_remove_blood_children_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                CommonRelationshipUtils.remove_relationship_bit(previous_mother_remove_blood_children_sim_info, previous_mother_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        self.log.format_with_message('Done removing relations to old family', new_sim=previous_mother_sim_info)
        return True

    def _add_new_relation(self, new_mother_sim_info: SimInfo, child_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding relation to Sim', child=child_sim_info, mother=new_mother_sim_info)

        child_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(child_sim_info)
        new_mother_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_mother_sim_info)

        new_mother_blood_siblings_sim_info_list = list()
        with genealogy_caching():
            for new_sibling_sim_info in new_mother_genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found blood sibling on mother side.', parent=new_mother_sim_info, sibling=new_sibling_sim_info)
                new_mother_blood_siblings_sim_info_list.append(new_sibling_sim_info)

        new_mother_alternate_parent_sim_info_list = list()
        new_mother_blood_children_sim_info_list = list()
        with genealogy_caching():
            for new_child_sim_info in new_mother_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found blood child on mother side.', parent=new_mother_sim_info, child=new_child_sim_info)
                new_mother_blood_children_sim_info_list.append(new_child_sim_info)
                if CommonSimGenealogyUtils.is_father_of(new_mother_sim_info, new_child_sim_info):
                    new_child_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_child_sim_info)
                    if new_child_mother_sim_info is not None and new_child_mother_sim_info not in new_mother_alternate_parent_sim_info_list:
                        self.log.format_with_message('Found alternative mother', child=new_child_sim_info, mother=new_child_mother_sim_info)
                        new_mother_alternate_parent_sim_info_list.append(new_child_mother_sim_info)
                if CommonSimGenealogyUtils.is_mother_of(new_mother_sim_info, new_child_sim_info):
                    new_child_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_child_sim_info)
                    if new_child_father_sim_info is not None and new_child_father_sim_info not in new_mother_alternate_parent_sim_info_list:
                        self.log.format_with_message('Found alternative father', child=new_child_sim_info, father=new_child_father_sim_info)
                        new_mother_alternate_parent_sim_info_list.append(new_child_father_sim_info)

        new_mother_alternate_parent_parent_sim_info_list = list()
        new_mother_alternate_parent_siblings_sim_info_list = list()
        new_mother_alternate_parent_children_sim_info_list = list()
        for new_mother_alternate_parent_sim_info in new_mother_alternate_parent_sim_info_list:
            self.log.format_with_message('Alternative parent', alt_parent=new_mother_alternate_parent_sim_info)
            new_mother_alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_mother_alternate_parent_sim_info)
            with genealogy_caching():
                for new_sibling_sim_info in new_mother_alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    new_mother_alternate_parent_siblings_sim_info_list.append(new_sibling_sim_info)

            with genealogy_caching():
                for new_step_sibling_sim_info in new_mother_alternate_parent_genealogy_tracker.get_child_sim_infos_gen():
                    if new_step_sibling_sim_info in new_mother_blood_children_sim_info_list:
                        continue
                    new_mother_alternate_parent_children_sim_info_list.append(new_step_sibling_sim_info)
            with genealogy_caching():
                for new_grandparent_sim_info in new_mother_alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    new_mother_alternate_parent_parent_sim_info_list.append(new_grandparent_sim_info)

        new_mother_alternate_parent_cousin_sim_info_list = list()
        for new_mother_alternate_parent_siblings_sim_info in new_mother_alternate_parent_siblings_sim_info_list:
            new_mother_alternate_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_mother_alternate_parent_siblings_sim_info)
            with genealogy_caching():
                for new_step_sibling_sim_info in new_mother_alternate_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                    new_mother_alternate_parent_cousin_sim_info_list.append(new_step_sibling_sim_info)

        new_mother_alternate_cousin_parent_sim_info_list = list()
        new_mother_blood_cousins_sim_info_list = list()
        for new_mother_blood_siblings_sim_info in new_mother_blood_siblings_sim_info_list:
            new_mother_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_mother_blood_siblings_sim_info)
            with genealogy_caching():
                for new_cousin_sim_info in new_mother_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found blood cousin on mother side.', parent=new_mother_sim_info, cousin=new_cousin_sim_info)
                    new_mother_blood_cousins_sim_info_list.append(new_cousin_sim_info)
                    if CommonSimGenealogyUtils.is_father_of(new_mother_blood_siblings_sim_info, new_cousin_sim_info):
                        new_cousin_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_cousin_sim_info)
                        if new_cousin_mother_sim_info is not None:
                            new_mother_alternate_cousin_parent_sim_info_list.append(new_cousin_mother_sim_info)
                    if CommonSimGenealogyUtils.is_mother_of(new_mother_blood_siblings_sim_info, new_cousin_sim_info):
                        new_cousin_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_cousin_sim_info)
                        if new_cousin_father_sim_info is not None:
                            new_mother_alternate_cousin_parent_sim_info_list.append(new_cousin_father_sim_info)

        new_mother_alternate_cousin_parent_parent_sim_info_list = list()
        new_mother_alternate_cousin_parent_siblings_sim_info_list = list()
        new_mother_alternate_cousin_parent_children_sim_info_list = list()
        for new_mother_alternate_cousin_parent_sim_info in new_mother_alternate_cousin_parent_sim_info_list:
            new_mother_alternate_cousin_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_mother_alternate_cousin_parent_sim_info)
            with genealogy_caching():
                for new_cousin_sim_info in new_mother_alternate_cousin_parent_genealogy_tracker.get_child_sim_infos_gen():
                    new_mother_alternate_cousin_parent_children_sim_info_list.append(new_cousin_sim_info)
            with genealogy_caching():
                for new_uncle_aunt_sim_info in new_mother_alternate_cousin_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    new_mother_alternate_cousin_parent_siblings_sim_info_list.append(new_uncle_aunt_sim_info)
            with genealogy_caching():
                for new_grandparent_sim_info in new_mother_alternate_cousin_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    new_mother_alternate_cousin_parent_parent_sim_info_list.append(new_grandparent_sim_info)

        # Mother One New as Mother of New Child
        new_mother_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_mother_sim_info)
        new_mother_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_mother_sim_info)

        previous_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(child_sim_info)

        if previous_father_sim_info is not None:
            previous_father_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_father_sim_info)
            # Grandparents
            previous_father_blood_parents_sim_info_list = list()
            # Uncle/Aunt
            previous_father_blood_siblings_sim_info_list = list()
            with genealogy_caching():
                for previous_father_blood_sibling_sim_info in previous_father_genealogy_tracker.get_siblings_sim_infos_gen():
                    previous_father_blood_siblings_sim_info_list.append(previous_father_blood_sibling_sim_info)
            with genealogy_caching():
                for previous_father_blood_parents_sim_info in previous_father_genealogy_tracker.get_parent_sim_infos_gen():
                    previous_father_blood_parents_sim_info_list.append(previous_father_blood_parents_sim_info)

            # Uncle/Aunt
            previous_father_blood_alternate_cousin_parent_sim_info_list = list()
            # Cousin
            previous_father_blood_sibling_cousin_sim_info_list = list()
            for previous_father_blood_siblings_sim_info in previous_father_blood_siblings_sim_info_list:
                previous_father_blood_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_father_blood_siblings_sim_info)
                with genealogy_caching():
                    for previous_father_blood_sibling_cousin_sim_info in previous_father_blood_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        previous_father_blood_sibling_cousin_sim_info_list.append(previous_father_blood_sibling_cousin_sim_info)
                        if CommonSimGenealogyUtils.is_father_of(previous_father_blood_siblings_sim_info, previous_father_blood_sibling_cousin_sim_info):
                            previous_father_blood_sibling_cousin_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(previous_father_blood_sibling_cousin_sim_info)
                            if previous_father_blood_sibling_cousin_mother_sim_info is not None:
                                previous_father_blood_alternate_cousin_parent_sim_info_list.append(previous_father_blood_sibling_cousin_mother_sim_info)
                        if CommonSimGenealogyUtils.is_mother_of(previous_father_blood_siblings_sim_info, previous_father_blood_sibling_cousin_sim_info):
                            previous_father_blood_sibling_cousin_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(previous_father_blood_sibling_cousin_sim_info)
                            if previous_father_blood_sibling_cousin_father_sim_info is not None:
                                previous_father_blood_alternate_cousin_parent_sim_info_list.append(previous_father_blood_sibling_cousin_father_sim_info)

            # Grandparents
            previous_father_blood_alternate_cousin_parent_parents_sim_info_list = list()
            # Uncle/Aunt
            previous_father_blood_alternate_cousin_parent_siblings_sim_info_list = list()
            # Cousin
            previous_father_blood_alternate_cousin_parent_cousin_sim_info_list = list()
            for previous_father_blood_alternate_cousin_parent_sim_info in previous_father_blood_alternate_cousin_parent_sim_info_list:
                previous_father_blood_alternate_cousin_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_father_blood_alternate_cousin_parent_sim_info)
                with genealogy_caching():
                    for previous_father_blood_alternate_cousin_parent_cousin_sim_info in previous_father_blood_alternate_cousin_parent_genealogy_tracker.get_child_sim_infos_gen():
                        if previous_father_blood_alternate_cousin_parent_cousin_sim_info in previous_father_blood_sibling_cousin_sim_info_list:
                            continue
                        previous_father_blood_alternate_cousin_parent_cousin_sim_info_list.append(previous_father_blood_alternate_cousin_parent_cousin_sim_info)
                with genealogy_caching():
                    for previous_father_blood_alternate_cousin_parent_siblings_sim_info in previous_father_blood_alternate_cousin_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                        previous_father_blood_alternate_cousin_parent_siblings_sim_info_list.append(previous_father_blood_alternate_cousin_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_father_blood_alternate_cousin_parent_parents_sim_info in previous_father_blood_alternate_cousin_parent_genealogy_tracker.get_parent_sim_infos_gen():
                        previous_father_blood_alternate_cousin_parent_parents_sim_info_list.append(previous_father_blood_alternate_cousin_parent_parents_sim_info)

            # Cousin
            previous_father_blood_alternate_cousin_parent_siblings_children_sim_info_list = list()
            for previous_father_blood_alternate_cousin_parent_siblings_sim_info in previous_father_blood_alternate_cousin_parent_siblings_sim_info_list:
                previous_father_blood_alternate_cousin_parent_siblings_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(previous_father_blood_alternate_cousin_parent_siblings_sim_info)
                with genealogy_caching():
                    for previous_father_blood_alternate_cousin_parent_siblings_children_sim_info in previous_father_blood_alternate_cousin_parent_siblings_genealogy_tracker.get_child_sim_infos_gen():
                        previous_father_blood_alternate_cousin_parent_siblings_children_sim_info_list.append(previous_father_blood_alternate_cousin_parent_siblings_children_sim_info)

            for previous_father_blood_siblings_sim_info in previous_father_blood_siblings_sim_info_list:
                self.log.format_with_message('Setting as step sibling', step_sibling=previous_father_blood_siblings_sim_info, parent=new_mother_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_siblings_sim_info, new_mother_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.add_relationship_bit(new_mother_sim_info, previous_father_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            for previous_father_blood_parents_sim_info in previous_father_blood_parents_sim_info_list:
                self.log.format_with_message('Setting as step parent', step_parent=previous_father_blood_parents_sim_info, parent=new_mother_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_parents_sim_info, new_mother_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.add_relationship_bit(new_mother_sim_info, previous_father_blood_parents_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

            for previous_father_blood_sibling_cousin_sim_info in previous_father_blood_sibling_cousin_sim_info_list:
                self.log.format_with_message('Setting as step niece/nephew', step_niece_nephew=previous_father_blood_sibling_cousin_sim_info, parent=new_mother_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_sibling_cousin_sim_info, new_mother_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(new_mother_sim_info, previous_father_blood_sibling_cousin_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            self.log.format_with_message('Setting as step parent', parent=previous_father_sim_info, child=child_sim_info)
            CommonRelationshipUtils.add_relationship_bit(previous_father_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

            for previous_father_blood_parents_sim_info in previous_father_blood_parents_sim_info_list:
                self.log.format_with_message('Setting as step grandparent', grandparent=previous_father_blood_parents_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_parents_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_parents_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            for previous_father_blood_siblings_sim_info in previous_father_blood_siblings_sim_info_list:
                self.log.format_with_message('Setting as step aunt/uncle', aunt_uncle=previous_father_blood_siblings_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_siblings_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

            for previous_father_blood_alternate_cousin_parent_sim_info in previous_father_blood_alternate_cousin_parent_sim_info_list:
                self.log.format_with_message('Setting as step aunt/uncle', aunt_uncle=previous_father_blood_alternate_cousin_parent_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

            for previous_father_blood_sibling_cousin_sim_info in previous_father_blood_sibling_cousin_sim_info_list:
                self.log.format_with_message('Setting as step cousin', cousin=previous_father_blood_sibling_cousin_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_sibling_cousin_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_sibling_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            for previous_father_blood_alternate_cousin_parent_parents_sim_info in previous_father_blood_alternate_cousin_parent_parents_sim_info_list:
                self.log.format_with_message('Setting as step grandparent', grandparent=previous_father_blood_alternate_cousin_parent_parents_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_parents_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_alternate_cousin_parent_parents_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

            for previous_father_blood_alternate_cousin_parent_siblings_sim_info in previous_father_blood_alternate_cousin_parent_siblings_sim_info_list:
                self.log.format_with_message('Setting as step aunt/uncle', aunt_uncle=previous_father_blood_alternate_cousin_parent_siblings_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_siblings_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_alternate_cousin_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

            for previous_father_blood_alternate_cousin_parent_cousin_sim_info in previous_father_blood_alternate_cousin_parent_cousin_sim_info_list:
                self.log.format_with_message('Setting as step cousin', cousin=previous_father_blood_alternate_cousin_parent_cousin_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_cousin_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_alternate_cousin_parent_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            for previous_father_blood_alternate_cousin_parent_siblings_children_sim_info in previous_father_blood_alternate_cousin_parent_siblings_children_sim_info_list:
                self.log.format_with_message('Setting as step cousin', cousin=previous_father_blood_alternate_cousin_parent_siblings_children_sim_info, child=child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_siblings_children_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, previous_father_blood_alternate_cousin_parent_siblings_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            for new_mother_child_sim_info in new_mother_blood_children_sim_info_list:
                self.log.format_with_message('Setting as step parent', parent=previous_father_sim_info, child=new_mother_child_sim_info)
                CommonRelationshipUtils.add_relationship_bit(previous_father_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_sim_info, CommonRelationshipBitId.FAMILY_PARENT)

                for previous_father_blood_parents_sim_info in previous_father_blood_parents_sim_info_list:
                    self.log.format_with_message('Setting as step grandparent', grandparent=previous_father_blood_parents_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_parents_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_parents_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

                for previous_father_blood_siblings_sim_info in previous_father_blood_siblings_sim_info_list:
                    self.log.format_with_message('Setting as step aunt/uncle', aunt_uncle=previous_father_blood_siblings_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_siblings_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                for previous_father_blood_alternate_cousin_parent_sim_info in previous_father_blood_alternate_cousin_parent_sim_info_list:
                    self.log.format_with_message('Setting as step aunt/uncle', aunt_uncle=previous_father_blood_alternate_cousin_parent_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                for previous_father_blood_sibling_cousin_sim_info in previous_father_blood_sibling_cousin_sim_info_list:
                    self.log.format_with_message('Setting as step cousin', cousin=previous_father_blood_sibling_cousin_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_sibling_cousin_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_sibling_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for previous_father_blood_alternate_cousin_parent_parents_sim_info in previous_father_blood_alternate_cousin_parent_parents_sim_info_list:
                    self.log.format_with_message('Setting as step grandparent', grandparent=previous_father_blood_alternate_cousin_parent_parents_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_parents_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_alternate_cousin_parent_parents_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)

                for previous_father_blood_alternate_cousin_parent_siblings_sim_info in previous_father_blood_alternate_cousin_parent_siblings_sim_info_list:
                    self.log.format_with_message('Setting as step aunt/uncle', aunt_uncle=previous_father_blood_alternate_cousin_parent_siblings_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_siblings_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_alternate_cousin_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

                for previous_father_blood_alternate_cousin_parent_cousin_sim_info in previous_father_blood_alternate_cousin_parent_cousin_sim_info_list:
                    self.log.format_with_message('Setting as step cousin', cousin=previous_father_blood_alternate_cousin_parent_cousin_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_cousin_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_alternate_cousin_parent_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for previous_father_blood_alternate_cousin_parent_siblings_children_sim_info in previous_father_blood_alternate_cousin_parent_siblings_children_sim_info_list:
                    self.log.format_with_message('Setting as step cousin', cousin=previous_father_blood_alternate_cousin_parent_siblings_children_sim_info, child=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(previous_father_blood_alternate_cousin_parent_siblings_children_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, previous_father_blood_alternate_cousin_parent_siblings_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

            with genealogy_caching():
                for new_blood_child_sim_info in child_genealogy_tracker.get_siblings_sim_infos_gen():
                    self.log.format_with_message('Setting as mother', child=new_blood_child_sim_info, mother=new_mother_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                    CommonSimGenealogyUtils.set_as_mother_of(new_mother_sim_info, new_blood_child_sim_info)

                    for new_mother_blood_siblings_sim_info in new_mother_blood_siblings_sim_info_list:
                        self.log.format_with_message('Setting as aunt/uncle', child=new_blood_child_sim_info, aunt_uncle=new_mother_blood_siblings_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_blood_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    for new_mother_alternate_cousin_parent_sim_info in new_mother_alternate_cousin_parent_sim_info_list:
                        self.log.format_with_message('Setting as aunt/uncle', child=new_blood_child_sim_info, aunt_uncle=new_mother_alternate_cousin_parent_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    for new_mother_alternate_cousin_parent_siblings_sim_info in new_mother_alternate_cousin_parent_siblings_sim_info_list:
                        self.log.format_with_message('Setting as aunt/uncle', child=new_blood_child_sim_info, aunt_uncle=new_mother_alternate_cousin_parent_siblings_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    for new_mother_alternate_cousin_parent_children_sim_info in new_mother_alternate_cousin_parent_children_sim_info_list:
                        self.log.format_with_message('Setting as cousin', child=new_blood_child_sim_info, cousin=new_mother_alternate_cousin_parent_children_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_children_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                    for new_mother_alternate_cousin_parent_parent_sim_info in new_mother_alternate_cousin_parent_parent_sim_info_list:
                        self.log.format_with_message('Setting as grandparent', child=new_blood_child_sim_info, grandparent=new_mother_alternate_cousin_parent_parent_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

                    for new_mother_child_sim_info in new_mother_blood_children_sim_info_list:
                        self.log.format_with_message('Setting as sibling', child=new_blood_child_sim_info, sibling=new_mother_child_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

                    for new_mother_blood_cousins_sim_info in new_mother_blood_cousins_sim_info_list:
                        self.log.format_with_message('Setting as cousin', child=new_blood_child_sim_info, cousin=new_mother_blood_cousins_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_blood_cousins_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                    for new_mother_alternate_parent_sim_info in new_mother_alternate_parent_sim_info_list:
                        self.log.format_with_message('Setting as step parent', child=new_blood_child_sim_info, parent=new_mother_alternate_parent_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                    for new_mother_alternate_parent_parent_sim_info in new_mother_alternate_parent_parent_sim_info_list:
                        self.log.format_with_message('Setting as step grandparent', child=new_blood_child_sim_info, grandparent=new_mother_alternate_parent_parent_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

                    for new_mother_alternate_parent_siblings_sim_info in new_mother_alternate_parent_siblings_sim_info_list:
                        self.log.format_with_message('Setting as step aunt/uncle', child=new_blood_child_sim_info, uncle_aunt=new_mother_alternate_parent_siblings_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                    for new_mother_alternate_parent_children_sim_info in new_mother_alternate_parent_children_sim_info_list:
                        self.log.format_with_message('Setting as step sibling', child=new_blood_child_sim_info, step_sibling=new_mother_alternate_parent_children_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_children_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                    for new_mother_alternate_parent_cousin_sim_info in new_mother_alternate_parent_cousin_sim_info_list:
                        self.log.format_with_message('Setting as step cousin', child=new_blood_child_sim_info, cousin=new_mother_alternate_parent_cousin_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_cousin_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                    if new_mother_father_sim_info is not None:
                        self.log.format_with_message('Setting as grandfather', child=new_blood_child_sim_info, grandfather=new_mother_father_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_father_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_father_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                        CommonSimGenealogyUtils.set_as_mothers_father_of(new_mother_father_sim_info, new_blood_child_sim_info)

                    if new_mother_mother_sim_info is not None:
                        self.log.format_with_message('Setting as grandfather', child=new_blood_child_sim_info, grandfather=new_mother_mother_sim_info)
                        CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_mother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                        CommonRelationshipUtils.add_relationship_bit(new_mother_mother_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                        CommonSimGenealogyUtils.set_as_mothers_mother_of(new_mother_mother_sim_info, new_blood_child_sim_info)
        else:
            # Mother One New as Mother of New Child Siblings
            for new_blood_child_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER, instanced_only=False):
                self.log.format_with_message('Setting as mother', child=new_blood_child_sim_info, mother=new_mother_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_mother_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
                CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonSimGenealogyUtils.set_as_mother_of(new_mother_sim_info, new_blood_child_sim_info)

                for new_mother_blood_siblings_sim_info in new_mother_blood_siblings_sim_info_list:
                    self.log.format_with_message('Setting as aunt/uncle', child=new_blood_child_sim_info, aunt_uncle=new_mother_blood_siblings_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_blood_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                for new_mother_alternate_cousin_parent_sim_info in new_mother_alternate_cousin_parent_sim_info_list:
                    self.log.format_with_message('Setting as aunt/uncle', child=new_blood_child_sim_info, aunt_uncle=new_mother_alternate_cousin_parent_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                for new_mother_alternate_cousin_parent_siblings_sim_info in new_mother_alternate_cousin_parent_siblings_sim_info_list:
                    self.log.format_with_message('Setting as aunt/uncle', child=new_blood_child_sim_info, aunt_uncle=new_mother_alternate_cousin_parent_siblings_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                for new_mother_alternate_cousin_parent_children_sim_info in new_mother_alternate_cousin_parent_children_sim_info_list:
                    self.log.format_with_message('Setting as cousin', child=new_blood_child_sim_info, cousin=new_mother_alternate_cousin_parent_children_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_children_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for new_mother_alternate_cousin_parent_parent_sim_info in new_mother_alternate_cousin_parent_parent_sim_info_list:
                    self.log.format_with_message('Setting as grandparent', child=new_blood_child_sim_info, grandparent=new_mother_alternate_cousin_parent_parent_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_cousin_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

                for new_mother_child_sim_info in new_mother_blood_children_sim_info_list:
                    self.log.format_with_message('Setting as sibling', child=new_blood_child_sim_info, sibling=new_mother_child_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

                for new_mother_blood_cousins_sim_info in new_mother_blood_cousins_sim_info_list:
                    self.log.format_with_message('Setting as cousin', child=new_blood_child_sim_info, cousin=new_mother_blood_cousins_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_blood_cousins_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for new_mother_alternate_parent_sim_info in new_mother_alternate_parent_sim_info_list:
                    self.log.format_with_message('Setting as step parent', child=new_blood_child_sim_info, parent=new_mother_alternate_parent_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

                for new_mother_alternate_parent_parent_sim_info in new_mother_alternate_parent_parent_sim_info_list:
                    self.log.format_with_message('Setting as step grandparent', child=new_blood_child_sim_info, parent=new_mother_alternate_parent_parent_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_parent_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

                for new_mother_alternate_parent_siblings_sim_info in new_mother_alternate_parent_siblings_sim_info_list:
                    self.log.format_with_message('Setting as step aunt/uncle', child=new_blood_child_sim_info, uncle_aunt=new_mother_alternate_parent_siblings_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_siblings_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

                for new_mother_alternate_parent_children_sim_info in new_mother_alternate_parent_children_sim_info_list:
                    self.log.format_with_message('Setting as step sibling', child=new_blood_child_sim_info, step_sibling=new_mother_alternate_parent_children_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_children_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

                for new_mother_alternate_parent_cousin_sim_info in new_mother_alternate_parent_cousin_sim_info_list:
                    self.log.format_with_message('Setting as step cousin', child=new_blood_child_sim_info, cousin=new_mother_alternate_parent_cousin_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_alternate_parent_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_cousin_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                if new_mother_father_sim_info is not None:
                    self.log.format_with_message('Setting as grandfather', child=new_blood_child_sim_info, grandfather=new_mother_father_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_father_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_father_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonSimGenealogyUtils.set_as_mothers_father_of(new_mother_father_sim_info, new_blood_child_sim_info)

                if new_mother_mother_sim_info is not None:
                    self.log.format_with_message('Setting as grandfather', child=new_blood_child_sim_info, grandfather=new_mother_mother_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_blood_child_sim_info, new_mother_mother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_mother_mother_sim_info, new_blood_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    CommonSimGenealogyUtils.set_as_mothers_mother_of(new_mother_mother_sim_info, new_blood_child_sim_info)

        self.log.format_with_message('Setting as mother', child=child_sim_info, mother=new_mother_sim_info)
        CommonRelationshipUtils.add_relationship_bit(new_mother_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
        CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
        CommonSimGenealogyUtils.set_as_mother_of(new_mother_sim_info, child_sim_info)

        for new_mother_blood_siblings_sim_info in new_mother_blood_siblings_sim_info_list:
            self.log.format_with_message('Setting as aunt/uncle', child=child_sim_info, aunt_uncle=new_mother_blood_siblings_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_blood_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(new_mother_blood_siblings_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for new_mother_alternate_cousin_parent_sim_info in new_mother_alternate_cousin_parent_sim_info_list:
            self.log.format_with_message('Setting as aunt/uncle', child=child_sim_info, aunt_uncle=new_mother_alternate_cousin_parent_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_cousin_parent_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for new_mother_alternate_cousin_parent_siblings_sim_info in new_mother_alternate_cousin_parent_siblings_sim_info_list:
            self.log.format_with_message('Setting as aunt/uncle', child=child_sim_info, aunt_uncle=new_mother_alternate_cousin_parent_siblings_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_cousin_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_siblings_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for new_mother_alternate_cousin_parent_children_sim_info in new_mother_alternate_cousin_parent_children_sim_info_list:
            self.log.format_with_message('Setting as cousin', child=child_sim_info, cousin=new_mother_alternate_cousin_parent_children_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_cousin_parent_children_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_children_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        for new_mother_alternate_cousin_parent_parent_sim_info in new_mother_alternate_cousin_parent_parent_sim_info_list:
            self.log.format_with_message('Setting as grandparent', child=child_sim_info, grandparent=new_mother_alternate_cousin_parent_parent_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_cousin_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_cousin_parent_parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        for new_mother_child_sim_info in new_mother_blood_children_sim_info_list:
            self.log.format_with_message('Setting as sibling', child=child_sim_info, sibling=new_mother_child_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
            CommonRelationshipUtils.add_relationship_bit(new_mother_child_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for new_mother_blood_cousins_sim_info in new_mother_blood_cousins_sim_info_list:
            self.log.format_with_message('Setting as cousin', child=child_sim_info, cousin=new_mother_blood_cousins_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_blood_cousins_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
            CommonRelationshipUtils.add_relationship_bit(new_mother_blood_cousins_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        for new_mother_alternate_parent_sim_info in new_mother_alternate_parent_sim_info_list:
            self.log.format_with_message('Setting as step parent', child=child_sim_info, parent=new_mother_alternate_parent_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_parent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for new_mother_alternate_parent_parent_sim_info in new_mother_alternate_parent_parent_sim_info_list:
            self.log.format_with_message('Setting as step grandparent', child=child_sim_info, parent=new_mother_alternate_parent_parent_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_parent_parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        for new_mother_alternate_parent_siblings_sim_info in new_mother_alternate_parent_siblings_sim_info_list:
            self.log.format_with_message('Setting as step aunt/uncle', child=child_sim_info, uncle_aunt=new_mother_alternate_parent_siblings_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_parent_siblings_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_siblings_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for new_mother_alternate_parent_children_sim_info in new_mother_alternate_parent_children_sim_info_list:
            self.log.format_with_message('Setting as step sibling', child=child_sim_info, step_sibling=new_mother_alternate_parent_children_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_parent_children_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_children_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for new_mother_alternate_parent_cousin_sim_info in new_mother_alternate_parent_cousin_sim_info_list:
            self.log.format_with_message('Setting as step cousin', child=child_sim_info, cousin=new_mother_alternate_parent_cousin_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_alternate_parent_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
            CommonRelationshipUtils.add_relationship_bit(new_mother_alternate_parent_cousin_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        if new_mother_father_sim_info is not None:
            self.log.format_with_message('Setting as grandfather', child=child_sim_info, grandfather=new_mother_father_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_father_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_mother_father_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_father_of(new_mother_father_sim_info, child_sim_info)

        if new_mother_mother_sim_info is not None:
            self.log.format_with_message('Setting as grandfather', child=child_sim_info, grandfather=new_mother_mother_sim_info)
            CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_mother_mother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_mother_mother_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(new_mother_mother_sim_info, child_sim_info)

        self.log.format_with_message('Done adding relation', child=child_sim_info, mother=new_mother_sim_info)
        return True
