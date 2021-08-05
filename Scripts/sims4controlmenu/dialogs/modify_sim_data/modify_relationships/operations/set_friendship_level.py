"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_relationship_level_operation import \
    S4CMSetRelationshipLevelOp


class S4CMSetFriendshipLevelOp(S4CMSetRelationshipLevelOp):
    """Set the friendship level between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_friendship'

    def _determine_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        return CommonRelationshipUtils._determine_friendship_track(sim_info_a, sim_info_b)
