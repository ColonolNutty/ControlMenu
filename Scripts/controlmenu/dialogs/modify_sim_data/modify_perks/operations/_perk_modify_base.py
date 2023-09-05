"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from bucks.bucks_enums import BucksType
from bucks.bucks_perk import BucksPerk
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from event_testing.resolver import SingleSimResolver
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.sims.common_sim_bucks_utils import CommonSimBucksUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CMPerkModifyOp(CMSingleSimOperation):
    """Modify perks."""
    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_perk'

    @property
    def bucks_perk_type(self) -> Union[BucksType, None]:
        """The type of bucks perk."""
        raise NotImplementedError()

    # <T ev="12289">RetailBucks</T>
    # <T ev="40961">VampirePowerBucks</T>
    # <T ev="40962">VampireWeaknessBucks</T>
    # <T ev="57345">VetBucks</T>
    # <T ev="64">ClubBucks</T>
    # <T ev="65">RestaurantBucks</T>
    # <T ev="66">RecycleBitsBucks</T>
    # <T ev="67">RecyclePiecesBucks</T>
    # <T ev="61441">FamePerkBucks</T>
    # <T ev="61442">FameQuirkBucks</T>
    # <T ev="49153">WitchPerkBucks</T>
    # <T ev="67587">InfluenceBuck</T>
    # <T ev="51201">GalacticCredits</T>
    # <T ev="135169">WerewolfAbilityBucks</T>
    # <T ev="135170">WerewolfQuestAbilityBucks</T>

    @property
    def title(self) -> int:
        """The title of the dialog."""
        raise NotImplementedError()

    @property
    def is_add(self) -> bool:
        """Whether this will add or remove perks."""
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:

        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(True)

        option_dialog = CommonChooseObjectOptionDialog(
            self.title,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=500
        )

        def _on_chosen(_: str, _bucks_perk: BucksPerk):
            if _bucks_perk is None:
                _on_close()
                return
            self._modify_perk(sim_info, _bucks_perk)
            _reopen()

        sim = CommonSimUtils.get_sim_instance(sim_info)
        for available_buck_perk in CommonSimBucksUtils.get_available_perks_gen(sim_info, self.bucks_perk_type):
            available_buck_perk: BucksPerk = available_buck_perk
            has_perk_unlocked = CommonSimBucksUtils.has_perk_unlocked(sim_info, available_buck_perk)
            display_name = available_buck_perk.display_name(sim)
            tooltip = None
            is_enabled = True
            if self.is_add:
                if has_perk_unlocked:
                    is_enabled = False
            else:
                if not has_perk_unlocked:
                    is_enabled = False
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(CMSimControlMenuStringId.PERK_NOT_UNLOCKED)
            if self.is_add and available_buck_perk.required_unlocks:
                missing_required_perk_display_names = list()
                for required_perk in available_buck_perk.required_unlocks:
                    if not CommonSimBucksUtils.has_perk_unlocked(sim_info, required_perk):
                        is_enabled = False
                        missing_required_perk_display_names.append(required_perk.display_name(sim))
                if missing_required_perk_display_names:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(CommonLocalizationUtils.combine_localized_strings((CMSimControlMenuStringId.REQUIRED_PERKS_ARE_NOT_UNLOCKED, CommonLocalizationUtils.combine_localized_strings(missing_required_perk_display_names, separator=CommonLocalizedStringSeparator.COMMA_SPACE)), separator=CommonLocalizedStringSeparator.COLON_SPACE))
            if self.is_add and available_buck_perk.conflicting_perks:
                conflicting_perk_display_names = list()
                for conflicting_perk in available_buck_perk.conflicting_perks:
                    if CommonSimBucksUtils.has_perk_unlocked(sim_info, conflicting_perk):
                        is_enabled = False
                        conflicting_perk_display_names.append(conflicting_perk.display_name(sim))

                if conflicting_perk_display_names:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(CommonLocalizationUtils.combine_localized_strings((CMSimControlMenuStringId.CONFLICTING_PERKS_ALREADY_UNLOCKED, CommonLocalizationUtils.combine_localized_strings(conflicting_perk_display_names, separator=CommonLocalizedStringSeparator.COMMA_SPACE)), separator=CommonLocalizedStringSeparator.COLON_SPACE))
            resolver = SingleSimResolver(sim_info)
            if is_enabled:
                if self.is_add and available_buck_perk.available_for_puchase_tests:
                    available_result = available_buck_perk.available_for_puchase_tests.run_tests(resolver=resolver, search_for_tooltip=True)
                    if not available_result:
                        tooltip = available_result.tooltip
            if has_perk_unlocked:
                display_name = CommonLocalizationUtils.colorize(display_name, text_color=CommonLocalizedStringColor.GREEN)
            description = available_buck_perk.perk_description(sim)
            if available_buck_perk.icon:
                icon = CommonIconUtils._load_icon(available_buck_perk.icon.key)
            else:
                icon = None
            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(available_buck_perk.guid64),
                    available_buck_perk,
                    CommonDialogOptionContext(
                        display_name,
                        description,
                        tooltip_text_identifier=tooltip,
                        icon=icon,
                        is_enabled=is_enabled
                    ),
                    on_chosen=_on_chosen
                )
            )

        option_dialog.show(sort_options=True)
        return True

    # noinspection PyMissingOrEmptyDocstring
    def can_run_with_sim(self, sim_info: SimInfo) -> bool:
        return super().can_run_with_sim(sim_info) and self.bucks_perk_type is not None

    def _modify_perk(self, sim_info: SimInfo, bucks_perk: BucksPerk):
        raise NotImplementedError()


class CMPerkAddOp(CMPerkModifyOp):
    """Add a perk."""
    @property
    def bucks_perk_type(self) -> Union[BucksType, None]:
        """The type of bucks perk."""
        raise NotImplementedError()

    @property
    def title(self) -> int:
        """The title of the dialog."""
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def is_add(self) -> bool:
        return True

    def _modify_perk(self, sim_info: SimInfo, bucks_perk: BucksPerk):
        CommonSimBucksUtils.unlock_perk(sim_info, bucks_perk, no_cost=True)


class CMPerkRemoveOp(CMPerkModifyOp):
    """Remove a perk."""
    @property
    def bucks_perk_type(self) -> Union[BucksType, None]:
        """The type of bucks perk."""
        raise NotImplementedError()

    @property
    def title(self) -> int:
        """The title of the dialog."""
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def is_add(self) -> bool:
        return False

    def _modify_perk(self, sim_info: SimInfo, bucks_perk: BucksPerk):
        CommonSimBucksUtils.lock_perk(sim_info, bucks_perk, refund_cost=False)
