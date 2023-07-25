"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sim_option_dialog import \
    CommonPremadeChooseSimOptionDialog
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.modinfo import ModInfo


class CMCreatePregnancyOp(CMSingleSimOperation):
    """Clear a pregnancy in a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_create_pregnancy'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        if CommonSimPregnancyUtils.is_pregnant(sim_info):
            self.log.format_with_message(f'Failed, {sim_info} is already pregnant.')
            on_completed(False)
            return False

        if not CommonSimPregnancyUtils.can_impregnate(sim_info) and not CommonSimPregnancyUtils.can_be_impregnated(sim_info):
            self.log.format_with_message(f'Failed, {sim_info} can neither impregnate nor be impregnated.')
            on_completed(False)
            return False

        def _on_chosen(chosen_sim_info: SimInfo) -> None:
            if chosen_sim_info is None:
                on_completed(False)
                return
            result = CommonSimPregnancyUtils.start_pregnancy(sim_info, chosen_sim_info)
            on_completed(result)

        def _can_create_pregnancy(partner_sim_info: SimInfo) -> bool:
            if sim_info is partner_sim_info:
                return False
            has_permission = CommonSimPregnancyUtils.has_permission_for_pregnancies_with(sim_info, partner_sim_info)
            if not has_permission:
                self.log.format_with_message(f'Failed, {sim_info} does not have permission for pregnancy with {partner_sim_info}. Reason: {has_permission.reason}')
            return has_permission.result

        dialog = CommonPremadeChooseSimOptionDialog(
            CMSimControlMenuStringId.WHO_WILL_IMPREGNATE_SIM,
            0,
            title_tokens=(sim_info,),
            include_sim_callback=_can_create_pregnancy,
            instanced_sims_only=False,
            mod_identity=ModInfo.get_identity(),
            on_sim_chosen=_on_chosen,
            on_close=lambda: on_completed(False)
        )
        if not dialog.has_options():
            self.log.debug(f'No Sims were found to be able to create a pregnancy with {sim_info}')
            on_completed(False)
            return False
        self.log.format_with_message('Showing dialog.')
        # Sort the Sims in the dialog by their name.
        dialog._internal_dialog._rows = tuple(sorted(dialog._internal_dialog._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
        dialog.show(sim_info=sim_info)
        return True
