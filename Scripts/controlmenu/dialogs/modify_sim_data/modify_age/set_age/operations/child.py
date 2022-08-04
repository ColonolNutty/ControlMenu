"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.common_age import CommonAge
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.set_age_operation import CMSetAgeOp


class CMSetAgeChildOp(CMSetAgeOp):
    """Set the age of a Sim to a Child."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def age(self) -> CommonAge:
        return CommonAge.CHILD
