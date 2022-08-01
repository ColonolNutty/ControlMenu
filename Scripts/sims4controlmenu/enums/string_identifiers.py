"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class S4CMStringId(CommonInt):
    """Identifiers for localization strings.

    .. note:: These identifiers point to text within String Tables within package files.

    """
    CONTROL_MENU = 2505893517
    DEBUG_COMMAND = 413439000
    CONFIRMATION = 2520436614
    YES = 979470758
    NO = 1668749452
    CANCEL = 2760337059
    NONE = 748895195

    # Dialogs
    MODIFY_SIM_DATA = 1795263806
    MODIFY_GAME_WORLD_DATA = 3470674117

    # Teleport
    CHOOSE_SIMS_TO_TELEPORT = 3029254654

    # Spawn
    CHOOSE_SIMS_TO_SPAWN = 487599508

    # Tokens: {0.String} (Default) {1.String} (Min) {2.String} (Max)
    DEFAULT_MIN_MAX = 0x1DFBED1C
