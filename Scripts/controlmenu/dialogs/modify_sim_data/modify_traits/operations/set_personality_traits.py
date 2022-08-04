"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple

from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.option_dialogs.common_choose_objects_option_dialog import CommonChooseObjectsOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
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
from traits.trait_tracker import TraitTracker
from traits.traits import Trait


class CMSetPersonalityTraitsSimOp(CMSingleSimOperation):
    """Add Personality Traits to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_add_personality_traits_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop, current_page: int = 1) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed, current_page=option_dialog.current_page)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_submit(chosen_traits: Tuple[Trait]):
            trait_tracker: TraitTracker = sim_info.trait_tracker
            for personality_trait in trait_tracker.personality_traits:
                CommonTraitUtils.remove_trait(sim_info, personality_trait)

            for chosen_trait in chosen_traits:
                CommonTraitUtils.add_trait(sim_info, chosen_trait)

            # noinspection PyUnresolvedReferences
            CommonBasicNotification(
                CMSimControlMenuStringId.SET_PERSONALITY_TRAITS_TITLE,
                CMSimControlMenuStringId.SET_PERSONALITY_TRAITS_DESCRIPTION,
                description_tokens=(CommonSimUtils.get_sim_instance(sim_info),)
            ).show(icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info)))
            _reopen()

        option_dialog = CommonChooseObjectsOptionDialog(
            CMSimControlMenuStringId.SET_PERSONALITY_TRAITS_MAX,
            0,
            title_tokens=(str(sim_info.trait_tracker.equip_slot_number),),
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        current_personality_trait_ids = [CommonTraitUtils.get_trait_id(pers_trait) for pers_trait in sim_info.trait_tracker.personality_traits]
        self.log.format_with_message('current_personality_traits', current_personality_trait_ids=current_personality_trait_ids)
        all_traits = [personality_trait for (trait_type, personality_trait) in CommonResourceUtils.load_all_instances(Types.TRAIT) if personality_trait.is_personality_trait and personality_trait.is_valid_trait(sim_info)]
        for trait in sorted(all_traits, key=lambda _trait: CommonTraitUtils.get_trait_name(_trait).lower()):
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
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(trait_name, trait.trait_type.name))
                else:
                    # noinspection PyUnresolvedReferences
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(CommonLocalizationUtils.create_localized_string(display_name, tokens=(sim_info,)), trait.trait_type.name))
                display_name = CommonLocalizationUtils.colorize(display_name, CommonLocalizedStringColor.GREEN) if CommonTraitUtils.has_trait(sim_info, trait_id) else display_name
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
                            is_selected=trait_id in current_personality_trait_ids
                        )
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display trait.', trait=trait, trait_name=CommonTraitUtils.get_trait_name(trait), trait_id=trait_id, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(
            sim_info=sim_info,
            page=current_page,
            min_selectable=0,
            max_selectable=sim_info.trait_tracker.equip_slot_number,
            on_submit=_on_submit,
            allow_no_selection=True
        )
        return True
