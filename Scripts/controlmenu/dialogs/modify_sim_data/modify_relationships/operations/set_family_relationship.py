"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Tuple

from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.engaged import \
    CMSetSimAAsEngagedToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.girlfriend_or_boyfriend import \
    CMSetSimAAsGirlfriendOrBoyfriendToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.promised import \
    CMSetSimAAsPromisedToSimBOp
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sim_option_dialog import \
    CommonPremadeChooseSimOptionDialog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.aunt_or_uncle import \
    CMSetSimAAsAuntOrUncleToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.child import \
    CMSetSimAAsChildToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.cousin import \
    CMSetSimAAsCousinToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.father import \
    CMSetSimAAsFatherToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandchild import \
    CMSetSimAAsGrandchildToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandfather_on_fathers_side import \
    CMSetSimAAsGrandfatherOnFathersSideToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandfather_on_mothers_side import \
    CMSetSimAAsGrandfatherOnMothersSideToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandmother_on_fathers_side import \
    CMSetSimAAsGrandmotherOnFathersSideToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.grandmother_on_mothers_side import \
    CMSetSimAAsGrandmotherOnMothersSideToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.husband_or_wife import \
    CMSetSimAAsHusbandOrWifeToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.mother import \
    CMSetSimAAsMotherToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.niece_or_nephew import \
    CMSetSimAAsNieceOrNephewToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.sibling import \
    CMSetSimAAsSiblingToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.step_sibling import \
    CMSetSimAAsStepSiblingToSimBOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId


class CMSetFamilyRelationsBitOp(CMSingleSimOperation):
    """Set a relationship level between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_family_relations'

    @property
    def _relation_operations(self) -> Tuple[CMSetSimAAsRelationToSimBOperation]:
        result: Tuple[CMSetSimAAsRelationToSimBOperation, ...] = (
            CMSetSimAAsAuntOrUncleToSimBOp(),
            CMSetSimAAsChildToSimBOp(),
            CMSetSimAAsCousinToSimBOp(),
            CMSetSimAAsFatherToSimBOp(),
            CMSetSimAAsGrandchildToSimBOp(),
            CMSetSimAAsGrandfatherOnFathersSideToSimBOp(),
            CMSetSimAAsGrandfatherOnMothersSideToSimBOp(),
            CMSetSimAAsGrandmotherOnFathersSideToSimBOp(),
            CMSetSimAAsGrandmotherOnMothersSideToSimBOp(),
            CMSetSimAAsHusbandOrWifeToSimBOp(),
            CMSetSimAAsGirlfriendOrBoyfriendToSimBOp(),
            CMSetSimAAsEngagedToSimBOp(),
            CMSetSimAAsPromisedToSimBOp(),
            CMSetSimAAsMotherToSimBOp(),
            CMSetSimAAsNieceOrNephewToSimBOp(),
            CMSetSimAAsSiblingToSimBOp(),
            CMSetSimAAsStepSiblingToSimBOp(),
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_chosen(chosen_sim_info: SimInfo) -> None:
            if chosen_sim_info is None:
                on_completed(False)
                return
            self.run_with_sims(sim_info, chosen_sim_info, on_completed=on_completed)

        def _is_allowed(target_sim_info: SimInfo):
            return self.can_run_with_sims(sim_info, target_sim_info)

        dialog = CommonPremadeChooseSimOptionDialog(
            CMSimControlMenuStringId.SET_FAMILY_RELATIONS,
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

    # noinspection PyMissingOrEmptyDocstring
    def can_run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        return super().can_run_with_sims(sim_info_a, sim_info_b) and sim_info_a is not sim_info_b and CommonRelationshipUtils.has_permission_to_be_blood_relative_of(sim_info_a, sim_info_b)

    # noinspection PyMissingOrEmptyDocstring
    def run_with_sims(self, sim_info: SimInfo, chosen_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop):
        def _on_none_chosen(_: Any, __: Any):
            try:
                CommonSimGenealogyUtils.remove_family_relations_with(sim_info, chosen_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(chosen_sim_info, sim_info)
            except Exception as ex:
                self.log.error('Failed to remove family relations', exception=ex)
            self.run_with_sims(sim_info, chosen_sim_info, on_completed=on_completed)

        def _on_bit_chosen(_: Any, chosen_operation: CMSetSimAAsRelationToSimBOperation):
            if _ is None or chosen_operation is None:
                return
            if chosen_operation.has_relation(sim_info, chosen_sim_info):
                self.run_with_sims(sim_info, chosen_sim_info, on_completed=on_completed)
                return

            def _on_yes_selected(_: Any):
                if chosen_operation is None:
                    self.run_with_sims(sim_info, chosen_sim_info, on_completed=on_completed)
                    return

                def _on_completed(___: bool):
                    self.run_with_sims(sim_info, chosen_sim_info, on_completed=on_completed)

                chosen_operation.run(sim_info, chosen_sim_info, on_completed=_on_completed)

            def _on_no_selected(_: Any):
                self.run_with_sims(sim_info, chosen_sim_info, on_completed=on_completed)

            confirmation = CommonOkCancelDialog(
                CMStringId.CONFIRMATION,
                CMSimControlMenuStringId.SIM_WILL_BECOME_RELATIONSHIP_TO_SIM_CONFIRMATION_TEXT,
                description_tokens=(sim_info, chosen_operation.get_display_name(chosen_sim_info, sim_info), chosen_sim_info),
                ok_text_identifier=CMStringId.YES,
                cancel_text_identifier=CMStringId.NO
            )
            confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)
            return True

        option_dialog = CommonChooseButtonOptionDialog(
            ModInfo.get_identity(),
            CMSimControlMenuStringId.CHOOSE_FAMILY_RELATION,
            CMSimControlMenuStringId.CHOOSE_WHAT_SIM_WILL_BECOME_TO_SIM,
            description_tokens=(sim_info, chosen_sim_info),
            include_previous_button=True,
            on_previous=lambda: on_completed(False),
            on_close=lambda: on_completed(False)
        )

        options = list()
        has_a_relation = False
        for relationship_operation in self._relation_operations:
            relationship_operation: CMSetSimAAsRelationToSimBOperation = relationship_operation
            display_name = relationship_operation.get_display_name(chosen_sim_info, sim_info)
            has_relation = relationship_operation.has_relation(sim_info, chosen_sim_info)
            if has_relation:
                has_a_relation = True
            options.append(
                CommonDialogButtonOption(
                    str(relationship_operation.relationship_bit_id),
                    relationship_operation,
                    CommonDialogResponseOptionContext(
                        CommonLocalizationUtils.colorize(display_name, CommonLocalizedStringColor.GREEN) if has_relation else display_name,
                        disabled_text_identifier=relationship_operation.get_disabled_text(sim_info, chosen_sim_info)
                    ),
                    on_chosen=_on_bit_chosen
                )
            )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'None',
                None,
                CommonDialogResponseOptionContext(
                    CommonLocalizationUtils.colorize(CMStringId.NONE, CommonLocalizedStringColor.GREEN) if not has_a_relation else CMStringId.NONE,
                ),
                on_chosen=_on_none_chosen
            )
        )

        for option in options:
            option_dialog.add_option(option)

        if not option_dialog.has_options():
            on_completed(False)
            return

        option_dialog.show(sim_info=sim_info)
