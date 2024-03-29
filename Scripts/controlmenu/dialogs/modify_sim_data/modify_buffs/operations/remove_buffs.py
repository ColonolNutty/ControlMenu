"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from buffs.buff import Buff
from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId


class CMRemoveBuffsSimOp(CMSingleSimOperation):
    """Remove Buffs from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_remove_buffs_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_buff_id: int, chosen_buff: Buff):
            if chosen_buff is None:
                on_completed(False)
                return

            def _on_yes_selected(_: Any):
                CommonBuffUtils.remove_buff(sim_info, _buff_id)
                # noinspection PyUnresolvedReferences
                CommonBasicNotification(
                    CMSimControlMenuStringId.REMOVED_BUFF_TITLE,
                    CMSimControlMenuStringId.REMOVED_BUFF_DESCRIPTION,
                    title_tokens=(chosen_buff.buff_name(sim_info), str(_buff_id)),
                    description_tokens=(CommonSimUtils.get_sim_instance(sim_info), chosen_buff.buff_name(sim_info), str(_buff_id), CommonBuffUtils.get_buff_name(chosen_buff))
                ).show(icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info)))
                _reopen()

            def _on_no_selected(_: Any):
                _reopen()

            # noinspection PyUnresolvedReferences
            confirmation = CommonOkCancelDialog(
                CMStringId.CONFIRMATION,
                CMSimControlMenuStringId.ARE_YOU_SURE_YOU_WANT_TO_REMOVE_BUFF,
                description_tokens=(chosen_buff.buff_name(sim_info), str(_buff_id), CommonBuffUtils.get_buff_name(chosen_buff), CommonSimUtils.get_sim_instance(sim_info)),
                ok_text_identifier=CMStringId.YES,
                cancel_text_identifier=CMStringId.NO,
                mod_identity=self.mod_identity
            )
            confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.REMOVE_BUFFS,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        for buff in CommonBuffUtils.get_buffs(sim_info):
            buff: Buff = buff
            buff_id = CommonBuffUtils.get_buff_id(buff)
            if buff_id is None:
                self.log.format_with_message('Missing buff id for Buff.', buff=buff)
                continue
            try:
                # noinspection PyUnresolvedReferences
                display_name = buff.buff_name(sim_info)
                if display_name.hash == 0:
                    buff_name = CommonBuffUtils.get_buff_name(buff) or 'Unknown Buff Name'
                    buff_name = buff_name[0].upper() + buff_name[1:]
                    # noinspection PyUnresolvedReferences
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(buff_name, str(buff_id)))
                else:
                    # noinspection PyUnresolvedReferences
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(display_name, str(buff_id)))
                # noinspection PyUnresolvedReferences
                description = CommonLocalizationUtils.create_localized_string(buff.buff_description, tokens=(sim_info,))
                # noinspection PyUnresolvedReferences
                icon = buff.icon or CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                option_dialog.add_option(
                    CommonDialogSelectOption(
                        buff_id,
                        buff,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=icon,
                            is_enabled=self._is_buff_allowed_for_removal(buff)
                        ),
                        on_chosen=_on_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display buff.', buff=buff, buff_name=CommonBuffUtils.get_buff_name(buff), buff_id=buff_id, exception=ex)

        if not option_dialog.has_options():
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    def _is_buff_allowed_for_removal(self, buff: Buff) -> bool:
        buff_id = CommonBuffUtils.get_buff_id(buff)
        if buff_id is None:
            self.log.format_with_message('Missing buff id for Buff.', buff=buff)
            return False
        return buff_id not in (
            CommonBuffId.ALIEN_IS_ALIEN,
            CommonBuffId.TRAIT_BABY,
            CommonBuffId.TRAIT_TODDLER,
            CommonBuffId.TRAIT_CHILD,
            CommonBuffId.TRAIT_TEEN,
            CommonBuffId.TRAIT_YOUNG_ADULT,
            CommonBuffId.TRAIT_ADULT,
            CommonBuffId.TRAIT_ELDER
        )
