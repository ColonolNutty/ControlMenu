"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_traits.operations.add_traits import CMAddTraitsSimOp
from controlmenu.dialogs.modify_sim_data.modify_traits.operations.modify_likes_dislikes import \
    CMModifyLikesDislikesSimOp
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_traits.operations.set_personality_traits import \
    CMSetPersonalityTraitsSimOp
from controlmenu.dialogs.modify_sim_data.modify_traits.operations.remove_traits import CMRemoveTraitsSimOp
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifyTraitsDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_traits_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.TRAITS

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

        if CMSetPersonalityTraitsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'SetPersonalityTraits',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.SET_PERSONALITY_TRAITS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetPersonalityTraitsSimOp())
                )
            )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'AddTraits',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.ADD_TRAITS
                ),
                on_chosen=lambda *_, **__: _operation_run(CMAddTraitsSimOp())
            )
        )

        if CMRemoveTraitsSimOp().can_run_with_sim(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveTraits',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.REMOVE_TRAITS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMRemoveTraitsSimOp())
                )
            )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyLikesDislikes',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.LIKES_DISLIKES
                ),
                on_chosen=lambda *_, **__: _operation_run(CMModifyLikesDislikesSimOp())
            )
        )
        return True
