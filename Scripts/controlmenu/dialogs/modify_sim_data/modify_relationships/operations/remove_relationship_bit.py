"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from relationships.relationship_bit import RelationshipBit
from relationships.relationship_tracker import RelationshipTracker
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sim_option_dialog import \
    CommonPremadeChooseSimOptionDialog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMRemoveRelationshipBitOp(CMSingleSimOperation):
    """Remove relationship bits between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_remove_relationship_bit'

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
            CMSimControlMenuStringId.REMOVE_RELATIONSHIP_BIT,
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
    def run_with_sims(self, sim_info: SimInfo, chosen_sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop):
        def _on_close() -> None:
            on_completed(False)

        def _reopen() -> None:
            self.run_with_sims(sim_info, chosen_sim_info, on_completed=on_completed)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.REMOVE_RELATIONSHIP_BIT,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_option_chosen(_: str, _relationship_bit: RelationshipBit):
            if _relationship_bit is None:
                _on_close()
                return
            self.log.format_with_message('Removing relationship bits from Sims', _relationship_bit=_relationship_bit, sim=sim_info, chosen_sim=chosen_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, chosen_sim_info, _relationship_bit)
            _reopen()

        sim = CommonSimUtils.get_sim_instance(sim_info)
        chosen_sim = CommonSimUtils.get_sim_instance(chosen_sim_info)
        relationship_tracker: RelationshipTracker = sim_info.relationship_tracker
        for relationship_bit in relationship_tracker.get_all_bits(target_sim_id=CommonSimUtils.get_sim_id(chosen_sim_info)):
            relationship_bit: RelationshipBit = relationship_bit
            display_name_value = relationship_bit.display_name
            if display_name_value:
                display_name = display_name_value(sim, chosen_sim)
            else:
                display_name = relationship_bit.__name__

            description_value = relationship_bit.bit_description
            if description_value:
                description = description_value(sim, chosen_sim)
            else:
                description = 0

            # noinspection PyUnresolvedReferences
            icon = relationship_bit.icon or CommonIconUtils.load_question_mark_icon()
            # MISSING ICON Identifier
            _MISSING_IMAGE_ICON_ID = 3526464109639239417
            if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                icon = CommonIconUtils.load_question_mark_icon()
            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(getattr(relationship_bit, 'guid64')),
                    relationship_bit,
                    CommonDialogOptionContext(
                        CommonLocalizationUtils.combine_localized_strings((display_name, relationship_bit.__name__), separator=CommonLocalizedStringSeparator.SPACE_PARENTHESIS_SURROUNDED),
                        description,
                        icon=icon,
                    ),
                    on_chosen=_on_option_chosen
                )
            )

        if not option_dialog.has_options():
            self.log.format_with_message('No relationship bits available for the Sim!', sim=sim_info)
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True
