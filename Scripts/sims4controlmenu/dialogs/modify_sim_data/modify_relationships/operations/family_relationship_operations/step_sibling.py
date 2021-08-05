"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsStepSiblingToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a step sibling of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_STEP_SIBLING

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_STEP_SIBLING

    def _update_family_tree(self, step_sibling_sim_info_a: SimInfo, step_sibling_sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_selected(_: str, operation: Any):
            if operation is None:
                on_completed(False)
                return
            operation(step_sibling_sim_info_a, step_sibling_sim_info_b, on_completed=on_completed)

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            S4CMSimControlMenuStringId.WHICH_PARENT_IS_SHARED,
            S4CMSimControlMenuStringId.WHICH_PARENT_IS_SHARED_DESCRIPTION,
            description_tokens=(step_sibling_sim_info_b, step_sibling_sim_info_a),
            include_previous_button=True
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Mother',
                self._share_mother,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.MOTHER
                ),
                on_chosen=_on_selected
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Father',
                self._share_father,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.FATHER
                ),
                on_chosen=_on_selected
            )
        )

        option_dialog.show()
        return True

    def _share_mother(self, step_sibling_sim_info_a: SimInfo, step_sibling_sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
            S4CMSetSimAAsMotherToSimBOp
        mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(step_sibling_sim_info_b)
        if mother_sim_info is None:
            on_completed(False)
            return False
        return S4CMSetSimAAsMotherToSimBOp().run(mother_sim_info, step_sibling_sim_info_a, on_completed=on_completed)

    def _share_father(self, step_sibling_sim_info_a: SimInfo, step_sibling_sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
            S4CMSetSimAAsFatherToSimBOp
        father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(step_sibling_sim_info_b)
        if father_sim_info is None:
            on_completed(False)
            return False
        return S4CMSetSimAAsFatherToSimBOp().run(father_sim_info, step_sibling_sim_info_a, on_completed=on_completed)
