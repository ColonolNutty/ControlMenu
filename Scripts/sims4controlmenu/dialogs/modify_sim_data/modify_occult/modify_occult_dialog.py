"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.alien import S4CMAlienAddOp, S4CMAlienRemoveOp
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.mermaid import S4CMMermaidAddOp, \
    S4CMMermaidRemoveOp
from sims4controlmenu.dialogs.modify_sim_data.sim_operation import S4CMSingleSimOperation
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.skeleton import S4CMSkeletonAddOp, \
    S4CMSkeletonRemoveOp
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.vampire import S4CMVampireAddOp, \
    S4CMVampireRemoveOp
from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.witch import S4CMWitchAddOp, S4CMWitchRemoveOp


class S4CMModifyOccultDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_occult_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMSimControlMenuStringId.MODIFY_OCCULT

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None]
    ) -> bool:
        def _operation_add(operation: S4CMSingleSimOperation):
            operation.run(self._sim_info)
            reopen()

        def _operation_remove_all() -> None:
            S4CMAlienRemoveOp().run(self._sim_info)
            S4CMMermaidRemoveOp().run(self._sim_info)
            S4CMSkeletonRemoveOp().run(self._sim_info)
            S4CMVampireRemoveOp().run(self._sim_info)
            S4CMWitchRemoveOp().run(self._sim_info)
            reopen()

        option_dialog.add_option(
            CommonDialogButtonOption(
                'RemoveAllOccults',
                CommonOccultType.NON_OCCULT,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.REMOVE_ALL_OCCULTS
                ),
                on_chosen=lambda *_, **__: _operation_remove_all()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'AlienAdd',
                CommonOccultType.ALIEN,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.BECOME_ALIEN
                ),
                on_chosen=lambda *_, **__: _operation_add(S4CMAlienAddOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'MermaidAdd',
                CommonOccultType.MERMAID,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.BECOME_MERMAID
                ),
                on_chosen=lambda *_, **__: _operation_add(S4CMMermaidAddOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'SkeletonAdd',
                CommonOccultType.SKELETON,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.BECOME_SKELETON
                ),
                on_chosen=lambda *_, **__: _operation_add(S4CMSkeletonAddOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'VampireAdd',
                CommonOccultType.VAMPIRE,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.BECOME_VAMPIRE
                ),
                on_chosen=lambda *_, **__: _operation_add(S4CMVampireAddOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'WitchAdd',
                CommonOccultType.WITCH,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.BECOME_WITCH
                ),
                on_chosen=lambda *_, **__: _operation_add(S4CMWitchAddOp())
            )
        )
        return True
