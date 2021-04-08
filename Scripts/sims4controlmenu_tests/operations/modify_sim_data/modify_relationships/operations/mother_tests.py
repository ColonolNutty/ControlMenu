"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4controlmenu.commonlib.utils.common_sim_genealogy_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
    S4CMSetSimAAsMotherToSimBOp
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu_tests.operations.modify_sim_data.modify_relationships.operations.full_family import S4CMFullFamily


@CommonTestService.test_class(ModInfo.get_identity())
class _S4CMSetSimAAsMotherToSimBOpTests:
    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_remove_relationships_of_previous_mother_from_previous_family() -> None:
        new_full_family = S4CMFullFamily()
        old_full_family = S4CMFullFamily(suffix='2')
        sim_a_mother = old_full_family.mother_one
        sim_b_child = new_full_family.child_one
        previous_mother_one = new_full_family.mother_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_a_mother, sim_b_child), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_a_mother, sim_b_child)

            # -----------------------Previous Mother Blood Relations With Previous Children-----------------------

            blood_children_of_previous_mother_one_list = (
                new_full_family.child_one,
                new_full_family.child_two
            )

            blood_grandchildren_of_previous_mother_one_list = (
                new_full_family.grand_child_one,
                new_full_family.grand_child_two
            )

            blood_siblings_of_previous_mother_one_list = (
                new_full_family.step_child_one,
            )

            blood_uncle_aunt_of_previous_mother_one_list = (
                new_full_family.uncle_five,
                new_full_family.uncle_six
            )

            blood_cousin_of_previous_mother_one_list = (
                new_full_family.cousin_nine,
                new_full_family.cousin_ten,
                new_full_family.cousin_eleven,
                new_full_family.cousin_twelve
            )

            previous_mother_name = CommonSimNameUtils.get_full_name(previous_mother_one)
            # Previous Mother One is no longer mother of father of new grandchildren.
            for blood_grandchildren_of_previous_mother_one in blood_grandchildren_of_previous_mother_one_list:
                blood_grandchildren_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_grandchildren_of_previous_mother_one)
                # Mother
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandchildren_of_previous_mother_one, previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_grandchildren_of_previous_mother_one_name} was still a grandchild to {previous_mother_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_mother_one, blood_grandchildren_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{previous_mother_name} was still a grandparent to {blood_grandchildren_of_previous_mother_one_name}')
                blood_grandmother_grandchildren_of_previous_mother_one = CommonSimGenealogyUtils.get_fathers_mother_sim_info(blood_grandchildren_of_previous_mother_one)
                CommonAssertionUtils.is_false(blood_grandmother_grandchildren_of_previous_mother_one is previous_mother_one)

            # Previous Mother One is no longer mother of new children.
            for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                # Mother
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, previous_mother_one, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_child_of_previous_mother_one_name} was still a child to {previous_mother_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_mother_name} was still a parent to {blood_child_of_previous_mother_one_name}')
                blood_mother_of_blood_child_of_previous_mother_one = CommonSimGenealogyUtils.get_mother_sim_info(blood_child_of_previous_mother_one)
                CommonAssertionUtils.is_false(blood_mother_of_blood_child_of_previous_mother_one is previous_mother_one)

            # Previous Half Siblings of Previous Mother should no longer be Half Siblings with new children.
            for blood_siblings_of_previous_mother_one in blood_siblings_of_previous_mother_one_list:
                blood_siblings_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_siblings_of_previous_mother_one)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, blood_siblings_of_previous_mother_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_child_of_previous_mother_one_name} was still a sibling to {blood_siblings_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_siblings_of_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_siblings_of_previous_mother_one_name} was still a sibling to {blood_child_of_previous_mother_one_name}')

            # Previous Uncle/Aunt no longer Uncle/Aunt of new children.
            for blood_uncle_aunt_of_previous_mother_one in blood_uncle_aunt_of_previous_mother_one_list:
                blood_uncle_aunt_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_uncle_aunt_of_previous_mother_one)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, blood_uncle_aunt_of_previous_mother_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{blood_child_of_previous_mother_one_name} was still a niece/nephew to {blood_uncle_aunt_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_uncle_aunt_of_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_uncle_aunt_of_previous_mother_one_name} was still an aunt/uncle to {blood_child_of_previous_mother_one_name}')

            # Previous Cousin no longer Cousin of new children.
            for blood_cousin_of_previous_mother_one in blood_cousin_of_previous_mother_one_list:
                blood_cousin_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_cousin_of_previous_mother_one)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, blood_cousin_of_previous_mother_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_mother_one_name} was still a cousin to {blood_cousin_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_cousin_of_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_cousin_of_previous_mother_one_name} was still a cousin to {blood_child_of_previous_mother_one_name}')

            # Parents of previous mother one children should no longer be the grandparents of new children.
            blood_grandfather_previous_mother_one = new_full_family.grandfather_three
            blood_grandmother_previous_mother_one = new_full_family.grandmother_three
            blood_grandfather_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_grandfather_previous_mother_one)
            blood_grandmother_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_grandmother_previous_mother_one)
            for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                # Grandfather
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, blood_grandfather_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_mother_one_name} was still a grandchild to {blood_grandfather_previous_mother_one_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandfather_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_grandfather_previous_mother_one_name} was still a grandparent to {blood_child_of_previous_mother_one_name}')
                blood_grandfather_of_blood_child_of_previous_mother_one = CommonSimGenealogyUtils.get_mothers_father_sim_info(blood_child_of_previous_mother_one)
                CommonAssertionUtils.is_false(blood_grandfather_of_blood_child_of_previous_mother_one is blood_grandfather_previous_mother_one, f'{blood_grandfather_previous_mother_one_name} was still the biological grandfather of {blood_child_of_previous_mother_one_name}')

                # Grandmother
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, blood_grandmother_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_mother_one_name} was not a grandchild to {blood_grandmother_previous_mother_one_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandmother_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_grandmother_previous_mother_one_name} was not a grandparent to {blood_child_of_previous_mother_one_name}')
                blood_grandmother_of_blood_child_of_previous_mother_one = CommonSimGenealogyUtils.get_mothers_mother_sim_info(blood_child_of_previous_mother_one)
                CommonAssertionUtils.is_false(blood_grandmother_of_blood_child_of_previous_mother_one is blood_grandmother_previous_mother_one, f'{blood_grandmother_previous_mother_one_name} was still the biological grandmother of {blood_child_of_previous_mother_one_name}')

            # -----------------------Previous Mother Step Relations With Previous Children-----------------------

            step_parent_of_previous_mother_one_list = (
                new_full_family.father_two,
            )

            step_uncle_aunt_of_previous_mother_list = (
                new_full_family.aunt_one,
                new_full_family.aunt_two,
                new_full_family.uncle_three,
                new_full_family.uncle_four
            )

            step_grandparent_of_previous_mother_one_list = (
                new_full_family.grandfather_five,
                new_full_family.grandmother_five
            )

            step_cousin_of_previous_mother_one_list = (
                new_full_family.cousin_five,
                new_full_family.cousin_six,
                new_full_family.cousin_seven,
                new_full_family.cousin_eight,
                new_full_family.cousin_seventeen,
                new_full_family.cousin_eighteen
            )

            # Previous Step Parent no longer Parent of new children.
            for step_parent_of_previous_mother_one in step_parent_of_previous_mother_one_list:
                step_parent_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_mother_one)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_parent_of_previous_mother_one, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_child_of_previous_mother_one_name} was still a step child to {step_parent_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{step_parent_of_previous_mother_one_name} was still a step parent to {blood_child_of_previous_mother_one_name}')

            # Previous Step Uncle/Aunt no longer Step Uncle/Aunt of new children.
            for step_uncle_aunt_of_previous_mother in step_uncle_aunt_of_previous_mother_list:
                step_uncle_aunt_of_previous_mother_name = CommonSimNameUtils.get_full_name(step_uncle_aunt_of_previous_mother)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_uncle_aunt_of_previous_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{blood_child_of_previous_mother_one_name} was still a step niece/nephew to {step_uncle_aunt_of_previous_mother_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_uncle_aunt_of_previous_mother, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{step_uncle_aunt_of_previous_mother_name} was still a step aunt/uncle to {blood_child_of_previous_mother_one_name}')

            # Previous Step Grandparents no longer Step Grandparents of new children.
            for step_grandparent_of_previous_mother_one in step_grandparent_of_previous_mother_one_list:
                step_grandparent_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_grandparent_of_previous_mother_one)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_grandparent_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_mother_one_name} was still a step grandchild to {step_grandparent_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_grandparent_of_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{step_grandparent_of_previous_mother_one_name} was still a step grandparent to {blood_child_of_previous_mother_one_name}')

            # Previous Step Cousin no longer Step Cousin of new children.
            for step_cousin_of_previous_mother_one in step_cousin_of_previous_mother_one_list:
                step_cousin_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_cousin_of_previous_mother_one)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_cousin_of_previous_mother_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_mother_one_name} was still a step cousin to {step_cousin_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousin_of_previous_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{step_cousin_of_previous_mother_one_name} was still a step cousin to {blood_child_of_previous_mother_one_name}')

            # -----------------------Previous Father One Step Relations With Mother One Family-----------------------

            step_parent_of_previous_father_one_list = (
                new_full_family.grandfather_one,
                new_full_family.grandmother_one
            )

            step_children_of_previous_father_one_list = (
                new_full_family.step_child_two,
                new_full_family.step_child_three,
            )

            step_siblings_of_previous_father_one_list = (
                new_full_family.father_one,
                new_full_family.uncle_one,
                new_full_family.uncle_two,
                new_full_family.aunt_three,
                new_full_family.aunt_four
            )

            step_cousins_of_previous_father_one_list = (
                new_full_family.cousin_one,
                new_full_family.cousin_two,
                new_full_family.cousin_three,
                new_full_family.cousin_four
            )

            blood_parents_of_previous_mother_one_list = (
                new_full_family.grandfather_three,
                new_full_family.grandmother_three
            )

            step_children_of_previous_mother_one_list = (
                new_full_family.step_child_one,
            )

            blood_uncle_aunt_of_previous_mother_one_list = (
                new_full_family.mother_one,
                new_full_family.uncle_five,
                new_full_family.uncle_six
            )

            blood_cousin_of_previous_mother_one_list = (
                new_full_family.cousin_nine,
                new_full_family.cousin_ten,
                new_full_family.cousin_eleven,
                new_full_family.cousin_twelve
            )

            # Previous Father One no longer step parent of Step Child One new.
            previous_father_one_name = CommonSimNameUtils.get_full_name(new_full_family.father_one)
            previous_step_child_one_name = CommonSimNameUtils.get_full_name(new_full_family.step_child_one)
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_child_one_name} was still a step child to {previous_father_one_name}')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_one, new_full_family.father_one, CommonRelationshipBitId.FAMILY_PARENT), f'{previous_father_one_name} was still a step parent to {previous_step_child_one_name}')

            # Previous Mother One no longer step parent of Step Child Two new.
            previous_step_child_two_name = CommonSimNameUtils.get_full_name(new_full_family.step_child_two)
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_mother_one, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_child_two_name} was still a step child to {previous_mother_name}')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, previous_mother_one, CommonRelationshipBitId.FAMILY_PARENT), f'{previous_mother_name} was still a step parent to {previous_step_child_two_name}')

            # Previous Mother One no longer step parent of Step Child Three new.
            previous_step_child_three_name = CommonSimNameUtils.get_full_name(new_full_family.step_child_three)
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_mother_one, new_full_family.step_child_three, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_child_three_name} was still a step child to {previous_mother_name}')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_three, previous_mother_one, CommonRelationshipBitId.FAMILY_PARENT), f'{previous_mother_name} was still a step parent to {previous_step_child_three_name}')

            # Previous Father One siblings no longer step siblings of Mother One.
            for step_siblings_of_previous_father_one in step_siblings_of_previous_father_one_list:
                step_siblings_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_father_one)
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_father_one, previous_mother_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{previous_mother_name} was still a step sibling to {step_siblings_of_previous_father_one_name}')
                CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_mother_one, step_siblings_of_previous_father_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{step_siblings_of_previous_father_one_name} was still a step sibling to {previous_mother_name}')

            # Previous Father One siblings no longer step Aunt/Uncle of Mother One cousins.
            for step_siblings_of_previous_father_one in step_siblings_of_previous_father_one_list:
                step_siblings_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_father_one)
                for blood_cousin_of_previous_mother_one in blood_cousin_of_previous_mother_one_list:
                    blood_cousin_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_cousin_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_cousin_of_previous_mother_one, step_siblings_of_previous_father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_siblings_of_previous_father_one_name} was still a step aunt/uncle to {blood_cousin_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_father_one, blood_cousin_of_previous_mother_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_cousin_of_previous_mother_one_name} was still a step niece/nephew to {step_siblings_of_previous_father_one_name}')

            # Previous Father One siblings no longer step Aunt/Uncle of Mother One step children.
            for step_siblings_of_previous_father_one in step_siblings_of_previous_father_one_list:
                step_siblings_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_father_one)
                for step_children_of_previous_mother_one in step_children_of_previous_mother_one_list:
                    step_children_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_children_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_children_of_previous_mother_one, step_siblings_of_previous_father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_siblings_of_previous_father_one_name} was still a step aunt/uncle to {step_children_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_father_one, step_children_of_previous_mother_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{step_children_of_previous_mother_one_name} was still a step niece/nephew to {step_siblings_of_previous_father_one_name}')

            # Previous Father One siblings no longer step Children of Mother One parents.
            for blood_parents_of_previous_mother_one in blood_parents_of_previous_mother_one_list:
                blood_parents_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_parents_of_previous_mother_one)
                for step_siblings_of_previous_father_one in step_siblings_of_previous_father_one_list:
                    step_siblings_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_siblings_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_previous_father_one, blood_parents_of_previous_mother_one, CommonRelationshipBitId.FAMILY_PARENT), f'{step_siblings_of_previous_father_one_name} was still a step child to {blood_parents_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_parents_of_previous_mother_one, step_siblings_of_previous_father_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{blood_parents_of_previous_mother_one_name} was still a step parent to {step_siblings_of_previous_father_one_name}')

            # Previous Father One parents no longer step parents of Mother One siblings.
            for step_parent_of_previous_father_one in step_parent_of_previous_father_one_list:
                step_parent_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_father_one)
                for blood_uncle_aunt_of_previous_mother_one in blood_uncle_aunt_of_previous_mother_one_list:
                    blood_uncle_aunt_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_uncle_aunt_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_uncle_aunt_of_previous_mother_one, step_parent_of_previous_father_one, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_uncle_aunt_of_previous_mother_one_name} was still a step child to {step_parent_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_father_one, blood_uncle_aunt_of_previous_mother_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{step_parent_of_previous_father_one_name} was still a step parent to {blood_uncle_aunt_of_previous_mother_one_name}')

            # Previous Father One parents no longer step grandparents of Mother One Cousins.
            for step_parent_of_previous_father_one in step_parent_of_previous_father_one_list:
                step_parent_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_father_one)
                for blood_cousin_of_previous_mother_one in blood_cousin_of_previous_mother_one_list:
                    blood_cousin_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_cousin_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_cousin_of_previous_mother_one, step_parent_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_cousin_of_previous_mother_one_name} was still a step grandchild to {step_parent_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_father_one, blood_cousin_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{step_parent_of_previous_father_one_name} was still a step grandparent to {blood_cousin_of_previous_mother_one_name}')

            # Previous Mother One parents no longer step grandparents of Father One Cousins.
            for blood_parents_of_previous_mother_one in blood_parents_of_previous_mother_one_list:
                blood_parents_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_parents_of_previous_mother_one)
                for step_cousins_of_previous_father_one in step_cousins_of_previous_father_one_list:
                    step_cousins_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_cousins_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousins_of_previous_father_one, blood_parents_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_cousins_of_previous_father_one_name} was still a step grandchild to {blood_parents_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_parents_of_previous_mother_one, step_cousins_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_parents_of_previous_mother_one_name} was still a step grandparent to {step_cousins_of_previous_father_one_name}')

            # Previous Mother One parents no longer step grandparents of Father One Step Children.
            for blood_parents_of_previous_mother_one in blood_parents_of_previous_mother_one_list:
                blood_parents_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_parents_of_previous_mother_one)
                for step_children_of_previous_father_one in step_children_of_previous_father_one_list:
                    step_children_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_children_of_previous_father_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_children_of_previous_father_one, blood_parents_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_children_of_previous_father_one_name} was still a step grandchild to {blood_parents_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_parents_of_previous_mother_one, step_children_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_parents_of_previous_mother_one_name} was still a step grandparent to {step_children_of_previous_father_one_name}')

            # Previous Father One parents no longer step grandparents of Mother One Step Children.
            for step_parent_of_previous_father_one in step_parent_of_previous_father_one_list:
                step_parent_of_previous_father_one_name = CommonSimNameUtils.get_full_name(step_parent_of_previous_father_one)
                for step_children_of_previous_mother_one in step_children_of_previous_mother_one_list:
                    step_children_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(step_children_of_previous_mother_one)
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_children_of_previous_mother_one, step_parent_of_previous_father_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_children_of_previous_mother_one_name} was still a step grandchild to {step_parent_of_previous_father_one_name}')
                    CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_previous_father_one, step_children_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{step_parent_of_previous_father_one_name} was still a step grandparent to {step_children_of_previous_mother_one_name}')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_add_relationships_from_new_family() -> None:
        new_full_family = S4CMFullFamily()
        old_full_family = S4CMFullFamily(suffix='2')
        sim_a_mother = old_full_family.mother_one
        sim_b_child = new_full_family.child_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_a_mother, sim_b_child), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_a_mother, sim_b_child)

            # -----------------------Blood Relations With New Children-----------------------

            # Blood children on mothers side of family.
            blood_children_of_new_mother_one_list = (
                old_full_family.child_one,
                old_full_family.child_two
            )

            blood_children_of_previous_mother_one_list = (
                new_full_family.child_one,
                new_full_family.child_two
            )

            blood_grandchildren_of_previous_mother_one_list = (
                new_full_family.grand_child_one,
                new_full_family.grand_child_two
            )

            blood_step_child_mother_one_side_list = (
                old_full_family.step_child_one,
            )

            uncle_aunt_on_mother_one_side_list = (
                old_full_family.uncle_five,
                old_full_family.uncle_six,
                old_full_family.aunt_one,
                old_full_family.aunt_two
            )

            cousins_on_mother_one_side_list = (
                old_full_family.cousin_five,
                old_full_family.cousin_six,
                old_full_family.cousin_seven,
                old_full_family.cousin_eight,
                old_full_family.cousin_nine,
                old_full_family.cousin_ten,
                old_full_family.cousin_eleven,
                old_full_family.cousin_twelve
            )

            sim_a_mother_name = CommonSimNameUtils.get_full_name(sim_a_mother)
            # New Mother One is mother of father of new grandchildren.
            for blood_grandchildren_of_previous_mother_one in blood_grandchildren_of_previous_mother_one_list:
                blood_grandchildren_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_grandchildren_of_previous_mother_one)
                # Grandmother
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_grandchildren_of_previous_mother_one, sim_a_mother, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_grandchildren_of_previous_mother_one_name} was not a grandchild to {sim_a_mother_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, blood_grandchildren_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{sim_a_mother_name} was not a grandparent to {blood_grandchildren_of_previous_mother_one_name}')
                blood_grandmother_grandchildren_of_previous_mother_one = CommonSimGenealogyUtils.get_fathers_mother_sim_info(blood_grandchildren_of_previous_mother_one)
                CommonAssertionUtils.is_true(blood_grandmother_grandchildren_of_previous_mother_one is sim_a_mother, f'{sim_a_mother_name} was not the biological grandparent of {blood_grandchildren_of_previous_mother_one_name}')

            # New Mother One is mother of new children.
            for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                # Mother
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), f'{blood_child_of_previous_mother_one_name} was not a child to {sim_a_mother_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{sim_a_mother_name} was not a parent to {blood_child_of_previous_mother_one_name}')
                blood_mother_of_blood_child_of_previous_mother_one = CommonSimGenealogyUtils.get_mother_sim_info(blood_child_of_previous_mother_one)
                CommonAssertionUtils.is_true(blood_mother_of_blood_child_of_previous_mother_one is sim_a_mother, f'{sim_a_mother_name} was not the biological parent of {blood_child_of_previous_mother_one_name}')

            # Uncles/Aunts of new mother should be Uncles/Aunts of previous children.
            for uncle_aunt_on_mother_one_side in uncle_aunt_on_mother_one_side_list:
                uncle_or_aunt_name = CommonSimNameUtils.get_full_name(uncle_aunt_on_mother_one_side)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, uncle_aunt_on_mother_one_side, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{uncle_or_aunt_name} was not a uncle/aunt to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(uncle_aunt_on_mother_one_side, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_child_of_previous_mother_one_name} was not a nephew/niece to {uncle_or_aunt_name}')

            # Blood Children of new mother one should be brother/sister of new children because they share the same mother.
            for blood_children_of_new_mother_one in blood_children_of_new_mother_one_list:
                blood_children_of_new_mother_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_mother_one)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, blood_children_of_new_mother_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_children_of_new_mother_one_name} was not a sibling to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_mother_one, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_child_of_previous_mother_one_name} was not a sibling to {blood_children_of_new_mother_one_name}')

            # Blood Children of different father should be brother/sister of new children because they share the same mother.
            for blood_step_child_mother_one_side in blood_step_child_mother_one_side_list:
                blood_step_child_mother_one_side_name = CommonSimNameUtils.get_full_name(blood_step_child_mother_one_side)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, blood_step_child_mother_one_side, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_step_child_mother_one_side_name} was not a sibling to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_step_child_mother_one_side, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), f'{blood_child_of_previous_mother_one_name} was not a sibling to {blood_step_child_mother_one_side_name}')

            # Cousins of new mother one children should become cousins of new children.
            for cousin_on_mother_one_side in cousins_on_mother_one_side_list:
                cousin_on_mother_one_side_name = CommonSimNameUtils.get_full_name(cousin_on_mother_one_side)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, cousin_on_mother_one_side, CommonRelationshipBitId.FAMILY_COUSIN), f'{cousin_on_mother_one_side_name} was not a cousin to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(cousin_on_mother_one_side, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_mother_one_name} was not a cousin to {cousin_on_mother_one_side_name}')

            # Parents of new mother one children should become grandparents of new children.
            grandfather_on_mother_one_side = old_full_family.grandfather_three
            grandmother_on_mother_one_side = old_full_family.grandmother_three
            grandfather_on_mother_one_side_name = CommonSimNameUtils.get_full_name(grandfather_on_mother_one_side)
            grandmother_on_mother_one_side_name = CommonSimNameUtils.get_full_name(grandmother_on_mother_one_side)
            for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                # Grandfather
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, grandfather_on_mother_one_side, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_mother_one_name} was not a grandchild to {grandfather_on_mother_one_side_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(grandfather_on_mother_one_side, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{grandfather_on_mother_one_side_name} was not a grandparent to {blood_child_of_previous_mother_one_name}')
                blood_grandfather_of_blood_child_of_previous_mother_one = CommonSimGenealogyUtils.get_mothers_father_sim_info(blood_child_of_previous_mother_one)
                CommonAssertionUtils.is_true(blood_grandfather_of_blood_child_of_previous_mother_one is grandfather_on_mother_one_side, f'{grandfather_on_mother_one_side_name} was not the biological grandfather of {blood_child_of_previous_mother_one_name}')

                # Grandmother
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, grandmother_on_mother_one_side, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{blood_child_of_previous_mother_one_name} was not a grandchild to {grandmother_on_mother_one_side_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(grandmother_on_mother_one_side, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{grandmother_on_mother_one_side_name} was not a grandparent to {blood_child_of_previous_mother_one_name}')
                blood_grandmother_of_blood_child_of_previous_mother_one = CommonSimGenealogyUtils.get_mothers_mother_sim_info(blood_child_of_previous_mother_one)
                CommonAssertionUtils.is_true(blood_grandmother_of_blood_child_of_previous_mother_one is grandmother_on_mother_one_side, f'{grandmother_on_mother_one_side_name} was not the biological grandmother of {blood_child_of_previous_mother_one_name}')

            # -----------------------Step Relations With New Children-----------------------

            step_parent_of_new_children_list = (
                old_full_family.father_one,
                old_full_family.father_two,
            )

            step_uncle_aunt_of_new_children_list = (
                old_full_family.uncle_one,
                old_full_family.uncle_two,
                old_full_family.uncle_three,
                old_full_family.uncle_four
            )

            step_cousin_of_new_children_list = (
                old_full_family.cousin_one,
                old_full_family.cousin_two,
                old_full_family.cousin_three,
                old_full_family.cousin_four
            )

            step_grandparent_of_new_children_list = (
                old_full_family.grandfather_one,
                old_full_family.grandmother_one,
                old_full_family.grandfather_two,
                old_full_family.grandmother_two,
                old_full_family.grandfather_five,
                old_full_family.grandmother_five
            )

            # Step Parents
            for step_parent_of_new_children in step_parent_of_new_children_list:
                step_parent_of_new_children_name = CommonSimNameUtils.get_full_name(step_parent_of_new_children)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_parent_of_new_children, CommonRelationshipBitId.FAMILY_PARENT), f'{step_parent_of_new_children_name} was not a step parent to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_new_children, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{blood_child_of_previous_mother_one_name} was not a step child to {step_parent_of_new_children_name}')

            # Step Uncle
            for step_uncle_aunt_of_new_children in step_uncle_aunt_of_new_children_list:
                step_uncle_aunt_of_new_children_name = CommonSimNameUtils.get_full_name(step_uncle_aunt_of_new_children)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_uncle_aunt_of_new_children, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_uncle_aunt_of_new_children_name} was not a step aunt/uncle to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_uncle_aunt_of_new_children, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_child_of_previous_mother_one_name} was not a step niece/nephew to {step_uncle_aunt_of_new_children_name}')

            # Step Cousin
            for step_cousin_of_new_children in step_cousin_of_new_children_list:
                step_cousin_of_new_children_name = CommonSimNameUtils.get_full_name(step_cousin_of_new_children)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_cousin_of_new_children, CommonRelationshipBitId.FAMILY_COUSIN), f'{step_cousin_of_new_children_name} was not a step cousin to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousin_of_new_children, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_child_of_previous_mother_one_name} was not a step cousin to {step_cousin_of_new_children_name}')

            # Step Grandparent
            for step_grandparent_of_new_children in step_grandparent_of_new_children_list:
                step_grandparent_of_new_children_name = CommonSimNameUtils.get_full_name(step_grandparent_of_new_children)
                for blood_child_of_previous_mother_one in blood_children_of_previous_mother_one_list:
                    blood_child_of_previous_mother_one_name = CommonSimNameUtils.get_full_name(blood_child_of_previous_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_child_of_previous_mother_one, step_grandparent_of_new_children, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_grandparent_of_new_children_name} was not a step grandparent to {blood_child_of_previous_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_grandparent_of_new_children, blood_child_of_previous_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_child_of_previous_mother_one_name} was not a step grandchild to {step_grandparent_of_new_children_name}')

            # -----------------------Step Relations With Old Children-----------------------

            blood_children_of_new_mother_one_list = (
                old_full_family.child_one,
                old_full_family.child_two,
                old_full_family.step_child_one
            )

            step_parent_of_new_children_list = (
                new_full_family.father_one,
            )

            step_uncle_aunt_of_new_children_list = (
                new_full_family.uncle_one,
                new_full_family.uncle_two
            )

            step_cousin_of_new_children_list = (
                new_full_family.cousin_one,
                new_full_family.cousin_two,
                new_full_family.cousin_three,
                new_full_family.cousin_four
            )

            step_grandparent_of_new_children_list = (
                new_full_family.grandfather_one,
                new_full_family.grandmother_one
            )

            # Step Parents
            for step_parent_of_new_children in step_parent_of_new_children_list:
                step_parent_of_new_children_name = CommonSimNameUtils.get_full_name(step_parent_of_new_children)
                for blood_children_of_new_mother_one in blood_children_of_new_mother_one_list:
                    blood_children_of_new_mother_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_mother_one, step_parent_of_new_children, CommonRelationshipBitId.FAMILY_PARENT), f'{step_parent_of_new_children_name} was not a step parent to {blood_children_of_new_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_new_children, blood_children_of_new_mother_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{blood_children_of_new_mother_one_name} was not a step child to {step_parent_of_new_children_name}')

            # Step Uncle
            for step_uncle_aunt_of_new_children in step_uncle_aunt_of_new_children_list:
                step_uncle_aunt_of_new_children_name = CommonSimNameUtils.get_full_name(step_uncle_aunt_of_new_children)
                for blood_children_of_new_mother_one in blood_children_of_new_mother_one_list:
                    blood_children_of_new_mother_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_mother_one, step_uncle_aunt_of_new_children, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{step_uncle_aunt_of_new_children_name} was not a step aunt/uncle to {blood_children_of_new_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_uncle_aunt_of_new_children, blood_children_of_new_mother_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{blood_children_of_new_mother_one_name} was not a step niece/nephew to {step_uncle_aunt_of_new_children_name}')

            # Step Cousin
            for step_cousin_of_new_children in step_cousin_of_new_children_list:
                step_cousin_of_new_children_name = CommonSimNameUtils.get_full_name(step_cousin_of_new_children)
                for blood_children_of_new_mother_one in blood_children_of_new_mother_one_list:
                    blood_children_of_new_mother_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_mother_one, step_cousin_of_new_children, CommonRelationshipBitId.FAMILY_COUSIN), f'{step_cousin_of_new_children_name} was not a step cousin to {blood_children_of_new_mother_one_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_cousin_of_new_children, blood_children_of_new_mother_one, CommonRelationshipBitId.FAMILY_COUSIN), f'{blood_children_of_new_mother_one_name} was not a step cousin to {step_cousin_of_new_children_name}')

            # Step Grandparent
            for step_grandparent_of_new_children in step_grandparent_of_new_children_list:
                step_grandparent_of_new_children_name = CommonSimNameUtils.get_full_name(step_grandparent_of_new_children)
                for blood_children_of_new_mother_one in blood_children_of_new_mother_one_list:
                    blood_children_of_new_mother_one_name = CommonSimNameUtils.get_full_name(blood_children_of_new_mother_one)
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_grandparent_of_new_children, blood_children_of_new_mother_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), f'{blood_children_of_new_mother_one_name} was not a step grandchild to {step_grandparent_of_new_children_name}')
                    CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(blood_children_of_new_mother_one, step_grandparent_of_new_children, CommonRelationshipBitId.FAMILY_GRANDPARENT), f'{step_grandparent_of_new_children_name} was not a step grandparent to {blood_children_of_new_mother_one_name}')

            # -----------------------Step Relations With New Mother-----------------------
            previous_step_children_of_new_mother_list = (
                new_full_family.step_child_two,
                new_full_family.step_child_three,
            )

            step_siblings_of_new_mother_list = (
                new_full_family.uncle_one,
                new_full_family.uncle_two
            )

            step_nephew_niece_of_new_mother_list = (
                new_full_family.cousin_one,
                new_full_family.cousin_two,
                new_full_family.cousin_three,
                new_full_family.cousin_four
            )

            step_parent_of_new_mother_list = (
                new_full_family.grandfather_one,
                new_full_family.grandmother_one
            )

            # Step Children
            for previous_step_children_of_new_mother in previous_step_children_of_new_mother_list:
                previous_step_children_of_new_mother_name = CommonSimNameUtils.get_full_name(previous_step_children_of_new_mother)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(previous_step_children_of_new_mother, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), f'{sim_a_mother_name} was not a step parent to {previous_step_children_of_new_mother_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, previous_step_children_of_new_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{previous_step_children_of_new_mother_name} was not a step child to {sim_a_mother_name}')

            # Step Siblings
            for step_siblings_of_new_mother in step_siblings_of_new_mother_list:
                step_siblings_of_new_mother_name = CommonSimNameUtils.get_full_name(step_siblings_of_new_mother)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_siblings_of_new_mother, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{sim_a_mother_name} was not a step sibling to {step_siblings_of_new_mother_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, step_siblings_of_new_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), f'{step_siblings_of_new_mother_name} was not a step sibling to {sim_a_mother_name}')

            # Step Nephew/Niece
            for step_nephew_niece_of_new_mother in step_nephew_niece_of_new_mother_list:
                step_nephew_niece_of_new_mother_name = CommonSimNameUtils.get_full_name(step_nephew_niece_of_new_mother)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_nephew_niece_of_new_mother, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), f'{sim_a_mother_name} was not a step aunt/uncle to {step_nephew_niece_of_new_mother_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, step_nephew_niece_of_new_mother, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), f'{step_nephew_niece_of_new_mother_name} was not a step niece/nephew to {sim_a_mother_name}')

            # Step Parent
            for step_parent_of_new_mother in step_parent_of_new_mother_list:
                step_parent_of_new_mother_name = CommonSimNameUtils.get_full_name(step_parent_of_new_mother)
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(step_parent_of_new_mother, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), f'{sim_a_mother_name} was not a step child to {step_parent_of_new_mother_name}')
                CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, step_parent_of_new_mother, CommonRelationshipBitId.FAMILY_PARENT), f'{step_parent_of_new_mother_name} was not a step parent to {sim_a_mother_name}')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()

    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_mother_of_sim_b() -> None:
        # Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim B and Sim B as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_b), 'Failed to set Sim A as biological mother of Sim B')

            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should have been the mother of Sim B but was not.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_not_mother_of_sim_b() -> None:
        # Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_false(S4CMSetSimAAsMotherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should not have been the mother of Sim B but was.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_only_rel_bit_mother_of_sim_b() -> None:
        # Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as parent of Sim B and Sim B as child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim A')

            CommonAssertionUtils.is_false(S4CMSetSimAAsMotherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should not have been the mother of Sim B with only the relationship bit but was.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _has_relation_sim_a_is_only_family_tree_mother_of_sim_b() -> None:
        # Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim B and Sim B as biological child of Sim A
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_b), 'Failed to set Sim A as biological mother of Sim B')

            CommonAssertionUtils.is_false(S4CMSetSimAAsMotherToSimBOp().has_relation(sim_info_a, sim_info_b), 'Failed, Sim A should not have been the mother of Sim B with only the family tree but was.')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
