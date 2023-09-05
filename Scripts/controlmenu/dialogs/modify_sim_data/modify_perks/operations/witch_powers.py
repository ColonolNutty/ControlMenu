"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from bucks.bucks_enums import BucksType
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_perks.operations._perk_modify_base import CMPerkAddOp, CMPerkRemoveOp


class CMWitchPowersPerkAddOp(CMPerkAddOp):
    """Add Perks to a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_add_witch_powers'

    @property
    def bucks_perk_type(self) -> Union[BucksType, None]:
        """The type of bucks perk."""
        return getattr(BucksType, 'WitchPerkBucks', None)

    @property
    def title(self) -> int:
        """The title of the dialog."""
        return CMSimControlMenuStringId.WITCH_POWERS


class CMWitchPowersPerkRemoveOp(CMPerkRemoveOp):
    """Remove Perks from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_remove_witch_powers'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def bucks_perk_type(self) -> Union[BucksType, None]:
        return getattr(BucksType, 'WitchPerkBucks', None)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.WITCH_POWERS
