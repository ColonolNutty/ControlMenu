"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from controlmenu.dialogs.modify_sim_data.modify_perks._add_remove_perks_base_dialog import CMAddRemovePerksDialog
from controlmenu.dialogs.modify_sim_data.modify_perks.operations._perk_modify_base import CMPerkModifyOp
from controlmenu.dialogs.modify_sim_data.modify_perks.operations.vampire_powers import CMVampirePowersPerkAddOp
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_perks.operations.vampire_weaknesses import CMVampireWeaknessesPerkAddOp
from controlmenu.dialogs.modify_sim_data.modify_perks.operations.werewolf_abilities import CMWerewolfAbilitiesPerkAddOp
from controlmenu.dialogs.modify_sim_data.modify_perks.operations.werewolf_quest_abilities import \
    CMWerewolfQuestAbilitiesPerkAddOp
from controlmenu.dialogs.modify_sim_data.modify_perks.operations.witch_powers import CMWitchPowersPerkAddOp


class CMAddPerksDialog(CMAddRemovePerksDialog):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_add_perks_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.ADD_PERKS

    def _get_operations(self) -> Tuple[CMPerkModifyOp]:
        # noinspection PyTypeChecker
        return (
            CMVampirePowersPerkAddOp(),
            CMVampireWeaknessesPerkAddOp(),
            CMWitchPowersPerkAddOp(),
            CMWerewolfAbilitiesPerkAddOp(),
            CMWerewolfQuestAbilitiesPerkAddOp()
        )
