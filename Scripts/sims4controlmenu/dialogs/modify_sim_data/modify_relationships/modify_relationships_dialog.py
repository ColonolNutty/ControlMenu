"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.forget_sims import S4CMForgetSimsOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.has_met import S4CMAddHasMetSimsOp, \
    S4CMRemoveHasMetSimsOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_family_relationship import \
    S4CMSetFamilyRelationsBitOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_friendship_level import \
    S4CMSetFriendshipLevelOp
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_romance_level import \
    S4CMSetRomanceLevelOp
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase
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
        reopen: Callable[[], None],
        target_sim_info: SimInfo = None,
        **__
    ) -> bool:
        def _operation_run(operation: S4CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            if target_sim_info is not None:
                operation.run_with_sims(self._sim_info, target_sim_info, on_completed=_on_operation_complete)
            else:
                operation.run(self._sim_info, on_completed=_on_operation_complete)

        if target_sim_info is None:
            active_sim_info = CommonSimUtils.get_active_sim_info()
            if active_sim_info is not None and self._sim_info is not active_sim_info:
                option_dialog.add_option(
                    CommonDialogButtonOption(
                        'WithSelf',
                        None,
                        CommonDialogResponseOptionContext(
                            S4CMSimControlMenuStringId.SET_RELATIONSHIPS_WITH_SIM,
                            text_tokens=(active_sim_info, )
                        ),
                        on_chosen=lambda *_, **__: None if self.open(target_sim_info=active_sim_info) else None
                    )
                )

        if (target_sim_info is None and S4CMSetFriendshipLevelOp().can_run_with_sim(self._sim_info)) or S4CMSetFriendshipLevelOp().can_run_with_sims(self._sim_info, target_sim_info):
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

        if (target_sim_info is None and S4CMSetRomanceLevelOp().can_run_with_sim(self._sim_info)) or S4CMSetRomanceLevelOp().can_run_with_sims(self._sim_info, target_sim_info):
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

        if (target_sim_info is None and S4CMAddHasMetSimsOp().can_run_with_sim(self._sim_info)) or S4CMAddHasMetSimsOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'AddHasMet',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.ADD_HAS_MET,
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMAddHasMetSimsOp())
                )
            )

        if (target_sim_info is None and S4CMRemoveHasMetSimsOp().can_run_with_sim(self._sim_info)) or S4CMRemoveHasMetSimsOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveHasMet',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.REMOVE_HAS_MET,
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMRemoveHasMetSimsOp())
                )
            )

        if (target_sim_info is None and S4CMSetFamilyRelationsBitOp().can_run_with_sim(self._sim_info)) or S4CMSetFamilyRelationsBitOp().can_run_with_sims(self._sim_info, target_sim_info):
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

        if (target_sim_info is None and S4CMForgetSimsOp().can_run_with_sim(self._sim_info)) or S4CMForgetSimsOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'ForgetSims',
                    None,
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.FORGET_SIMS,
                    ),
                    on_chosen=lambda *_, **__: _operation_run(S4CMForgetSimsOp())
                )
            )
        return True
