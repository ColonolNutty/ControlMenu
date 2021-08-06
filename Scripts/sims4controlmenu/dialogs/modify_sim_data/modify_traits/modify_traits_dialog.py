"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_traits.operations.set_personality_traits import \
    S4CMSetPersonalityTraitsSimOp
from sims4controlmenu.dialogs.modify_sim_data.modify_traits.operations.remove_traits import S4CMRemoveTraitsSimOp
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMModifyTraitsDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_traits_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMSimControlMenuStringId.MODIFY_TRAITS

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

        if S4CMSetPersonalityTraitsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'AddTraits',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.SET_PERSONALITY_TRAITS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMSetPersonalityTraitsSimOp())
                )
            )

        if S4CMRemoveTraitsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveTraits',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.REMOVE_TRAITS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMRemoveTraitsSimOp())
                )
            )
        return True
