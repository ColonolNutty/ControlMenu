"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_family_relationship import \
    S4CMSetFamilyRelationsBitOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_friendship_level import \
    S4CMSetFriendshipLevelOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_romance_level import \
    S4CMSetRomanceLevelOp
from sims4controlmenu.dialogs.modify_sim_data.sim_control_dialog_base import S4CMSimControlDialogBase
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.settings.setting_utils import S4CMSettingUtils


class S4CMModifyRelationshipsDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_relationships_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return S4CMSimControlMenuStringId.MODIFY_RELATIONSHIPS

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None]
    ) -> bool:
        def _operation_run(operation: S4CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        option_dialog.add_option(
            CommonDialogButtonOption(
                'FriendshipLevel',
                None,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.SET_FRIENDSHIP_LEVEL
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMSetFriendshipLevelOp())
            )
        )

        if S4CMSettingUtils.is_allowed_romantic_relationship(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RomanceLevel',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.SET_ROMANCE_LEVEL
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMSetRomanceLevelOp())
                )
            )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'FamilyRelations',
                None,
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.SET_FAMILY_RELATIONS
                ),
                on_chosen=lambda *_, **__: _operation_run(S4CMSetFamilyRelationsBitOp())
            )
        )
        return True
