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
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsGrandfatherOnMothersSideToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a grandfather on mothers side of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_GRANDPARENT

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_GRANDCHILD

    @property
    def _display_name(self) -> int:
        return S4CMSimControlMenuStringId.GRANDFATHER_ON_MOTHERS_SIDE

    # noinspection PyMissingOrEmptyDocstring
    def run(self, new_parent_sim_info: SimInfo, grandchild_sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
            S4CMSetSimAAsFatherToSimBOp
        grandchild_parent = CommonSimGenealogyUtils.get_mother_sim_info(grandchild_sim_info)
        S4CMSetSimAAsFatherToSimBOp().run(new_parent_sim_info, grandchild_parent, on_completed=on_completed)
        return False
