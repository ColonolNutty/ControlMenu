"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.enums.string_identifiers import S4CMStringId
from sims4controlmenu.enums.trait_ids import S4CMTraitId
from traits.traits import Trait


class S4CMRemoveTraitsSimOp(S4CMSingleSimOperation):
    """Remove Traits from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_remove_traits_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_trait_id: int, chosen_trait: Trait):
            if chosen_trait is None:
                on_completed(False)
                return

            def _on_yes_selected(_: Any):
                CommonTraitUtils.remove_trait(sim_info, _trait_id)
                # noinspection PyUnresolvedReferences
                CommonBasicNotification(
                    S4CMSimControlMenuStringId.REMOVED_TRAIT_TITLE,
                    S4CMSimControlMenuStringId.REMOVED_TRAIT_DESCRIPTION,
                    title_tokens=(chosen_trait.display_name(sim_info), str(_trait_id)),
                    description_tokens=(CommonSimUtils.get_sim_instance(sim_info), chosen_trait.display_name(sim_info), str(_trait_id), CommonTraitUtils.get_trait_name(chosen_trait))
                ).show(icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info)))
                _reopen()

            def _on_no_selected(_: Any):
                _reopen()

            # noinspection PyUnresolvedReferences
            confirmation = CommonOkCancelDialog(
                S4CMStringId.CONFIRMATION,
                S4CMSimControlMenuStringId.ARE_YOU_SURE_YOU_WANT_TO_REMOVE_TRAIT,
                description_tokens=(chosen_trait.display_name(sim_info), str(_trait_id), CommonTraitUtils.get_trait_name(chosen_trait), CommonSimUtils.get_sim_instance(sim_info)),
                ok_text_identifier=S4CMStringId.YES,
                cancel_text_identifier=S4CMStringId.NO
            )
            confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)

        option_dialog = CommonChooseObjectOptionDialog(
            S4CMSimControlMenuStringId.REMOVE_TRAITS,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        for trait in CommonTraitUtils.get_traits(sim_info):
            trait: Trait = trait
            trait_id = CommonTraitUtils.get_trait_id(trait)
            if trait_id is None:
                self.log.format_with_message('Missing trait id for Trait.', trait=trait)
                continue
            try:
                # noinspection PyUnresolvedReferences
                display_name = trait.display_name(sim_info)
                if display_name.hash == 0:
                    trait_name = CommonTraitUtils.get_trait_name(trait) or 'Unknown Trait Name'
                    trait_name = trait_name[0].upper() + trait_name[1:]
                    # noinspection PyUnresolvedReferences
                    display_name = CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(trait_name, trait.trait_type.name))
                else:
                    # noinspection PyUnresolvedReferences
                    display_name = CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(CommonLocalizationUtils.create_localized_string(display_name, tokens=(sim_info,)), trait.trait_type.name))
                # noinspection PyUnresolvedReferences
                description = CommonLocalizationUtils.create_localized_string(trait.trait_description._string_id, tokens=(sim_info,))
                # noinspection PyUnresolvedReferences
                icon = trait.icon or CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                option_dialog.add_option(
                    CommonDialogSelectOption(
                        trait_id,
                        trait,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=icon,
                            is_enabled=self._is_trait_allowed_for_removal(trait)
                        ),
                        on_chosen=_on_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display trait.', trait=trait, trait_name=CommonTraitUtils.get_trait_name(trait), trait_id=trait_id, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    def _is_trait_allowed_for_removal(self, trait: Trait) -> bool:
        trait_id = CommonTraitUtils.get_trait_id(trait)
        if trait_id is None:
            self.log.format_with_message('Missing trait id for Trait.', trait=trait)
            return False
        return trait_id not in (
            CommonTraitId.BABY,
            CommonTraitId.TODDLER,
            CommonTraitId.CHILD,
            CommonTraitId.YOUNG_ADULT,
            CommonTraitId.ADULT,
            CommonTraitId.ELDER,
            CommonTraitId.GENDER_FEMALE,
            CommonTraitId.GENDER_MALE,
            CommonTraitId.SPECIES_HUMAN,
            CommonTraitId.SPECIES_EXTENDED_SMALL_DOGS,
            CommonTraitId.SPECIES_EXTENDED_LARGE_DOGS,
            CommonTraitId.SPECIES_DOG,
            CommonTraitId.SPECIES_CAT,
            CommonTraitId.SPECIES_FOX,
            CommonTraitId.OCCULT_MERMAID,
            CommonTraitId.OCCULT_MERMAID_TYAE,
            CommonTraitId.OCCULT_NO_OCCULT,
            CommonTraitId.OCCULT_ROBOT,
            CommonTraitId.OCCULT_VAMPIRE,
            CommonTraitId.OCCULT_WITCH,
            CommonTraitId.OCCULT_ALIEN,
            CommonTraitId.BATUU_ALIEN,
            CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
            CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
            CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
            CommonTraitId.S4CL_MAIN_TRAIT_CAT,
            CommonTraitId.S4CL_MAIN_TRAIT_FOX,
            S4CMTraitId.S4CM_CONTROLLABLE_HUMAN_SIM,
            S4CMTraitId.S4CM_CONTROLLABLE_LARGE_DOG_SIM,
            S4CMTraitId.S4CM_CONTROLLABLE_SMALL_DOG_SIM,
            S4CMTraitId.S4CM_CONTROLLABLE_CAT_SIM,
            S4CMTraitId.S4CM_CONTROLLABLE_FOX_SIM
        )
