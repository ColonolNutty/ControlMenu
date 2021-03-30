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
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.aunt_or_uncle import \
    S4CMSetSimAAsAuntOrUncleToSimBOp
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu.tests.operations.modify_sim_data.modify_relationships.operations.full_family import S4CMFullFamily


@CommonTestService.test_class(ModInfo.get_identity())
class _S4CMSetSimAAsAuntOrUncleToSimBOpTests:
    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_aunt_uncle_nephew_niece_with_no_parents() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._no_sides(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be uncle of Sim B and Sim B should be nephew of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim A was not marked as aunt/uncle of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as niece/nephew of Sim A')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_aunt_uncle_nephew_niece_with_father() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Father
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be uncle of Sim B and Sim B should be nephew of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim A was not marked as aunt/uncle of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as niece/nephew of Sim A')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_aunt_uncle_nephew_niece_with_mother() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Mother
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._mothers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be uncle of Sim B and Sim B should be nephew of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim A was not marked as aunt/uncle of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as niece/nephew of Sim A')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_aunt_uncle_nephew_niece_with_father_multiple_uncles() -> None:
        # Uncle 1
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Father
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Existing Uncle 1
        sim_info_d_uncle_existing: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle 2
        sim_info_e_uncle_new: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_uncle_new, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim E as brother of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim D as uncle of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_uncle_existing, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim B as nephew of Sim D')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim C as brother of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_uncle_existing, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother of Sim C')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be uncle to Sim B and Sim B should be nephew to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim A was not marked as uncle to Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as nephew to Sim A')

            # Sim D should be uncle to Sim B and Sim B should be nephew to Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim D was not marked as uncle to Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_uncle_existing, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as nephew to Sim D')

            # Sim D should be uncle to Sim B and Sim B should be nephew to Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as brother to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim C')

            # Sim E should be uncle to Sim B and Sim B should be nephew to Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim E was not marked as uncle to Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_uncle_new, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as nephew to Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_uncle_existing, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e_uncle_new, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_aunt_uncle_nephew_niece_with_mother_multiple_uncles() -> None:
        # Uncle 1
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Mother
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Existing Uncle 1
        sim_info_d_uncle_existing: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle 2
        sim_info_e_uncle_new: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_uncle_new, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim E as brother of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim D as uncle of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_uncle_existing, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim B as nephew of Sim D')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim C as brother of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_uncle_existing, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother of Sim C')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._mothers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be uncle to Sim B and Sim B should be nephew to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim A was not marked as uncle to Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim C was not marked as nephew to Sim A')

            # Sim D should be uncle to Sim B and Sim B should be nephew to Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim D was not marked as uncle to Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_uncle_existing, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as nephew to Sim D')

            # Sim D should be uncle to Sim B and Sim B should be nephew to Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_uncle_existing, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim A')

            # Sim D should be uncle to Sim B and Sim B should be nephew to Sim D
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as brother to Sim A')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim C')

            # Sim E should be uncle to Sim B and Sim B should be nephew to Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim E was not marked as uncle to Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_uncle_new, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim B was not marked as nephew to Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_uncle_existing, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e_uncle_new, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_brother_sister_with_father() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Father
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be brother to Sim C and Sim C should be brother to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as brother to Sim A')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_brother_sister_with_mother() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Mother
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._mothers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be sister to Sim C and Sim C should be sister to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as sister to Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as sister to Sim A')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_brother_sister_with_father_multiple_uncles() -> None:
        # Uncle 1
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Father
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Existing Uncle 1
        sim_info_d_uncle_existing: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle 2
        sim_info_e_uncle_new: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_uncle_new, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim E as brother of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim C as brother of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_uncle_existing, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother of Sim C')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be brother to Sim C and Sim C should be brother to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as brother to Sim A')

            # Sim A should be brother to Sim C and Sim C should be brother to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_uncle_existing, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother to Sim A')

            # Sim E should be brother to Sim C and Sim C should be brother to Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother to Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_uncle_new, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as brother to Sim E')

            # Sim E should be brother to Sim D and Sim D should be brother to Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_uncle_existing, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother to Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_uncle_new, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother to Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_uncle_existing, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e_uncle_new, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_brother_sister_with_mother_multiple_uncles() -> None:
        # Uncle 1
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Mother
        sim_info_c_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Existing Uncle 1
        sim_info_d_uncle_existing: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle 2
        sim_info_e_uncle_new: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_uncle_new, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim E as brother of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim C as brother of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_uncle_existing, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother of Sim C')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_c_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim as parent of Sim')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim as child of Sim')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_c_parent, sim_info_b_nephew), 'Failed to set Sim as biological parent of Sim')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._mothers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim A should be brother to Sim C and Sim C should be brother to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as brother to Sim A')

            # Sim A should be brother to Sim D and Sim D should be brother to Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_uncle_existing, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother to Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother to Sim A')

            # Sim E should be brother to Sim C and Sim C should be brother to Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_parent, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother to Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_uncle_new, sim_info_c_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim C was not marked as brother to Sim E')

            # Sim E should be brother to Sim D and Sim D should be brother to Sim E
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_uncle_existing, sim_info_e_uncle_new, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother to Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_uncle_new, sim_info_d_uncle_existing, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother to Sim E')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_parent, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_uncle_existing, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e_uncle_new, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_cousins_with_no_parents() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin
        sim_info_c_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a_uncle, sim_info_c_cousin), 'Failed to set Sim A as biological parent of Sim C')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._no_sides(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim B should be cousin of Sim C and Sim C should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim C was not marked as cousin of Sim B')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_cousin, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_cousins_with_no_parents_multiple_uncles() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin
        sim_info_c_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle
        sim_info_d_new_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin 2
        sim_info_e_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim C as brother of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a_uncle, sim_info_c_cousin), 'Failed to set Sim A as biological parent of Sim C')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim A as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim C as nephew of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim A as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim C as nephew of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_cousin, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_cousin, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_d_new_uncle, sim_info_e_cousin), 'Failed to set Sim A as biological parent of Sim C')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._no_sides(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim B should be cousin of Sim C and Sim C should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim C was not marked as cousin of Sim B')

            # Sim B should be cousin of Sim E and Sim E should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim E was not marked as cousin of Sim B')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_cousin, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_new_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e_cousin, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_cousins_with_mother_multiple_uncles() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin
        sim_info_c_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle
        sim_info_d_new_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin 2
        sim_info_e_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Mother
        sim_info_f_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a_uncle, sim_info_c_cousin), 'Failed to set Sim A as biological parent of Sim C')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim A as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim C as nephew of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim A as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim C as nephew of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_cousin, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed to set Sim E as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed to set Sim C as cousin of Sim E')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_cousin, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim E as parent of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim D as child of Sim E')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_d_new_uncle, sim_info_e_cousin), 'Failed to set Sim E as biological parent of Sim D')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_f_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_f_parent, sim_info_b_nephew), 'Failed to set Sim F as biological parent of Sim B')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._mothers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim B should be cousin of Sim C and Sim C should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim C was not marked as cousin of Sim B')

            # Sim B should be cousin of Sim E and Sim E should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim E was not marked as cousin of Sim B')

            # Sim B should be cousin of Sim E and Sim E should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_cousin, sim_info_f_parent, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim F was not marked as cousin of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_f_parent, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim E was not marked as cousin of Sim F')

            # Sim B should be sister of Sim E and Sim E should be sister of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_f_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_f_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother of Sim A')

            # Sim B should be sister of Sim E and Sim E should be sister of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_new_uncle, sim_info_f_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_f_parent, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother of Sim D')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_cousin, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_new_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e_cousin, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f_parent, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_cousins_with_father_multiple_uncles() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin
        sim_info_c_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # New Uncle
        sim_info_d_new_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin 2
        sim_info_e_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Father
        sim_info_f_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim A as brother of Sim D')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed to set Sim D as brother of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a_uncle, sim_info_c_cousin), 'Failed to set Sim A as biological parent of Sim C')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim A as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim C as nephew of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed to set Sim A as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed to set Sim C as nephew of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_cousin, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed to set Sim A as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed to set Sim C as cousin of Sim A')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_e_cousin, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_new_uncle, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim E as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_d_new_uncle, sim_info_e_cousin), 'Failed to set Sim D as biological parent of Sim E')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_f_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim F as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_f_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim F')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_f_parent, sim_info_b_nephew), 'Failed to set Sim F as biological parent of Sim B')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim B should be cousin of Sim C and Sim C should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim C was not marked as cousin of Sim B')

            # Sim B should be cousin of Sim E and Sim E should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim E was not marked as cousin of Sim B')

            # Sim B should be cousin of Sim E and Sim E should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_e_cousin, sim_info_f_parent, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim F was not marked as cousin of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_f_parent, sim_info_e_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim E was not marked as cousin of Sim F')

            # Sim B should be brother of Sim E and Sim E should be brother of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_a_uncle, sim_info_f_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim A was not marked as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_f_parent, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother of Sim A')

            # Sim B should be brother of Sim E and Sim E should be brother of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_new_uncle, sim_info_f_parent, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim D was not marked as brother of Sim E')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_f_parent, sim_info_d_new_uncle, CommonRelationshipBitId.FAMILY_BROTHER_SISTER), 'Failed, Sim E was not marked as brother of Sim D')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_cousin, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_new_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_e_cousin, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_f_parent, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_cousins_with_father() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin
        sim_info_c_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Father
        sim_info_d_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_d_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_father_of(sim_info_d_parent, sim_info_b_nephew), 'Failed to set Sim D as biological parent of Sim B')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a_uncle, sim_info_c_cousin), 'Failed to set Sim A as biological parent of Sim C')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._fathers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim B should be cousin of Sim C and Sim C should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim C was not marked as cousin of Sim B')

            # Sim A should be uncle of Sim C and Sim C should be nephew of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_d_parent, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim D was not marked as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_parent, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim C was not marked as nephew of Sim D')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_cousin, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_parent, cause='S4CM: testing cleanup')

    @staticmethod
    @CommonTestService.test()
    def _setting_uncle_should_update_cousins_with_mother() -> None:
        # Uncle
        sim_info_a_uncle: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Nephew
        sim_info_b_nephew: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Cousin
        sim_info_c_cousin: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        # Mother
        sim_info_d_parent: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        try:
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_b_nephew, sim_info_d_parent, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim D as parent of Sim B')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_d_parent, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim B as child of Sim D')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_d_parent, sim_info_b_nephew), 'Failed to set Sim D as biological parent of Sim B')

            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_c_cousin, sim_info_a_uncle, CommonRelationshipBitId.FAMILY_PARENT), 'Failed to set Sim A as parent of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.add_relationship_bit(sim_info_a_uncle, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_SON_DAUGHTER), 'Failed to set Sim C as child of Sim A')
            CommonAssertionUtils.is_true(CommonSimGenealogyUtils.set_as_mother_of(sim_info_a_uncle, sim_info_c_cousin), 'Failed to set Sim A as biological parent of Sim C')

            # Run operation
            CommonAssertionUtils.is_true(S4CMSetSimAAsAuntOrUncleToSimBOp()._mothers_side(sim_info_a_uncle, sim_info_b_nephew), 'Failed to update family tree.')
            S4CMSetSimAAsAuntOrUncleToSimBOp()._add_relationship_bits(sim_info_a_uncle, sim_info_b_nephew)

            # Sim B should be cousin of Sim C and Sim C should be cousin of Sim B
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_b_nephew, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim B was not marked as cousin of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_b_nephew, CommonRelationshipBitId.FAMILY_COUSIN), 'Failed, Sim C was not marked as cousin of Sim B')

            # Sim A should be uncle of Sim C and Sim C should be nephew of Sim A
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_c_cousin, sim_info_d_parent, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), 'Failed, Sim D was not marked as uncle of Sim C')
            CommonAssertionUtils.is_true(CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info_d_parent, sim_info_c_cousin, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW), 'Failed, Sim C was not marked as nephew of Sim D')
        except Exception as ex:
            raise ex
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info_a_uncle, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_b_nephew, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_c_cousin, cause='S4CM: testing cleanup')
            CommonSimSpawnUtils.delete_sim(sim_info_d_parent, cause='S4CM: testing cleanup')

    def _big_family(self) -> None:
        family_one = S4CMFullFamily()
        try:
            pass
        finally:
            family_one.destroy()
