"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Dict, Tuple

from cas.cas_preference_item import CasPreferenceItem
from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_objects_option_dialog import CommonChooseObjectsOptionDialog
from sims4communitylib.dialogs.option_dialogs.common_multi_pane_choose_option_dialog import \
    CommonMultiPaneChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import \
    CommonDialogObjectOption
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


class CMModifyLikesDislikesSimOp(CMSingleSimOperation):
    """Add Likes to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_likes_dislikes_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(True)

        def _on_submit(chosen_options: Dict[int, Tuple[int]]):
            _likes_traits = chosen_options[0]
            _dislikes_traits = chosen_options[1]

            for _trait_id in traits:
                CommonTraitUtils.remove_trait(sim_info, _trait_id)

            for _liked_trait in _likes_traits:
                CommonTraitUtils.add_trait(sim_info, _liked_trait)

            for _disliked_trait in _dislikes_traits:
                CommonTraitUtils.add_trait(sim_info, _disliked_trait)
            _reopen()

        sub_dialog_one = CommonChooseObjectsOptionDialog(
            CMSimControlMenuStringId.LIKES,
            CMSimControlMenuStringId.LIKES_DESCRIPTION,
            mod_identity=self.mod_identity
        )

        sub_dialog_two = CommonChooseObjectsOptionDialog(
            CMSimControlMenuStringId.DISLIKES,
            CMSimControlMenuStringId.DISLIKES_DESCRIPTION,
            mod_identity=self.mod_identity
        )

        sim = CommonSimUtils.get_sim_instance(sim_info)
        count = 0

        traits = list()

        likes_dislikes = list()

        for sim_preference_item in CommonResourceUtils.load_all_instance_values(Types.CAS_PREFERENCE_ITEM):
            sim_preference_item: CasPreferenceItem = sim_preference_item
            like_trait = sim_preference_item.like
            dislike_trait = sim_preference_item.dislike

            likes_dislikes.append((sim_preference_item, like_trait, dislike_trait))

        for (_sim_preference_item, _like_trait, _dislike_trait) in sorted(tuple(likes_dislikes), key=lambda f: CommonTraitUtils.get_trait_name(f[1])):
            like_trait_id = CommonTraitUtils.get_trait_id(_like_trait)
            dislike_trait_id = CommonTraitUtils.get_trait_id(_dislike_trait)
            traits.append(like_trait_id)
            traits.append(dislike_trait_id)

            like_display_name = _like_trait.display_name(sim)
            likes_description = _like_trait.trait_description
            dislike_display_name = _dislike_trait.display_name(sim)
            dislike_description = _dislike_trait.trait_description

            # noinspection PyTypeChecker
            sub_dialog_one.add_option(
                CommonDialogObjectOption(
                    str(_like_trait),
                    _like_trait,
                    CommonDialogOptionContext(
                        CommonLocalizationUtils.colorize(like_display_name, CommonLocalizedStringColor.GREEN),
                        likes_description(sim),
                        icon=CommonIconUtils.load_arrow_right_icon(),
                        is_selected=CommonTraitUtils.has_trait(sim_info, like_trait_id),
                        tooltip_text_identifier=_sim_preference_item.tooltip
                    )
                )
            )

            # noinspection PyTypeChecker
            sub_dialog_two.add_option(
                CommonDialogObjectOption(
                    str(_dislike_trait),
                    _dislike_trait,
                    CommonDialogOptionContext(
                        CommonLocalizationUtils.colorize(dislike_display_name, CommonLocalizedStringColor.RED),
                        dislike_description(sim),
                        icon=CommonIconUtils.load_arrow_right_icon(),
                        is_selected=CommonTraitUtils.has_trait(sim_info, dislike_trait_id),
                        tooltip_text_identifier=_sim_preference_item.tooltip
                    )
                )
            )
            count += 1

        option_dialog = CommonMultiPaneChooseOptionDialog(
            self.mod_identity,
            CMSimControlMenuStringId.LIKES_DISLIKES,
            CMSimControlMenuStringId.LIKES_DISLIKES_DESCRIPTION,
            description_tokens=(sim_info,),
            on_close=_on_close
        )

        option_dialog.add_sub_dialog(sub_dialog_one, min_selectable=0, max_selectable=count)
        option_dialog.add_sub_dialog(sub_dialog_two, min_selectable=0, max_selectable=count)

        option_dialog.show(
            on_submit=_on_submit,
            sim_info=sim_info
        )
        return True
