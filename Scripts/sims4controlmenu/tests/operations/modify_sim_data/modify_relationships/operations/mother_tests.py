"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
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
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
    S4CMSetSimAAsMotherToSimBOp
from sims4controlmenu.modinfo import ModInfo


@CommonTestService.test_class(ModInfo.get_identity())
class _S4CMSetSimAAsMotherToSimBOpTests:
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

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_mother_from_sim_c_to_sim_a() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Run Operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim A should be parent of Sim B and Sim B should be child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed, Sim A was not a parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed, Sim B was not a child of Sim A')

            # Sim C should NOT be parent of Sim B and Sim B should NOT be child of Sim C
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed, Sim C was still marked as Parent of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed, Sim B was still marked as a child of Sim C')

            # Sim A should be biological mother of Sim B
            mother_sim_info_b = CommonSimGenealogyUtils.get_mother_sim_info(sim_info_b)
            CommonAssertionUtils.is_true(mother_sim_info_b is sim_info_a, 'Failed, Sim A was not marked as the biological mother of Sim B. Sim: {}'.format(CommonSimNameUtils.get_full_name(mother_sim_info_b)))
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_grandmother_from_sim_d_to_sim_e() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Grandfather
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Grandfather
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim E as biological parent of Sim A and Sim A as biological child of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim E as parent of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim A as child of Sim E')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_e, sim_info_a), 'Failed to set Sim E as biological mother of Sim A')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_d, sim_info_c), 'Failed to set Sim D as biological mother of Sim C')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim D as biological grandmother of Sim B and Sim B as biological grandchild of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed to set Sim D as grandparent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed to set Sim B as grandchild of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mothers_mother_of(sim_info_d, sim_info_b), 'Failed to set Sim D as biological grandmother of Sim B on mothers side')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be grandparent of Sim B and Sim B should not be grandchild of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed, Sim D was still marked as Grandparent of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed, Sim B was still marked as a Grandchild of Sim D')

            # Sim E should be grandparent of Sim B and Sim B should be grandchild of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed, Sim E was not marked as Grandparent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed, Sim B was not marked as a Grandchild of Sim E')

            # Sim D should be grandparent of Sim C and Sim C should be grandchild of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_PARENT), 'Failed, Sim D was no longer marked as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed, Sim C was no longer marked as a child of Sim D')

            # Sim E should be biological grandmother of Sim B
            grandmother_sim_info_b = CommonSimGenealogyUtils.get_mothers_mother_sim_info(sim_info_b)
            CommonAssertionUtils.is_true(grandmother_sim_info_b is sim_info_e, 'Failed, Sim B did not have Sim E as grandmother. Sim: {}'.format(CommonSimNameUtils.get_full_name(grandmother_sim_info_b)))

            # Sim D should be biological mother of Sim C
            grandmother_sim_info_c = CommonSimGenealogyUtils.get_mother_sim_info(sim_info_c)
            CommonAssertionUtils.is_true(grandmother_sim_info_c is sim_info_d, 'Failed, Sim C did not have Sim D as mother. Sim: {}'.format(CommonSimNameUtils.get_full_name(grandmother_sim_info_c)))
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_grandfather_from_sim_d_to_sim_e() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Grandfather
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Grandfather
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim E as biological father of Sim A and Sim A as biological child of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim E as parent of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim A as child of Sim E')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_e, sim_info_a), 'Failed to set Sim E as biological father of Sim A')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_d, sim_info_c), 'Failed to set Sim D as biological father of Sim C')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim D as biological grandparent of Sim B and Sim B as biological grandchild of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed to set Sim D as grandparent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed to set Sim B as grandchild of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mothers_father_of(sim_info_d, sim_info_b), 'Failed to set Sim D as biological grandfather of Sim B on mothers side')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be grandparent of Sim B and Sim B should not be grandchild of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed, Sim D was still marked as Grandparent of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed, Sim B was still marked as a Grandchild of Sim D')

            # Sim E should be grandparent of Sim B and Sim B should be grandchild of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed, Sim E was not marked as Grandparent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed, Sim B was not marked as a Grandchild of Sim E')

            # Sim E should be biological grandfather of Sim B
            grandfather_sim_info_b = CommonSimGenealogyUtils.get_mothers_father_sim_info(sim_info_b)
            CommonAssertionUtils.is_true(grandfather_sim_info_b is sim_info_e, 'Failed, Sim B did not have Sim E as grandfather. Sim: {}'.format(CommonSimNameUtils.get_full_name(grandfather_sim_info_b)))
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_uncle_from_sim_f_to_sim_g() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Grandfather
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Grandfather
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Uncle
        sim_info_f: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle
        sim_info_g: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim E as biological father of Sim G and Sim G as biological child of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_g, sim_info_e, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim E as parent of Sim G')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_g, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim G as child of Sim E')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_e, sim_info_g), 'Failed to set Sim E as biological father of Sim G')

            # Sim E as biological father of Sim A and Sim A as biological child of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim E as parent of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim A as child of Sim E')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_e, sim_info_a), 'Failed to set Sim E as biological father of Sim A')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_g, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother or sister of Sim G')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_g, sim_info_a, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim G as brother or sister of Sim A')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_d, sim_info_c), 'Failed to set Sim D as biological father of Sim C')

            # Sim D as parent of Sim F and Sim F as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_d, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim F')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_f, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim F as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_d, sim_info_f), 'Failed to set Sim D as biological father of Sim F')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_c, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim C as brother or sister of Sim F')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_f, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim F as brother or sister of Sim C')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim D as biological grandmother of Sim B and Sim B as biological grandchild of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed to set Sim D as grandparent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed to set Sim B as grandchild of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mothers_father_of(sim_info_d, sim_info_b), 'Failed to set Sim D as biological grandfather of Sim B on mothers side')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim F should not be aunt/uncle of Sim B and Sim B should not be niece/nephew of Sim F
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_f, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim F was still marked as Aunt/Uncle of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_f, sim_info_b, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was still marked as Niece/Nephew of Sim F')

            # Sim G should be aunt/uncle of Sim B and Sim B should be niece/nephew of Sim G
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_g, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim G was not marked as Aunt/Uncle of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_g, sim_info_b, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as Niece/Nephew of Sim G')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_g, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_cousin_from_sim_h_to_sim_i() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Grandfather
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Grandfather
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Uncle
        sim_info_f: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle
        sim_info_g: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Cousin
        sim_info_h: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Cousin
        sim_info_i: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim E as biological father of Sim G and Sim G as biological child of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_g, sim_info_e, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim E as parent of Sim G')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_g, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim G as child of Sim E')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_e, sim_info_g), 'Failed to set Sim E as biological father of Sim G')

            # Sim E as biological father of Sim A and Sim A as biological child of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim E as parent of Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim A as child of Sim E')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_e, sim_info_a), 'Failed to set Sim E as biological father of Sim A')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_g, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother or sister of Sim G')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_g, sim_info_a, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim G as brother or sister of Sim A')

            # Sim D as biological parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_d, sim_info_c), 'Failed to set Sim D as biological father of Sim C')

            # Sim D as biological parent of Sim F and Sim F as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_d, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim F')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_f, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim F as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_d, sim_info_f), 'Failed to set Sim D as biological father of Sim F')

            # Sim F as biological parent of Sim H and Sim H as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_h, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim H')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_h, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim H as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_h), 'Failed to set Sim F as biological father of Sim H')

            # Sim G as biological parent of Sim I and Sim I as biological child of Sim G
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_i, sim_info_g, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim G as parent of Sim I')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_g, sim_info_i, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim I as child of Sim G')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_g, sim_info_i), 'Failed to set Sim G as biological father of Sim I')

            # Sim B as cousin of Sim H and Sim H as cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_h, sim_info_b, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed to set Sim B as cousin of Sim H')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_h, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed to set Sim H as cousin of Sim B')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_c, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim C as brother or sister of Sim F')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_f, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim F as brother or sister of Sim C')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim D as biological grandparent of Sim B and Sim B as biological grandchild of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed to set Sim D as grandparent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed to set Sim B as grandchild of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mothers_father_of(sim_info_d, sim_info_b), 'Failed to set Sim D as biological grandfather of Sim B on mothers side')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim H should not be cousin of Sim B and Sim B should not be cousin of Sim H
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_h, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim H was still marked as Cousin of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_h, sim_info_b, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was still marked as Cousin of Sim H')

            # Sim I should be cousin of Sim B and Sim B should be cousin of Sim I
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_i, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim I was not marked as Cousin of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_i, sim_info_b, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as Cousin of Sim I')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_g, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_h, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_i, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_set_new_mother_as_grandmother_of_children_of_sim_b() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child Of Sim B
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim B as biological parent of Sim D and Sim D as biological child of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim B as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim B')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_b, sim_info_d), 'Failed to set Sim B as biological mother of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim C as biological grandparent of Sim D and Sim D as biological grandchild of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed to set Sim C as grandparent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed to set Sim D as grandchild of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mothers_mother_of(sim_info_d, sim_info_c), 'Failed to set Sim C as biological grandmother of Sim D on mothers side')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim C should not be grandparent of Sim D and Sim D should not be grandchild of Sim C
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed, Sim C was still marked as grandparent of Sim D')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed, Sim D was still marked as grandchild of Sim C')

            # Sim A should be grandparent of Sim D and Sim D should be grandchild of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_a, CommonRelationshipBitId.FAMILY_GRANDPARENT), 'Failed, Sim A was not marked as grandparent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a, sim_info_d, CommonRelationshipBitId.FAMILY_GRANDCHILD), 'Failed, Sim D was not marked as grandchild of Sim A')

            # Sim A should be biological grandmother of Sim D
            grandmother_sim_info_d = CommonSimGenealogyUtils.get_mothers_mother_sim_info(sim_info_d)
            CommonAssertionUtils.is_true(grandmother_sim_info_d is sim_info_a, 'Failed, Sim D did not have Sim A as grandmother. Sim: {}'.format(CommonSimNameUtils.get_full_name(grandmother_sim_info_d)))
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_brother_or_sister_from_sim_d_to_sim_e_with_different_father() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Brother
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Brother
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Sim B Father
        sim_info_f: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Sim E Father (New)
        sim_info_g: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Sim D Father
        sim_info_h: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim E and Sim E as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_e), 'Failed to set Sim A as biological mother of Sim E')

            # Sim F as biological parent of Sim B and Sim B as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_g, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim G as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_g, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim G')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_g, sim_info_e), 'Failed to set Sim G as biological father of Sim E')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_d), 'Failed to set Sim C as biological mother of Sim D')

            # Sim F as biological parent of Sim B and Sim B as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_h, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim H as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_h, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim H')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_h, sim_info_d), 'Failed to set Sim H as biological father of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim F as biological parent of Sim B and Sim B as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_b), 'Failed to set Sim F as biological father of Sim B')

            # Sim D as brother/sister of Sim B and Sim B as brother/sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed to set Sim D as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed to set Sim B as step brother/step sister of Sim D')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be brother/sister of Sim B and Sim B should not be brother/sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was still marked as brother/sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was still marked as a brother/sister of Sim D')

            # Sim D should be step brother/step sister of Sim B and Sim B should not be step brother/step sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim D was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim D')

            # Sim E should be step brother/step sister of Sim B and Sim B should be step brother/step sister of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim E was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_g, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_h, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_brother_or_sister_from_sim_d_to_sim_e_with_sim_d_and_sim_b_same_father() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Brother
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Brother
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Sim B and Sim D Father
        sim_info_f: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Sim E Father (New)
        sim_info_g: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim E and Sim E as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_e), 'Failed to set Sim A as biological mother of Sim E')

            # Sim F as biological parent of Sim B and Sim B as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_g, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim G as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_g, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim G')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_g, sim_info_e), 'Failed to set Sim G as biological father of Sim E')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_d), 'Failed to set Sim C as biological mother of Sim D')

            # Sim F as biological parent of Sim B and Sim B as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim H as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim H')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_d), 'Failed to set Sim H as biological father of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim F as biological parent of Sim B and Sim B as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_b), 'Failed to set Sim F as biological father of Sim B')

            # Sim D as brother/sister of Sim B and Sim B as brother/sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother/sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim B as brother/sister of Sim D')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be brother/sister of Sim B and Sim B should not be brother/sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was still marked as brother/sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was still marked as a brother/sister of Sim D')

            # Sim D should be step brother/step sister of Sim B and Sim B should not be step brother/step sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim D was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim D')

            # Sim E should be step brother/step sister of Sim B and Sim B should be step brother/step sister of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim E was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_g, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_brother_or_sister_from_sim_d_to_sim_e_with_new_father_without_original_father() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Brother
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Brother
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Father
        sim_info_f: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim E and Sim E as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_e), 'Failed to set Sim A as biological mother of Sim E')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_d), 'Failed to set Sim C as biological mother of Sim D')

            # Sim G as biological parent of Sim E and Sim E as biological child of Sim G
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim G as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim G')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_e), 'Failed to set Sim G as biological father of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim D as brother/sister of Sim B and Sim B as brother/sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother/sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim B as brother/sister of Sim D')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be brother/sister of Sim B and Sim B should not be brother/sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was still marked as brother/sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was still marked as a brother/sister of Sim D')

            # Sim D should be step brother/step sister of Sim B and Sim B should not be step brother/step sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim D was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim D')

            # Sim E should be step brother/step sister of Sim B and Sim B should be step brother/step sister of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim E was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_brother_or_sister_from_sim_d_to_sim_e_without_new_or_original_father() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Brother
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Brother
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim E and Sim E as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_e), 'Failed to set Sim A as biological mother of Sim E')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_d), 'Failed to set Sim C as biological mother of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim D as brother/sister of Sim B and Sim B as brother/sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother/sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim B as brother/sister of Sim D')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be brother/sister of Sim B and Sim B should not be brother/sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was still marked as brother/sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was still marked as a brother/sister of Sim D')

            # Sim D should be step brother/step sister of Sim B and Sim B should not be step brother/step sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim D was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim D')

            # Sim E should be step brother/step sister of Sim B and Sim B should be step brother/step sister of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was not marked as a step brother/step sister of Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_brother_or_sister_from_sim_d_to_sim_e_with_original_father_without_new_father() -> None:
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Brother
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Brother
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Father
        sim_info_f: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim E and Sim E as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_e), 'Failed to set Sim A as biological mother of Sim E')

            # Sim D as parent of Sim C and Sim C as biological child of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_d), 'Failed to set Sim C as biological mother of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_d), 'Failed to set Sim F as biological father of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_b), 'Failed to set Sim F as biological father of Sim B')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim D as brother/sister of Sim B and Sim B as brother/sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother/sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim B as brother/sister of Sim D')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be brother/sister of Sim B and Sim B should not be brother/sister of Sim D
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was still marked as brother/sister of Sim B')
            CommonAssertionUtils.is_false(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was still marked as a brother/sister of Sim D')

            # Sim D should be step brother/step sister of Sim B and Sim B should not be step brother/step sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim D was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim D')

            # Sim E should be step brother/step sister of Sim B and Sim B should be step brother/step sister of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim E was not marked as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed, Sim B was not marked as a step brother/step sister of Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_sim_a_as_mother_to_sim_b_should_change_brother_or_sister_from_sim_d_to_sim_e_with_same_father() -> None:
        # If they have the same father and they are changing to the same mother, they should essentially become part of the same family.
        # New Mother
        sim_info_a: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Child
        sim_info_b: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Mother
        sim_info_c: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Old Brother
        sim_info_d: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Brother
        sim_info_e: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Current Father
        sim_info_f: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Sim A as biological parent of Sim E and Sim E as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_e), 'Failed to set Sim A as biological mother of Sim E')

            # Sim F as biological parent of Sim E and Sim E as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_e, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_e), 'Failed to set Sim F as biological father of Sim E')

            # Sim A as parent of Sim D and Sim D as biological child of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_a, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a, sim_info_d), 'Failed to set Sim C as biological mother of Sim D')

            # Sim F as parent of Sim D and Sim D as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_d, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_d), 'Failed to set Sim F as biological father of Sim D')

            # Sim C as biological parent of Sim B and Sim B as biological child of Sim C
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_c, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim C as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim C')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c, sim_info_b), 'Failed to set Sim C as biological mother of Sim B')

            # Sim F as biological parent of Sim B and Sim B as biological child of Sim F
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_f, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f, sim_info_b, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f, sim_info_b), 'Failed to set Sim F as biological father of Sim B')

            # Sim D as brother/sister of Sim B and Sim B as step brother/step sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed to set Sim D as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed to set Sim B as step brother/step sister of Sim D')

            # Sim D as brother/sister of Sim B and Sim B as step brother/step sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed to set Sim D as step brother/step sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_STEP_SIBLING), 'Failed to set Sim B as step brother/step sister of Sim D')

            # Sim E as brother/sister of Sim B and Sim E as step brother/step sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d, sim_info_e, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother/sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim B as brother/sister of Sim D')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsMotherToSimBOp()._update_family_tree(sim_info_a, sim_info_b), 'Failed to update family tree.')
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(sim_info_a, sim_info_b)

            # Sim D should not be brother/sister of Sim B and Sim B should not be brother/sister of Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother/sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was not marked as brother/sister of Sim D')

            # Sim E should be step brother/step sister of Sim B and Sim B should be step brother/step sister of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b, sim_info_e, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother/sister of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_b, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim B was not marked as brother/sister of Sim E')

            # Sim E should be step brother/step sister of Sim B and Sim B should be step brother/step sister of Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d, sim_info_e, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother/sister of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e, sim_info_d, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother/sister of Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f, cause='S4CM: testing cleanup')
