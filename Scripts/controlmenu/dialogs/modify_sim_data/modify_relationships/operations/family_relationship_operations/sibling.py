"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation


class CMSetSimAAsSiblingToSimBOp(CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a sibling of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_BROTHER_SISTER

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_BROTHER_SISTER

    def _update_family_tree(self, new_brother_or_sister_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
            CMSetSimAAsMotherToSimBOp
        from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
            CMSetSimAAsFatherToSimBOp
        father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
        if father_sim_info is not None:
            CMSetSimAAsFatherToSimBOp()._update_family_tree(father_sim_info, new_brother_or_sister_sim_info)
        mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
        if mother_sim_info is not None:
            CMSetSimAAsMotherToSimBOp()._update_family_tree(mother_sim_info, new_brother_or_sister_sim_info)
        return True

    def _add_relationship_bits(self, new_brother_or_sister_sim_info: SimInfo, sim_info: SimInfo) -> CommonExecutionResult:
        from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
            CMSetSimAAsMotherToSimBOp
        from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
            CMSetSimAAsFatherToSimBOp
        father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
        if father_sim_info is not None:
            CMSetSimAAsFatherToSimBOp()._add_relationship_bits(father_sim_info, new_brother_or_sister_sim_info)
        mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
        if mother_sim_info is not None:
            CMSetSimAAsMotherToSimBOp()._add_relationship_bits(mother_sim_info, new_brother_or_sister_sim_info)
        return super()._add_relationship_bits(new_brother_or_sister_sim_info, sim_info)
