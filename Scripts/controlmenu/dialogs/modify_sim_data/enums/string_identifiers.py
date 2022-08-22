"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CMSimControlMenuStringId(CommonInt):
    """Identifiers for localization strings.

    .. note:: These identifiers point to text within String Tables within package files.

    """
    # Tokens: {0.String} ({1.String})
    STRING_SPACE_PAREN_STRING = 0x1A406429
    # Tokens: {0.String}: {1.String}
    STRING_COLON_SPACE_STRING = 0x6284ACBA
    HIDDEN = 0xD7E16575

    # Occult
    MODIFY_OCCULT = 0x346492D3
    REMOVE_ALL_OCCULTS = 0x0B476121
    BECOME_ALIEN = 0x749D0ECB
    BECOME_MERMAID = 0xAF297AC7
    BECOME_PLANT_SIM = 0xFCD7BF4C
    BECOME_SERVO = 0x120EE6FD
    BECOME_SERVO_CONFIRMATION_DESCRIPTION = 0x412E5927
    BECOME_SKELETON = 0x065D398B
    BECOME_SCARECROW_CONFIRMATION_DESCRIPTION = 0x06611643
    BECOME_VAMPIRE = 0x363CB944
    BECOME_WITCH = 0x5AE12D1B

    # Tokens: {0.String} (Value)
    ADD_STRING = 0xC156E3A9
    # Tokens: {0.String} (Value)
    REMOVE_STRING = 0x197C2798
    # Tokens: {0.String} (Value)
    SWITCH_TO_STRING_FORM = 0x7890F3D3

    # Tokens: {0.SimFirstName}
    SIM_ALREADY_HAS_THIS_OCCULT = 0x7780F5C9
    # Tokens: {0.SimFirstName}
    SIM_DOES_NOT_HAVE_THIS_OCCULT = 0xB01467DB
    # Tokens: {0.SimFirstName}
    SIM_IS_ALREADY_IN_THIS_FORM = 0x4958758A
    CANNOT_ADD_ROBOT_OCCULT_TYPE_TO_SIM_WITH_OTHER_OCCULT_TYPES = 0x9E8E69B1
    CANNOT_ADD_THIS_OCCULT_TYPE_TO_A_ROBOT_SIM = 0x269E8F6A

    # Age
    MODIFY_AGE = 0xE9E56362
    SET_AGE = 0xB3264F82

    # Pregnancy
    PREGNANCY = 0x3F70BCAA
    CLEAR_PREGNANCY = 0x7DF04CB1
    CREATE_PREGNANCY = 0x13F5526C
    INDUCE_LABOR = 0xA329A277
    # Tokens: {0.SimFirstName}
    SIM_IS_ALREADY_PREGNANT = 0xC658465A
    # Tokens: {0.SimFirstName}
    SIM_IS_NOT_PREGNANT = 0x4992E851
    # Tokens: {0.SimFirstName}
    SIM_IS_UNABLE_TO_CREATE_PREGNANCY = 0x08BEAE9B
    TOO_MANY_SIMS_IN_HOUSEHOLD_ALREADY = 0x75D08CBA
    WHO_WILL_BE_THE_OTHER_PARENT = 0xC3C1B868
    # Tokens: {0.SimFirstName}
    WHO_WILL_IMPREGNATE_SIM = 0x1AE628AC
    SET_PREGNANCY_SPEED = 0x6920C40F
    SET_PREGNANCY_SPEED_DESCRIPTION = 0x335F7272
    # Tokens: {0.SimFirstName}
    OTHER_PARENT = 0x2C01701B

    # Money
    MODIFY_CURRENCY = 0xBAD2DD9C
    ADD_SIMOLEONS = 0x5A635027
    REMOVE_SIMOLEONS = 0x65E9AA30
    HOW_MANY_SIMOLEONS = 0xE00491B6

    # Relationships
    CHOOSE_LEVEL = 0x1B5E1A84
    ADD_HAS_MET = 0xBE410840
    REMOVE_HAS_MET = 0x0157739B
    HAS_MET = 0x41A3AFB5
    MODIFY_RELATIONSHIPS = 0x741F75B6
    SET_RELATIONSHIPS_WITH_SIM = 0x51C40570
    SET_FRIENDSHIP_LEVEL = 0x25C4E9F9
    SET_ROMANCE_LEVEL = 0x93B7794A
    SET_RELATIONSHIP_WITH_WHO = 0xBA044050
    MINIMUM = 0xE526A69B
    MAXIMUM = 0x4F4C352D
    CHOOSE_FAMILY_RELATION = 0x41B84622
    # Tokens: {0.SimFirstName}{0.SimLastName} (Sim A) {1.SimFirstName} {1.SimLastName} (Sim B)
    CHOOSE_WHAT_SIM_WILL_BECOME_TO_SIM = 0x0C94F88C
    SET_FAMILY_RELATIONS = 0xA6C21FA2
    FORGET_SIMS = 0x0218A7AA
    # Tokens: {0.SimFirstName}
    FORGET_SIMS_DESCRIPTION = 0x6BA1F751
    # Tokens: {0.SimFirstName}
    CHOOSE_SIMS_FOR_SIM_TO_FORGET = 0x7A053B51
    CHOOSE_SIMS_TO_ADD_HAS_MET = 0xD9556577
    CHOOSE_SIMS_TO_REMOVE_HAS_MET = 0x3C861ED6

    CHOOSE_PARENT_RELATIONSHIP = 0xCAD046A0
    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim A) {1.String} (Relation) {2.SimFirstName} {2.SimLastName} (Sim B)
    SIM_WILL_BECOME_RELATIONSHIP_TO_SIM_CONFIRMATION_TEXT = 0x51B70D56

    # Tokens: {0.SimFirstName}{0.SimLastName} (Sim A) {1.String} (Relation One) {2.String} (Relation 2) {3.SimFirstName} {3.SimLastName} (Sim B)
    WILL_SIM_BECOME_A_RELATION_OR_RELATION_TO_SIM = 0x9FD70C5E

    FATHER = 0x85CDBE47
    MOTHER = 0x61F8E62C
    GRANDFATHER = 0x61EDCDDF
    GRANDFATHER_ON_FATHERS_SIDE = 0xD9B918B4
    GRANDFATHER_ON_MOTHERS_SIDE = 0xF048CE2B
    GRANDMOTHER = 0x4C0D9844
    GRANDMOTHER_ON_FATHERS_SIDE = 0xE2A4C6AF
    GRANDMOTHER_ON_MOTHERS_SIDE = 0x118FE3A4
    PARENT = 0x5F6317D5
    GRANDPARENT = 0xA655380D
    WHOSE_SIDE_OF_THE_FAMILY = 0xB8DB8EB5

    UPDATE_FAMILY_TREE_TITLE = 0xC98F7129
    UPDATE_FAMILY_TREE_DESCRIPTION = 0x8B0BD292

    WHICH_PARENT_IS_SHARED = 0xF277109A
    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim A) {1.SimFirstName} {1.SimLastName} (Sim B)
    WHICH_PARENT_IS_SHARED_DESCRIPTION = 0xE00D7889

    # Tokens: {0.SimFirstName} {0.SimLastName}
    SIM_NEEDS_TO_HAVE_MOTHER_OR_FATHER_BEFORE_YOU_CAN_ADD_UNCLES_OR_AUNTS_TO_THEM = 0xC00A3700

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim) {1.String} (Relation Required) {2.String} (Relation To Add)
    SIM_NEEDS_TO_HAVE_A_RELATION_BEFORE_YOU_CAN_ADD_A_RELATION_TO_THEM = 0x65A3BC6A

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim) {1.String} (Relation Required) {2.String} (Relation Required) {3.String} (Relation To Add)
    SIM_NEEDS_TO_HAVE_A_RELATION_OR_RELATION_BEFORE_YOU_CAN_ADD_A_RELATION_TO_THEM = 0x4C579BC5

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim) {1.String} (Relation 1) {2.String} (Relation 2) {3.SimFirstName} {3.SimLastName} (Sim)
    SIM_CANNOT_BE_BOTH_RELATION_AND_RELATION_OF_SIM = 0x96E1A667

    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim A) {1.String} (Relation)
    SIM_DOES_NOT_HAVE_A_RELATION = 0x3013910A

    # Outfit
    CHANGE_OUTFIT = 0x059D1798
    CHOOSE_OUTFIT = 0xB21D57DB

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

    # Household
    HOUSEHOLD = 0x846D3A8C
    SET_MAXIMUM_HOUSEHOLD_SIZE = 0x874F35A5
    SET_MAXIMUM_HOUSEHOLD_SIZE_DESCRIPTION = 0x3EB6C306
