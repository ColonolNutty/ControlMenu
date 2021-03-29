"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Tuple
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sim_option_dialog import \
    CommonPremadeChooseSimOptionDialog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.commonlib.utils.common_sim_family_tree_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.aunt_or_uncle import \
    S4CMSetSimAAsAuntOrUncleToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.child import \
    S4CMSetSimAAsChildToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.cousin import \
    S4CMSetSimAAsCousinToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
    S4CMSetSimAAsFatherToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandchild import \
    S4CMSetSimAAsGrandchildToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandfather_on_fathers_side import \
    S4CMSetSimAAsGrandfatherOnFathersSideToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandfather_on_mothers_side import \
    S4CMSetSimAAsGrandfatherOnMothersSideToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandmother_on_fathers_side import \
    S4CMSetSimAAsGrandmotherOnFathersSideToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandmother_on_mothers_side import \
    S4CMSetSimAAsGrandmotherOnMothersSideToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.husband_or_wife import \
    S4CMSetSimAAsHusbandOrWifeToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
    S4CMSetSimAAsMotherToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.niece_or_nephew import \
    S4CMSetSimAAsNieceOrNephewToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.sibling import \
    S4CMSetSimAAsSiblingToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.step_sibling import \
    S4CMSetSimAAsStepSiblingToSimBOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.enums.string_identifiers import S4CMStringId
from sims4controlmenu.settings.setting_utils import S4CMSettingUtils


class S4CMSetFamilyRelationsBitOp(S4CMSingleSimOperation):
    """Set a relationship level between two Sims."""

    @property
    def _relation_operations(self) -> Tuple[S4CMSetSimAAsRelationToSimBOperation]:
        result: Tuple[S4CMSetSimAAsRelationToSimBOperation] = (
            S4CMSetSimAAsAuntOrUncleToSimBOp(),
            S4CMSetSimAAsChildToSimBOp(),
            S4CMSetSimAAsCousinToSimBOp(),
            S4CMSetSimAAsFatherToSimBOp(),
            S4CMSetSimAAsGrandchildToSimBOp(),
            S4CMSetSimAAsGrandfatherOnFathersSideToSimBOp(),
            S4CMSetSimAAsGrandfatherOnMothersSideToSimBOp(),
            S4CMSetSimAAsGrandmotherOnFathersSideToSimBOp(),
            S4CMSetSimAAsGrandmotherOnMothersSideToSimBOp(),
            S4CMSetSimAAsHusbandOrWifeToSimBOp(),
            S4CMSetSimAAsMotherToSimBOp(),
            S4CMSetSimAAsNieceOrNephewToSimBOp(),
            S4CMSetSimAAsSiblingToSimBOp(),
            S4CMSetSimAAsStepSiblingToSimBOp(),
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_chosen(chosen_sim_info: SimInfo) -> None:
            if chosen_sim_info is None:
                on_completed(False)
                return

            def _on_none_chosen(_: Any, __: Any):
                try:
                    CommonSimGenealogyUtils.remove_family_relation_to(sim_info, chosen_sim_info)
                except Exception as ex:
                    self.log.error('Failed to remove family relations', exception=ex)
                _on_chosen(chosen_sim_info)

            def _on_bit_chosen(_: Any, chosen_operation: S4CMSetSimAAsRelationToSimBOperation):
                if _ is None or chosen_operation is None:
                    return
                if chosen_operation.has_relation(sim_info, chosen_sim_info):
                    _on_chosen(chosen_sim_info)

                def _on_yes_selected(_: Any):
                    if chosen_operation is None:
                        _on_chosen(chosen_sim_info)

                    def _on_completed(___: bool):
                        _on_chosen(chosen_sim_info)

                    chosen_operation.run(sim_info, chosen_sim_info, on_completed=_on_completed)

                def _on_no_selected(_: Any):
                    _on_chosen(chosen_sim_info)

                confirmation = CommonOkCancelDialog(
                    S4CMStringId.CONFIRMATION,
                    S4CMSimControlMenuStringId.SIM_WILL_BECOME_RELATIONSHIP_TO_SIM_CONFIRMATION_TEXT,
                    description_tokens=(sim_info, chosen_operation._display_name_override, chosen_sim_info),
                    ok_text_identifier=S4CMStringId.YES,
                    cancel_text_identifier=S4CMStringId.NO
                )
                confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)
                return True

            option_dialog = CommonChooseButtonOptionDialog(
                ModInfo.get_identity(),
                S4CMSimControlMenuStringId.CHOOSE_FAMILY_RELATION,
                S4CMSimControlMenuStringId.CHOOSE_WHAT_SIM_WILL_BECOME_TO_SIM,
                description_tokens=(sim_info, chosen_sim_info),
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

            for relationship_operation in self._relation_operations:
                relationship_operation: S4CMSetSimAAsRelationToSimBOperation = relationship_operation
                relationship_option = relationship_operation.relationship_option
                display_name = relationship_option.get_display_name(sim_info, chosen_sim_info)
                has_relation = relationship_operation.has_relation(chosen_sim_info, sim_info)
                option_dialog.add_option(
                    CommonDialogButtonOption(
                        str(relationship_option.relationship_bit_id),
                        relationship_operation,
                        CommonDialogResponseOptionContext(
                            CommonLocalizationUtils.colorize(display_name, CommonLocalizedStringColor.GREEN) if has_relation else display_name
                        ),
                        on_chosen=_on_bit_chosen
                    )
                )

            if not option_dialog.has_options():
                on_completed(False)
                return

            option_dialog.show(sim_info=sim_info)

        def _is_allowed(target_sim_info: SimInfo):
            return sim_info is not target_sim_info and S4CMSettingUtils.are_allowed_family_relationship_bits(sim_info, target_sim_info)

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
