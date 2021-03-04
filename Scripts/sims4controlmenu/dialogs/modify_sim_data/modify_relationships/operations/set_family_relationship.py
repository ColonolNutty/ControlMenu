"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple, Any, List, Dict

from protocolbuffers.Localization_pb2 import LocalizedString
from relationships.relationship_bit import RelationshipBit
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sim_option_dialog import \
    CommonPremadeChooseSimOptionDialog
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.enums.string_identifiers import S4CMStringId


class S4CMRelationshipBitOption:
    """Used for displaying relationship options."""
    def __init__(self, display_name: LocalizedString, relationship_bit_id: int):
        self.display_name = display_name
        self.relationship_bit_id = relationship_bit_id


class S4CMSetFamilyRelationsBitOp(S4CMSingleSimOperation):
    """Set a relationship level between two Sims."""

    @property
    def _relationship_bits(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonRelationshipBitId.FAMILY_BROTHER_SISTER,
            CommonRelationshipBitId.FAMILY_SON_DAUGHTER,
            CommonRelationshipBitId.FAMILY_GRANDCHILD,
            CommonRelationshipBitId.FAMILY_GRANDPARENT,
            CommonRelationshipBitId.FAMILY_PARENT,
            CommonRelationshipBitId.FAMILY_STEP_SIBLING,
            CommonRelationshipBitId.FAMILY_COUSIN,
            CommonRelationshipBitId.FAMILY_AUNT_UNCLE,
            CommonRelationshipBitId.FAMILY_NIECE_NEPHEW,
            CommonRelationshipBitId.FAMILY_HUSBAND_WIFE
        )
        return result

    @property
    def _relationship_bit_to_opposite_mapping(self) -> Dict[int, int]:
        result: Dict[int, int] = {
            CommonRelationshipBitId.FAMILY_BROTHER_SISTER: CommonRelationshipBitId.FAMILY_BROTHER_SISTER,
            CommonRelationshipBitId.FAMILY_SON_DAUGHTER: CommonRelationshipBitId.FAMILY_PARENT,
            CommonRelationshipBitId.FAMILY_GRANDCHILD: CommonRelationshipBitId.FAMILY_GRANDPARENT,
            CommonRelationshipBitId.FAMILY_GRANDPARENT: CommonRelationshipBitId.FAMILY_GRANDCHILD,
            CommonRelationshipBitId.FAMILY_PARENT: CommonRelationshipBitId.FAMILY_SON_DAUGHTER,
            CommonRelationshipBitId.FAMILY_STEP_SIBLING: CommonRelationshipBitId.FAMILY_STEP_SIBLING,
            CommonRelationshipBitId.FAMILY_COUSIN: CommonRelationshipBitId.FAMILY_COUSIN,
            CommonRelationshipBitId.FAMILY_AUNT_UNCLE: CommonRelationshipBitId.FAMILY_NIECE_NEPHEW,
            CommonRelationshipBitId.FAMILY_NIECE_NEPHEW: CommonRelationshipBitId.FAMILY_AUNT_UNCLE,
            CommonRelationshipBitId.FAMILY_HUSBAND_WIFE: CommonRelationshipBitId.FAMILY_HUSBAND_WIFE
        }
        return result

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_chosen(chosen_sim_info: SimInfo) -> None:
            if chosen_sim_info is None:
                on_completed(False)
                return
            relationship_options = self._load_relationship_options(sim_info, chosen_sim_info)
            if not relationship_options:
                on_completed(False)
                return

            def _on_none_chosen(_: Any, __: Any):
                self._remove_other_relationship_bits(sim_info, chosen_sim_info)
                _on_chosen(chosen_sim_info)

            def _on_bit_chosen(_: Any, chosen_option: S4CMRelationshipBitOption):
                if _ is None or chosen_option is None:
                    return
                self._remove_other_relationship_bits(sim_info, chosen_sim_info)
                result = CommonRelationshipUtils.add_relationship_bit(sim_info, chosen_sim_info, chosen_option.relationship_bit_id)
                if result:
                    opposite_relationship_bit_id = self._relationship_bit_to_opposite_mapping.get(chosen_option.relationship_bit_id, -1)
                    if opposite_relationship_bit_id != -1:
                        CommonRelationshipUtils.add_relationship_bit(chosen_sim_info, sim_info, opposite_relationship_bit_id)
                _on_chosen(chosen_sim_info)

            option_dialog = CommonChooseButtonOptionDialog(
                ModInfo.get_identity(),
                S4CMSimControlMenuStringId.CHOOSE_FAMILY_RELATION,
                0,
                include_previous_button=True,
                on_previous=lambda: on_completed(False),
                on_close=lambda: on_completed(False)
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'None',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMStringId.NONE
                    ),
                    on_chosen=_on_none_chosen
                )
            )

            for relationship_option in relationship_options:
                option_dialog.add_option(
                    CommonDialogButtonOption(
                        str(relationship_option.relationship_bit_id),
                        relationship_option,
                        CommonDialogResponseOptionContext(
                            CommonLocalizationUtils.colorize(relationship_option.display_name, CommonLocalizedStringColor.GREEN) if CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info, chosen_sim_info, relationship_option.relationship_bit_id) else relationship_option.display_name
                        ),
                        on_chosen=_on_bit_chosen
                    )
                )

            if not option_dialog.has_options():
                on_completed(False)
                return

            option_dialog.show(sim_info=sim_info)

        def _is_allowed(target_sim_info: SimInfo):
            return sim_info is not target_sim_info

        dialog = CommonPremadeChooseSimOptionDialog(
            S4CMSimControlMenuStringId.SET_FAMILY_RELATIONS,
            0,
            title_tokens=(sim_info,),
            include_sim_callback=_is_allowed,
            instanced_sims_only=False,
            mod_identity=ModInfo.get_identity(),
            on_sim_chosen=_on_chosen,
            on_close=lambda: on_completed(False)
        )
        if not dialog.has_options():
            on_completed(False)
            return False
        # Sort the Sims in the dialog by their name.
        dialog._internal_dialog._rows = tuple(sorted(dialog._internal_dialog._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
        dialog.show(sim_info=sim_info)
        return True

    def _remove_other_relationship_bits(self, sim_info_a: SimInfo, sim_info_b: SimInfo):
        for relationship_bit_id in self._relationship_bits:
            CommonRelationshipUtils.remove_relationship_bit(sim_info_a, sim_info_b, relationship_bit_id)
            CommonRelationshipUtils.remove_relationship_bit(sim_info_b, sim_info_a, relationship_bit_id)

    def _load_relationship_options(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Tuple[S4CMRelationshipBitOption]:
        relationship_options: List[S4CMRelationshipBitOption] = list()
        for relationship_bit_id in self._relationship_bits:
            relationship_bit: RelationshipBit = CommonResourceUtils.load_instance(Types.RELATIONSHIP_BIT, relationship_bit_id)
            if relationship_bit is None:
                continue
            # noinspection PyUnresolvedReferences
            bit_display_name = relationship_bit.display_name
            bit_display_name = CommonLocalizationUtils.create_localized_string(bit_display_name, tokens=(sim_info_a, sim_info_b))
            relationship_options.append(S4CMRelationshipBitOption(bit_display_name, relationship_bit_id))
        return tuple(relationship_options)
