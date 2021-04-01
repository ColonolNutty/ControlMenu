"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation
from sims4controlmenu.enums.string_identifiers import S4CMStringId


class S4CMSetSimAAsGrandchildToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a grandchild of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_GRANDCHILD

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_GRANDPARENT

    # noinspection PyMissingOrEmptyDocstring
    def get_disabled_text(self, grandchild_sim_info: SimInfo, grandparent_sim_info: SimInfo) -> Union[LocalizedString, None]:
        if not CommonSimGenealogyUtils.has_mother(grandchild_sim_info) and not CommonSimGenealogyUtils.has_father(grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.SIM_NEEDS_TO_HAVE_A_RELATION_OR_RELATION_BEFORE_YOU_CAN_ADD_A_RELATION_TO_THEM, tokens=(grandchild_sim_info, S4CMSimControlMenuStringId.FATHER, S4CMSimControlMenuStringId.MOTHER, self.get_opposite_display_name(grandchild_sim_info, grandparent_sim_info)))
        if CommonSimGenealogyUtils.is_father_of(grandparent_sim_info, grandchild_sim_info):
            return CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.SIM_CANNOT_BE_BOTH_RELATION_AND_RELATION_OF_SIM, tokens=(grandparent_sim_info, S4CMSimControlMenuStringId.FATHER, self.get_opposite_display_name(grandchild_sim_info, grandparent_sim_info), grandchild_sim_info))
        return super().get_disabled_text(grandchild_sim_info, grandparent_sim_info)

    # noinspection PyMissingOrEmptyDocstring
    def run(self, grandchild_sim_info: SimInfo, grandparent_sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_bit_chosen(_: Any, chosen_operation: S4CMSetSimAAsRelationToSimBOperation):
            if _ is None or chosen_operation is None:
                return
            if chosen_operation.has_relation(grandparent_sim_info, grandchild_sim_info):
                on_completed(True)
                return

            def _on_yes_selected(_: Any):
                chosen_operation.run(grandparent_sim_info, grandchild_sim_info, on_completed=on_completed)

            def _on_no_selected(_: Any):
                self.run(grandchild_sim_info, grandparent_sim_info, on_completed=on_completed)

            confirmation = CommonOkCancelDialog(
                S4CMStringId.CONFIRMATION,
                S4CMSimControlMenuStringId.SIM_WILL_BECOME_RELATIONSHIP_TO_SIM_CONFIRMATION_TEXT,
                description_tokens=(grandparent_sim_info, chosen_operation.get_display_name(grandchild_sim_info, grandparent_sim_info), grandchild_sim_info),
                ok_text_identifier=S4CMStringId.YES,
                cancel_text_identifier=S4CMStringId.NO
            )
            confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)
            return True

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            S4CMSimControlMenuStringId.CHOOSE_FAMILY_RELATION,
            S4CMSimControlMenuStringId.CHOOSE_WHAT_SIM_WILL_BECOME_TO_SIM,
            description_tokens=(grandparent_sim_info, grandchild_sim_info),
            include_previous_button=True,
            on_previous=lambda: on_completed(False),
            on_close=lambda: on_completed(False)
        )

        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandfather_on_fathers_side import \
            S4CMSetSimAAsGrandfatherOnFathersSideToSimBOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandfather_on_mothers_side import \
            S4CMSetSimAAsGrandfatherOnMothersSideToSimBOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandmother_on_fathers_side import \
            S4CMSetSimAAsGrandmotherOnFathersSideToSimBOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandmother_on_mothers_side import \
            S4CMSetSimAAsGrandmotherOnMothersSideToSimBOp

        relationship_operations = (
            S4CMSetSimAAsGrandfatherOnFathersSideToSimBOp(),
            S4CMSetSimAAsGrandfatherOnMothersSideToSimBOp(),
            S4CMSetSimAAsGrandmotherOnFathersSideToSimBOp(),
            S4CMSetSimAAsGrandmotherOnMothersSideToSimBOp()
        )

        for relationship_operation in relationship_operations:
            relationship_operation: S4CMSetSimAAsRelationToSimBOperation = relationship_operation
            display_name = relationship_operation.get_display_name(grandchild_sim_info, grandparent_sim_info)
            has_relation = relationship_operation.has_relation(grandparent_sim_info, grandchild_sim_info)
            option_dialog.add_option(
                CommonDialogButtonOption(
                    str(relationship_operation.relationship_bit_id),
                    relationship_operation,
                    CommonDialogResponseOptionContext(
                        CommonLocalizationUtils.colorize(display_name, CommonLocalizedStringColor.GREEN) if has_relation else display_name,
                        disabled_text_identifier=relationship_operation.get_disabled_text(grandparent_sim_info, grandchild_sim_info)
                    ),
                    on_chosen=_on_bit_chosen
                )
            )

        if not option_dialog.has_options():
            on_completed(False)
            return False

        option_dialog.show(sim_info=grandparent_sim_info)
        return True
