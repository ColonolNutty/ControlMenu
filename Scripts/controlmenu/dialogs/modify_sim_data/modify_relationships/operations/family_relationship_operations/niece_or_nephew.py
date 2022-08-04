"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Callable

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation


class CMSetSimAAsNieceOrNephewToSimBOp(CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a niece or nephew of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_NIECE_NEPHEW

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_AUNT_UNCLE

    # noinspection PyMissingOrEmptyDocstring
    def get_disabled_text(self, new_niece_or_nephew_sim_info: SimInfo, new_aunt_or_uncle_sim_info: SimInfo) -> Union[LocalizedString, None]:
        if not CommonSimGenealogyUtils.has_mother(new_niece_or_nephew_sim_info) and not CommonSimGenealogyUtils.has_father(new_niece_or_nephew_sim_info):
            return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_NEEDS_TO_HAVE_MOTHER_OR_FATHER_BEFORE_YOU_CAN_ADD_UNCLES_OR_AUNTS_TO_THEM, tokens=(new_niece_or_nephew_sim_info,))
        return super().get_disabled_text(new_niece_or_nephew_sim_info, new_aunt_or_uncle_sim_info)

    # noinspection PyMissingOrEmptyDocstring
    def run(self, new_niece_or_nephew_sim_info: SimInfo, new_aunt_or_uncle_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.aunt_or_uncle import \
            CMSetSimAAsAuntOrUncleToSimBOp
        return CMSetSimAAsAuntOrUncleToSimBOp().run(new_aunt_or_uncle_sim_info, new_niece_or_nephew_sim_info, on_completed=on_completed)
