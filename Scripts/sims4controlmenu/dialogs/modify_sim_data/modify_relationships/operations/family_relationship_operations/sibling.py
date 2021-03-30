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

    # noinspection PyMissingOrEmptyDocstring
    def run(self, new_brother_or_sister_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_yes_selected(_: str, __: Any):
            self._with_family_tree_updates(new_brother_or_sister_sim_info, sim_info)
            on_completed(True)

        def _on_no_selected(_: str, __: Any):
            self._without_family_tree_updates(new_brother_or_sister_sim_info, sim_info)
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

    def _with_family_tree_updates(self, new_brother_or_sister_sim_info: SimInfo, sim_info: SimInfo):
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
        self._without_family_tree_updates(new_brother_or_sister_sim_info, sim_info)

    def _without_family_tree_updates(self, new_brother_or_sister_sim_info: SimInfo, sim_info: SimInfo):
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
