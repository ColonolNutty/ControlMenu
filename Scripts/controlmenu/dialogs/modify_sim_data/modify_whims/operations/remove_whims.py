"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from controlmenu.commonlib.utils.common_sim_whim_utils import CMCommonSimWhimUtils
from controlmenu.commonlib.utils.common_whim_utils import CMCommonWhimUtils
from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId
from situations.situation_goal import SituationGoal
from whims.whim import Whim


class CMRemoveWhimsSimOp(CMSingleSimOperation):
    """Remove Whims from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_remove_whims_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_whim_id: int, chosen_whim: Whim):
            if chosen_whim is None:
                on_completed(False)
                return
            _whim_name = CMCommonWhimUtils.get_whim_name(chosen_whim)

            def _on_yes_selected(_: Any):
                CMCommonSimWhimUtils.remove_whim(sim_info, _whim_id)
                CommonBasicNotification(
                    CMSimControlMenuStringId.REMOVED_WHIM_TITLE,
                    CMSimControlMenuStringId.REMOVED_WHIM_DESCRIPTION,
                    title_tokens=(_whim_name, str(_whim_id)),
                    description_tokens=(CommonSimUtils.get_sim_instance(sim_info), _whim_name, str(_whim_id), CMCommonWhimUtils.get_whim_name(chosen_whim))
                ).show(icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info)))
                _reopen()

            def _on_no_selected(_: Any):
                _reopen()

            confirmation = CommonOkCancelDialog(
                CMStringId.CONFIRMATION,
                CMSimControlMenuStringId.ARE_YOU_SURE_YOU_WANT_TO_REMOVE_WHIM,
                description_tokens=(_whim_name, str(_whim_id), CMCommonWhimUtils.get_whim_name(chosen_whim), CommonSimUtils.get_sim_instance(sim_info)),
                ok_text_identifier=CMStringId.YES,
                cancel_text_identifier=CMStringId.NO
            )
            confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.REMOVE_WHIMS,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        for whim_slot in CMCommonSimWhimUtils.get_whim_slots(sim_info):
            if whim_slot.is_empty():
                continue
            goal: SituationGoal = whim_slot.goal_instance
            whim: Whim = whim_slot.whim
            whim_guid = CMCommonWhimUtils.get_whim_guid(whim)
            if whim_guid is None:
                self.log.format_with_message('Missing whim id for Whim.', whim=whim)
                continue
            try:
                tuning_name = CMCommonWhimUtils.get_whim_name(whim) or 'Unknown Whim Name'

                display_name = goal.get_display_name()
                display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(display_name, tuning_name))

                description = CMCommonWhimUtils.get_whim_description(whim, goal)

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
                            is_enabled=self.is_whim_allowed_for_removal(whim)
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

    def is_whim_allowed_for_removal(self, whim: Whim) -> bool:
        """is_whim_allowed_for_removal(whim)

        Determine if a whim is allowed for removal via Control Menu or not.

        :param whim: An instance of a Whim.
        :type whim: Whim
        :return: True, if the whim is allowed for removal. False, if not.
        :rtype: bool
        """
        return True
