"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils


class CMSimPregnancyUtils:
    """Utilities for pregnancy. """
    @staticmethod
    def can_create_pregnancy(sim_info: SimInfo, *_, **__) -> bool:
        """can_create_pregnancy(sim_info, *_, **__)

        Determine if a Sim is able to create a pregnancy.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim can produce a pregnancy. False, if not.
        :rtype: bool
        """
        return CommonSimPregnancyUtils.has_permission_for_pregnancies(sim_info).result

    @staticmethod
    def can_create_pregnancy_together(sim_info_a: SimInfo, sim_info_b: SimInfo, *_, **__) -> bool:
        """can_create_pregnancy_together(sim_info_a, sim_info_b, *_, **__)

        Determine if two Sims are capable of creating a pregnancy together.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if the Sim can produce a pregnancy. False, if not.
        :rtype: bool
        """
        return CommonSimPregnancyUtils.has_permission_for_pregnancies_with(sim_info_a, sim_info_b).result
