"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils


class CMSetSimAAsPromisedToSimBOp(CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as promised to Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.ROMANTIC_PROMISED

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.ROMANTIC_PROMISED

    @property
    def _should_update_family_tree(self) -> bool:
        return False

    # noinspection PyMissingOrEmptyDocstring
    def is_allowed_between_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> CommonTestResult:
        return CommonRelationshipUtils.has_permission_for_romantic_relationship_with(sim_info_a, sim_info_b)
