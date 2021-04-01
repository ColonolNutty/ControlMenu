"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsGrandmotherOnFathersSideToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a grandmother on fathers side of Sim B"""

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
        return S4CMSimControlMenuStringId.GRANDMOTHER_ON_FATHERS_SIDE

    # noinspection PyMissingOrEmptyDocstring
    def get_disabled_text(self, grandparent_sim_info: SimInfo, grandchild_sim_info: SimInfo) -> Union[LocalizedString, None]:
        if not CommonSimGenealogyUtils.has_father(grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.SIM_NEEDS_TO_HAVE_A_RELATION_BEFORE_YOU_CAN_ADD_A_RELATION_TO_THEM, tokens=(grandchild_sim_info, S4CMSimControlMenuStringId.FATHER, self.get_display_name(grandparent_sim_info, grandchild_sim_info)))
        if CommonSimGenealogyUtils.is_father_of(grandparent_sim_info, grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.SIM_CANNOT_BE_BOTH_RELATION_AND_RELATION_OF_SIM, tokens=(grandparent_sim_info, S4CMSimControlMenuStringId.FATHER, self.get_display_name(grandchild_sim_info, grandparent_sim_info), grandchild_sim_info))
        if CommonSimGenealogyUtils.is_mother_of(grandparent_sim_info, grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.SIM_CANNOT_BE_BOTH_RELATION_AND_RELATION_OF_SIM, tokens=(grandparent_sim_info, S4CMSimControlMenuStringId.MOTHER, self.get_display_name(grandchild_sim_info, grandparent_sim_info), grandchild_sim_info))
        return super().get_disabled_text(grandparent_sim_info, grandchild_sim_info)

    # noinspection PyMissingOrEmptyDocstring
    def run(self, grandparent_sim_info: SimInfo, grandchild_sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
            S4CMSetSimAAsMotherToSimBOp
        parent_sim_info = CommonSimGenealogyUtils.get_father_sim_info(grandchild_sim_info)
        return S4CMSetSimAAsMotherToSimBOp().run(grandparent_sim_info, parent_sim_info, on_completed=on_completed)
