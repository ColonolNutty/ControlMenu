"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_relationship_level_operation import \
    S4CMSetRelationshipLevelOp


class S4CMSetFriendshipLevelOp(S4CMSetRelationshipLevelOp):
    """Set the friendship level between two Sims."""

    def _determine_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        return self._determine_friendship_track(sim_info_a, sim_info_b)

    def _determine_friendship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        if CommonSpeciesUtils.is_human(sim_info_a):
            if CommonSpeciesUtils.is_pet(sim_info_b):
                return CommonRelationshipTrackId.SIM_TO_PET_FRIENDSHIP
            elif CommonSpeciesUtils.is_human(sim_info_b):
                return CommonRelationshipTrackId.FRIENDSHIP
        elif CommonSpeciesUtils.is_pet(sim_info_a):
            if CommonSpeciesUtils.is_pet(sim_info_b):
                return -1
            elif CommonSpeciesUtils.is_human(sim_info_b):
                return CommonRelationshipTrackId.SIM_TO_PET_FRIENDSHIP
        return -1
