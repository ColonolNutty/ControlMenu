"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CMStringId(CommonInt):
    """Identifiers for localization strings.

    .. note:: These identifiers point to text within String Tables within package files.

    """
    CONTROL_MENU = 0x955CE68D
    DEBUG_COMMAND = 0x18A49418
    CONFIRMATION = 0x963ACF86
    YES = 0x3A6189A6
    NO = 0x6377188C
    CANCEL = 0xA48766A3
    NONE = 0x2CA33BDB

    # Dialogs
    MODIFY_SIM_DATA = 0x6B018D3E
    MODIFY_GAME_WORLD_DATA = 0xCEDE48C5

    # Teleport
    CHOOSE_SIMS_TO_TELEPORT = 0xB48EC1FE

    # Spawn
    CHOOSE_SIMS_TO_SPAWN = 0x1D102D94

    # Tokens: {0.String} (Default) {1.String} (Min) {2.String} (Max)
    DEFAULT_MIN_MAX = 0x1DFBED1C
