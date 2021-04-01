"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsSiblingToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a sibling of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_BROTHER_SISTER

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_BROTHER_SISTER

    def _update_family_tree(self, new_brother_or_sister_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
            S4CMSetSimAAsMotherToSimBOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
            S4CMSetSimAAsFatherToSimBOp
        father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
        if father_sim_info is not None:
            S4CMSetSimAAsFatherToSimBOp()._update_family_tree(father_sim_info, new_brother_or_sister_sim_info)
        mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
        if mother_sim_info is not None:
            S4CMSetSimAAsMotherToSimBOp()._update_family_tree(mother_sim_info, new_brother_or_sister_sim_info)
        return True

    def _add_relationship_bits(self, new_brother_or_sister_sim_info: SimInfo, sim_info: SimInfo) -> bool:
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
            S4CMSetSimAAsMotherToSimBOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
            S4CMSetSimAAsFatherToSimBOp
        father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
        if father_sim_info is not None:
            S4CMSetSimAAsFatherToSimBOp()._add_relationship_bits(father_sim_info, new_brother_or_sister_sim_info)
        mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
        if mother_sim_info is not None:
            S4CMSetSimAAsMotherToSimBOp()._add_relationship_bits(mother_sim_info, new_brother_or_sister_sim_info)
        return super()._add_relationship_bits(new_brother_or_sister_sim_info, sim_info)
