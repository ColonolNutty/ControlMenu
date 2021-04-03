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

    def _update_family_tree(self, parent_sim_info: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as mother of Sim B', parent=parent_sim_info, sim_b=sim_info_b)
            self._remove_old_relation(parent_sim_info)
            # self._add_new_relation(parent_sim_info, sim_info_b)
            self.log.format_with_message('Done setting Sim A as mother of Sim B', parent=parent_sim_info, sim_b=sim_info_b)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as mother.', exception=ex)
            on_completed(False)
        return True

    def _remove_old_relation(self, sim_info: SimInfo) -> bool:
        # Mother 1
        # Remove Parent Blood Relations of Mother 1 with Grandfather 3 and Grandmother 3
        # Remove Grandparent Blood Relations of Mother 1 with Parent of Grandfather 3 and Grandmother 3
        # Remove Sibling Blood Relations of Mother 1 with Uncle 5 and Uncle 6
        # Remove Niece/Nephew of Mother 1 with Cousin 9, Cousin 10, Cousin 11, and Cousin 12
        # Remove Cousins of Mother 1 with Step Children of Grandfather 3 and Grandmother 3
        # Remove Aunt/Uncle of Mother 1 with Siblings of Grandfather 3 and Grandmother 3

        # Father 1
        # Remove Niece/Nephew of Father 1 with Cousin 9, 10, 11, and 12

        # Father 2
        # Remove Niece/Nephew of Father 2 with Cousin 9, 10, 11, and 12

        # Uncle 1
        # Remove Niece/Nephew of Uncle 1 with Cousin 9, 10, 11, and 12

        # Uncle 2
        # Remove Niece/Nephew of Uncle 2 with Cousin 9, 10, 11, and 12

        # Uncle 3
        # Remove Niece/Nephew of Uncle 3 with Cousin 9, 10, 11, and 12

        # Uncle 4
        # Remove Niece/Nephew of Uncle 4 with Cousin 9, 10, 11, and 12

        # Uncle 5
        # Remove Niece/Nephew of Uncle 5 with Child 1, Child 2, and Step Child 1

        # Uncle 6
        # Remove Niece/Nephew of Uncle 6 with Child 1, Child 2, and Step Child 1

        # Grandmother 3
        # Remove Child Blood Relations of Grandmother 3 with Mother 1
        # Remove Grandchild Blood Relations of Grandmother 3 with Child 1, Child 2, and Step Child 1

        # Grandfather 3
        # Remove Child Blood Relations of Grandfather 3 with Mother 1
        # Remove Grandchild Blood Relations of Grandfather 3 with Child 1, Child 2, and Step Child 1

        # Children
        # Child 1
        # Remove Aunt/Uncle of Child 1 with Uncle 5 and Uncle 6
        # Remove Grandparent Blood Relations of Child 1 with Grandfather 3 and Grandmother 3

        # Child 2
        # Remove Aunt/Uncle of Child 2 with Uncle 5 and Uncle 6
        # Remove Grandparent Blood Relations of Child 2 with Grandfather 3 and Grandmother 3

        # Cousin 9
        # Remove Aunt/Uncle of Cousin 9 with Mother 1, Father 1, Father 2, Uncle 1, 2, 3, and 4
        # Remove Cousin of Cousin 9 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Cousin 10
        # Remove Aunt/Uncle of Cousin 10 with Mother 1, Father 1, Father 2, Uncle 1, Uncle 2, Uncle 3, and Uncle 4
        # Remove Cousin of Cousin 10 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Cousin 11
        # Remove Aunt/Uncle of Cousin 11 with Mother 1, Father 1, Father 2, Uncle 1, Uncle 2, Uncle 3, and Uncle 4
        # Remove Cousin of Cousin 11 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Cousin 12
        # Remove Aunt/Uncle of Cousin 12 with Mother 1, Father 1, Father 2, Uncle 1, Uncle 2, Uncle 3, and Uncle 4
        # Remove Cousin of Cousin 12 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Step Relations
        # Mother 1
        # Remove Step Parent Relations of Mother 1 with Step Parent of Uncle 5 and Uncle 6
        # Remove Step Grandparent Relations of Mother 1 with Step Grandparent of Uncle 5 and Uncle 6
        # Remove Step Sibling of Mother 1 with Step Siblings of Uncle 5 and Uncle 6
        # Remove Step Niece/Nephew of Mother 1 with Step Niece/Nephew of Uncle 5 and Uncle 6
        # Remove Step Aunt/Uncle of Mother 1 with Step Siblings of Grandfather 3 and Grandmother 3

        # Father 1
        # Remove Step Niece/Nephew of Father 1 with Cousin 9, 10, 11, and 12
        # Remove Step Sibling of Father 1 with Uncle 5 and Uncle 6

        # Father 2
        # Remove Step Niece/Nephew of Father 2 with Cousin 9, 10, 11, and 12
        # Remove Step Sibling of Father 2 with Uncle 5 and Uncle 6

        # Uncle 1
        # Remove Step Niece/Nephew of Uncle 1 with Cousin 9, 10, 11, and 12
        # Remove Step Sibling of Uncle 1 with Uncle 5 and Uncle 6

        # Uncle 2
        # Remove Step Niece/Nephew of Uncle 2 with Cousin 9, 10, 11, and 12
        # Remove Step Sibling of Uncle 2 with Uncle 5 and Uncle 6

        # Uncle 3
        # Remove Step Niece/Nephew of Uncle 3 with Cousin 9, 10, 11, and 12
        # Remove Step Sibling of Uncle 3 with Uncle 5 and Uncle 6

        # Uncle 4
        # Remove Step Niece/Nephew of Uncle 4 with Cousin 9, 10, 11, and 12
        # Remove Step Sibling of Uncle 4 with Uncle 5 and Uncle 6

        # Uncle 5
        # Remove Step Niece/Nephew of Uncle 5 with Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8
        # Remove Step Sibling of Uncle 5 with Uncle 1, 2, 3, and 4

        # Uncle 6
        # Remove Step Niece/Nephew of Uncle 6 with Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8
        # Remove Step Sibling of Uncle 6 with Uncle 1, 2, 3, and 4

        # Grandmother 3
        # Remove Child Blood Relations of Grandmother 3 with Mother 1
        # Remove Step Child Relations of Grandmother 3 with Father 1, Father 2, Uncle 1, 2, 3, and 4
        # Remove Grandchild Blood Relations of Grandmother 3 with Child 1, Child 2, and Step Child 1
        # Remove Step Grandchild Relations of Grandmother 3 with Step Child 2

        # Grandfather 3
        # Remove Child Blood Relations of Grandfather 3 with Mother 1
        # Remove Step Child Relations of Grandfather 3 with Father 1, Father 2, Uncle 1, 2, 3, and 4
        # Remove Grandchild Blood Relations of Grandfather 3 with Child 1, Child 2, and Step Child 1
        # Remove Step Grandchild Relations of Grandfather 3 with Step Child 2

        # Children
        # Child 1
        # Remove Aunt/Uncle of Child 1 with Uncle 5 and Uncle 6
        # Remove Grandparent Blood Relations of Child 1 with Grandfather 3 and Grandmother 3

        # Child 2
        # Remove Aunt/Uncle of Child 2 with Uncle 5 and Uncle 6
        # Remove Grandparent Blood Relations of Child 2 with Grandfather 3 and Grandmother 3

        # Cousin 9
        # Remove Aunt/Uncle of Cousin 9 with Mother 1, Father 1, Father 2, Uncle 1, 2, 3, and 4
        # Remove Cousin of Cousin 9 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Cousin 10
        # Remove Aunt/Uncle of Cousin 10 with Mother 1, Father 1, Father 2, Uncle 1, Uncle 2, Uncle 3, and Uncle 4
        # Remove Cousin of Cousin 10 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Cousin 11
        # Remove Aunt/Uncle of Cousin 11 with Mother 1, Father 1, Father 2, Uncle 1, Uncle 2, Uncle 3, and Uncle 4
        # Remove Cousin of Cousin 11 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Cousin 12
        # Remove Aunt/Uncle of Cousin 12 with Mother 1, Father 1, Father 2, Uncle 1, Uncle 2, Uncle 3, and Uncle 4
        # Remove Cousin of Cousin 12 with Child 1, Child 2, Step Child 1, Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, and 8

        # Remove ALL blood relations from mother and children of mother from their mothers parents and brothers.
        # Remove ALL step relations if the step relations are on the siblings.
        self.log.format_with_message('Removing relations to old family', new_sim=sim_info)
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)

        # Remove Blood Family
        old_blood_family_sim_info_list = list()
        # Remove Blood Brothers/Sisters
        with genealogy_caching():
            for sibling_sim_info in genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found blood sibling by blood. Removing them.', sim=sim_info, sibling=sibling_sim_info)
                old_blood_family_sim_info_list.append(sibling_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(sim_info, sibling_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                CommonRelationshipUtils.remove_relationship_bit(sibling_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for sibling_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER, instanced_only=False):
            if sibling_sim_info in old_blood_family_sim_info_list:
                continue
            self.log.format_with_message('Found blood sibling through relationship bit. Removing them.', sim=sim_info, sibling=sibling_sim_info)
            old_blood_family_sim_info_list.append(sibling_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, sibling_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
            CommonRelationshipUtils.remove_relationship_bit(sibling_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        old_blood_family_sim_info_list_temp = list(old_blood_family_sim_info_list)
        for blood_family_sim_info in old_blood_family_sim_info_list_temp:
            blood_family_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(blood_family_sim_info)
            with genealogy_caching():
                for blood_niece_nephew_sim_info in blood_family_genealogy_tracker.get_child_sim_infos_gen():
                    if blood_niece_nephew_sim_info in old_blood_family_sim_info_list:
                        continue
                    self.log.format_with_message('Found blood niece/nephew. Removing them.', sim=sim_info, niece_nephew=blood_niece_nephew_sim_info)
                    old_blood_family_sim_info_list.append(blood_niece_nephew_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(blood_niece_nephew_sim_info, sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, blood_niece_nephew_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Remove Blood Grandfather
        if CommonSimGenealogyUtils.has_father(sim_info):
            blood_grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
            if blood_grandfather_sim_info not in old_blood_family_sim_info_list:
                old_blood_family_sim_info_list.append(blood_grandfather_sim_info)
            self.log.format_with_message('Found father. Removing them.', sim=sim_info, father=blood_grandfather_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, blood_grandfather_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(blood_grandfather_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_father_relation(sim_info)

        # Remove Blood Grandmother
        if CommonSimGenealogyUtils.has_mother(sim_info):
            blood_grandmother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
            if blood_grandmother_sim_info not in old_blood_family_sim_info_list:
                old_blood_family_sim_info_list.append(blood_grandmother_sim_info)
            self.log.format_with_message('Found mother. Removing them.', sim=sim_info, mother=blood_grandmother_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, blood_grandmother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(blood_grandmother_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_mother_relation(sim_info)

        for old_blood_family_sim_info in old_blood_family_sim_info_list:
            with genealogy_caching():
                for blood_child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Removing blood family from Child.', sim=blood_child_sim_info, blood_family=old_blood_family_sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(blood_child_sim_info, old_blood_family_sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, blood_child_sim_info)

        self.log.format_with_message('Done removing relations to old family', new_sim=sim_info)
        return True

    def _add_new_relation(self, parent_sim_info: SimInfo, new_child_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding new mother to Sim', sim=new_child_sim_info, parent_sim=parent_sim_info)
        # Add new Mother
        CommonSimGenealogyUtils.set_as_mother_of(parent_sim_info, new_child_sim_info)
        self.log.format_with_message('Done adding new mother', sim=new_child_sim_info, parent=parent_sim_info)
        return True
