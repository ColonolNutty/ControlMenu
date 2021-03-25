"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4controlmenu.commonlib.utils.common_sim_relationship_utils import S4CMSimRelationshipUtils


class S4CMSettingUtils:
    """Setting utils"""
    @staticmethod
    def is_enabled_for_interactions(sim_info: SimInfo) -> bool:
        """Whether or not the Sim is enabled for S4CM interactions."""
        if CommonAgeUtils.is_teen(sim_info) and not S4CMSettingUtils.should_treat_teen_sims_as_adult_sims():
            return False
        return CommonAgeUtils.is_teen_adult_or_elder(sim_info)

    @staticmethod
    def should_treat_teen_sims_as_adult_sims() -> bool:
        """Whether or not Teen Sims should be treated as Adult Sims."""
        return True

    @staticmethod
    def is_allowed_romantic_relationship(sim_info: SimInfo) -> bool:
        """Determine if a Sim is allowed to have a romantic relationship with another Sim."""
        return CommonAgeUtils.is_teen(sim_info) or S4CMSettingUtils.is_enabled_for_interactions(sim_info)

    @staticmethod
    def are_allowed_family_relationship(sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """Whether or not two Sims are allowed to have a family relationship."""
        return CommonSpeciesUtils.are_same_species(sim_info_a, sim_info_b)

    @staticmethod
    def are_allowed_romantic_relationship(sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """Whether or not two Sims are allowed to have a Romantic relationship together."""
        if not S4CMSettingUtils.is_allowed_romantic_relationship(sim_info_a) or not S4CMSettingUtils.is_allowed_romantic_relationship(sim_info_b):
            return False
        if S4CMSimRelationshipUtils.are_family(sim_info_a, sim_info_b):
            return False
        if not CommonSpeciesUtils.are_same_species(sim_info_a, sim_info_b):
            return False
        if CommonAgeUtils.is_teen(sim_info_a) and CommonAgeUtils.is_teen(sim_info_b):
            return True
        # Teen to Teen is ok, this check prevents Teen to Adult/Elder/etc. like vanilla has it.
        if CommonAgeUtils.is_teen(sim_info_a) or CommonAgeUtils.is_teen(sim_info_b):
            return False
        # If the Sims are not Adults, they can be assumed to be either a Young Adult, Adult, or Elder
        return CommonAgeUtils.is_adult_or_elder(sim_info_a)\
               and CommonAgeUtils.is_adult_or_elder(sim_info_b)
