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
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
    S4CMSetSimAAsMotherToSimBOp
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu.tests.operations.modify_sim_data.modify_relationships.operations.full_family import S4CMFullFamily


@CommonTestService.test_class(ModInfo.get_identity())
class _S4CMSetSimAAsMotherToSimBOpTests:
    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_remove_relationships_from_old_family() -> None:
        new_full_family = S4CMFullFamily()
        old_full_family = S4CMFullFamily()
        sim_a_mother = old_full_family.mother_one
        sim_b_child = new_full_family.child_one
        old_child_one = old_full_family.child_one
        old_child_two = old_full_family.child_two
        old_step_child_one = old_full_family.step_child_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_a_mother, sim_b_child), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_a_mother, sim_b_child)

            # Mother 1

            # Grandfather
            # Child of Grandfather 3
            # Step Child of Grandfather 2 and Grandfather 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was no longer a step child of Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was no longer a step child of Grandfather One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandfather Three')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was still a step grandchild to Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was still a step grandchild to Grandfather One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was still a grandchild to Grandfather Three')
            child_one_grandfather_sim_info = CommonSimGenealogyUtils.get_mothers_father_sim_info(old_child_one)
            CommonAssertionUtils.is_false(child_one_grandfather_sim_info is old_full_family.grandfather_three, 'Child One still had Grandfather Three as their biological grandfather')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was still a step grandchild to Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was still a step grandchild to Grandfather One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was still a grandchild to Grandfather Three')
            child_two_grandfather_sim_info = CommonSimGenealogyUtils.get_mothers_father_sim_info(old_child_two)
            CommonAssertionUtils.is_false(child_two_grandfather_sim_info is old_full_family.grandfather_three, 'Child Two still had Grandfather Three as their biological grandfather')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was still a step grandchild to Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was still a step grandchild to Grandfather One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was still a grandchild to Grandfather Three')
            step_child_one_grandfather_sim_info = CommonSimGenealogyUtils.get_mothers_father_sim_info(old_step_child_one)
            CommonAssertionUtils.is_false(step_child_one_grandfather_sim_info is old_full_family.grandfather_three, 'Step Child One still had Grandfather Three as their biological grandfather')

            # Grandmother
            # Child of Grandmother 3
            # Step Child of Grandmother 2 and Grandmother 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandmother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandmother Three')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was still a grandchild to Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was still a grandchild to Grandmother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was still a grandchild of Grandmother Three')
            child_one_grandmother_sim_info = CommonSimGenealogyUtils.get_mothers_mother_sim_info(old_child_one)
            CommonAssertionUtils.is_false(child_one_grandmother_sim_info is old_full_family.grandmother_three, 'Child One still had Grandmother Three as their biological grandmother')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was still a grandchild to Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was still a grandchild to Grandmother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was still a grandchild of Grandmother Three')
            child_two_grandmother_sim_info = CommonSimGenealogyUtils.get_mothers_mother_sim_info(old_child_two)
            CommonAssertionUtils.is_false(child_two_grandmother_sim_info is old_full_family.grandmother_three, 'Child Two still had Grandmother Three as their biological grandmother')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was still a grandchild to Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was still a grandchild to Grandmother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was still a grandchild of Grandmother Three')
            step_child_one_grandmother_sim_info = CommonSimGenealogyUtils.get_mothers_mother_sim_info(old_step_child_one)
            CommonAssertionUtils.is_false(step_child_one_grandmother_sim_info is old_full_family.grandmother_three, 'Step Child One still had Grandmother Three as their biological grandmother')

            # Mother 1 (old)
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Two was still a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather One was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Three was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a son to Grandfather Three')
            sim_a_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_a_mother)
            CommonAssertionUtils.is_false(sim_a_father_sim_info is old_full_family.grandfather_three, 'Sim A still had Grandfather Three as their biological father')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Two was still a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother One was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Three was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a son to Grandmother Three')
            sim_a_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_a_mother)
            CommonAssertionUtils.is_false(sim_a_mother_sim_info is old_full_family.grandmother_three, 'Sim A still had Grandmother Three as their biological mother')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_five, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Five was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_six, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Six was still a sibling to Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.father_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Father Two was still a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle One was still a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Two was still a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Three was still a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Four was still a step sibling to Sim A')

            # Parent of Child 1, Child 2, and Step Child 1
            # Step Parent of Step Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child One was no longer a child of Sim A')
            child_one_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(old_child_one)
            CommonAssertionUtils.is_true(child_one_mother_sim_info is sim_a_mother, 'Child One no longer had Sim A as their biological mother.')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child Two was no longer a child of Sim A')
            child_two_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(old_child_two)
            CommonAssertionUtils.is_true(child_two_mother_sim_info is sim_a_mother, 'Child Two no longer had Sim A as their biological mother.')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child One was no longer a child of Sim A')
            step_child_one_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(old_step_child_one)
            CommonAssertionUtils.is_true(step_child_one_mother_sim_info is sim_a_mother, 'Step Child One no longer had Sim A as their biological mother.')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child Two was no longer a child of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child One was no longer a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child Two was no longer a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child One was no longer a step child of Father One')

            # Aunt of Cousin 9, 10, 11, and 12
            # Step Aunt of Cousin 1, 2, 3, 4, 5, 6, 7, and 8
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was no longer a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was no longer a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Three was no longer a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Four was no longer a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Five was no longer a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Six was no longer a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Seven was no longer a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eight was no longer a nephew to Sim A')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Nine was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Ten was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eleven was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Twelve was still a nephew to Sim A')

            # Sibling of Uncle 5 and Uncle 6
            # Step Sibling of Uncle 1, 2, 3, and 4
            # Uncle 5
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_five, sim_a_mother, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was still a sibling of Uncle Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_five, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was still a nephew of Uncle Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_five, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was still a nephew of Uncle Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_five, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was still a nephew of Uncle Five')

            # Uncle 6
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_six, sim_a_mother, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was still a sibling to Uncle Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_six, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was still a nephew to Uncle Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_six, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was still a nephew to Uncle Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_six, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was still a nephew to Uncle Six')

            # Uncle 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was no longer a step sibling to Uncle One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was no longer a nephew to Uncle One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was no longer a nephew to Uncle One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was no longer a nephew to Uncle One')

            # Uncle 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was no longer a step sibling to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was no longer a nephew to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was no longer a nephew to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was no longer a nephew to Uncle Two')

            # Uncle 3
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was no longer a step sibling to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was no longer a nephew to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was no longer a nephew to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was no longer a nephew to Uncle Three')

            # Uncle 4
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was no longer a step sibling to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was no longer a nephew to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was no longer a nephew to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was no longer a nephew to Uncle Four')

            # Child 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was no longer a sibling of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was no longer a brother of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was no longer a sibling of Step Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was no longer a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin Nine')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin Ten')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin Eleven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin Twelve')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was no longer a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was no longer a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was no longer a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was no longer a grandparent of Child One')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was still a grandparent of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was still a grandparent of Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was no longer an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was no longer an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was no longer an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was no longer an aunt of Child One')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was still an uncle of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was still an uncle of Child One')

            # Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was no longer a sibling of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was no longer a brother of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was no longer a brother of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was no longer a sibling of Step Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was no longer a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin Nine')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin Ten')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin Eleven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin Twelve')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was no longer a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was no longer a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was no longer a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was no longer a grandparent of Child Two')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was still a grandparent of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was still a grandparent of Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was no longer an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was no longer an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was no longer an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was no longer an aunt of Child Two')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was still an uncle of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was still an uncle of Child Two')

            # Step Child 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Step Child One was no longer a sibling of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Step Child One was no longer a brother of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Step Child One was no longer a sibling of Step Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was no longer a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was still a cousin of Cousin Nine')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was still a cousin of Cousin Ten')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was still a cousin of Cousin Eleven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was still a cousin of Cousin Twelve')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was no longer a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was no longer a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was no longer a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was no longer a grandparent of Step Child One')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was still a grandparent of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was still a grandparent of Step Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was no longer an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was no longer an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was no longer an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was no longer an aunt of Step Child One')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was still an uncle of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was still an uncle of Step Child One')

            # Cousin 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin One')

            # Cousin 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin Two')

            # Cousin 3
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin Three')

            # Cousin 4
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin Four')

            # Cousin 5
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin Five')

            # Cousin 6
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin Six')

            # Cousin 7
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin Seven')

            # Cousin 8
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was no longer a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was no longer a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was no longer a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was no longer an uncle to Cousin Eight')

            # Cousin 9
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_nine, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_nine, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_nine, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_nine, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Cousin Nine')

            # Cousin 10
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_ten, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_ten, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_ten, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_ten, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Cousin Ten')

            # Cousin 11
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eleven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eleven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eleven, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eleven, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Cousin Eleven')

            # Cousin 12
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_twelve, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_twelve, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_twelve, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_twelve, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Cousin Twelve')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_add_relationships_from_new_family() -> None:
        new_full_family = S4CMFullFamily()
        old_full_family = S4CMFullFamily()
        sim_a_mother = old_full_family.mother_one
        sim_b_child = new_full_family.child_one
        old_child_one = old_full_family.child_one
        old_child_two = old_full_family.child_two
        old_step_child_one = old_full_family.step_child_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_a_mother, sim_b_child), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_a_mother, sim_b_child)

            # Mother 1

            # Grandfather
            # Child of Grandfather 3
            # Step Child of Grandfather 2 and Grandfather 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a step child of Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a step child of Grandfather One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_two, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a step child of Grandfather Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a step child of Grandfather One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandfather Three')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a step grandchild to Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a step grandchild to Grandfather One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_two, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a step grandchild to Grandfather Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a step grandchild to Grandfather One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a grandchild to Grandfather Three')
            child_one_grandfather_sim_info = CommonSimGenealogyUtils.get_mothers_father_sim_info(old_child_one)
            CommonAssertionUtils.is_true(child_one_grandfather_sim_info is new_full_family.grandfather_three, 'Child One still had Grandfather Three as their biological grandfather')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a step grandchild to Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a step grandchild to Grandfather One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_two, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a step grandchild to Grandfather Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a step grandchild to Grandfather One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a grandchild to Grandfather Three')
            child_two_grandfather_sim_info = CommonSimGenealogyUtils.get_mothers_father_sim_info(old_child_two)
            CommonAssertionUtils.is_true(child_two_grandfather_sim_info is new_full_family.grandfather_three, 'Child Two still had Grandfather Three as their biological grandfather')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_two, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a step grandchild to Grandfather Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a step grandchild to Grandfather One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_two, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a step grandchild to Grandfather Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a step grandchild to Grandfather One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a grandchild to Grandfather Three')
            step_child_one_grandfather_sim_info = CommonSimGenealogyUtils.get_mothers_father_sim_info(old_step_child_one)
            CommonAssertionUtils.is_true(step_child_one_grandfather_sim_info is new_full_family.grandfather_three, 'Step Child One still had Grandfather Three as their biological grandfather')

            # Grandmother
            # Child of Grandmother 3
            # Step Child of Grandmother 2 and Grandmother 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_two, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother Three')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a grandchild to Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a grandchild to Grandmother One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_two, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a grandchild to Grandmother Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a grandchild to Grandmother One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child One was not a grandchild of Grandmother Three')
            child_one_grandmother_sim_info = CommonSimGenealogyUtils.get_mothers_mother_sim_info(old_child_one)
            CommonAssertionUtils.is_true(child_one_grandmother_sim_info is new_full_family.grandmother_three, 'Child One still had Grandmother Three as their biological grandmother')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a grandchild to Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a grandchild to Grandmother One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_two, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a grandchild to Grandmother Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a grandchild to Grandmother One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Child Two was not a grandchild of Grandmother Three')
            child_two_grandmother_sim_info = CommonSimGenealogyUtils.get_mothers_mother_sim_info(old_child_two)
            CommonAssertionUtils.is_true(child_two_grandmother_sim_info is new_full_family.grandmother_three, 'Child Two still had Grandmother Three as their biological grandmother')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_two, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a grandchild to Grandmother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a grandchild to Grandmother One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_two, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a grandchild to Grandmother Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a grandchild to Grandmother One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, old_step_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Step Child One was not a grandchild of Grandmother Three')
            step_child_one_grandmother_sim_info = CommonSimGenealogyUtils.get_mothers_mother_sim_info(old_step_child_one)
            CommonAssertionUtils.is_true(step_child_one_grandmother_sim_info is new_full_family.grandmother_three, 'Step Child One still had Grandmother Three as their biological grandmother')

            # Mother 1 (old)
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Two was not a step parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather One was not a step parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Two new was not a step parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather One new was not a step parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Three was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a son to Grandfather Three')
            sim_a_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_a_mother)
            CommonAssertionUtils.is_true(sim_a_father_sim_info is new_full_family.grandfather_three, 'Sim A still had Grandfather Three as their biological father')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Two was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother One was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Two new was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother One new was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Three was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, sim_a_mother, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a son to Grandmother Three')
            sim_a_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_a_mother)
            CommonAssertionUtils.is_true(sim_a_mother_sim_info is new_full_family.grandmother_three, 'Sim A still had Grandmother Three as their biological mother')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.uncle_five, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Five was not a sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.uncle_six, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Six was not a sibling to Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.father_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Father Two was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle One was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Two was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Three was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Four was not a step sibling to Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.father_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Father Two new was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle One new was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Two new was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.uncle_three, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Three new was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.uncle_four, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Four new was not a step sibling to Sim A')

            # Parent of Child 1, Child 2, and Step Child 1
            # Step Parent of Step Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child One was not a child of Sim A')
            child_one_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(old_child_one)
            CommonAssertionUtils.is_true(child_one_mother_sim_info is sim_a_mother, 'Child One did not have Sim A as their biological mother.')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child Two was not a child of Sim A')
            child_two_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(old_child_two)
            CommonAssertionUtils.is_true(child_two_mother_sim_info is sim_a_mother, 'Child Two did not have Sim A as their biological mother.')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child One was not a child of Sim A')
            step_child_one_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(old_step_child_one)
            CommonAssertionUtils.is_true(step_child_one_mother_sim_info is sim_a_mother, 'Step Child One did not have Sim A as their biological mother.')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child Two was not a child of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child One was not a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child Two was not a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child One was not a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child One was not a step child of Father One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child One was not a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Child Two was not a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child One was not a child of Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_step_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Step Child One was not a step child of Father One')

            # Aunt of Cousin 9, 10, 11, and 12
            # Step Aunt of Cousin 1, 2, 3, 4, 5, 6, 7, and 8
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Three was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Four was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Five was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Six was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Seven was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eight was not a nephew to Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Three new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Four new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Five new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Six new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Seven new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eight new was not a nephew to Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Nine was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Ten was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eleven was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_mother, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Twelve was not a nephew to Sim A')

            # Sibling of Uncle 5 and Uncle 6
            # Step Sibling of Uncle 1, 2, 3, and 4
            # Uncle 5
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_five, sim_a_mother, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a sibling of Uncle Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_five, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew of Uncle Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_five, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew of Uncle Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_five, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew of Uncle Five')

            # Uncle 6
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_six, sim_a_mother, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a sibling to Uncle Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_six, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_six, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_six, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle Six')

            # Uncle 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_one, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle One new')

            # Uncle 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle Two')

            # Uncle 3
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_three, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle Three')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_three, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_three, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_three, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_three, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle Three')

            # Uncle 4
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_four, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle Four')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_four, sim_a_mother, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a step sibling to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_four, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_four, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Uncle Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_four, old_step_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child One was not a nephew to Uncle Four')

            # Child 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was not a parent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was not a sibling of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was not a brother of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was not a sibling of Step Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was not a sibling of Step Child Two new')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was not a brother of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child One was not a sibling of Step Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Nine')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Ten')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Eleven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Twelve')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was not a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was not a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was not a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was not a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was not a grandparent of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was not a grandparent of Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was not an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was not an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was not an aunt of Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was not an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was not an aunt of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was not an aunt of Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was not an uncle of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was not an uncle of Child One')

            # Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was not a parent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was not a sibling of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was not a sibling of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was not a sibling of Step Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was not a sibling of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was not a sibling of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Child Two was not a sibling of Step Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Nine')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Ten')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Eleven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Twelve')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was not a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was not a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was not a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was not a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was not a grandparent of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was not a grandparent of Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was not an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was not an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was not an aunt of Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was not an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was not an aunt of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was not an aunt of Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was not an uncle of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was not an uncle of Child Two')

            # Step Child 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, sim_a_mother, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was not a parent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Step Child One was not a sibling of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Step Child One was not a brother of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Step Child One was not a sibling of Step Child Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Step Child One was not a brother of Step Child One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Step Child One was not a sibling of Step Child Two new')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Nine')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Ten')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Eleven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Twelve')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was not a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was not a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Step Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was not a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was not a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Step Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was not a grandparent of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was not a grandparent of Step Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was not an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was not an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, old_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was not an aunt of Step Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One was not an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was not an aunt of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was not an aunt of Step Child One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was not an uncle of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_step_child_one, new_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was not an uncle of Step Child One')

            # Cousin 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_one, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_one, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_one, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_one, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin One')

            # Cousin 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_two, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_two, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_two, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_two, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Two')

            # Cousin 3
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Three')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Three')

            # Cousin 4
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Four')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Four')

            # Cousin 5
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_five, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Five')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_five, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_five, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_five, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_five, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Five')

            # Cousin 6
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_six, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Six')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_six, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_six, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_six, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_six, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Six')

            # Cousin 7
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_seven, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Seven')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_seven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_seven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_seven, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_seven, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Seven')

            # Cousin 8
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eight, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Eight')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eight, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eight, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eight, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eight, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Eight')

            # Cousin 9
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_nine, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_nine, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_nine, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_nine, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Nine')

            # Cousin 10
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_ten, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_ten, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_ten, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_ten, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Ten')

            # Cousin 11
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eleven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eleven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eleven, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eleven, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Eleven')

            # Cousin 12
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_twelve, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_twelve, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_twelve, old_step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_twelve, sim_a_mother, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Twelve')
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
