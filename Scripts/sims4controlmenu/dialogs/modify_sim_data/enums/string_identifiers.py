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
    # Tokens: {0.String} ({1.String})
    STRING_PAREN_STRING = 0x1A406429

    # Occult
    MODIFY_OCCULT = 879006419
    REMOVE_ALL_OCCULTS = 189227297
    BECOME_ALIEN = 1956449995
    BECOME_MERMAID = 2938731207
    BECOME_SERVO = 302966525
    BECOME_SERVO_CONFIRMATION_DESCRIPTION = 1093556519
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

    # Money
    MODIFY_CURRENCY = 3134381468
    ADD_SIMOLEONS = 1516458023
    REMOVE_SIMOLEONS = 1709812272
    HOW_MANY_SIMOLEONS = 3758395830

    # Relationships
    CHOOSE_LEVEL = 459152004
    ADD_HAS_MET = 0xBE410840
    REMOVE_HAS_MET = 0x0157739B
    HAS_MET = 0x41A3AFB5
    MODIFY_RELATIONSHIPS = 1948218806
    SET_RELATIONSHIPS_WITH_SIM = 0x51C40570
    SET_FRIENDSHIP_LEVEL = 633661945
    SET_ROMANCE_LEVEL = 2478274890
    SET_RELATIONSHIP_WITH_WHO = 3120840784
    MINIMUM = 3844515483
    MAXIMUM = 1330394413
    CHOOSE_FAMILY_RELATION = 1102595618
    # Tokens: {0.SimFirstName}{0.SimLastName} (Sim A) {1.SimFirstName} {1.SimLastName} (Sim B)
    CHOOSE_WHAT_SIM_WILL_BECOME_TO_SIM = 211089548
    SET_FAMILY_RELATIONS = 2797739938
    FORGET_SIMS = 35170218
    # Tokens: {0.SimFirstName}
    FORGET_SIMS_DESCRIPTION = 1805776721
    # Tokens: {0.SimFirstName}
    CHOOSE_SIMS_FOR_SIM_TO_FORGET = 2047163217
    CHOOSE_SIMS_TO_ADD_HAS_MET = 0xD9556577
    CHOOSE_SIMS_TO_REMOVE_HAS_MET = 0x3C861ED6

    CHOOSE_PARENT_RELATIONSHIP = 3402647200
    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim A) {1.String} (Relation) {2.SimFirstName} {2.SimLastName} (Sim B)
    SIM_WILL_BECOME_RELATIONSHIP_TO_SIM_CONFIRMATION_TEXT = 1370950998

    # Tokens: {0.SimFirstName}{0.SimLastName} (Sim A) {1.String} (Relation One) {2.String} (Relation 2) {3.SimFirstName} {3.SimLastName} (Sim B)
    WILL_SIM_BECOME_A_RELATION_OR_RELATION_TO_SIM = 2681670750

    FATHER = 2244853319
    MOTHER = 1643701804
    GRANDFATHER = 1642974687
    GRANDFATHER_ON_FATHERS_SIDE = 3652786356
    GRANDFATHER_ON_MOTHERS_SIDE = 4031303211
    GRANDMOTHER = 1275959364
    GRANDMOTHER_ON_FATHERS_SIDE = 3802449583
    GRANDMOTHER_ON_MOTHERS_SIDE = 294642596
    PARENT = 1600329685
    GRANDPARENT = 2790602765
    WHOSE_SIDE_OF_THE_FAMILY = 3101396661

    UPDATE_FAMILY_TREE_TITLE = 3381621033
    UPDATE_FAMILY_TREE_DESCRIPTION = 2332807826

    WHICH_PARENT_IS_SHARED = 4067889306
    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim A) {1.SimFirstName} {1.SimLastName} (Sim B)
    WHICH_PARENT_IS_SHARED_DESCRIPTION = 3758979209

    # Tokens: {0.SimFirstName} {0.SimLastName}
    SIM_NEEDS_TO_HAVE_MOTHER_OR_FATHER_BEFORE_YOU_CAN_ADD_UNCLES_OR_AUNTS_TO_THEM = 3221894912

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim) {1.String} (Relation Required) {2.String} (Relation To Add)
    SIM_NEEDS_TO_HAVE_A_RELATION_BEFORE_YOU_CAN_ADD_A_RELATION_TO_THEM = 1705229418

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim) {1.String} (Relation Required) {2.String} (Relation Required) {3.String} (Relation To Add)
    SIM_NEEDS_TO_HAVE_A_RELATION_OR_RELATION_BEFORE_YOU_CAN_ADD_A_RELATION_TO_THEM = 1280809925

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim) {1.String} (Relation 1) {2.String} (Relation 2) {3.SimFirstName} {3.SimLastName} (Sim)
    SIM_CANNOT_BE_BOTH_RELATION_AND_RELATION_OF_SIM = 2531370599

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim A) {1.String} (Relation)
    SIM_DOES_NOT_HAVE_A_RELATION = 806588682

    # Outfit
    CHANGE_OUTFIT = 94181272
    CHOOSE_OUTFIT = 2988267483

    # Traits
    MODIFY_TRAITS = 0xE11E0436
    REMOVE_TRAITS = 0xF6CBA3F4
    # Tokens: {0.String} (Trait Display Name) {1.String} (Trait Id)
    REMOVED_TRAIT_TITLE = 0xDA729790
    # Tokens: {0.SimFirstName} (Sim) {1.String} (Trait Display Name) {2.String} (Trait Id) {3.String} (Trait Tuning Name)
    REMOVED_TRAIT_DESCRIPTION = 0x07FF910B
    # Tokens: {0.String} (Trait Display Name) {1.String} (Trait Id) {2.String} (Trait Tuning Name) from {3.SimFirstName} (Sim)
    ARE_YOU_SURE_YOU_WANT_TO_REMOVE_TRAIT = 0x7C089D5A

    SET_PERSONALITY_TRAITS = 0x20CCE602
    # Tokens: {0.String} (Max Num Of Personality Traits)
    SET_PERSONALITY_TRAITS_MAX = 0x84DD2C14
    SET_PERSONALITY_TRAITS_TITLE = 0xF148D57D
    # Tokens: {0.SimFirstName} (Sim)
    SET_PERSONALITY_TRAITS_DESCRIPTION = 0x8DEFA22D

    # Buffs
    MODIFY_BUFFS = 0x399E3051
    REMOVE_BUFFS = 0xB7D6BB0B
    # Tokens: {0.String} (Buff Display Name) {1.String} (Buff Id)
    REMOVED_BUFF_TITLE = 0x0A91F13F
    # Tokens: {0.SimFirstName} (Sim) {1.String} (Buff Display Name) {2.String} (Buff Id) {3.String} (Buff Tuning Name)
    REMOVED_BUFF_DESCRIPTION = 0xEFA4E682
    # Tokens: {0.String} (Buff Display Name) {1.String} (Buff Id) {2.String} (Buff Tuning Name) from {3.SimFirstName} (Sim)
    ARE_YOU_SURE_YOU_WANT_TO_REMOVE_BUFF = 0x7C193D8F
