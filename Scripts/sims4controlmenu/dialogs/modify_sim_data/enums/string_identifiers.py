"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class S4CMSimControlMenuStringId(CommonInt):
    """Identifiers for localization strings.

    .. note:: These identifiers point to strings within String Tables within package files.

    """
    # Occult
    MODIFY_OCCULT = 879006419
    REMOVE_ALL_OCCULTS = 189227297
    BECOME_ALIEN = 1956449995
    BECOME_MERMAID = 2938731207
    BECOME_SKELETON = 106772875
    BECOME_VAMPIRE = 909949252
    BECOME_WITCH = 1524706587

    # Age
    MODIFY_AGE = 3924124514
    SET_AGE = 3005632386

    # Pregnancy
    PREGNANCY = 1064352938
    CLEAR_PREGNANCY = 2112900273
    CREATE_PREGNANCY = 334844524
    INDUCE_LABOR = 2737414775
    # Tokens: {0.SimFirstName}
    SIM_IS_ALREADY_PREGNANT = 3327673946
    # Tokens: {0.SimFirstName}
    SIM_IS_NOT_PREGNANT = 1234364497
    # Tokens: {0.SimFirstName}
    SIM_IS_UNABLE_TO_CREATE_PREGNANCY = 146714267
    TOO_MANY_SIMS_IN_HOUSEHOLD_ALREADY = 1976601786
    WHO_WILL_BE_THE_OTHER_PARENT = 3284252776
    # Tokens: {0.SimFirstName}
    WHO_WILL_IMPREGNATE_SIM = 451291308
