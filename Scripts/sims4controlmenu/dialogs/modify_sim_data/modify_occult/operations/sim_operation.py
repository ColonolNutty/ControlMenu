"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo


class S4CMSimOperation:
    """Perform an operation on a Sim"""
    def add(self, sim_info: SimInfo) -> bool:
        """Apply the operation."""
        raise NotImplementedError()

    def remove(self, sim_info: SimInfo) -> bool:
        """Reverse the operation."""
        raise NotImplementedError()
