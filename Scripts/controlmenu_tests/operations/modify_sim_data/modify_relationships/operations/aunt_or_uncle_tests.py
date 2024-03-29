"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.aunt_or_uncle import \
    CMSetSimAAsAuntOrUncleToSimBOp
from controlmenu.modinfo import ModInfo
from controlmenu_tests.operations.modify_sim_data.modify_relationships.operations.full_family import CMFullFamily


@CommonTestService.test_class(ModInfo.get_identity())
class _CMSetSimAAsAuntOrUncleToSimBOpTests:
    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_uncle_to_sim_b_should_remove_relationships_from_old_family() -> None:
        new_full_family = CMFullFamily()
        old_full_family = CMFullFamily()
        sim_a_uncle = old_full_family.uncle_one
        sim_b_child = new_full_family.child_one
        old_child_one = old_full_family.cousin_one
        old_child_two = old_full_family.cousin_two
        try:
            # Run operation
            CommonAssertionUtils.is_true(CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_a_uncle, sim_b_child), 'Failed to update family tree')
            CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_a_uncle, sim_b_child)

            # Grandfather
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandfather Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandfather Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandfather One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was still a grandchild to Grandfather Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_four, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was still a grandchild to Grandfather Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was still a grandchild to Grandfather One')
            cousin_one_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(old_child_one)
            CommonAssertionUtils.is_false(cousin_one_grandfather_sim_info is old_full_family.grandfather_one, 'Cousin One still had Grandfather One as their biological grandfather')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was still a grandchild to Grandfather Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_four, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was still a grandchild to Grandfather Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was still a grandchild to Grandfather One')
            cousin_two_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(old_child_two)
            CommonAssertionUtils.is_false(cousin_two_grandfather_sim_info is old_full_family.grandfather_one, 'Cousin Two still had Grandfather One as their biological grandfather')

            # Grandmother
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandmother Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandmother Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a child of Grandmother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was still a grandchild to Grandmother Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_four, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was still a grandchild to Grandmother Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was still a grandchild of Grandmother One')
            cousin_one_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(old_child_one)
            CommonAssertionUtils.is_false(cousin_one_grandmother_sim_info is old_full_family.grandmother_one, 'Cousin One still had Grandmother One as their biological grandmother')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was still a grandchild to Grandmother Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_four, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was still a grandchild to Grandmother Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was still a grandchild of Grandmother One')
            cousin_two_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(old_child_two)
            CommonAssertionUtils.is_false(cousin_two_grandmother_sim_info is old_full_family.grandmother_one, 'Cousin Two still had Grandmother One as their biological grandmother')

            # Uncle 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Three was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandfather_four, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Four was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather One was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a son to Grandfather One')
            sim_a_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_false(sim_a_father_sim_info is old_full_family.grandfather_one, 'Sim A still had Grandfather One as their biological father')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Three was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandmother_four, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Four was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother One was still a parent to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was still a son to Grandmother One')
            sim_a_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_false(sim_a_mother_sim_info is old_full_family.grandmother_one, 'Sim A still had Grandmother One as their biological mother')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Father One was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Two was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.mother_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Mother One was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.mother_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Mother Two was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.uncle_five, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Five was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.uncle_six, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Six was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.uncle_seven, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Seven was still a sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.uncle_eight, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Eight was still a sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin One was no longer a child of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin Two was no longer a child of Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child Two was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Three was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Four was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Nine was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Ten was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eleven was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Twelve was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Thirteen was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Fourteen was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Fifteen was still a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Sixteen was still a nephew to Sim A')

            # Uncle 2
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was still a sibling of Uncle Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew of Uncle Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_two, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew of Uncle Two')

            # Father 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was still a sibling to Father One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Father One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.father_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Father One')

            # Mother 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.mother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was still a sibling to Mother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.mother_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Mother One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.mother_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Mother One')

            # Mother 2
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.mother_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was still a sibling to Mother Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.mother_two, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Mother Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.mother_two, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Mother Two')

            # Uncle 5
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_five, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was still a sibling to Uncle Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_five, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Uncle Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_five, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Uncle Five')

            # Uncle 6
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_six, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was still a sibling to Uncle Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_six, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Uncle Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_six, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Uncle Six')

            # Uncle 7
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_seven, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was still a sibling to Uncle Seven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_seven, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Uncle Seven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_seven, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Uncle Seven')

            # Uncle 8
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_eight, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was still a sibling to Uncle Eight')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_eight, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was still a nephew to Uncle Eight')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.uncle_eight, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was still a nephew to Uncle Eight')

            # Cousin 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin One')
            cousin_one_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_child_one)
            CommonAssertionUtils.is_true(cousin_one_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin One was no longer a sibling of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Step Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Nine')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Ten')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Eleven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Twelve')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was still a cousin of Cousin Sixteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandfather_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Four was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.grandmother_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Four was still a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.mother_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother One was still an aunt of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.mother_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother Two was still an aunt of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was still an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was still an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_seven, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Seven was still an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_eight, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Eight was still an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was still an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was still an uncle of Cousin One')

            # Cousin 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin Two')
            cousin_two_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_child_two)
            CommonAssertionUtils.is_true(cousin_two_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin Two was no longer a sibling of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Step Child One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Step Child Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Three')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Four')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Nine')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Ten')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Eleven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Twelve')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was still a cousin of Cousin Sixteen')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandfather_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Four was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.grandmother_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Four was still a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.mother_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother One was still an aunt of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.mother_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother Two was still an aunt of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was still an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was still an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_seven, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Seven was still an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_eight, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Eight was still an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was still an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was still an uncle of Cousin Two')

            # Cousin 3
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Three')

            # Cousin 4
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Four')

            # Cousin 9
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_nine, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_nine, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_nine, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Nine')

            # Cousin 10
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_ten, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_ten, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_ten, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Ten')

            # Cousin 11
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eleven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eleven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_eleven, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Eleven')

            # Cousin 12
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_twelve, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_twelve, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_twelve, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Twelve')

            # Cousin 13
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_thirteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Thirteen was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_thirteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Thirteen was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_thirteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Thirteen')

            # Cousin 14
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_fourteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fourteen was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_fourteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fourteen was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_fourteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Fourteen')

            # Cousin 15
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_fifteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fifteen was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_fifteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fifteen was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_fifteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Fifteen')

            # Cousin 16
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_sixteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Sixteen was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_sixteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Sixteen was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.cousin_sixteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Cousin Sixteen')

            # Child 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_one, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_one, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Child One')

            # Child 2
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_two, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_two, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Child Two')

            # Step Child 1
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_one, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_one, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Step Child One')

            # Step Child 2
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_two, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was still a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_two, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was still a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_full_family.step_child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was still an uncle of Step Child Two')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_uncle_to_sim_b_should_add_relationships_from_new_family() -> None:
        new_full_family = CMFullFamily()
        old_full_family = CMFullFamily()
        sim_a_uncle = old_full_family.uncle_one
        sim_b_child = new_full_family.child_one
        old_child_one = old_full_family.cousin_one
        old_child_two = old_full_family.cousin_two
        try:
            # Run operation
            CommonAssertionUtils.is_true(CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_a_uncle, sim_b_child), 'Failed to update family tree')
            CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_a_uncle, sim_b_child)

            # Grandfather
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandfather Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandfather Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandfather One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was not a grandchild to Grandfather Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_four, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was not a grandchild to Grandfather Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was not a grandchild to Grandfather One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Grandfather One was not a grandparent to Cousin One')
            cousin_one_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(old_child_one)
            CommonAssertionUtils.is_true(cousin_one_grandfather_sim_info is new_full_family.grandfather_one, 'Cousin One still had Grandfather One as their biological grandfather')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was not a grandchild to Grandfather Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_four, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was not a grandchild to Grandfather Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was not a grandchild to Grandfather One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Grandfather One was not a grandparent to Cousin Two')
            cousin_two_grandfather_sim_info = CommonSimGenealogyUtils.get_fathers_father_sim_info(new_full_family.cousin_two)
            CommonAssertionUtils.is_true(cousin_two_grandfather_sim_info is new_full_family.grandfather_one, 'Cousin Two still had Grandfather One as their biological grandfather')

            # Grandmother
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a child of Grandmother One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was not a grandchild to Grandmother Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_four, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was not a grandchild to Grandmother Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, old_child_one, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin One was not a grandchild of Grandmother One')
            cousin_one_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(old_child_one)
            CommonAssertionUtils.is_true(cousin_one_grandmother_sim_info is new_full_family.grandmother_one, 'Cousin One did not have Grandmother One as their biological grandmother')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_three, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was not a grandchild to Grandmother Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_four, old_child_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was not a grandchild to Grandmother Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Cousin Two was not a grandchild of Grandmother One')
            cousin_two_grandmother_sim_info = CommonSimGenealogyUtils.get_fathers_mother_sim_info(new_full_family.cousin_two)
            CommonAssertionUtils.is_true(cousin_two_grandmother_sim_info is new_full_family.grandmother_one, 'Cousin Two did not have Grandmother One as their biological grandmother')

            # Uncle 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Three was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandfather_four, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather Four was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandfather One was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandfather_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a son to Grandfather One')
            sim_a_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_true(sim_a_father_sim_info is new_full_family.grandfather_one, 'Sim A did not have Grandfather One as their biological father')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Three was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandmother_four, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother Four was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_PARENT), 'Grandmother One was not a parent to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.grandmother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Sim A was not a son to Grandmother One')
            sim_a_mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_a_uncle)
            CommonAssertionUtils.is_true(sim_a_mother_sim_info is new_full_family.grandmother_one, 'Sim A did not have Grandmother One as their biological mother')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.father_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Father One was not a sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle One new was not a sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Uncle Two was not a sibling to Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.mother_one, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Mother One was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.mother_two, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Mother Two was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_five, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Five was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_six, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Six was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_seven, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Seven was not a step sibling to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_eight, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Eight was not a step sibling to Sim A')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_three, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Three was a step sibling to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.uncle_four, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Uncle Four was a step sibling to Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_child_one, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin One was no longer a child of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, old_child_two, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Cousin Two was no longer a child of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Step Child Two was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child One was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Child Two was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two new was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Three was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Four was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Nine was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Ten was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eleven was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Twelve was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Thirteen was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Fourteen was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Fifteen was not a nephew to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Sixteen was not a nephew to Sim A')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Five was a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Six was a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Seven was a nephew to Sim A')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_a_uncle, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Eight was a nephew to Sim A')

            # Uncle 1 (new)
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a sibling of Uncle One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew of Uncle One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew of Uncle One new')

            # Uncle 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a sibling of Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew of Uncle Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_two, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew of Uncle Two')

            # Father 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Sim A was not a sibling to Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Father One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.father_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Father One')

            # Mother 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.mother_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a sibling to Mother One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.mother_one, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Mother One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.mother_one, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Mother One')

            # Mother 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.mother_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a sibling to Mother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.mother_two, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Mother Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.mother_two, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Mother Two')

            # Uncle 5
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_five, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a sibling to Uncle Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_five, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Uncle Five')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_five, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Uncle Five')

            # Uncle 6
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_six, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a sibling to Uncle Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_six, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Uncle Six')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_six, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Uncle Six')

            # Uncle 7
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_seven, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a sibling to Uncle Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_seven, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Uncle Seven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_seven, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Uncle Seven')

            # Uncle 8
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_eight, sim_a_uncle, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Sim A was not a sibling to Uncle Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_eight, old_child_one, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin One was not a nephew to Uncle Eight')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.uncle_eight, old_child_two, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Cousin Two was not a nephew to Uncle Eight')

            # Cousin 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin One')
            cousin_one_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_child_one)
            CommonAssertionUtils.is_true(cousin_one_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, old_child_two, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin One was no longer a sibling of Cousin Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One old was not a cousin of Cousin One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One old was not a cousin of Cousin Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Step Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Nine')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Ten')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Eleven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Twelve')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was a cousin of Cousin Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was a cousin of Cousin Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was a cousin of Cousin Seven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin One was a cousin of Cousin Eight')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was not a grandparent of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandfather_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Four was not a grandparent of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was not a grandparent of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandmother_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Four was not a grandparent of Cousin One')
            
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was a grandparent of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was a grandparent of Cousin One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.mother_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother One was not an aunt of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.mother_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother Two was not an aunt of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_seven, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Seven was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_eight, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Eight was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One new was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_seven, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Seven was not an uncle of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_eight, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Eight was not an uncle of Cousin One')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.father_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father Two was an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was an uncle of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_one, new_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was an uncle of Cousin One')

            # Cousin 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Sim A was no longer a parent of Cousin Two')
            cousin_two_father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(old_child_two)
            CommonAssertionUtils.is_true(cousin_two_father_sim_info is sim_a_uncle, 'Sim A was no longer the biological father of Cousin Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, old_child_one, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Cousin Two was no longer a sibling of Cousin One')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two old was not a cousin of Cousin One new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two old was not a cousin of Cousin Two new')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.step_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Step Child One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.step_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Step Child Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_three, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Three')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_four, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Four')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_nine, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Nine')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_ten, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Ten')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_eleven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Eleven')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_twelve, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Twelve')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_thirteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Thirteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_fourteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Fourteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_fifteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Fifteen')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_sixteen, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was not a cousin of Cousin Sixteen')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_five, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was a cousin of Cousin Five')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_six, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was a cousin of Cousin Six')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_seven, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was a cousin of Cousin Seven')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.cousin_eight, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Two was a cousin of Cousin Eight')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandfather_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather One was not a grandparent of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandmother_one, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother One was not a grandparent of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandfather_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Three was not a grandparent of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandfather_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Four was not a grandparent of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandmother_three, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Three was not a grandparent of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandmother_four, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Four was not a grandparent of Cousin Two')
            
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandfather_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandfather Two was a grandparent of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.grandmother_two, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Grandmother Two was a grandparent of Cousin Two')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.mother_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother One was not an aunt of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.mother_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Mother Two was not an aunt of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_five, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Five was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_six, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Six was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_seven, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Seven was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_eight, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Eight was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle One new was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Two was not an uncle of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.father_one, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father One was not an uncle of Cousin Two')

            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.father_two, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Father Two was an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_three, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Three was an uncle of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(old_child_two, new_full_family.uncle_four, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Uncle Four was an uncle of Cousin Two')

            # Cousin 3
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Three was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_three, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Three')

            # Cousin 4
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Four was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_four, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Four')

            # Cousin 5
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_five, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_five, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Five was a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_five, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Five')

            # Cousin 6
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_six, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_six, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Six was a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_six, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was an uncle of Cousin Six')

            # Cousin 7
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_seven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_seven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Seven was a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_seven, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was an uncle of Cousin Seven')

            # Cousin 8
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eight, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was a cousin of Cousin One')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eight, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eight was a cousin of Cousin Two')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eight, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was an uncle of Cousin Eight')

            # Cousin 9
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_nine, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_nine, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Nine was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_nine, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Nine')

            # Cousin 10
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_ten, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_ten, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Ten was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_ten, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Ten')

            # Cousin 11
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eleven, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eleven, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Eleven was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_eleven, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Eleven')

            # Cousin 12
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_twelve, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_twelve, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Twelve was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_twelve, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Twelve')

            # Cousin 13
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_thirteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Thirteen was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_thirteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Thirteen was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_thirteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Thirteen')

            # Cousin 14
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_fourteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fourteen was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_fourteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fourteen was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_fourteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Fourteen')

            # Cousin 15
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_fifteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fifteen was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_fifteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Fifteen was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_fifteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Fifteen')

            # Cousin 16
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_sixteen, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Sixteen was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_sixteen, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Cousin Sixteen was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.cousin_sixteen, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Cousin Sixteen')

            # Child 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_one, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_one, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child One was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Child One')

            # Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_two, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_two, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Child Two was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Child Two')

            # Step Child 1
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_one, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_one, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child One was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_one, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Step Child One')

            # Step Child 2
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, old_child_one, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was not a cousin of Cousin One')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, old_child_two, CommonRelationshipBitId.FAMILY_COUSIN), 'Step Child Two was not a cousin of Cousin Two')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(new_full_family.step_child_two, sim_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Sim A was not an uncle of Step Child Two')
        finally:
            new_full_family.destroy()
            old_full_family.destroy()
