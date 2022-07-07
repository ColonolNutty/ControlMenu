"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.utils.common_sim_pregnancy_utils import S4CMSimPregnancyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.pregnancy.operations.clear_pregnancy import S4CMClearPregnancyOp
from sims4controlmenu.dialogs.modify_sim_data.pregnancy.operations.create_pregnancy import S4CMCreatePregnancyOp
from sims4controlmenu.dialogs.modify_sim_data.pregnancy.operations.induce_labor import S4CMInduceLaborOp
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMPregnancyDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_pregnancy_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMSimControlMenuStringId.PREGNANCY

    @property
    def description(self) -> int:
        """The title of the dialog."""
        if CommonSimPregnancyUtils.is_pregnant(self._sim_info):
            return 0
        return 0

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: S4CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        is_pregnant = CommonSimPregnancyUtils.is_pregnant(self._sim_info)

        can_produce_pregnancy = S4CMSimPregnancyUtils.can_create_pregnancy(self._sim_info)

        create_pregnancy_disabled_text = None
        if is_pregnant:
            create_pregnancy_disabled_text = S4CMSimControlMenuStringId.SIM_IS_ALREADY_PREGNANT
        elif not can_produce_pregnancy:
            create_pregnancy_disabled_text = S4CMSimControlMenuStringId.SIM_IS_UNABLE_TO_CREATE_PREGNANCY
        elif not CommonHouseholdUtils.has_free_household_slots(self._sim_info):
            create_pregnancy_disabled_text = S4CMSimControlMenuStringId.TOO_MANY_SIMS_IN_HOUSEHOLD_ALREADY

        option_dialog.add_option(
            CommonDialogButtonOption(
                'CreatePregnancy',
                None,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.CREATE_PREGNANCY,
                    disabled_text_identifier=create_pregnancy_disabled_text,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMCreatePregnancyOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'InduceLabor',
                None,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.INDUCE_LABOR,
                    disabled_text_identifier=S4CMSimControlMenuStringId.SIM_IS_NOT_PREGNANT if not is_pregnant else None,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMInduceLaborOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ClearPregnancy',
                None,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.CLEAR_PREGNANCY,
                    disabled_text_identifier=S4CMSimControlMenuStringId.SIM_IS_NOT_PREGNANT if not is_pregnant else None,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMClearPregnancyOp())
            )
        )
        return True
