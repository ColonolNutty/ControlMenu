"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
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
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation


class CMSetSimAAsGrandfatherOnMothersSideToSimBOp(CMSetSimAAsRelationToSimBOperation):
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
        return CMSimControlMenuStringId.GRANDFATHER_ON_MOTHERS_SIDE

    # noinspection PyMissingOrEmptyDocstring
    def get_disabled_text(self, grandparent_sim_info: SimInfo, grandchild_sim_info: SimInfo) -> Union[LocalizedString, None]:
        if not CommonSimGenealogyUtils.has_mother(grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_NEEDS_TO_HAVE_A_RELATION_BEFORE_YOU_CAN_ADD_A_RELATION_TO_THEM, tokens=(grandchild_sim_info, CMSimControlMenuStringId.MOTHER, self.get_display_name(grandparent_sim_info, grandchild_sim_info)))
        if CommonSimGenealogyUtils.is_father_of(grandparent_sim_info, grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_CANNOT_BE_BOTH_RELATION_AND_RELATION_OF_SIM, tokens=(grandparent_sim_info, CMSimControlMenuStringId.FATHER, self.get_display_name(grandchild_sim_info, grandparent_sim_info), grandchild_sim_info))
        if CommonSimGenealogyUtils.is_mother_of(grandparent_sim_info, grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_CANNOT_BE_BOTH_RELATION_AND_RELATION_OF_SIM, tokens=(grandparent_sim_info, CMSimControlMenuStringId.MOTHER, self.get_display_name(grandchild_sim_info, grandparent_sim_info), grandchild_sim_info))
        return super().get_disabled_text(grandparent_sim_info, grandchild_sim_info)

    # noinspection PyMissingOrEmptyDocstring
    def run(self, grandparent_sim_info: SimInfo, grandchild_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        result = CommonSimGenealogyUtils.set_as_mothers_father_of(grandparent_sim_info, grandchild_sim_info)
        if on_completed is not None:
            on_completed(result)
        return result
