"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
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


class S4CMSetSimAAsGrandfatherOnFathersSideToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a grandfather on fathers side of Sim B"""

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
        return S4CMSimControlMenuStringId.GRANDFATHER_ON_FATHERS_SIDE

    # noinspection PyMissingOrEmptyDocstring
    def run(self, new_parent_sim_info: SimInfo, grandchild_sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        if CommonSimGenealogyUtils.has_father(grandchild_sim_info):
            from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
                S4CMSetSimAAsFatherToSimBOp
            grandchild_father = CommonSimGenealogyUtils.get_father_sim_info(grandchild_sim_info)
            return S4CMSetSimAAsFatherToSimBOp().run(new_parent_sim_info, grandchild_father, on_completed=on_completed)
        else:
            def _on_yes_selected(_: str, __: Any):
                def _on_family_tree_updated(result: bool):
                    if result:
                        self._add_relationship_bits(new_parent_sim_info, grandchild_sim_info)
                    on_completed(result)

                self._update_family_tree(new_parent_sim_info, grandchild_sim_info, on_completed=_on_family_tree_updated)

            def _on_no_selected(_: str, __: Any):
                self._add_relationship_bits(new_parent_sim_info, grandchild_sim_info)
                on_completed(True)

            option_dialog = CommonChooseButtonOptionDialog(
                self.mod_identity,
                S4CMSimControlMenuStringId.UPDATE_FAMILY_TREE_TITLE,
                S4CMSimControlMenuStringId.UPDATE_FAMILY_TREE_DESCRIPTION,
                previous_button_text=S4CMStringId.CANCEL,
                include_previous_button=True,
                on_previous=lambda: on_completed(False),
                on_close=lambda: on_completed(False)
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Yes',
                    'YES',
                    CommonDialogResponseOptionContext(
                        S4CMStringId.YES
                    ),
                    on_chosen=_on_yes_selected
                )
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'No',
                    'NO',
                    CommonDialogResponseOptionContext(
                        S4CMStringId.NO
                    ),
                    on_chosen=_on_no_selected
                )
            )

            option_dialog.show()
            return True

    def _update_family_tree(self, sim_info_a: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        on_completed(True)
        return True
