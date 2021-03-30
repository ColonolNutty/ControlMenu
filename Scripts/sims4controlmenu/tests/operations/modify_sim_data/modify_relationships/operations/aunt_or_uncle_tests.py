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
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.aunt_or_uncle import \
    S4CMSetSimAAsAuntOrUncleToSimBOp
from sims4controlmenu.modinfo import ModInfo


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


class S4CMFullFamily:
    """A Full Family"""

    def __init__(self) -> None:
        # Father 1 Side:
        self.grandfather_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.grandmother_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.father_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()

        # Father 2 Side:
        self.grandfather_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.grandmother_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_five: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_six: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_seven: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_eight: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.father_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()

        # Mother 1 Side:
        self.grandfather_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.grandmother_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_five: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_six: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_nine: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_ten: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_eleven: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_twelve: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.mother_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()

        # Mother 1 Side:
        self.grandfather_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.grandmother_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_seven: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.uncle_eight: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_thirteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_fourteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_fifteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.cousin_sixteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.mother_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()

        # Children:
        self.child_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.child_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.step_child_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info()
        self.step_child_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info()

    def _setup_relationships(self) -> None:
        # Father 1 Side:
        # Grandfather 1 (Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4)
        # Grandmother 1 (Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4)
        # Uncle 1 (Child of Grandfather 1 and Grandmother 1, Sibling of Father 1 and Uncle 2, Parent of Cousin 1 and Cousin 2, Uncle of Child 1, Child 2, Cousin 3, and Cousin 4)
        # Uncle 2 (Child of Grandfather 1 and Grandmother 1, Sibling of Father 1 and Uncle 1, Parent of Cousin 3 and Cousin 4, Uncle of Child 1, Child 2, Cousin 1, and Cousin 2)
        # Father 1 (Child of Grandfather 1 and Grandmother 1, Sibling of Uncle 1 and Uncle 2, Parent of Child 1, Child 2, and Step Child 2, Uncle of Cousin 1, 2, 3, and 4)
        # Cousin 1 (Child of Uncle 1, Sibling of Cousin 2, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 2 and Father 1)
        # Cousin 2 (Child of Uncle 1, Sibling of Cousin 1, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 2 and Father 1)
        # Cousin 3 (Child of Uncle 2, Sibling of Cousin 4, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 1 and Father 1)
        # Cousin 4 (Child of Uncle 2, Sibling of Cousin 3, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 1 and Father 1)
        self._setup_father_one_side()

        # Father 2 Side:
        # Grandfather 2 (Parent of Father 2, Uncle 3, and Uncle 4, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8)
        # Grandmother 2 (Parent of Father 2, Uncle 3, and Uncle 4, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8)
        # Uncle 3 (Child of Grandfather 2 and Grandmother 2, Sibling of Father 2 and Uncle 4, Parent of Cousin 5 and Cousin 6, Uncle of Step Child 1, Cousin 7, and Cousin 8)
        # Uncle 4 (Child of Grandfather 2 and Grandmother 2, Sibling of Father 2 and Uncle 3, Parent of Cousin 7 and Cousin 8, Uncle of Step Child 1, Cousin 5, and Cousin 6)
        # Father 2 (Child of Grandfather 2 and Grandmother 2, Sibling of Uncle 3 and Uncle 4, Parent of Step Child 1, Uncle of Cousin 5, 6, 7, and 8)
        # Cousin 5 (Child of Uncle 3, Sibling of Cousin 6, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 4 and Father 2)
        # Cousin 6 (Child of Uncle 3, Sibling of Cousin 5, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 4 and Father 2)
        # Cousin 7 (Child of Uncle 4, Sibling of Cousin 8, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 3 and Father 2)
        # Cousin 8 (Child of Uncle 4, Sibling of Cousin 7, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 3 and Father 2)
        self._setup_father_two_side()

        # Mother 1 Side:
        # Grandfather 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12)
        # Grandmother 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12)
        # Uncle 5 (Child of Grandfather 3 and Grandmother 3, Sibling of Mother 1 and Uncle 6, Parent of Cousin 9 and Cousin 10, Uncle of Child 1, Child 2, Cousin 11, and Cousin 12)
        # Uncle 6 (Child of Grandfather 3 and Grandmother 3, Sibling of Mother 1 and Uncle 5, Parent of Cousin 11 and Cousin 12, Uncle of Child 1, Child 2, Cousin 9, and Cousin 10)
        # Mother 1 (Child of Grandfather 3 and Grandmother 3, Sibling of Uncle 5 and Uncle 6, Parent of Child 1, Child 2, and Step Child 1, Uncle of Cousin 9, 10, 11, and 12)
        # Cousin 9 (Child of Uncle 5, Sibling of Cousin 10, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 6 and Mother 1)
        # Cousin 10 (Child of Uncle 5, Sibling of Cousin 9, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 6 and Mother 1)
        # Cousin 11 (Child of Uncle 6, Sibling of Cousin 12, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 5 and Mother 1)
        # Cousin 12 (Child of Uncle 6, Sibling of Cousin 11, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 5 and Mother 1)
        self._setup_mother_one_side()

        # Mother 2 Side:
        # Grandfather 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16)
        # Grandmother 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16)
        # Uncle 7 (Child of Grandfather 4 and Grandmother 4, Sibling of Mother 2 and Uncle 8, Parent of Cousin 13 and Cousin 14, Uncle of Step Child 2, Cousin 15, and Cousin 16)
        # Uncle 8 (Child of Grandfather 4 and Grandmother 4, Sibling of Mother 2 and Uncle 7, Parent of Cousin 15 and Cousin 16, Uncle of Step Child 2, Cousin 13, and Cousin 14)
        # Mother 2 (Child of Grandfather 4 and Grandmother 4, Sibling of Uncle 7 and Uncle 8, Parent of Step Child 2, Uncle of Cousin 13, 14, 15, and 16)
        # Cousin 13 (Child of Uncle 7, Sibling of Cousin 14, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 8 and Mother 2)
        # Cousin 14 (Child of Uncle 7, Sibling of Cousin 13, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 8 and Mother 2)
        # Cousin 15 (Child of Uncle 8, Sibling of Cousin 16, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 7 and Mother 2)
        # Cousin 16 (Child of Uncle 8, Sibling of Cousin 15, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 7 and Mother 2)
        self._setup_mother_two_side()

        # Children:
        # Child 1 (Child of Father 1 and Mother 1, Sibling of Child 2, Step Sibling of Step Child 1 and Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Nephew of Uncle 1, 2, 5, and 6)
        # Child 2 (Child of Father 1 and Mother 1, Sibling of Child 1, Step Sibling of Step Child 1 and Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Nephew of Uncle 1, 2, 5, and 6)
        # Step Child 1 (Child of Mother 1 and Father 2, Step Sibling of Child 1 and Child 2, Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2, Grandfather 3, Grandmother 2, and Grandmother 3, Nephew of Uncle 3, 4, 5, and 6)
        # Step Child 2 (Child of Father 1 and Mother 2, Step Sibling of Child 1 and Child 2, Step Child 1, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1, Grandfather 4, Grandmother 1, and Grandmother 4, Nephew of Uncle 1, 2, 7, and 8)
        self._setup_children()

    def _setup_father_one_side(self) -> None:
        # Grandfather 1 (Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4)
        # Grandmother 1 (Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4)
        grandparents_one_children = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        grandparents_one_grandchildren = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        # Grandfather
        for child in grandparents_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_one, child)

        for grandchild in grandparents_one_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_one, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_father_of(self.grandfather_one, grandchild)

        # Grandmother
        for child in grandparents_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_one, child)

        for grandchild in grandparents_one_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_one, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(self.grandmother_one, grandchild)

        # Uncle 1 (Child of Grandfather 1 and Grandmother 1, Sibling of Father 1 and Uncle 2, Parent of Cousin 1 and Cousin 2, Uncle of Child 1, Child 2, Cousin 3, and Cousin 4)
        uncle_one_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        uncle_one_siblings = (
            self.father_one,
            self.uncle_two
        )

        uncle_one_children = (
            self.cousin_one,
            self.cousin_two
        )

        uncle_one_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_three,
            self.cousin_four
        )

        for parent in uncle_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_one, child)

        for uncle_or_aunt in uncle_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 2 (Child of Grandfather 1 and Grandmother 1, Sibling of Father 1 and Uncle 1, Parent of Cousin 3 and Cousin 4, Uncle of Child 1, Child 2, Cousin 1, and Cousin 2)
        uncle_two_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        uncle_two_siblings = (
            self.father_one,
            self.uncle_one
        )

        uncle_two_children = (
            self.cousin_three,
            self.cousin_four
        )

        uncle_two_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_one,
            self.cousin_two
        )

        for parent in uncle_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_two, child)

        for uncle_or_aunt in uncle_two_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Father 1 (Child of Grandfather 1 and Grandmother 1, Sibling of Uncle 1 and Uncle 2, Parent of Child 1, Child 2, and Step Child 2, Uncle of Cousin 1, 2, 3, and 4)
        father_one_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        father_one_siblings = (
            self.uncle_one,
            self.uncle_two
        )

        father_one_children = (
            self.child_one,
            self.child_two,
            self.step_child_two
        )

        father_one_nephews = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        for parent in father_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in father_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in father_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.father_one, child)

        for uncle_or_aunt in father_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 1 (Child of Uncle 1, Sibling of Cousin 2, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 2 and Father 1)
        cousin_one_parents = (
            self.uncle_one,
        )

        cousin_one_siblings = (
            self.cousin_two,
        )

        cousin_one_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_one_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_one_uncles_and_aunts = (
            self.uncle_two,
            self.father_one
        )

        for parent in cousin_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_one_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_one_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_one_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 2 (Child of Uncle 1, Sibling of Cousin 1, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 2 and Father 1)
        cousin_two_parents = (
            self.uncle_one,
        )

        cousin_two_siblings = (
            self.cousin_one,
        )

        cousin_two_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_two_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_two_uncles_and_aunts = (
            self.uncle_two,
            self.father_one
        )

        for parent in cousin_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_two_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_two_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_two_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 3 (Child of Uncle 2, Sibling of Cousin 4, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 1 and Father 1)
        cousin_three_parents = (
            self.uncle_two,
        )

        cousin_three_siblings = (
            self.cousin_four,
        )

        cousin_three_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_three_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_three_uncles_and_aunts = (
            self.uncle_one,
            self.father_one
        )

        for parent in cousin_three_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_three_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_three_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_three_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_three_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 4 (Child of Uncle 2, Sibling of Cousin 3, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 1 and Father 1)
        cousin_four_parents = (
            self.uncle_two,
        )

        cousin_four_siblings = (
            self.cousin_three,
        )

        cousin_four_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_four_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_four_uncles_and_aunts = (
            self.uncle_one,
            self.father_one
        )

        for parent in cousin_four_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_four_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_four_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_four_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_four_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_father_two_side(self) -> None:
        # Grandfather 2 (Parent of Father 2, Uncle 3, and Uncle 4, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8)
        # Grandmother 2 (Parent of Father 2, Uncle 3, and Uncle 4, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8)
        grandparents_two_children = (
            self.father_two,
            self.uncle_three,
            self.uncle_four
        )

        grandparents_two_grandchildren = (
            self.step_child_one,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight
        )

        # Grandfather
        for child in grandparents_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_two, child)

        for grandchild in grandparents_two_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_two, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_father_of(self.grandfather_two, grandchild)

        # Grandmother
        for child in grandparents_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_two, child)

        for grandchild in grandparents_two_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_two, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(self.grandmother_two, grandchild)

        # Uncle 3 (Child of Grandfather 2 and Grandmother 2, Sibling of Father 2 and Uncle 4, Parent of Cousin 5 and Cousin 6, Uncle of Step Child 1, Cousin 7, and Cousin 8)
        uncle_three_parents = (
            self.grandfather_two,
            self.grandmother_two
        )

        uncle_three_siblings = (
            self.father_two,
            self.uncle_four
        )

        uncle_three_children = (
            self.cousin_five,
            self.cousin_six
        )

        uncle_three_nephews = (
            self.step_child_one,
            self.cousin_seven,
            self.cousin_eight
        )

        for parent in uncle_three_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_three_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_three, child)

        for uncle_or_aunt in uncle_three_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 4 (Child of Grandfather 2 and Grandmother 2, Sibling of Father 2 and Uncle 3, Parent of Cousin 7 and Cousin 8, Uncle of Step Child 1, Cousin 5, and Cousin 6)
        uncle_four_parents = (
            self.grandfather_two,
            self.grandmother_two
        )

        uncle_four_siblings = (
            self.father_two,
            self.uncle_three
        )

        uncle_four_children = (
            self.cousin_seven,
            self.cousin_eight
        )

        uncle_four_nephews = (
            self.step_child_one,
            self.cousin_five,
            self.cousin_six
        )

        for parent in uncle_four_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_four_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_four_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_four, child)

        for uncle_or_aunt in uncle_four_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Father 2 (Child of Grandfather 2 and Grandmother 2, Sibling of Uncle 3 and Uncle 4, Parent of Step Child 1, Uncle of Cousin 5, 6, 7, and 8)
        father_two_parents = (
            self.grandfather_two,
            self.grandmother_two
        )

        father_two_siblings = (
            self.uncle_three,
            self.uncle_four
        )

        father_two_children = (
            self.step_child_one,
        )

        father_two_nephews = (
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight
        )

        for parent in father_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in father_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in father_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.father_two, child)

        for uncle_or_aunt in father_two_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 5 (Child of Uncle 3, Sibling of Cousin 6, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 4 and Father 2)
        cousin_five_parents = (
            self.uncle_three,
        )

        cousin_five_siblings = (
            self.cousin_six,
        )

        cousin_five_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_five_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_five_uncles_and_aunts = (
            self.uncle_four,
            self.father_two
        )

        for parent in cousin_five_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_five_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_five_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_five_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_five_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 6 (Child of Uncle 3, Sibling of Cousin 5, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 4 and Father 2)
        cousin_six_parents = (
            self.uncle_three,
        )

        cousin_six_siblings = (
            self.cousin_five,
        )

        cousin_six_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_six_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_six_uncles_and_aunts = (
            self.uncle_four,
            self.father_two
        )

        for parent in cousin_six_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_six_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_six_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_six_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_six_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 7 (Child of Uncle 4, Sibling of Cousin 8, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 3 and Father 2)
        cousin_seven_parents = (
            self.uncle_four,
        )

        cousin_seven_siblings = (
            self.cousin_eight,
        )

        cousin_seven_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_seven_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_seven_uncles_and_aunts = (
            self.uncle_three,
            self.father_two
        )

        for parent in cousin_seven_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_seven_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_seven_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_seven_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_seven_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 8 (Child of Uncle 4, Sibling of Cousin 7, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2 and Grandmother 2, Nephew of Uncle 3 and Father 2)
        cousin_eight_parents = (
            self.uncle_four,
        )

        cousin_eight_siblings = (
            self.cousin_seven,
        )

        cousin_eight_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_eight_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_eight_uncles_and_aunts = (
            self.uncle_three,
            self.father_two
        )

        for parent in cousin_eight_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_eight_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_eight_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_eight_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_eight_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_mother_one_side(self) -> None:
        # Grandfather 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12)
        # Grandmother 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12)
        grandparents_three_children = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        grandparents_three_grandchildren = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        # Grandfather
        for child in grandparents_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_three, child)

        for grandchild in grandparents_three_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_three, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_father_of(self.grandfather_three, grandchild)

        # Grandmother
        for child in grandparents_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_three, child)

        for grandchild in grandparents_three_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_three, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(self.grandmother_three, grandchild)

        # Uncle 5 (Child of Grandfather 3 and Grandmother 3, Sibling of Mother 1 and Uncle 6, Parent of Cousin 9 and Cousin 10, Uncle of Child 1, Child 2, Cousin 11, and Cousin 12)
        uncle_five_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        uncle_five_siblings = (
            self.mother_one,
            self.uncle_six
        )

        uncle_five_children = (
            self.cousin_nine,
            self.cousin_ten
        )

        uncle_five_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_eleven,
            self.cousin_twelve
        )

        for parent in uncle_five_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_five_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_five_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_five, child)

        for uncle_or_aunt in uncle_five_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 6 (Child of Grandfather 3 and Grandmother 3, Sibling of Mother 1 and Uncle 5, Parent of Cousin 11 and Cousin 12, Uncle of Child 1, Child 2, Cousin 9, and Cousin 10)
        uncle_six_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        uncle_six_siblings = (
            self.mother_one,
            self.uncle_five
        )

        uncle_six_children = (
            self.cousin_eleven,
            self.cousin_twelve
        )

        uncle_six_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_nine,
            self.cousin_ten
        )

        for parent in uncle_six_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_six_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_six_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_six, child)

        for uncle_or_aunt in uncle_six_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Mother 1 (Child of Grandfather 3 and Grandmother 3, Sibling of Uncle 5 and Uncle 6, Parent of Child 1, Child 2, and Step Child 1, Uncle of Cousin 9, 10, 11, and 12)
        mother_one_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        mother_one_siblings = (
            self.uncle_five,
            self.uncle_six
        )

        mother_one_children = (
            self.child_one,
            self.child_two,
            self.step_child_one
        )

        mother_one_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_nine,
            self.cousin_ten
        )

        for parent in mother_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in mother_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in mother_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.mother_one, child)

        for uncle_or_aunt in mother_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 9 (Child of Uncle 5, Sibling of Cousin 10, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 6 and Mother 1)
        cousin_nine_parents = (
            self.uncle_five,
        )

        cousin_nine_siblings = (
            self.cousin_ten,
        )

        cousin_nine_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_nine_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_nine_uncles_and_aunts = (
            self.uncle_six,
            self.mother_one
        )

        for parent in cousin_nine_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_nine_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_nine_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_nine_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_nine_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 10 (Child of Uncle 5, Sibling of Cousin 9, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 6 and Mother 1)
        cousin_ten_parents = (
            self.uncle_five,
        )

        cousin_ten_siblings = (
            self.cousin_nine,
        )

        cousin_ten_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_ten_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_ten_uncles_and_aunts = (
            self.uncle_six,
            self.mother_one
        )

        for parent in cousin_ten_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_ten_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_ten_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_ten_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_ten_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 11 (Child of Uncle 6, Sibling of Cousin 12, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 5 and Mother 1)
        cousin_eleven_parents = (
            self.uncle_six,
        )

        cousin_eleven_siblings = (
            self.cousin_twelve,
        )

        cousin_eleven_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_eleven_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_eleven_uncles_and_aunts = (
            self.uncle_five,
            self.mother_one
        )

        for parent in cousin_eleven_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_eleven_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_eleven_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_eleven_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_eleven_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 12 (Child of Uncle 6, Sibling of Cousin 11, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, and 16, Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 5 and Mother 1)
        cousin_twelve_parents = (
            self.uncle_six,
        )

        cousin_twelve_siblings = (
            self.cousin_eleven,
        )

        cousin_twelve_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_twelve_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_twelve_uncles_and_aunts = (
            self.uncle_five,
            self.mother_one
        )

        for parent in cousin_twelve_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_twelve_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_twelve_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_twelve_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_twelve_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_mother_two_side(self) -> None:
        # Grandfather 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16)
        # Grandmother 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16)
        grandparents_four_children = (
            self.mother_two,
            self.uncle_seven,
            self.uncle_eight
        )

        grandparents_four_grandchildren = (
            self.step_child_two,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        # Grandfather
        for child in grandparents_four_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_four, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_four, child)

        for grandchild in grandparents_four_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_four, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_father_of(self.grandfather_four, grandchild)

        # Grandmother
        for child in grandparents_four_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_four, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_four, child)

        for grandchild in grandparents_four_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_four, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(self.grandmother_four, grandchild)

        # Uncle 7 (Child of Grandfather 4 and Grandmother 4, Sibling of Mother 2 and Uncle 8, Parent of Cousin 13 and Cousin 14, Uncle of Step Child 2, Cousin 15, and Cousin 16)
        uncle_seven_parents = (
            self.grandfather_four,
            self.grandmother_four
        )

        uncle_seven_siblings = (
            self.mother_two,
            self.uncle_eight
        )

        uncle_seven_children = (
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        uncle_seven_nephews = (
            self.step_child_two,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        for parent in uncle_seven_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_seven_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_seven_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_seven, child)

        for uncle_or_aunt in uncle_seven_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 8 (Child of Grandfather 4 and Grandmother 4, Sibling of Mother 2 and Uncle 7, Parent of Cousin 15 and Cousin 16, Uncle of Step Child 2, Cousin 13, and Cousin 14)
        uncle_eight_parents = (
            self.grandfather_four,
            self.grandmother_four
        )

        uncle_eight_siblings = (
            self.mother_two,
            self.uncle_seven
        )

        uncle_eight_children = (
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        uncle_eight_nephews = (
            self.step_child_two,
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        for parent in uncle_eight_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_eight_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in uncle_eight_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_eight, child)

        for uncle_or_aunt in uncle_eight_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Mother 2 (Child of Grandfather 4 and Grandmother 4, Sibling of Uncle 7 and Uncle 8, Parent of Step Child 2, Uncle of Cousin 13, 14, 15, and 16)
        mother_one_parents = (
            self.grandfather_four,
            self.grandmother_four
        )

        mother_one_siblings = (
            self.uncle_seven,
            self.uncle_eight
        )

        mother_one_children = (
            self.step_child_two,
        )

        mother_one_nephews = (
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        for parent in mother_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in mother_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in mother_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.mother_one, child)

        for uncle_or_aunt in mother_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 13 (Child of Uncle 7, Sibling of Cousin 14, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 8 and Mother 2)
        cousin_thirteen_parents = (
            self.uncle_seven,
        )

        cousin_thirteen_siblings = (
            self.cousin_fourteen,
        )

        cousin_thirteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_thirteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_thirteen_uncles_and_aunts = (
            self.uncle_eight,
            self.mother_two
        )

        for parent in cousin_thirteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_thirteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_thirteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_thirteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_thirteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 14 (Child of Uncle 7, Sibling of Cousin 13, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 8 and Mother 2)
        cousin_fourteen_parents = (
            self.uncle_seven,
        )

        cousin_fourteen_siblings = (
            self.cousin_thirteen,
        )

        cousin_fourteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_fourteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_fourteen_uncles_and_aunts = (
            self.uncle_eight,
            self.mother_two
        )

        for parent in cousin_fourteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_fourteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_fourteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_fourteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_fourteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 15 (Child of Uncle 8, Sibling of Cousin 16, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 7 and Mother 2)
        cousin_fifteen_parents = (
            self.uncle_eight,
        )

        cousin_fifteen_siblings = (
            self.cousin_sixteen,
        )

        cousin_fifteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        cousin_fifteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_fifteen_uncles_and_aunts = (
            self.uncle_seven,
            self.mother_two
        )

        for parent in cousin_fifteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_fifteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_fifteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_fifteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_fifteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 16 (Child of Uncle 8, Sibling of Cousin 15, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Nephew of Uncle 7 and Mother 2)
        cousin_sixteen_parents = (
            self.uncle_eight,
        )

        cousin_sixteen_siblings = (
            self.cousin_fifteen,
        )

        cousin_sixteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        cousin_sixteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_sixteen_uncles_and_aunts = (
            self.uncle_seven,
            self.mother_two
        )

        for parent in cousin_sixteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_sixteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_sixteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_sixteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_sixteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_children(self) -> None:
        # Child 1 (Child of Father 1 and Mother 1, Sibling of Child 2, Step Sibling of Step Child 1 and Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Nephew of Uncle 1, 2, 5, and 6)
        child_one_parents = (
            self.father_one,
            self.mother_one
        )

        child_one_siblings = (
            self.child_two,
        )

        child_one_step_siblings = (
            self.step_child_one,
            self.step_child_two,
        )

        child_one_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        child_one_grandparents = (
            self.grandfather_one,
            self.grandfather_three,
            self.grandmother_one,
            self.grandfather_three
        )

        child_one_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_five,
            self.uncle_six
        )

        for parent in child_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in child_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in child_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for cousin in child_one_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in child_one_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in child_one_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Child 2 (Child of Father 1 and Mother 1, Sibling of Child 1, Step Sibling of Step Child 1 and Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Nephew of Uncle 1, 2, 5, and 6)
        child_two_parents = (
            self.father_one,
            self.mother_one
        )

        child_two_siblings = (
            self.child_one,
        )

        child_two_step_siblings = (
            self.step_child_one,
            self.step_child_two,
        )

        child_two_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        child_two_grandparents = (
            self.grandfather_one,
            self.grandfather_three,
            self.grandmother_one,
            self.grandfather_three
        )

        child_two_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_five,
            self.uncle_six
        )

        for parent in child_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in child_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in child_two_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for cousin in child_two_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in child_two_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in child_two_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Step Child 1 (Child of Mother 1 and Father 2, Step Sibling of Child 1 and Child 2, Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 2, Grandfather 3, Grandmother 2, and Grandmother 3, Nephew of Uncle 3, 4, 5, and 6)
        step_child_one_parents = (
            self.mother_one,
            self.father_two
        )

        step_child_one_step_siblings = (
            self.child_one,
            self.child_two,
            self.step_child_two
        )

        step_child_one_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        step_child_one_grandparents = (
            self.grandfather_two,
            self.grandfather_three,
            self.grandmother_two,
            self.grandfather_three
        )

        step_child_one_uncles_and_aunts = (
            self.uncle_three,
            self.uncle_four,
            self.uncle_five,
            self.uncle_six
        )

        for parent in step_child_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_sibling in step_child_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for cousin in step_child_one_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in step_child_one_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in step_child_one_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Step Child 2 (Child of Father 1 and Mother 2, Step Sibling of Child 1 and Child 2, Step Child 1, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1, Grandfather 4, Grandmother 1, and Grandmother 4, Nephew of Uncle 1, 2, 7, and 8)
        step_child_two_parents = (
            self.father_one,
            self.mother_two
        )

        step_child_two_step_siblings = (
            self.child_one,
            self.child_two,
            self.step_child_one
        )

        step_child_two_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        step_child_two_grandparents = (
            self.grandfather_one,
            self.grandfather_four,
            self.grandmother_one,
            self.grandfather_four
        )

        step_child_two_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_seven,
            self.uncle_eight
        )

        for parent in step_child_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_sibling in step_child_two_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for cousin in step_child_two_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in step_child_two_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in step_child_two_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def destroy(self) -> None:
        """destroy()

        Destroy the family and delete all Sims.
        """
        CommonSimSpawnUtils.delete_sim(self.grandfather_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.father_one, cause='S4CM: testing cleanup')

        # Father 2 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_five, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_six, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_seven, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_eight, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.father_two, cause='S4CM: testing cleanup')

        # Mother 1 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_five, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_six, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_nine, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_ten, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_eleven, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_twelve, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.mother_one, cause='S4CM: testing cleanup')

        # Mother 1 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_seven, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_eight, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_thirteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_fourteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_fifteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_sixteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.mother_two, cause='S4CM: testing cleanup')

        # Children:
        CommonSimSpawnUtils.delete_sim(self.child_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.child_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.step_child_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.step_child_two, cause='S4CM: testing cleanup')
