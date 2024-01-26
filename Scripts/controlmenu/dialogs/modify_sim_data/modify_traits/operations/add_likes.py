"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.enums.trait_ids import CMTraitId
from traits.trait_type import TraitType
from traits.traits import Trait


class CMAddLikesSimOp(CMSingleSimOperation):
    """Add Likes to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_add_likes_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop, current_page: int = 1) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed, current_page=option_dialog.current_page)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_trait_id: int, chosen_trait: Trait):
            if chosen_trait is None:
                on_completed(False)
                return

            if CommonTraitUtils.has_trait(sim_info, _trait_id):
                CommonTraitUtils.remove_trait(sim_info, _trait_id)
                # noinspection PyUnresolvedReferences
                CommonBasicNotification(
                    CMSimControlMenuStringId.REMOVED_TRAIT_TITLE,
                    CMSimControlMenuStringId.REMOVED_TRAIT_DESCRIPTION,
                    title_tokens=(chosen_trait.display_name(sim_info), str(_trait_id)),
                    description_tokens=(CommonSimUtils.get_sim_instance(sim_info), chosen_trait.display_name(sim_info), str(_trait_id), CommonTraitUtils.get_trait_name(chosen_trait))
                ).show(icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info)))
            else:
                _trait = CommonTraitUtils.load_trait_by_id(_trait_id)
                if hasattr(_trait, 'conflicting_traits') and _trait.conflicting_traits:
                    for conflicting_trait in _trait.conflicting_traits:
                        CommonTraitUtils.remove_trait(sim_info, conflicting_trait)
                modify_result = CommonTraitUtils.add_trait(sim_info, _trait_id)

                if not modify_result:
                    # noinspection PyUnresolvedReferences
                    CommonBasicNotification(
                        CMSimControlMenuStringId.FAILED_TO_ADD_TRAIT_TITLE,
                        CMSimControlMenuStringId.FAILED_TO_ADD_TRAIT_DESCRIPTION,
                        title_tokens=(chosen_trait.display_name(sim_info), str(_trait_id)),
                        description_tokens=(CommonSimUtils.get_sim_instance(sim_info), chosen_trait.display_name(sim_info), str(_trait_id), CommonTraitUtils.get_trait_name(chosen_trait))
                    ).show(icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info)))
                else:
                    # noinspection PyUnresolvedReferences
                    CommonBasicNotification(
                        CMSimControlMenuStringId.ADDED_TRAIT_TITLE,
                        CMSimControlMenuStringId.ADDED_TRAIT_DESCRIPTION,
                        title_tokens=(chosen_trait.display_name(sim_info), str(_trait_id)),
                        description_tokens=(CommonSimUtils.get_sim_instance(sim_info), chosen_trait.display_name(sim_info), str(_trait_id), CommonTraitUtils.get_trait_name(chosen_trait))
                    ).show(icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info)))
            _reopen()

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.MODIFY_LIKES,
            CMSimControlMenuStringId.MODIFY_LIKES_DISLIKES_DESCRIPTION,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        for (trait_guid, trait) in CommonResourceUtils.load_all_instances_as_guid_to_instance(Types.TRAIT, return_type=Trait).items():
            if trait_guid is None:
                self.log.format_with_message('Missing trait id for Trait.', trait=trait)
                continue
            if trait.trait_type in (TraitType.PERSONALITY, TraitType.GENDER_OPTIONS):
                self.log.format_with_message('No showing trait due to it being a personality trait.', trait=trait)
                continue
            if trait.trait_type not in (TraitType.LIKE,):
                self.log.format_with_message('No showing trait due to it not being a Likes trait.', trait=trait)
                continue
            if not trait.is_valid_trait(sim_info):
                self.log.format_with_message('No showing trait due to it being unavailable for Sim.', trait=trait, sim=sim_info)
                continue
            try:
                # noinspection PyUnresolvedReferences
                display_name = trait.display_name(sim_info)
                if display_name.hash == 0:
                    trait_name = CommonTraitUtils.get_trait_name(trait) or 'Unknown Trait Name'
                    trait_name = trait_name[0].upper() + trait_name[1:]
                    # noinspection PyUnresolvedReferences
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(trait_name, trait.trait_type.name))
                else:
                    # noinspection PyUnresolvedReferences
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(CommonLocalizationUtils.create_localized_string(display_name, tokens=(sim_info,)), trait.trait_type.name))

                if CommonTraitUtils.has_trait(sim_info, trait_guid):
                    display_name = CommonLocalizationUtils.colorize(display_name, CommonLocalizedStringColor.GREEN)

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
                        trait_guid,
                        trait,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=icon,
                            is_enabled=self.is_trait_allowed_for_addition(trait)
                        ),
                        on_chosen=_on_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display trait.', trait=trait, trait_name=CommonTraitUtils.get_trait_name(trait), trait_id=trait_guid, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True, page=current_page)
        return True

    def is_trait_allowed_for_addition(self, trait: Trait) -> bool:
        """is_trait_allowed_for_addition(trait)

        Determine if a trait is allowed for removal via Control Menu or not.

        :param trait: An instance of a Trait.
        :type trait: Trait
        :return: True, if the trait is allowed for removal. False, if not.
        :rtype: bool
        """
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
            CMTraitId.CONTROL_MENU_MAIN,
            CMTraitId.CONTROLLABLE_HUMAN_SIM,
            CMTraitId.CONTROLLABLE_LARGE_DOG_SIM,
            CMTraitId.CONTROLLABLE_SMALL_DOG_SIM,
            CMTraitId.CONTROLLABLE_CAT_SIM,
            CMTraitId.CONTROLLABLE_FOX_SIM
        )
