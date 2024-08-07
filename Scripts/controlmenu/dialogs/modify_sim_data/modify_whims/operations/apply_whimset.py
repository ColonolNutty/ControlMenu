"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.commonlib.utils.common_sim_whim_utils import CMCommonSimWhimUtils
from controlmenu.commonlib.utils.common_whim_utils import CMCommonWhimUtils
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from situations.situation_goal import SituationGoal
from whims.whim_set import WhimSetBaseMixin


class _CMFakeActor:
    def __init__(self, sim_info: SimInfo):
        self.sim_info = sim_info


class CMApplyWhimsetSimOp(CMSingleSimOperation):
    """Apply whimset to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_add_by_whimset_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen(*_, **__) -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_whim_id: int, chosen_whimset: WhimSetBaseMixin):
            if chosen_whimset is None:
                on_completed(False)
                return
            CMCommonSimWhimUtils.apply_whimset(sim_info, chosen_whimset)
            _reopen()

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.APPLY_WHIMSET,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        actor = _CMFakeActor(sim_info)
        for whimset in CMCommonWhimUtils.get_all_whim_sets_generator():
            whimset_guid = CMCommonWhimUtils.get_whimset_guid(whimset)
            if whimset_guid is None:
                self.log.format_with_message('Missing whimset id for Whimset.', whimset=whimset)
                continue
            try:
                has_valid_goal = False
                for whim in CMCommonWhimUtils.get_whimset_whims(whimset):
                    # noinspection PyUnresolvedReferences
                    goal: SituationGoal = whim.goal
                    goal_can_be_given = goal.can_be_given_as_goal(actor, None)
                    if goal_can_be_given:
                        has_valid_goal = True
                        break
                if not has_valid_goal:
                    self.log.format_with_message('No available goal found on whimset', whimset=whimset)
                    continue

                display_name = CMCommonWhimUtils.get_whimset_name(whimset)

                description = 0

                icon = CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon is None or icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                option_dialog.add_option(
                    CommonDialogSelectOption(
                        whimset_guid,
                        whimset,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=icon,
                            is_enabled=self.is_whimset_allowed_for_add(whimset)
                        ),
                        on_chosen=_on_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display whimset.', whimset=whimset, whim_name=CMCommonWhimUtils.get_whimset_name(whimset), whimset_id=whimset_guid, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    def is_whimset_allowed_for_add(self, whimset: WhimSetBaseMixin) -> bool:
        """is_whimset_allowed_for_add(whimset)

        Determine if a Whimset is allowed for add via Control Menu or not.

        :param whimset: An instance of a Whimset.
        :type whimset: WhimSetBaseMixin
        :return: True, if the Whimset is allowed for add. False, if not.
        :rtype: bool
        """
        return True
