"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.resolver import DoubleSimResolver
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class S4CMSimPregnancyUtils:
    """Utilities for pregnancy. """
    @staticmethod
    def can_create_pregnancy(sim_info: SimInfo, ignore_gender_options: bool=False) -> bool:
        """can_create_pregnancy(sim_info, ignore_gender_options=False)

        Determine if a Sim is able to create a pregnancy.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param ignore_gender_options: If set to True, pregnancy gender options will be ignored.\
        If set to False, the Sim will be checked for having either Can Impregnate or Can Be Impregnated. Default is False.
        :type ignore_gender_options: bool, optional
        :return: True, if the Sim can produce a pregnancy. False, if not.
        :rtype: bool
        """
        if not ignore_gender_options:
            if not CommonSimPregnancyUtils.can_impregnate(sim_info) and not CommonSimPregnancyUtils.can_be_impregnated(sim_info):
                return False
        return CommonAgeUtils.is_adult_or_elder(sim_info)

    @staticmethod
    def can_create_pregnancy_together(sim_info_a: SimInfo, sim_info_b: SimInfo, ignore_gender_options=False) -> bool:
        """can_create_pregnancy_together(sim_info_a, sim_info_b, ignore_gender_options=False)

        Determine if two Sims can create a pregnancy together.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :param ignore_gender_options: If set to True, pregnancy gender options will be ignored.\
        If set to False, each Sim will be checked for having either Can Impregnate or Can Be Impregnated. Default is False.
        :type ignore_gender_options: bool, optional
        :return: True, if the Sim can produce a pregnancy. False, if not.
        :rtype: bool
        """
        if not S4CMSimPregnancyUtils.can_create_pregnancy(sim_info_a, ignore_gender_options=ignore_gender_options)\
                or not S4CMSimPregnancyUtils.can_create_pregnancy(sim_info_b, ignore_gender_options=ignore_gender_options):
            return False
        if not CommonSpeciesUtils.are_same_species(sim_info_a, sim_info_b):
            # If both Sims are dogs, that is an ok combination.
            if not CommonSpeciesUtils.is_dog(sim_info_a) or not CommonSpeciesUtils.is_dog(sim_info_b):
                return False
        return PregnancyTracker.AT_BIRTH_TESTS.run_tests(DoubleSimResolver(sim_info_a, sim_info_b)) or PregnancyTracker.AT_BIRTH_TESTS.run_tests(DoubleSimResolver(sim_info_b, sim_info_a))
