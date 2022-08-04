"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_relationship_level_operation import \
    CMSetRelationshipLevelOp
from controlmenu.settings.setting_utils import CMSettingUtils


class CMSetRomanceLevelOp(CMSetRelationshipLevelOp):
    """Set the romance level between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_romance'

    def _determine_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, None]:
        return CommonRelationshipUtils.get_romance_relationship_track(sim_info_a, sim_info_b)

    def _is_allowed_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        if not super()._is_allowed_relationship_track(sim_info_a, sim_info_b):
            return False
        from controlmenu.settings.setting_utils import CMSettingUtils
        return CMSettingUtils.are_allowed_romantic_relationship(sim_info_a, sim_info_b)

    def can_run_with_sim(self, sim_info: SimInfo) -> bool:
        """Determine if this operation can run using the specified Sim."""
        return super().can_run_with_sim(sim_info) and CMSettingUtils.is_allowed_romantic_relationship(sim_info)
