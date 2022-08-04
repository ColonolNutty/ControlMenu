"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from controlmenu.settings.settings import CMSetting


class CMSettingUtils:
    """Setting utils"""
    @staticmethod
    def is_sim_allowed_to_perform_adult_sim_operations(sim_info: SimInfo) -> CommonTestResult:
        """Determine if the Sim is allowed to perform Operations intended for Adult Sims."""
        return CommonOutfitUtils.has_permission_to_change_to_nude(sim_info)

    @staticmethod
    def is_allowed_romantic_relationship(sim_info: SimInfo) -> CommonTestResult:
        """Determine if a Sim is allowed to have a romantic relationship with another Sim."""
        return CommonRelationshipUtils.has_permission_for_romantic_relationships(sim_info)

    @staticmethod
    def are_allowed_family_relationship_bits(sim_info_a: SimInfo, sim_info_b: SimInfo) -> CommonTestResult:
        """Determine if two Sims are allowed to have a family relationship bits."""
        return CommonRelationshipUtils.has_permission_to_be_blood_relative_of(sim_info_a, sim_info_b)

    @staticmethod
    def are_allowed_romantic_relationship(sim_info_a: SimInfo, sim_info_b: SimInfo) -> CommonTestResult:
        """Determine if two Sims are allowed to have a Romantic relationship together."""
        return CommonRelationshipUtils.has_permission_for_romantic_relationship_with(sim_info_a, sim_info_b)

    @staticmethod
    def get_maximum_household_size() -> int:
        """Retrieve the maximum size for households."""
        return CMSettingUtils._get_value(CMSetting.MAXIMUM_HOUSEHOLD_SIZE)

    @staticmethod
    def get_pregnancy_speed_modifier() -> int:
        """Retrieve the speed modifier for pregnancy."""
        return CMSettingUtils._get_value(CMSetting.PREGNANCY_SPEED)

    @staticmethod
    def get_real_milliseconds_per_sim_second() -> int:
        """Retrieve the number of real milliseconds per sim second."""
        return CMSettingUtils._get_value(CMSetting.REAL_MILLISECONDS_PER_SIM_SECOND)

    @staticmethod
    def get_clock_speed_multiplier() -> int:
        """Retrieve the multiplier for clock speed."""
        return CMSettingUtils._get_value(CMSetting.CLOCK_SPEED_MULTIPLIER)

    @staticmethod
    def get_maximum_number_of_sims_per_lot() -> int:
        """Retrieve the maximum number of Sims allowed on a lot at any given time."""
        return CMSettingUtils._get_value(CMSetting.MAXIMUM_SIMS_PER_LOT)

    @staticmethod
    def _get_value(key: str) -> Any:
        from controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils
        return CMMainDataManagerUtils().get_main_mod_settings_data_store().get_value_by_key(key)

    @staticmethod
    def _set_value(key: str, value: Any) -> Any:
        from controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils
        return CMMainDataManagerUtils().get_main_mod_settings_data_store().set_value_by_key(key, value)
