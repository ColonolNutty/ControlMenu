"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.commonlib.utils.common_sim_whim_utils import CMCommonSimWhimUtils
from controlmenu.commonlib.utils.common_whim_utils import CMCommonWhimUtils
from controlmenu.modinfo import ModInfo
from event_testing.results import TestResult
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from situations.situation_goal import SituationGoal
from situations.situation_goal_targeted_sim import SituationGoalRanInteractionOnTargetedSim
from whims.whim import Whim
from whims.whims_tracker import WhimType


class _CMFakeActor:
    def __init__(self, sim_info: SimInfo):
        self.sim_info = sim_info


class CMAddWhimsSimOp(CMSingleSimOperation):
    """Add Whims to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_add_whims_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen(*_, **__) -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_: str, chosen_whim_type: WhimType):
            if chosen_whim_type is None:
                on_completed(False)
                return
            self._choose_whim_for_slot(sim_info, chosen_whim_type, on_completed=_reopen)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.CHOOSE_A_WHIM_SLOT,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        for whim_type in WhimType.values:
            if whim_type == WhimType.INVALID:
                continue
            try:
                option_dialog.add_option(
                    CommonDialogSelectOption(
                        whim_type.name,
                        whim_type,
                        CommonDialogOptionContext(
                            whim_type.name,
                            0,
                            icon=CommonIconUtils.load_arrow_navigate_into_icon()
                        ),
                        on_chosen=_on_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display whim type.', whim_type=whim_type, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    # noinspection PyMissingOrEmptyDocstring
    def _choose_whim_for_slot(self, sim_info: SimInfo, whim_type: WhimType, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self._choose_whim_for_slot(sim_info, whim_type, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_whim_id: int, chosen_whim: Whim):
            if chosen_whim is None:
                on_completed(False)
                return
            _whim_name = CMCommonWhimUtils.get_whim_name(chosen_whim)
            # CMCommonSimWhimUtils.remove_whim_by_type(sim_info, whim_type)
            whims_tracker = CMCommonSimWhimUtils.get_whim_tracker(sim_info)
            whims_tracker.debug_activate_whim(chosen_whim)
            # whim_sets = CMCommonWhimUtils.get_all_whim_sets_by_whim_generator(chosen_whim)
            _reopen()

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.ADD_WHIMS_WHIM_TYPE,
            0,
            title_tokens=(whim_type.name,),
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _whim_matches_whim_type(_whim: Whim) -> bool:
            # noinspection PyUnresolvedReferences
            return _whim.type == whim_type

        actor = _CMFakeActor(sim_info)
        for whim in CMCommonWhimUtils.get_all_whims_generator(include_whim_callback=_whim_matches_whim_type):
            # noinspection PyUnresolvedReferences
            goal: SituationGoal = whim.goal
            whim_guid = CMCommonWhimUtils.get_whim_guid(whim)
            if whim_guid is None:
                self.log.format_with_message('Missing whim id for Whim.', whim=whim)
                continue
            try:
                goal_can_be_given = goal.can_be_given_as_goal(actor, None)
                if not goal_can_be_given:
                    self.log.format_with_message('Goal cannot be given to Sim.', sim=sim_info, whim=whim, result=goal_can_be_given)
                    continue
                tuning_name = CMCommonWhimUtils.get_whim_name(whim) or 'Unknown Whim Name'

                if goal._display_data:
                    display_name = goal._display_data.instance_display_name
                else:
                    display_name = goal.get_display_name()

                display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(display_name, tuning_name))

                description = whim.fluff_description
                if description is not None:
                    description = description()

                icon = goal.display_icon or CommonIconUtils.load_question_mark_icon()
                if goal._display_data:
                    icon = goal._display_data.instance_display_secondary_icon or icon
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon is None or icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                option_dialog.add_option(
                    CommonDialogSelectOption(
                        whim_guid,
                        whim,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=icon,
                            is_enabled=self.is_whim_allowed_for_add(whim)
                        ),
                        on_chosen=_on_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display whim.', whim=whim, whim_name=CMCommonWhimUtils.get_whim_name(whim), whim_id=whim_guid, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    def is_whim_allowed_for_add(self, whim: Whim) -> bool:
        """is_whim_allowed_for_add(whim)

        Determine if a whim is allowed for add via Control Menu or not.

        :param whim: An instance of a Whim.
        :type whim: Whim
        :return: True, if the whim is allowed for add. False, if not.
        :rtype: bool
        """
        return True


_log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'cm_whims')
# _log.enable()


# @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SituationGoalRanInteractionOnTargetedSim, SituationGoalRanInteractionOnTargetedSim._can_sim_pass_test.__name__)
def _cm_can_sim_pass_test(original, cls, target_sim_info, actor_sim_info, inherited_target_sim_info) -> TestResult:
    original_result = original(target_sim_info, actor_sim_info, inherited_target_sim_info)
    if not original_result:
        _log.format_with_message('Failed whim with Sim', target_sim=target_sim_info, actor_sim=actor_sim_info, inherited_target_sim_info=inherited_target_sim_info, result=original_result, whim=cls)
    return original_result
