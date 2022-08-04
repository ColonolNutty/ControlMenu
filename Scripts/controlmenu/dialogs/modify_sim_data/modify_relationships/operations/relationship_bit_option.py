"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CMRelationshipBitOption:
    """Used for displaying relationship options."""
    def __init__(self, display_name: LocalizedString, relationship_bit_id: int):
        self._display_name = display_name
        self.relationship_bit_id = relationship_bit_id

    def get_display_name(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> LocalizedString:
        """get_display_name(sim_info_a, sim_info_b)

        Create a display name for the relationship bit option.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: A localized string.
        :rtype: LocalizedString
        """
        return CommonLocalizationUtils.create_localized_string(self._display_name, tokens=(sim_info_a, sim_info_b))
