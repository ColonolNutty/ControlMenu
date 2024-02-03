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
    SIM = 0x22706EFA
    GAME_WORLD = 0x0DCD0F9F

    # Teleport
    CHOOSE_SIMS_TO_TELEPORT = 0xB48EC1FE

    # Spawn
    CHOOSE_SIMS_TO_SPAWN = 0x1D102D94

    # Tokens: {0.String} (Default) {1.String} (Min) {2.String} (Max)
    DEFAULT_MIN_MAX = 0x1DFBED1C

    CHOOSE_SIM = 0xD46633C2
    CHOOSE_SIM_TO_DO_INTERACTIONS = 0xCC398F21
    MANIPULATION_FAILED = 0x87082985
    MANIPULATION_SUCCESS = 0x960119E3
    NO_INTERACTIONS_FOUND = 0x6D8137D3
    # Tokens: {0.SimFirstName} (Sim Doing Interaction) {1.String} (Reason for fail)
    SIM_WAS_UNABLE_TO_PERFORM_THE_CHOSEN_INTERACTION_REASON = 0x36813300
    # Tokens: {0.SimFirstName} (Sim Doing Interaction)
    SIM_WILL_PERFORM_CHOSEN_INTERACTION = 0x04AA4E9F
    CHOOSE_INTERACTION = 0x6E8929D2
    # Tokens: {0.SimFirstName} (Sim Doing Interaction)
    CHOOSE_INTERACTION_FOR_SIM_TO_PERFORM = 0x0BF38EF9
    DISCLAIMER = 0xE664C8E0
    MANIPULATE_SIM_TO_PERFORM_DISCLAIMER_DESCRIPTION = 0x58ADB006

    # Mood Override
    # Tokens: {0.SimFirstName} (Sim)
    CHOOSE_MOOD_OVERRIDE = 0xD5ED6839
    CHOOSE_MOOD_OVERRIDE_DESCRIPTION = 0x8AFEFF47
