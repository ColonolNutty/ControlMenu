"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class S4CMSimModifySkillsStringId(CommonInt):
    """String identifiers for the modify skills dialog."""
    MODIFY_SKILLS = 0x7F658567
    MAX_ALL_SKILLS = 0x24596042
    SET_SKILL_LEVELS = 0x016A7191
    # Tokens: {0.String} (Min) {1.String} (Max) {2.String} (Current)
    ENTER_A_VALE_BETWEEN_MIN_AND_MAX_FOR_SKILL = 0xE8FED0B1
    REMOVE_ALL_SKILLS = 0xAE29C02E
    ARE_YOU_SURE_YOU_WANT_TO_REMOVE_ALL_SKILLS_FROM_SIM = 0xAC6423AF
    ARE_YOU_SURE_YOU_WANT_TO_MAX_ALL_SKILLS_FOR_SIM = 0x9D537898

    REMOVED_ALL_SKILLS_TITLE = 0x919BAE0D
    REMOVED_ALL_SKILLS_DESCRIPTION = 0xA03F913E

    MAXED_ALL_SKILLS_TITLE = 0xDA696DED
    MAXED_ALL_SKILLS_DESCRIPTION = 0x48BF671E
