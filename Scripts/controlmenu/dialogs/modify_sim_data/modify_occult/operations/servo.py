"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId


class CMServoAddOp(CMSingleSimOperation):
    """Add the Servo Occult to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_servo'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        if CommonOccultUtils.is_robot(sim_info):
            on_completed(CommonExecutionResult(False, reason=f'{sim_info} is already a Robot.'))
            return False

        def _on_ok_selected(_: Any):
            # trait_Humanoid_Robots_MainTrait
            trait_id = CommonTraitId.OCCULT_ROBOT
            result = CommonTraitUtils.add_trait(sim_info, trait_id)
            on_completed(result)

        def _on_cancel_selected(_: Any):
            on_completed(CommonExecutionResult(False, reason='Cancelled to change.'))

        confirmation = CommonOkCancelDialog(
            CMStringId.CONFIRMATION,
            CMSimControlMenuStringId.BECOME_SERVO_CONFIRMATION_DESCRIPTION,
        )
        confirmation.show(on_ok_selected=_on_ok_selected, on_cancel_selected=_on_cancel_selected)
        return True


class CMServoRemoveOp(CMSingleSimOperation):
    """Remove the Servo Occult from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_servo'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[CommonExecutionResult], None] = CommonFunctionUtils.noop) -> bool:
        if not CommonOccultUtils.is_robot(sim_info):
            on_completed(CommonExecutionResult(False, reason=f'{sim_info} is not a robot.'))
            return False
        # trait_Humanoid_Robots_MainTrait
        trait_id = CommonTraitId.OCCULT_ROBOT
        result = CommonTraitUtils.remove_trait(sim_info, trait_id)
        on_completed(result)
        return result.result
