"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo


class S4CMSimRelationshipUtils:
    """Relationship utils."""
    @staticmethod
    def are_family(sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """Determine if two Sims are family."""
        return not sim_info_a.incest_prevention_test(sim_info_b)
