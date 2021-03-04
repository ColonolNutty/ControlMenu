"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.set_relationship_level_operation import \
    S4CMSetRelationshipLevelOp


class S4CMSetRomanceLevelOp(S4CMSetRelationshipLevelOp):
    """Set the romance level between two Sims."""

    def _determine_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        return self._determine_romance_track(sim_info_a, sim_info_b)

    def _determine_romance_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        if CommonSpeciesUtils.is_human(sim_info_a) and CommonSpeciesUtils.is_human(sim_info_b):
            return CommonRelationshipTrackId.ROMANCE
        return -1

    def _is_allowed_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        if not super()._is_allowed_relationship_track(sim_info_a, sim_info_b):
            return False
        if CommonAgeUtils.is_teen(sim_info_a) and CommonAgeUtils.is_teen(sim_info_b):
            return True
        # Teen to Teen is ok, this check prevents Teen to Adult/Elder/etc. like vanilla has it.
        if CommonAgeUtils.is_teen(sim_info_a) or CommonAgeUtils.is_teen(sim_info_b):
            return False
        return CommonAgeUtils.is_adult_or_elder(sim_info_a)\
               and CommonAgeUtils.is_adult_or_elder(sim_info_b)
