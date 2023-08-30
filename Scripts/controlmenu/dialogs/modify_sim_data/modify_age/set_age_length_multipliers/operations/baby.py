"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.set_age_length_multiplier_operation import \
    CMSetAgeLengthMultiplierOp
from controlmenu.settings.settings import CMSetting
from sims4communitylib.enums.common_age import CommonAge


class CMSetAgeLengthMultiplierBabyOp(CMSetAgeLengthMultiplierOp):
    """Set the age length multiplier for an Age."""

    @property
    def age(self) -> CommonAge:
        """The age the multiplier is for."""
        return CommonAge.BABY

    @property
    def setting(self) -> str:
        """The setting being modified."""
        return CMSetting.AGE_LENGTH_MULTIPLIER_BABY
