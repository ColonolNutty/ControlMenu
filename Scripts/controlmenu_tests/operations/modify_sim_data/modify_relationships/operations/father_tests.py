"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyMissingOrEmptyDocstring
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
    CMSetSimAAsFatherToSimBOp
from controlmenu.modinfo import ModInfo
from controlmenu_tests.operations.modify_sim_data.modify_relationships.operations.full_family import CMFullFamily


@CommonTestService.test_class(ModInfo.get_identity())
class _CMSetSimAAsFatherToSimBOpTests:
    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_father_of_sim_b() -> None:
        # Father
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim B and Sim B as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_a, sim_info_b), 'Failed to set Sim A as biological father of Sim B')

            CommonAssertionUtils.is_true(CMSetSimAAsFatherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should have been the father of Sim B but was not.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_not_father_of_sim_b() -> None:
        # Father
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_false(CMSetSimAAsFatherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should not have been the father of Sim B but was.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_only_rel_bit_father_of_sim_b() -> None:
        # Father
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as parent of Sim B and Sim B as child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim A')

            CommonAssertionUtils.is_false(CMSetSimAAsFatherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should not have been the father of Sim B with only the relationship bit but was.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_only_family_tree_father_of_sim_b() -> None:
        # Father
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim B and Sim B as biological child of Sim A
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_a, sim_info_b), 'Failed to set Sim A as biological father of Sim B')

            CommonAssertionUtils.is_false(CMSetSimAAsFatherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should not have been the father of Sim B with only the family tree but was.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_father_to_sim_b_should_remove_relationships_of_previous_father_from_previous_family() -> None:
        new_full_family = CMFullFamily()
        old_full_family = CMFullFamily(suffix='2')
        sim_a_father = old_full_family.father_one
        sim_b_child = new_full_family.child_one
        previous_father_one = new_full_family.father_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(CMSetSimAAsFatherToSimBOp()._update_family_tree(sim_a_father, sim_b_child), 'Failed to update family tree.')
            CMSetSimAAsFatherToSimBOp()._add_relationship_bits(sim_a_father, sim_b_child)

            # -----------------------Previous Father Blood Relations With Previous Children-----------------------

            blood_children_of_previous_father_one_list = (
                new_full_family.child_one,
                new_full_family.child_two
            )

            blood_grandchildren_of_previous_father_one_list = (
                new_full_family.grand_child_one,
                new_full_family.grand_child_two
            )

            blood_siblings_of_previous_father_one_list = (
                new_full_family.step_child_two,
            )

            blood_uncle_aunt_of_previous_father_one_list = (
                new_full_family.uncle_one,
                new_full_family.uncle_two
            )

            blood_cousin_of_previous_father_one_list = (
                new_full_family.cousin_one,
                new_full_family.cousin_two,
                new_full_family.cousin_three,
                new_full_family.cousin_four
            )

            previous_father_name = CommonSimNameUtils.get_full_name(previous_father_one)
            # Previous Father One is no longer the Father of the Father of new grandchildren.
            for blood_grandchildren_of_previous_father_one in blood_grandchildren_of_previous_father_one_list:
                blood_grandchildren_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_grandchildren_of_previous_father_one)
                # Mother
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandchildren_of_previous_father_one, previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_grandchildren_of_previous_father_one_name} was still a grandchild to {previous_father_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_father_one, blood_grandchildren_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{previous_father_name} was still a grandparent to {blood_grandchildren_of_previous_father_one_name}')
                blood_grandfather_grandchildren_of_previous_father_one = CommonSimGenealogyUtils.get_fathers_father_sim_info(blood_grandchildren_of_previous_father_one)
                CommonAssertionUtils.is_false(blood_grandfather_grandchildren_of_previous_father_one is previous_father_one)

            # Previous Father One is no longer father of new children.
            for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                # Mother
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, previous_father_one, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_child_of_previous_father_one_name} was still a child to {previous_father_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_father_name} was still a parent to {blood_child_of_previous_father_one_name}')
                blood_father_of_blood_child_of_previous_father_one = CommonSimGenealogyUtils.get_father_sim_info(blood_child_of_previous_father_one)
                CommonAssertionUtils.is_false(blood_father_of_blood_child_of_previous_father_one is previous_father_one)

            # Previous Half Siblings of Previous Father should no longer be Half Siblings with new children.
            for blood_siblings_of_previous_father_one in blood_siblings_of_previous_father_one_list:
                blood_siblings_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_siblings_of_previous_father_one)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, blood_siblings_of_previous_father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_child_of_previous_father_one_name} was still a sibling to {blood_siblings_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_siblings_of_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_siblings_of_previous_father_one_name} was still a sibling to {blood_child_of_previous_father_one_name}')

            # Previous Uncle/Aunt no longer Uncle/Aunt of new children.
            for blood_uncle_aunt_of_previous_father_one in blood_uncle_aunt_of_previous_father_one_list:
                blood_uncle_aunt_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_uncle_aunt_of_previous_father_one)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, blood_uncle_aunt_of_previous_father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{blood_child_of_previous_father_one_name} was still a niece/nephew to {blood_uncle_aunt_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_uncle_aunt_of_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_uncle_aunt_of_previous_father_one_name} was still an aunt/uncle to {blood_child_of_previous_father_one_name}')

            # Previous Cousin no longer Cousin of new children.
            for blood_cousin_of_previous_father_one in blood_cousin_of_previous_father_one_list:
                blood_cousin_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_cousin_of_previous_father_one)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, blood_cousin_of_previous_father_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_father_one_name} was still a cousin to {blood_cousin_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_cousin_of_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_cousin_of_previous_father_one_name} was still a cousin to {blood_child_of_previous_father_one_name}')

            # Parents of previous Father One children should no longer be the grandparents of new children.
            blood_grandfather_previous_father_one = new_full_family.grandfather_one
            blood_grandmother_previous_father_one = new_full_family.grandmother_one
            blood_grandfather_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_grandfather_previous_father_one)
            blood_grandmother_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_grandmother_previous_father_one)
            for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                # Grandfather
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, blood_grandfather_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_father_one_name} was still a grandchild to {blood_grandfather_previous_father_one_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandfather_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_grandfather_previous_father_one_name} was still a grandparent to {blood_child_of_previous_father_one_name}')
                blood_grandfather_of_blood_child_of_previous_father_one = CommonSimGenealogyUtils.get_fathers_father_sim_info(blood_child_of_previous_father_one)
                CommonAssertionUtils.is_false(blood_grandfather_of_blood_child_of_previous_father_one is blood_grandfather_previous_father_one, f'{blood_grandfather_previous_father_one_name} was still the biological grandfather of {blood_child_of_previous_father_one_name}')

                # Grandmother
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, blood_grandmother_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_father_one_name} was not a grandchild to {blood_grandmother_previous_father_one_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandmother_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_grandmother_previous_father_one_name} was not a grandparent to {blood_child_of_previous_father_one_name}')
                blood_grandmother_of_blood_child_of_previous_father_one = CommonSimGenealogyUtils.get_fathers_mother_sim_info(blood_child_of_previous_father_one)
                CommonAssertionUtils.is_false(blood_grandmother_of_blood_child_of_previous_father_one is blood_grandmother_previous_father_one, f'{blood_grandmother_previous_father_one_name} was still the biological grandmother of {blood_child_of_previous_father_one_name}')

            # -----------------------Previous Father Step Relations With Previous Children-----------------------

            step_parent_of_previous_father_one_list = (
                new_full_family.mother_two,
            )

            step_uncle_aunt_of_previous_father_list = (
                new_full_family.aunt_three,
                new_full_family.aunt_four,
                new_full_family.uncle_seven,
                new_full_family.uncle_eight
            )

            step_grandparent_of_previous_father_one_list = (
                new_full_family.grandfather_six,
                new_full_family.grandmother_six
            )

            step_cousin_of_previous_father_one_list = (
                new_full_family.cousin_thirteen,
                new_full_family.cousin_fourteen,
                new_full_family.cousin_fifteen,
                new_full_family.cousin_sixteen,
                new_full_family.cousin_nineteen,
                new_full_family.cousin_twenty
            )

            # Previous Step Parent no longer Parent of new children.
            for step_parent_of_previous_father_one in step_parent_of_previous_father_one_list:
                step_parent_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_father_one)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_parent_of_previous_father_one, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_child_of_previous_father_one_name} was still a Step Child to {step_parent_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{step_parent_of_previous_father_one_name} was still a step parent to {blood_child_of_previous_father_one_name}')

            # Previous Step Uncle/Aunt no longer Step Uncle/Aunt of new children.
            for step_uncle_aunt_of_previous_father in step_uncle_aunt_of_previous_father_list:
                step_uncle_aunt_of_previous_father_name = CommonSimNameUtils.get_full_name(step_uncle_aunt_of_previous_father)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_uncle_aunt_of_previous_father, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{blood_child_of_previous_father_one_name} was still a step niece/nephew to {step_uncle_aunt_of_previous_father_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_uncle_aunt_of_previous_father, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{step_uncle_aunt_of_previous_father_name} was still a step aunt/uncle to {blood_child_of_previous_father_one_name}')

            # Previous Step Grandparents no longer Step Grandparents of new children.
            for step_grandparent_of_previous_father_one in step_grandparent_of_previous_father_one_list:
                step_grandparent_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_grandparent_of_previous_father_one)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_grandparent_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_father_one_name} was still a step grandchild to {step_grandparent_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_grandparent_of_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{step_grandparent_of_previous_father_one_name} was still a step grandparent to {blood_child_of_previous_father_one_name}')

            # Previous Step Cousin no longer Step Cousin of new children.
            for step_cousin_of_previous_father_one in step_cousin_of_previous_father_one_list:
                step_cousin_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_cousin_of_previous_father_one)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_cousin_of_previous_father_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_father_one_name} was still a step cousin to {step_cousin_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousin_of_previous_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{step_cousin_of_previous_father_one_name} was still a step cousin to {blood_child_of_previous_father_one_name}')

            # -----------------------Previous Mother One Step Relations With Mother One Family-----------------------

            step_parent_of_previous_mother_one_list = (
                new_full_family.grandfather_three,
                new_full_family.grandmother_three
            )

            step_children_of_previous_mother_one_list = (
                new_full_family.step_child_one,
                new_full_family.step_child_three,
            )

            step_siblings_of_previous_mother_one_list = (
                new_full_family.mother_one,
                new_full_family.uncle_five,
                new_full_family.uncle_six,
                new_full_family.aunt_one,
                new_full_family.aunt_two
            )

            step_cousins_of_previous_mother_one_list = (
                new_full_family.cousin_nine,
                new_full_family.cousin_ten,
                new_full_family.cousin_eleven,
                new_full_family.cousin_twelve
            )

            blood_parents_of_previous_father_one_list = (
                new_full_family.grandfather_one,
                new_full_family.grandmother_one
            )

            step_children_of_previous_father_one_list = (
                new_full_family.step_child_two,
            )

            blood_uncle_aunt_of_previous_father_one_list = (
                new_full_family.father_one,
                new_full_family.uncle_one,
                new_full_family.uncle_two
            )

            blood_cousin_of_previous_father_one_list = (
                new_full_family.cousin_one,
                new_full_family.cousin_two,
                new_full_family.cousin_three,
                new_full_family.cousin_four
            )

            # Previous Mother One no longer Step Parent of Step Child Two new.
            previous_mother_one_name = CommonSimNameUtils.get_full_name(new_full_family.mother_one)
            previous_step_child_two_name = CommonSimNameUtils.get_full_name(new_full_family.step_child_two)
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.mother_one, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_child_two_name} was still a Step Child to {previous_mother_one_name}')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, new_full_family.mother_one, CommonRelationshipBitId.FAMILY_PARENT), f'{previous_mother_one_name} was still a Step Parent to {previous_step_child_two_name}')

            # Previous Father One no longer Step Parent of Step Child One new.
            previous_step_child_one_name = CommonSimNameUtils.get_full_name(new_full_family.step_child_one)
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_father_one, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_child_one_name} was still a Step Child to {previous_father_name}')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_one, previous_father_one, CommonRelationshipBitId.FAMILY_PARENT), f'{previous_father_name} was still a Step Parent to {previous_step_child_one_name}')

            # Previous Father One no longer Step Parent of Step Child Three new.
            previous_step_child_three_name = CommonSimNameUtils.get_full_name(new_full_family.step_child_three)
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_father_one, new_full_family.step_child_three, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_child_three_name} was still a Step Child to {previous_father_name}')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_three, previous_father_one, CommonRelationshipBitId.FAMILY_PARENT), f'{previous_father_name} was still a Step Parent to {previous_step_child_three_name}')

            # Previous Mother One siblings no longer step siblings of Father One.
            for step_siblings_of_previous_mother_one in step_siblings_of_previous_mother_one_list:
                step_siblings_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_mother_one)
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_mother_one, previous_father_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{previous_father_name} was still a step sibling to {step_siblings_of_previous_mother_one_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_father_one, step_siblings_of_previous_mother_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{step_siblings_of_previous_mother_one_name} was still a step sibling to {previous_father_name}')

            # Previous Mother One siblings no longer step Aunt/Uncle of Father One cousins.
            for step_siblings_of_previous_mother_one in step_siblings_of_previous_mother_one_list:
                step_siblings_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_mother_one)
                for blood_cousin_of_previous_father_one in blood_cousin_of_previous_father_one_list:
                    blood_cousin_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_cousin_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_cousin_of_previous_father_one, step_siblings_of_previous_mother_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_siblings_of_previous_mother_one_name} was still a step aunt/uncle to {blood_cousin_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_mother_one, blood_cousin_of_previous_father_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_cousin_of_previous_father_one_name} was still a step niece/nephew to {step_siblings_of_previous_mother_one_name}')

            # Previous Mother One siblings no longer step Aunt/Uncle of Father One's Step Children.
            for step_siblings_of_previous_mother_one in step_siblings_of_previous_mother_one_list:
                step_siblings_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_mother_one)
                for step_children_of_previous_father_one in step_children_of_previous_father_one_list:
                    step_children_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_children_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_children_of_previous_father_one, step_siblings_of_previous_mother_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_siblings_of_previous_mother_one_name} was still a step aunt/uncle to {step_children_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_mother_one, step_children_of_previous_father_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{step_children_of_previous_father_one_name} was still a step niece/nephew to {step_siblings_of_previous_mother_one_name}')

            # Previous Mother One siblings no longer Step Children of Father One parents.
            for blood_parents_of_previous_father_one in blood_parents_of_previous_father_one_list:
                blood_parents_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_parents_of_previous_father_one)
                for step_siblings_of_previous_mother_one in step_siblings_of_previous_mother_one_list:
                    step_siblings_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_mother_one, blood_parents_of_previous_father_one, CommonRelationshipBitId.FAMILY_PARENT), f'{step_siblings_of_previous_mother_one_name} was still a Step Child to {blood_parents_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_parents_of_previous_father_one, step_siblings_of_previous_mother_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{blood_parents_of_previous_father_one_name} was still a Step Parent to {step_siblings_of_previous_mother_one_name}')

            # Previous Mother One parents no longer Step Parents of Father One siblings.
            for step_parent_of_previous_mother_one in step_parent_of_previous_mother_one_list:
                step_parent_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_mother_one)
                for blood_uncle_aunt_of_previous_father_one in blood_uncle_aunt_of_previous_father_one_list:
                    blood_uncle_aunt_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_uncle_aunt_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_uncle_aunt_of_previous_father_one, step_parent_of_previous_mother_one, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_uncle_aunt_of_previous_father_one_name} was still a Step Child to {step_parent_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_mother_one, blood_uncle_aunt_of_previous_father_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{step_parent_of_previous_mother_one_name} was still a Step Parent to {blood_uncle_aunt_of_previous_father_one_name}')

            # Previous Mother One parents no longer Step Grandparents of Father One Cousins.
            for step_parent_of_previous_mother_one in step_parent_of_previous_mother_one_list:
                step_parent_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_mother_one)
                for blood_cousin_of_previous_father_one in blood_cousin_of_previous_father_one_list:
                    blood_cousin_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_cousin_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_cousin_of_previous_father_one, step_parent_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_cousin_of_previous_father_one_name} was still a step grandchild to {step_parent_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_mother_one, blood_cousin_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{step_parent_of_previous_mother_one_name} was still a step grandparent to {blood_cousin_of_previous_father_one_name}')

            # Previous Father One parents no longer Step Grandparents of Mother One Cousins.
            for blood_parents_of_previous_father_one in blood_parents_of_previous_father_one_list:
                blood_parents_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_parents_of_previous_father_one)
                for step_cousins_of_previous_mother_one in step_cousins_of_previous_mother_one_list:
                    step_cousins_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_cousins_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousins_of_previous_mother_one, blood_parents_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_cousins_of_previous_mother_one_name} was still a step grandchild to {blood_parents_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_parents_of_previous_father_one, step_cousins_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_parents_of_previous_father_one_name} was still a step grandparent to {step_cousins_of_previous_mother_one_name}')

            # Previous Father One parents no longer Step Grandparents of Mother One's Step Children.
            for blood_parents_of_previous_father_one in blood_parents_of_previous_father_one_list:
                blood_parents_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_parents_of_previous_father_one)
                for step_children_of_previous_mother_one in step_children_of_previous_mother_one_list:
                    step_children_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_children_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_children_of_previous_mother_one, blood_parents_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_children_of_previous_mother_one_name} was still a step grandchild to {blood_parents_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_parents_of_previous_father_one, step_children_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_parents_of_previous_father_one_name} was still a step grandparent to {step_children_of_previous_mother_one_name}')

            # Previous Mother One parents no longer Step Grandparents of Father One's Step Children.
            for step_parent_of_previous_mother_one in step_parent_of_previous_mother_one_list:
                step_parent_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_mother_one)
                for step_children_of_previous_father_one in step_children_of_previous_father_one_list:
                    step_children_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_children_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_children_of_previous_father_one, step_parent_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_children_of_previous_father_one_name} was still a step grandchild to {step_parent_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_mother_one, step_children_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{step_parent_of_previous_mother_one_name} was still a step grandparent to {step_children_of_previous_father_one_name}')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_father_to_sim_b_should_add_relationships_from_new_family() -> None:
        new_full_family = CMFullFamily()
        old_full_family = CMFullFamily(suffix='2')
        sim_a_father = old_full_family.father_one
        sim_b_child = new_full_family.child_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(CMSetSimAAsFatherToSimBOp()._update_family_tree(sim_a_father, sim_b_child), 'Failed to update family tree.')
            CMSetSimAAsFatherToSimBOp()._add_relationship_bits(sim_a_father, sim_b_child)

            # -----------------------Blood Relations With New Children-----------------------

            # Blood children on fathers side of family.
            blood_children_of_new_father_one_list = (
                old_full_family.child_one,
                old_full_family.child_two
            )

            blood_children_of_previous_father_one_list = (
                new_full_family.child_one,
                new_full_family.child_two
            )

            blood_grandchildren_of_previous_father_one_list = (
                new_full_family.grand_child_one,
                new_full_family.grand_child_two
            )

            blood_step_child_father_one_side_list = (
                old_full_family.step_child_two,
            )

            uncle_aunt_on_father_one_side_list = (
                old_full_family.uncle_one,
                old_full_family.uncle_two,
                old_full_family.aunt_three,
                old_full_family.aunt_four
            )

            cousins_on_father_one_side_list = (
                old_full_family.cousin_one,
                old_full_family.cousin_two,
                old_full_family.cousin_three,
                old_full_family.cousin_four,
                old_full_family.cousin_thirteen,
                old_full_family.cousin_fourteen,
                old_full_family.cousin_fifteen,
                old_full_family.cousin_sixteen,
            )

            sim_a_father_name = CommonSimNameUtils.get_full_name(sim_a_father)
            # New Father One is the Father of the Father of new grandchildren.
            for blood_grandchildren_of_previous_father_one in blood_grandchildren_of_previous_father_one_list:
                blood_grandchildren_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_grandchildren_of_previous_father_one)
                # Grandfather
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandchildren_of_previous_father_one, sim_a_father, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_grandchildren_of_previous_father_one_name} was not a grandchild to {sim_a_father_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_father, blood_grandchildren_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{sim_a_father_name} was not a grandparent to {blood_grandchildren_of_previous_father_one_name}')
                blood_grandfather_grandchildren_of_previous_father_one = CommonSimGenealogyUtils.get_fathers_father_sim_info(blood_grandchildren_of_previous_father_one)
                CommonAssertionUtils.is_true(blood_grandfather_grandchildren_of_previous_father_one is sim_a_father, f'{sim_a_father_name} was not the biological grandparent of {blood_grandchildren_of_previous_father_one_name}')

            # New Father One is father of new children.
            for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                # Father
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, sim_a_father, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_child_of_previous_father_one_name} was not a child to {sim_a_father_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_father, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{sim_a_father_name} was not a parent to {blood_child_of_previous_father_one_name}')
                blood_father_of_blood_child_of_previous_father_one = CommonSimGenealogyUtils.get_father_sim_info(blood_child_of_previous_father_one)
                CommonAssertionUtils.is_true(blood_father_of_blood_child_of_previous_father_one is sim_a_father, f'{sim_a_father_name} was not the biological parent of {blood_child_of_previous_father_one_name}')

            # Uncles/Aunts of new father should be Uncles/Aunts of previous children.
            for uncle_aunt_on_father_one_side in uncle_aunt_on_father_one_side_list:
                uncle_or_aunt_name = CommonSimNameUtils.get_full_name(uncle_aunt_on_father_one_side)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, uncle_aunt_on_father_one_side, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{uncle_or_aunt_name} was not a uncle/aunt to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(uncle_aunt_on_father_one_side, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_child_of_previous_father_one_name} was not a nephew/niece to {uncle_or_aunt_name}')

            # Blood Children of new father one should be brother/sister of new children because they share the same father.
            for blood_children_of_new_father_one in blood_children_of_new_father_one_list:
                blood_children_of_new_father_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_father_one)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, blood_children_of_new_father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_children_of_new_father_one_name} was not a sibling to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_father_one, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_child_of_previous_father_one_name} was not a sibling to {blood_children_of_new_father_one_name}')

            # Blood Children of different mother should be brother/sister of new children because they share the same father.
            for blood_step_child_father_one_side in blood_step_child_father_one_side_list:
                blood_step_child_father_one_side_name = CommonSimNameUtils.get_full_name(blood_step_child_father_one_side)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, blood_step_child_father_one_side, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_step_child_father_one_side_name} was not a sibling to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_step_child_father_one_side, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_child_of_previous_father_one_name} was not a sibling to {blood_step_child_father_one_side_name}')

            # Cousins of new Father One children should become cousins of new children.
            for cousin_on_father_one_side in cousins_on_father_one_side_list:
                cousin_on_father_one_side_name = CommonSimNameUtils.get_full_name(cousin_on_father_one_side)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, cousin_on_father_one_side, CommonRelationshipBitId.FAMILY_COUSIN), f'{cousin_on_father_one_side_name} was not a cousin to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(cousin_on_father_one_side, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_father_one_name} was not a cousin to {cousin_on_father_one_side_name}')

            # Parents of new Father One children should become grandparents of new children.
            grandfather_on_father_one_side = old_full_family.grandfather_one
            grandmother_on_father_one_side = old_full_family.grandmother_one
            grandfather_on_father_one_side_name = CommonSimNameUtils.get_full_name(grandfather_on_father_one_side)
            grandmother_on_father_one_side_name = CommonSimNameUtils.get_full_name(grandmother_on_father_one_side)
            for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                # Grandfather
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, grandfather_on_father_one_side, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_father_one_name} was not a grandchild to {grandfather_on_father_one_side_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(grandfather_on_father_one_side, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{grandfather_on_father_one_side_name} was not a grandparent to {blood_child_of_previous_father_one_name}')
                blood_grandfather_of_blood_child_of_previous_father_one = CommonSimGenealogyUtils.get_fathers_father_sim_info(blood_child_of_previous_father_one)
                CommonAssertionUtils.is_true(blood_grandfather_of_blood_child_of_previous_father_one is grandfather_on_father_one_side, f'{grandfather_on_father_one_side_name} was not the biological grandfather of {blood_child_of_previous_father_one_name}')

                # Grandmother
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, grandmother_on_father_one_side, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_father_one_name} was not a grandchild to {grandmother_on_father_one_side_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(grandmother_on_father_one_side, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{grandmother_on_father_one_side_name} was not a grandparent to {blood_child_of_previous_father_one_name}')
                blood_grandmother_of_blood_child_of_previous_father_one = CommonSimGenealogyUtils.get_fathers_mother_sim_info(blood_child_of_previous_father_one)
                CommonAssertionUtils.is_true(blood_grandmother_of_blood_child_of_previous_father_one is grandmother_on_father_one_side, f'{grandmother_on_father_one_side_name} was not the biological grandmother of {blood_child_of_previous_father_one_name}')

            # -----------------------Step Relations With New Children-----------------------

            step_parent_of_new_children_list = (
                old_full_family.mother_one,
                old_full_family.mother_two,
            )

            step_uncle_aunt_of_new_children_list = (
                old_full_family.uncle_five,
                old_full_family.uncle_six,
                old_full_family.uncle_seven,
                old_full_family.uncle_eight
            )

            step_cousin_of_new_children_list = (
                old_full_family.cousin_nine,
                old_full_family.cousin_ten,
                old_full_family.cousin_eleven,
                old_full_family.cousin_twelve
            )

            step_grandparent_of_new_children_list = (
                old_full_family.grandfather_three,
                old_full_family.grandmother_three,
                old_full_family.grandfather_four,
                old_full_family.grandmother_four,
                old_full_family.grandfather_six,
                old_full_family.grandmother_six
            )

            # Step Parents
            for step_parent_of_new_children in step_parent_of_new_children_list:
                step_parent_of_new_children_name = CommonSimNameUtils.get_full_name(step_parent_of_new_children)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_parent_of_new_children, CommonRelationshipBitId.FAMILY_PARENT), f'{step_parent_of_new_children_name} was not a Step Parent to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_new_children, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{blood_child_of_previous_father_one_name} was not a Step Child to {step_parent_of_new_children_name}')

            # Step Uncle
            for step_uncle_aunt_of_new_children in step_uncle_aunt_of_new_children_list:
                step_uncle_aunt_of_new_children_name = CommonSimNameUtils.get_full_name(step_uncle_aunt_of_new_children)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_uncle_aunt_of_new_children, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_uncle_aunt_of_new_children_name} was not a step aunt/uncle to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_uncle_aunt_of_new_children, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_child_of_previous_father_one_name} was not a step niece/nephew to {step_uncle_aunt_of_new_children_name}')

            # Step Cousin
            for step_cousin_of_new_children in step_cousin_of_new_children_list:
                step_cousin_of_new_children_name = CommonSimNameUtils.get_full_name(step_cousin_of_new_children)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_cousin_of_new_children, CommonRelationshipBitId.FAMILY_COUSIN), f'{step_cousin_of_new_children_name} was not a step cousin to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousin_of_new_children, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_father_one_name} was not a step cousin to {step_cousin_of_new_children_name}')

            # Step Grandparent
            for step_grandparent_of_new_children in step_grandparent_of_new_children_list:
                step_grandparent_of_new_children_name = CommonSimNameUtils.get_full_name(step_grandparent_of_new_children)
                for blood_child_of_previous_father_one in blood_children_of_previous_father_one_list:
                    blood_child_of_previous_father_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_father_one, step_grandparent_of_new_children, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_grandparent_of_new_children_name} was not a step grandparent to {blood_child_of_previous_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_grandparent_of_new_children, blood_child_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_child_of_previous_father_one_name} was not a step grandchild to {step_grandparent_of_new_children_name}')

            # -----------------------Step Relations With Old Children-----------------------

            blood_children_of_new_father_one_list = (
                old_full_family.child_one,
                old_full_family.child_two,
                old_full_family.step_child_two
            )

            step_parent_of_new_children_list = (
                new_full_family.mother_one,
            )

            step_uncle_aunt_of_new_children_list = (
                new_full_family.uncle_five,
                new_full_family.uncle_six
            )

            step_cousin_of_new_children_list = (
                new_full_family.cousin_nine,
                new_full_family.cousin_ten,
                new_full_family.cousin_eleven,
                new_full_family.cousin_twelve
            )

            step_grandparent_of_new_children_list = (
                new_full_family.grandfather_three,
                new_full_family.grandmother_three
            )

            # Step Parents
            for step_parent_of_new_children in step_parent_of_new_children_list:
                step_parent_of_new_children_name = CommonSimNameUtils.get_full_name(step_parent_of_new_children)
                for blood_children_of_new_father_one in blood_children_of_new_father_one_list:
                    blood_children_of_new_father_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_father_one, step_parent_of_new_children, CommonRelationshipBitId.FAMILY_PARENT), f'{step_parent_of_new_children_name} was not a Step Parent to {blood_children_of_new_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_new_children, blood_children_of_new_father_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{blood_children_of_new_father_one_name} was not a Step Child to {step_parent_of_new_children_name}')

            # Step Uncle
            for step_uncle_aunt_of_new_children in step_uncle_aunt_of_new_children_list:
                step_uncle_aunt_of_new_children_name = CommonSimNameUtils.get_full_name(step_uncle_aunt_of_new_children)
                for blood_children_of_new_father_one in blood_children_of_new_father_one_list:
                    blood_children_of_new_father_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_father_one, step_uncle_aunt_of_new_children, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_uncle_aunt_of_new_children_name} was not a step aunt/uncle to {blood_children_of_new_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_uncle_aunt_of_new_children, blood_children_of_new_father_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_children_of_new_father_one_name} was not a step niece/nephew to {step_uncle_aunt_of_new_children_name}')

            # Step Cousin
            for step_cousin_of_new_children in step_cousin_of_new_children_list:
                step_cousin_of_new_children_name = CommonSimNameUtils.get_full_name(step_cousin_of_new_children)
                for blood_children_of_new_father_one in blood_children_of_new_father_one_list:
                    blood_children_of_new_father_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_father_one, step_cousin_of_new_children, CommonRelationshipBitId.FAMILY_COUSIN), f'{step_cousin_of_new_children_name} was not a step cousin to {blood_children_of_new_father_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousin_of_new_children, blood_children_of_new_father_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_children_of_new_father_one_name} was not a step cousin to {step_cousin_of_new_children_name}')

            # Step Grandparent
            for step_grandparent_of_new_children in step_grandparent_of_new_children_list:
                step_grandparent_of_new_children_name = CommonSimNameUtils.get_full_name(step_grandparent_of_new_children)
                for blood_children_of_new_father_one in blood_children_of_new_father_one_list:
                    blood_children_of_new_father_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_father_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_grandparent_of_new_children, blood_children_of_new_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_children_of_new_father_one_name} was not a step grandchild to {step_grandparent_of_new_children_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_father_one, step_grandparent_of_new_children, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_grandparent_of_new_children_name} was not a step grandparent to {blood_children_of_new_father_one_name}')

            # -----------------------Step Relations With New Father-----------------------
            previous_step_children_of_new_father_list = (
                new_full_family.step_child_one,
                new_full_family.step_child_three,
            )

            step_siblings_of_new_father_list = (
                new_full_family.uncle_five,
                new_full_family.uncle_six
            )

            step_nephew_niece_of_new_father_list = (
                new_full_family.cousin_nine,
                new_full_family.cousin_ten,
                new_full_family.cousin_eleven,
                new_full_family.cousin_twelve
            )

            step_parent_of_new_father_list = (
                new_full_family.grandfather_three,
                new_full_family.grandmother_three
            )

            # Step Children
            for previous_step_children_of_new_father in previous_step_children_of_new_father_list:
                previous_step_children_of_new_father_name = CommonSimNameUtils.get_full_name(previous_step_children_of_new_father)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_step_children_of_new_father, sim_a_father, CommonRelationshipBitId.FAMILY_PARENT), f'{sim_a_father_name} was not a Step Parent to {previous_step_children_of_new_father_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_father, previous_step_children_of_new_father, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_children_of_new_father_name} was not a Step Child to {sim_a_father_name}')

            # Step Siblings
            for step_siblings_of_new_father in step_siblings_of_new_father_list:
                step_siblings_of_new_father_name = CommonSimNameUtils.get_full_name(step_siblings_of_new_father)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_new_father, sim_a_father, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{sim_a_father_name} was not a step sibling to {step_siblings_of_new_father_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_father, step_siblings_of_new_father, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{step_siblings_of_new_father_name} was not a step sibling to {sim_a_father_name}')

            # Step Nephew/Niece
            for step_nephew_niece_of_new_father in step_nephew_niece_of_new_father_list:
                step_nephew_niece_of_new_father_name = CommonSimNameUtils.get_full_name(step_nephew_niece_of_new_father)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_nephew_niece_of_new_father, sim_a_father, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{sim_a_father_name} was not a step aunt/uncle to {step_nephew_niece_of_new_father_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_father, step_nephew_niece_of_new_father, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{step_nephew_niece_of_new_father_name} was not a step niece/nephew to {sim_a_father_name}')

            # Step Parent
            for step_parent_of_new_father in step_parent_of_new_father_list:
                step_parent_of_new_father_name = CommonSimNameUtils.get_full_name(step_parent_of_new_father)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_new_father, sim_a_father, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{sim_a_father_name} was not a Step Child to {step_parent_of_new_father_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_father, step_parent_of_new_father, CommonRelationshipBitId.FAMILY_PARENT), f'{step_parent_of_new_father_name} was not a Step Parent to {sim_a_father_name}')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()
