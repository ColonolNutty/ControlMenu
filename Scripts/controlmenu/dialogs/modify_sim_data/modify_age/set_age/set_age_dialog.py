"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.adult import CMSetAgeAdultOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.child import CMSetAgeChildOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.elder import CMSetAgeElderOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.teen import CMSetAgeTeenOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.toddler import CMSetAgeToddlerOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.young_adult import CMSetAgeYoungAdultOp
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMSetAgeDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_set_age_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.SET_AGE

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

        if CommonAgeUtils.is_age_available_for_sim(self._sim_info, CommonAge.TODDLER):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Toddler',
                    CommonAge.TODDLER,
                    CommonDialogResponseOptionContext(
                        CommonStringId.TODDLER
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetAgeToddlerOp())
                )
            )

        if CommonAgeUtils.is_age_available_for_sim(self._sim_info, CommonAge.CHILD):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Child',
                    CommonAge.CHILD,
                    CommonDialogResponseOptionContext(
                        CommonStringId.CHILD
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetAgeChildOp())
                )
            )

        if CommonAgeUtils.is_age_available_for_sim(self._sim_info, CommonAge.TEEN):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Teen',
                    CommonAge.TEEN,
                    CommonDialogResponseOptionContext(
                        CommonStringId.TEEN
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetAgeTeenOp())
                )
            )

        if CommonAgeUtils.is_age_available_for_sim(self._sim_info, CommonAge.YOUNGADULT):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'YoungAdult',
                    CommonAge.YOUNGADULT,
                    CommonDialogResponseOptionContext(
                        CommonStringId.YOUNG_ADULT
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetAgeYoungAdultOp())
                )
            )

        if CommonAgeUtils.is_age_available_for_sim(self._sim_info, CommonAge.ADULT):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Adult',
                    CommonAge.ADULT,
                    CommonDialogResponseOptionContext(
                        CommonStringId.ADULT
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetAgeAdultOp())
                )
            )

        if CommonAgeUtils.is_age_available_for_sim(self._sim_info, CommonAge.ELDER):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Elder',
                    CommonAge.ELDER,
                    CommonDialogResponseOptionContext(
                        CommonStringId.ELDER
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetAgeElderOp())
                )
            )
        return True
