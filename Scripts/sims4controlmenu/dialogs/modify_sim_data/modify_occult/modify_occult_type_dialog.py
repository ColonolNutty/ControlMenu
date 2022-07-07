"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.dialogs.sim_control_dialog_base import S4CMSimControlDialogBase


class S4CMModifyOccultTypeDialog(S4CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cm_modify_occult_type_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CommonOccultType.convert_to_localized_string_id(self._occult_type)

    def _get_add_operation(self) -> Union[S4CMSingleSimOperation, None]:
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.alien import S4CMAlienAddOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.mermaid import S4CMMermaidAddOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.servo import S4CMServoAddOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.skeleton import S4CMSkeletonAddOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.vampire import S4CMVampireAddOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.witch import S4CMWitchAddOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.plant_sim import S4CMPlantSimAddOp
        mapping = {
            CommonOccultType.ALIEN: S4CMAlienAddOp(),
            CommonOccultType.MERMAID: S4CMMermaidAddOp(),
            CommonOccultType.ROBOT: S4CMServoAddOp(),
            CommonOccultType.SKELETON: S4CMSkeletonAddOp(),
            CommonOccultType.VAMPIRE: S4CMVampireAddOp(),
            CommonOccultType.WITCH: S4CMWitchAddOp(),
            CommonOccultType.PLANT_SIM: S4CMPlantSimAddOp(),
        }
        return mapping.get(self._occult_type, None)

    def _get_remove_operation(self) -> Union[S4CMSingleSimOperation, None]:
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.alien import S4CMAlienRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.mermaid import S4CMMermaidRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.servo import S4CMServoRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.skeleton import S4CMSkeletonRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.vampire import S4CMVampireRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.witch import S4CMWitchRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.plant_sim import S4CMPlantSimRemoveOp
        mapping = {
            CommonOccultType.ALIEN: S4CMAlienRemoveOp(),
            CommonOccultType.MERMAID: S4CMMermaidRemoveOp(),
            CommonOccultType.ROBOT: S4CMServoRemoveOp(),
            CommonOccultType.SKELETON: S4CMSkeletonRemoveOp(),
            CommonOccultType.VAMPIRE: S4CMVampireRemoveOp(),
            CommonOccultType.WITCH: S4CMWitchRemoveOp(),
            CommonOccultType.PLANT_SIM: S4CMPlantSimRemoveOp(),
        }
        return mapping.get(self._occult_type, None)

    def __init__(
        self,
        occult_type: CommonOccultType,
        sim_info: SimInfo,
        on_close: Callable[[], None] = None,
        on_previous: Callable[[], None] = None
    ):
        super().__init__(sim_info, on_close=on_close, on_previous=on_previous)
        self._occult_type = occult_type

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

        def _add_occult(*_, **__) -> None:
            add_operation = self._get_add_operation()
            if add_operation is not None:
                _operation_run(add_operation)
            else:
                result = CommonOccultUtils.add_occult(self._sim_info, self._occult_type)
                if not result:
                    self.log.format_error_with_message(f'Failed to add occult type {self._occult_type.name}', result=result)
                reopen()

        def _remove_occult(*_, **__) -> None:
            remove_operation = self._get_remove_operation()
            if remove_operation is not None:
                _operation_run(remove_operation)
            else:
                result = CommonOccultUtils.remove_occult(self._sim_info, self._occult_type)
                if not result:
                    self.log.format_error_with_message(f'Failed to remove occult type {self._occult_type.name}', result=result)
                reopen()

        def _switch_to_occult(*_, **__) -> None:
            result = CommonOccultUtils.switch_to_occult_form(self._sim_info, self._occult_type)
            if not result:
                self.log.format_error_with_message(f'Failed to switch to occult type {self._occult_type.name}', result=result)
            reopen()

        def _switch_to_non_occult(*_, **__) -> None:
            result = CommonOccultUtils.switch_to_occult_form(self._sim_info, CommonOccultType.NON_OCCULT)
            if not result:
                self.log.format_error_with_message(f'Failed to switch to non occult type {self._occult_type.name}', result=result)
            reopen()

        has_occult = CommonSimOccultTypeUtils.is_occult_type(self._sim_info, self._occult_type)

        add_disabled_text = CommonStringId.S4CL_THIS_FEATURE_IS_NOT_YET_IMPLEMENTED if self._occult_type in (CommonOccultType.GHOST,) else S4CMSimControlMenuStringId.SIM_ALREADY_HAS_THIS_OCCULT if has_occult else None

        if self._occult_type == CommonOccultType.ROBOT:
            all_occult_types = tuple(CommonSimOccultTypeUtils.get_all_occult_types_for_sim_gen(self._sim_info))
            for conflicting_occult_type in (CommonOccultType.ALIEN, CommonOccultType.VAMPIRE, CommonOccultType.WITCH, CommonOccultType.MERMAID, CommonOccultType.PLANT_SIM):
                if CommonSimOccultTypeUtils.is_occult_type(self._sim_info, conflicting_occult_type):
                    add_disabled_text = S4CMSimControlMenuStringId.CANNOT_ADD_ROBOT_OCCULT_TYPE_TO_SIM_WITH_OTHER_OCCULT_TYPES
                    break
        elif self._occult_type in (CommonOccultType.ALIEN, CommonOccultType.VAMPIRE, CommonOccultType.WITCH, CommonOccultType.MERMAID, CommonOccultType.PLANT_SIM):
            if CommonOccultUtils.is_robot(self._sim_info):
                add_disabled_text = S4CMSimControlMenuStringId.CANNOT_ADD_THIS_OCCULT_TYPE_TO_A_ROBOT_SIM

        option_dialog.add_option(
            CommonDialogButtonOption(
                'AddOccult',
                'AddOccult',
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.ADD_STRING,
                    text_tokens=(CommonOccultType.convert_to_localized_string_id(self._occult_type),),
                    disabled_text_identifier=add_disabled_text,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _add_occult()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'RemoveOccult',
                'RemoveOccult',
                CommonDialogResponseOptionContext(
                    S4CMSimControlMenuStringId.REMOVE_STRING,
                    text_tokens=(CommonOccultType.convert_to_localized_string_id(self._occult_type),),
                    disabled_text_identifier=S4CMSimControlMenuStringId.SIM_DOES_NOT_HAVE_THIS_OCCULT if not has_occult else None,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _remove_occult()
            )
        )

        is_currently_occult = CommonSimOccultTypeUtils.is_currently_occult_type(self._sim_info, self._occult_type)

        if self._occult_type in (CommonOccultType.ALIEN, CommonOccultType.VAMPIRE, CommonOccultType.WEREWOLF, CommonOccultType.MERMAID):

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'SwitchOccult',
                    'SwitchOccult',
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.SWITCH_TO_STRING_FORM,
                        text_tokens=(CommonOccultType.convert_to_localized_string_id(self._occult_type),),
                        disabled_text_identifier=S4CMSimControlMenuStringId.SIM_DOES_NOT_HAVE_THIS_OCCULT if not has_occult else S4CMSimControlMenuStringId.SIM_IS_ALREADY_IN_THIS_FORM if is_currently_occult else None,
                        disabled_text_tokens=(self._sim_info,)
                    ),
                    on_chosen=lambda *_, **__: _switch_to_occult()
                )
            )

            option_dialog.add_option(
                CommonDialogButtonOption(
                    'SwitchNonOccult',
                    'SwitchNonOccult',
                    CommonDialogResponseOptionContext(
                        S4CMSimControlMenuStringId.SWITCH_TO_STRING_FORM,
                        text_tokens=(CommonOccultType.convert_to_localized_string_id(CommonOccultType.NON_OCCULT),),
                        disabled_text_identifier=S4CMSimControlMenuStringId.SIM_DOES_NOT_HAVE_THIS_OCCULT if not has_occult else S4CMSimControlMenuStringId.SIM_IS_ALREADY_IN_THIS_FORM if not is_currently_occult else None,
                        disabled_text_tokens=(self._sim_info,)
                    ),
                    on_chosen=lambda *_, **__: _switch_to_non_occult()
                )
            )
        return True
