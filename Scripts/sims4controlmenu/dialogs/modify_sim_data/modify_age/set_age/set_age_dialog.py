"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.adult import S4CMSetAgeAdultOp
from sims4controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.child import S4CMSetAgeChildOp
from sims4controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.elder import S4CMSetAgeElderOp
from sims4controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.teen import S4CMSetAgeTeenOp
from sims4controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.toddler import S4CMSetAgeToddlerOp
from sims4controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.young_adult import S4CMSetAgeYoungAdultOp
from sims4controlmenu.dialogs.modify_sim_data.sim_operation import S4CMSingleSimOperation


class S4CMSetAgeDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_set_age_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMSimControlMenuStringId.SET_AGE

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None]
    ) -> bool:
        def _operation_set(operation: S4CMSingleSimOperation):
            operation.run(self._sim_info)
            reopen()

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Toddler',
                CommonAge.TODDLER,
                CommonDialogResponseOptionContext(
                    CommonStringId.TODDLER
                ),
                on_chosen=lambda *_, **__: _operation_set(S4CMSetAgeToddlerOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Child',
                CommonAge.CHILD,
                CommonDialogResponseOptionContext(
                    CommonStringId.CHILD
                ),
                on_chosen=lambda *_, **__: _operation_set(S4CMSetAgeChildOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Teen',
                CommonAge.TEEN,
                CommonDialogResponseOptionContext(
                    CommonStringId.TEEN
                ),
                on_chosen=lambda *_, **__: _operation_set(S4CMSetAgeTeenOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'YoungAdult',
                CommonAge.YOUNGADULT,
                CommonDialogResponseOptionContext(
                    CommonStringId.YOUNG_ADULT
                ),
                on_chosen=lambda *_, **__: _operation_set(S4CMSetAgeYoungAdultOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Adult',
                CommonAge.ADULT,
                CommonDialogResponseOptionContext(
                    CommonStringId.ADULT
                ),
                on_chosen=lambda *_, **__: _operation_set(S4CMSetAgeAdultOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Elder',
                CommonAge.ELDER,
                CommonDialogResponseOptionContext(
                    CommonStringId.ELDER
                ),
                on_chosen=lambda *_, **__: _operation_set(S4CMSetAgeElderOp())
            )
        )
        return True
