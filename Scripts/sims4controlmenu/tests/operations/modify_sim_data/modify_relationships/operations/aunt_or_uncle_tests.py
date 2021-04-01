"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.aunt_or_uncle import \
    S4CMSetSimAAsAuntOrUncleToSimBOp
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu.tests.operations.modify_sim_data.modify_relationships.operations.full_family import S4CMFullFamily


@CommonTestService.test_class(ModInfo.get_identity())
class _S4CMSetSimAAsAuntOrUncleToSimBOpTests:
    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_uncle_to_sim_b_should_remove_relationships_from_old_family() -> None:
        new_full_family = S4CMFullFamily()
        old_full_family = S4CMFullFamily()
        sim_a_uncle = old_full_family.uncle_one
        sim_b_child = new_full_family.child_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_a_uncle, sim_b_child), 'Failed to update family tree')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_a_uncle, sim_b_child)

            # Grandfather
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandfather One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Grandfather One was still a grandparent to Cousin One')
            cousin_one_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(old_full_family.cousin_one)
            CommonAssertionUtils.is_false(cousin_one_grandfather_sim_info is old_full_family.grandfather_one, 'Cousin One still had Grandfather One as their biological grandfather')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Grandfather One was still a grandparent to Cousin Two')
            cousin_two_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(old_full_family.cousin_two)
            CommonAssertionUtils.is_false(cousin_two_grandfather_sim_info is old_full_family.grandfather_one, 'Cousin Two still had Grandfather One as their biological grandfather')

            # Grandmother
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandmother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was still a grandchild of Grandmother One')
            cousin_one_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(old_full_family.cousin_one)
            CommonAssertionUtils.is_false(cousin_one_grandmother_sim_info is old_full_family.grandmother_one, 'Cousin One still had Grandmother One as their biological grandmother')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was still a grandchild of Grandmother One')
            cousin_two_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(old_full_family.cousin_two)
            CommonAssertionUtils.is_false(cousin_two_grandmother_sim_info is old_full_family.grandmother_one, 'Cousin Two still had Grandmother One as their biological grandmother')

            # Uncle 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather One was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a son to Grandfather One')
            sim_a_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_false(sim_a_father_sim_info is old_full_family.grandfather_one, 'Sim A still had Grandfather One as their biological father')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother One was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a son to Grandmother One')
            sim_a_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_false(sim_a_mother_sim_info is old_full_family.grandmother_one, 'Sim A still had Grandmother One as their biological mother')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Father One was still a brother to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Two was still a brother to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin One was no longer a child of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin Two was no longer a child of Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Three was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Four was still a nephew to Sim A')

            # Uncle 2
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was still a brother of Uncle Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew of Uncle Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew of Uncle Two')

            # Father 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was still a brother to Father One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Father One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Father One')

            # Cousin 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin One')
            cousin_one_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_full_family.cousin_one)
            CommonAssertionUtils.is_true(cousin_one_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin One was no longer a brother of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Step Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Seven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Eight')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Nine')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Ten')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Eleven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Twelve')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Sixteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was still an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was still an uncle of Cousin One')

            # Cousin 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin Two')
            cousin_two_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_full_family.cousin_two)
            CommonAssertionUtils.is_true(cousin_two_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin Two was no longer a brother of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Step Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Seven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Eight')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Nine')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Ten')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Eleven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Twelve')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Sixteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was still an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was still an uncle of Cousin Two')

            # Cousin 3
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Cousin Three')

            # Cousin 4
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Cousin Four')

            # Child 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Child One')

            # Child 2
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Child Two')

            # Step Child 2
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle to Step Child Two')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_uncle_to_sim_b_should_add_relationships_from_new_family() -> None:
        new_full_family = S4CMFullFamily()
        old_full_family = S4CMFullFamily()
        sim_a_uncle = old_full_family.uncle_one
        sim_b_child = new_full_family.child_one
        try:
            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_a_uncle, sim_b_child), 'Failed to update family tree')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_a_uncle, sim_b_child)

            # Grandfather
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandfather One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Grandfather One was not a grandparent to Cousin One')
            cousin_one_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(old_full_family.cousin_one)
            CommonAssertionUtils.is_true(cousin_one_grandfather_sim_info is new_full_family.grandfather_one, 'Cousin One still had Grandfather One as their biological grandfather')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Grandfather One was not a grandparent to Cousin Two')
            cousin_two_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(new_full_family.cousin_two)
            CommonAssertionUtils.is_true(cousin_two_grandfather_sim_info is new_full_family.grandfather_one, 'Cousin Two still had Grandfather One as their biological grandfather')

            # Grandmother
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was not a grandchild of Grandmother One')
            cousin_one_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(old_full_family.cousin_one)
            CommonAssertionUtils.is_true(cousin_one_grandmother_sim_info is new_full_family.grandmother_one, 'Cousin One did not have Grandmother One as their biological grandmother')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was not a grandchild of Grandmother One')
            cousin_two_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(new_full_family.cousin_two)
            CommonAssertionUtils.is_true(cousin_two_grandmother_sim_info is new_full_family.grandmother_one, 'Cousin Two did not have Grandmother One as their biological grandmother')

            # Uncle 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather One was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a son to Grandfather One')
            sim_a_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_true(sim_a_father_sim_info is new_full_family.grandfather_one, 'Sim A did not have Grandfather One as their biological father')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother One was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a son to Grandmother One')
            sim_a_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_true(sim_a_mother_sim_info is new_full_family.grandmother_one, 'Sim A did not have Grandmother One as their biological mother')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Father One was not a brother to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle One new was not a brother to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Two was not a brother to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin One was no longer a child of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin Two was no longer a child of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Three was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Four was not a nephew to Sim A')

            # Uncle 1 (new)
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a brother of Uncle One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew of Uncle One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew of Uncle One new')

            # Uncle 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a brother of Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew of Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew of Uncle Two')

            # Father 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a brother to Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Father One')

            # Cousin 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin One')
            cousin_one_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_full_family.cousin_one)
            CommonAssertionUtils.is_true(cousin_one_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin One was no longer a brother of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One old was not a cousin of Cousin One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One old was not a cousin of Cousin Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Step Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Nine')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Ten')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Eleven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Twelve')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Sixteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One new was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_one, new_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was not an uncle of Cousin One')

            # Cousin 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin Two')
            cousin_two_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_full_family.cousin_two)
            CommonAssertionUtils.is_true(cousin_two_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin Two was no longer a brother of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two old was not a cousin of Cousin One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two old was not a cousin of Cousin Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Step Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Nine')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Ten')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Eleven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Twelve')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Sixteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One new was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_two, new_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was not an uncle of Cousin Two')

            # Cousin 3
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Three')

            # Cousin 4
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Cousin Four')

            # Child 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_one, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_one, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Child One')

            # Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Child Two')

            # Step Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, old_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, old_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle to Step Child Two')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()
