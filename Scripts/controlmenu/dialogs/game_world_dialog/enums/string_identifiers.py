"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CMGameWorldControlMenuStringId(CommonInt):
    """Identifiers for localization strings.

    .. note:: These identifiers point to text within String Tables within package files.

    """
    # Dialogs
    LOT_DATA = 0xBBB62312
    GAME_CLOCK = 0x36C0AF09

    # Clock
    SET_CLOCK_SPEED_SCALE = 0x161643FA
    SET_CLOCK_SPEED_SCALE_DESCRIPTION = 0x11DF58F6

    SET_CLOCK_SPEED = 0xBCD717D4
    SET_CLOCK_SPEED_STRING = 0x90807B2E
    SET_CLOCK_SPEED_DESCRIPTION = 0x08E5D321

    SET_REAL_MILLISECONDS_PER_SIM_SECOND = 0x55004CB3
    SET_REAL_MILLISECONDS_PER_SIM_SECOND_DESCRIPTION = 0x368A0827

    # Lots
    MAXIMUM_SIMS_PER_LOT_NAME = 0xFE955663
    MAXIMUM_SIMS_PER_LOT_DESCRIPTION = 0xA0977C9D

    CLEAR_LOT_CHANGES = 0xA8F79F66

    # Weather
    WEATHER = 0x12E95823
    CHANGE_WEATHER = 0x8527178D
    HOW_LONG_SHOULD_THE_WEATHER_LAST = 0x7079EEEE
    # Tokens: {0.String} (Temperature)
    TEMPERATURE = 0xF97BC1C8
    CLOUD_TYPE = 0x0CD2AFD1
    THUNDER_OR_LIGHTNING = 0x93D225E3
    CURRENT_WEATHER = 0xC88C4104

