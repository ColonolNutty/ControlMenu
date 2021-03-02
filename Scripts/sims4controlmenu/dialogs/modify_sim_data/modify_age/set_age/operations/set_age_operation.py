"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4controlmenu.dialogs.modify_sim_data.sim_operation import S4CMSingleSimOperation


class S4CMSetAgeOp(S4CMSingleSimOperation):
    """Set the age of a Sim."""

    @property
    def age(self) -> CommonAge:
        """The age to set the Sim to when this operation is run."""
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo) -> bool:
        result = CommonAgeUtils.set_age(sim_info, self.age)
        if result:
            CommonSimSpawnUtils.soft_reset(sim_info, cause='S4CM Sim Age Change')
        return result
