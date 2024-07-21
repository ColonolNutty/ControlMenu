"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_career.enums.string_ids import CMSimModifyCareerStringId
from controlmenu.dialogs.modify_sim_data.modify_career.operations.manage_careers import CMManageCareersSimOp
from controlmenu.dialogs.modify_sim_data.modify_career.operations.remove_careers import CMRemoveAllCareersSimOp
from controlmenu.dialogs.modify_sim_data.modify_career.operations.set_career import CMSetCareerSimOp
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase


class CMModifyCareersDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_careers_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimModifyCareerStringId.CAREER

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ManageCareers',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyCareerStringId.MANAGE_CAREERS
                ),
                on_chosen=lambda *_, **__: _operation_run(CMManageCareersSimOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetCareer',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyCareerStringId.SET_CAREER
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetCareerSimOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'RemoveAllCareers',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyCareerStringId.REMOVE_ALL_CAREERS
                ),
                on_chosen=lambda *_, **__: _operation_run(CMRemoveAllCareersSimOp())
            )
        )
        return True
