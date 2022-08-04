"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation


class CMSetSimAAsChildToSimBOp(CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a child of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_SON_DAUGHTER

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_PARENT

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info_a: SimInfo, new_parent_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_selected(_: str, operation: Any):
            if operation is None:
                on_completed(False)
                return
            operation(sim_info_a, new_parent_sim_info, on_completed=on_completed)

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            CMSimControlMenuStringId.CHOOSE_FAMILY_RELATION,
            CMSimControlMenuStringId.CHOOSE_WHAT_SIM_WILL_BECOME_TO_SIM,
            description_tokens=(new_parent_sim_info, sim_info_a),
            include_previous_button=True
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Mother',
                self._as_mother,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.MOTHER
                ),
                on_chosen=_on_selected
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Father',
                self._as_father,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.FATHER
                ),
                on_chosen=_on_selected
            )
        )

        option_dialog.show()
        return True

    def _as_mother(self, child_sim_info: SimInfo, parent_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
            CMSetSimAAsMotherToSimBOp
        return CMSetSimAAsMotherToSimBOp().run(parent_sim_info, child_sim_info, on_completed=on_completed)

    def _as_father(self, child_sim_info: SimInfo, parent_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
            CMSetSimAAsFatherToSimBOp
        return CMSetSimAAsFatherToSimBOp().run(parent_sim_info, child_sim_info, on_completed=on_completed)
