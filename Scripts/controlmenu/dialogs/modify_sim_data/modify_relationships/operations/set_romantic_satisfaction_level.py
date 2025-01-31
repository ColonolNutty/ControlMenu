"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Callable

from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_relationship_level_operation import \
    CMSetRelationshipLevelOp


class CMSetRomanticSatisfactionLevelOp(CMSetRelationshipLevelOp):
    """Set the romantic satisfaction level between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_romantic_satisfaction'

    def __init__(self, treat_sim_as_secondary: bool = True):
        super().__init__()
        self.treat_sim_as_secondary = treat_sim_as_secondary

    def _determine_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, None]:
        if hasattr(CommonRelationshipUtils, 'get_romantic_satisfaction_track'):
            return CommonRelationshipUtils.get_romantic_satisfaction_track(sim_info_a, sim_info_b)
        return 362100  # URT_RelSat_Main

    def _is_allowed_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> CommonTestResult:
        if not super()._is_allowed_relationship_track(sim_info_a, sim_info_b):
            return CommonTestResult.FALSE
        return CommonRelationshipUtils.has_permission_for_romantic_relationship_with(sim_info_a, sim_info_b)

    def can_run_with_sim(self, sim_info: SimInfo) -> bool:
        """Determine if this operation can run using the specified Sim."""
        return super().can_run_with_sim(sim_info) and CommonRelationshipUtils.has_permission_for_romantic_relationships(sim_info)

    # noinspection PyMissingOrEmptyDocstring
    def run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo, *_, **__):
        if self.treat_sim_as_secondary:
            return super().run_with_sims(sim_info_b, sim_info_a, *_, **__)
        else:
            return super().run_with_sims(sim_info_a, sim_info_b, *_, **__)
