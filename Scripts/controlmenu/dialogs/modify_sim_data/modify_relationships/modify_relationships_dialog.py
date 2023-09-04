"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.remove_family_relationships import \
    CMRemoveFamilyRelationsBitOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.remove_relationship_bit import \
    CMRemoveRelationshipBitOp
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.forget_sims import CMForgetSimsOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.has_met import CMAddHasMetSimsOp, \
    CMRemoveHasMetSimsOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_family_relationship import \
    CMSetFamilyRelationsBitOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_friendship_level import \
    CMSetFriendshipLevelOp
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_romance_level import \
    CMSetRomanceLevelOp
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifyRelationshipsDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_relationships_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.RELATIONSHIPS

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        target_sim_info: SimInfo = None,
        **__
    ) -> bool:
        def _operation_run(operation: CMSingleSimOperation):
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
                            CMSimControlMenuStringId.SET_RELATIONSHIPS_WITH_SIM,
                            text_tokens=(active_sim_info, )
                        ),
                        on_chosen=lambda *_, **__: None if self.open(target_sim_info=active_sim_info) else None
                    )
                )

        if (target_sim_info is None and CMSetFriendshipLevelOp().can_run_with_sim(self._sim_info)) or CMSetFriendshipLevelOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'FriendshipLevel',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.SET_FRIENDSHIP_LEVEL
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetFriendshipLevelOp())
                )
            )

        if (target_sim_info is None and CMSetRomanceLevelOp().can_run_with_sim(self._sim_info)) or CMSetRomanceLevelOp().can_run_with_sims(self._sim_info, target_sim_info):
            if CommonRelationshipUtils.has_permission_for_romantic_relationships(self._sim_info):
                option_dialog.add_option(
                    CommonDialogButtonOption(
                        'RomanceLevel',
                        None,
                        CommonDialogResponseOptionContext(
                            CMSimControlMenuStringId.SET_ROMANCE_LEVEL
                        ),
                        on_chosen=lambda *_, **__: _operation_run(CMSetRomanceLevelOp())
                    )
                )

        if (target_sim_info is None and CMAddHasMetSimsOp().can_run_with_sim(self._sim_info)) or CMAddHasMetSimsOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'AddHasMet',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.ADD_HAS_MET,
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMAddHasMetSimsOp())
                )
            )

        if (target_sim_info is None and CMRemoveHasMetSimsOp().can_run_with_sim(self._sim_info)) or CMRemoveHasMetSimsOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveHasMet',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.REMOVE_HAS_MET,
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMRemoveHasMetSimsOp())
                )
            )

        # Has blood relatives.
        has_blood_relatives = False
        for sim_info_b in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if self._sim_info is not sim_info_b and CommonRelationshipUtils.are_blood_relatives(self._sim_info, sim_info_b):
                has_blood_relatives = True
                break
        if (target_sim_info is None and CMSetFamilyRelationsBitOp().can_run_with_sim(self._sim_info) and has_blood_relatives) or CMSetFamilyRelationsBitOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'FamilyRelations',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.SET_FAMILY_RELATIONS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMSetFamilyRelationsBitOp())
                )
            )

        if (target_sim_info is None and CMRemoveFamilyRelationsBitOp().can_run_with_sim(self._sim_info)) or CMRemoveFamilyRelationsBitOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveFamilyRelations',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.REMOVE_FAMILY_RELATIONS
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMRemoveFamilyRelationsBitOp())
                )
            )

        if (target_sim_info is None and CMRemoveRelationshipBitOp().can_run_with_sim(self._sim_info)) or CMRemoveRelationshipBitOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'RemoveRelationshipBit',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.REMOVE_RELATIONSHIP_BIT,
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMRemoveRelationshipBitOp())
                )
            )

        if (target_sim_info is None and CMForgetSimsOp().can_run_with_sim(self._sim_info)) or CMForgetSimsOp().can_run_with_sims(self._sim_info, target_sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'ForgetSims',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.FORGET_SIMS,
                    ),
                    on_chosen=lambda *_, **__: _operation_run(CMForgetSimsOp())
                )
            )
        return True
