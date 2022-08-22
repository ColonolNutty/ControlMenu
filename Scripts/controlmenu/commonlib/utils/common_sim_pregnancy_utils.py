"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator

from sims.pregnancy.pregnancy_offspring_data import PregnancyOffspringData
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
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

    @staticmethod
    def get_number_of_babies(sim_info: SimInfo) -> int:
        """get_number_of_babies(sim_info)

        Retrieve the number of babies a Sim is pregnant with.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The number of babies a Sim is pregnant with or 0 if the Sim is not pregnant with babies.
        :rtype: int
        """
        if sim_info is None:
            return 0
        if not CommonSimPregnancyUtils.is_pregnant(sim_info):
            return 0
        pregnancy_tracker: PregnancyTracker = sim_info.pregnancy_tracker
        if pregnancy_tracker is None:
            return 0
        return pregnancy_tracker.offspring_count

    @staticmethod
    def get_babies_gen(sim_info: SimInfo) -> Iterator[PregnancyOffspringData]:
        """get_babies_gen(sim_info)

        Retrieve a collection of information about the babies a Sim is pregnant with.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of data about the babies a Sim is pregnant with.
        :rtype: Iterator[PregnancyOffspringData]
        """
        if sim_info is None:
            return tuple()
        if not CommonSimPregnancyUtils.is_pregnant(sim_info):
            return tuple()
        pregnancy_tracker: PregnancyTracker = sim_info.pregnancy_tracker
        if pregnancy_tracker is None:
            return tuple()
        yield from pregnancy_tracker.get_offspring_data_gen()
