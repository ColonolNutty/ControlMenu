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

    # Ghosts
    DEATH = 0x2E72D6B1
    SET_DEATH_TYPE_NAME = 0x7497594B
    SET_DEATH_TYPE_DESCRIPTION = 0xC6E69659
    REVIVE_GHOSTS = 0x6D0EA1AA
    ALL_GHOST_SIMS = 0xA69B8A9D
    SPECIFIC_GHOST_SIMS = 0xDB6675E0
    REVIVE_SIM = 0x7B8FAAC0
    CHOOSE_GHOSTS_TO_REVIVE = 0xC38B04D4
    # Tokens: {0.String} (Number of Ghosts)
    CURRENT_NUMBER_OF_GHOSTS_STRING = 0x8D866983
    # Tokens: {0.SimFirstName} (Sim)
    SIM_IS_NOT_A_GHOST = 0xDCFE1538
    # Tokens: {0.SimFirstName} (Sim)
    SIM_IS_ALREADY_A_GHOST = 0x92BE45E9
    # Tokens: {0.String} (Number Revived)
    REVIVED_COUNT_GHOSTS = 0xAB7B4FE6
    # Tokens: {0.SimFirstName} (Sim)
    KILL_SIM = 0x9DA179E9
    # Tokens: {0.SimFirstName} (Sim)
    WHAT_GRUESOME_FATE_SHALL_BEFALL_SIM = 0x9C77ED49

    # Occult
    OCCULT = 0x4230AED3
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
    AGE = 0x489C3762
    SET_AGE = 0xB3264F82
    SET_AGE_LENGTH_MULTIPLIERS = 0x059C0076
    SET_AGE_LENGTH_MULTIPLIERS_DESCRIPTION = 0x49D8B964
    SET_AGE_LENGTH_MULTIPLIER = 0xE1815707
    SET_AGE_LENGTH_MULTIPLIER_DESCRIPTION = 0x62D273BE

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
    # Tokens: {0.String} (Number of babies)
    NUMBER_OF_BABIES = 0xFAE047FE
    # Tokens: {0.String} (A list of genders)
    GENDERS_OF_BABIES = 0x2495850D
    # Tokens: {0.String} (A list of species)
    SPECIES_OF_BABIES = 0x29CA68E1
    # Tokens: {0.String} (Percentage)
    PREGNANCY_PROGRESS_PERCENTAGE = 0x706C882B
    NOT_PREGNANT = 0xDACAB5EF
    # Tokens: {0.SimFirstName} (Sim)
    SIM_HAS_NO_PREGNANCY_DATA = 0x6B8F2687
    # Tokens: {0.String} (A list of details)
    BABY_DETAILS = 0x000A33FE
    REROLL_OFFSPRING = 0x3BC26007

    # Money
    CURRENCY = 0xE0E2599C
    ADD_SIMOLEONS = 0x5A635027
    REMOVE_SIMOLEONS = 0x65E9AA30
    HOW_MANY_SIMOLEONS = 0xE00491B6

    # Body
    BODY = 0x6DFE676D
    FAT_LEVEL = 0xB6DDB918
    FIT_LEVEL = 0x7D559F80
    WHAT_LEVEL = 0xFA892D50
    WHAT_LEVEL_OF_FAT_DESCRIPTION = 0xD2CC58A9
    WHAT_LEVEL_OF_FIT_DESCRIPTION = 0x718FC571

    # Name
    NAME = 0x2F8B3BF4
    CHANGE_THE_NAME_OF_A_SIM = 0x96E71222
    FIRST_NAME = 0x0E45B89E
    LAST_NAME = 0x1471ECFA
    PRONOUNS = 0xE467D949
    MODIFY_PRONOUNS_OF_A_SIM = 0x512A243A
    SELECT_FROM_DEFAULT_PRONOUNS_NAME = 0xA5AA9F10
    SELECT_FROM_DEFAULT_PRONOUNS_DESCRIPTION = 0xDFDF1FAA
    HE_HIM = 0x319E52E4
    SHE_HER = 0x3A6A85A8
    THEY_THEM = 0x7B143E99

    # Relationships
    CHOOSE_LEVEL = 0x1B5E1A84
    ADD_HAS_MET = 0xBE410840
    REMOVE_HAS_MET = 0x0157739B
    HAS_MET = 0x41A3AFB5
    RELATIONSHIPS = 0xA14EE9B6
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

    REMOVE_FAMILY_RELATIONS = 0x3ED0B64C
    REMOVE_RELATIONSHIP_BIT = 0x948CD333

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
    TRAITS = 0xEEEA2036
    ADD_TRAITS = 0x7AA8C421
    # Tokens: {0.String} (Trait Type)
    ADD_TRAITS_TYPE = 0xDFF3ABDB
    CHOOSE_A_TYPE_OF_TRAIT = 0xCE32067C
    LIKES = 0x86679BEF
    LIKES_DESCRIPTION = 0x6B0D778E
    DISLIKES = 0x677E5791
    DISLIKES_DESCRIPTION = 0x32533472
    LIKES_DISLIKES = 0xBA520FA2
    LIKES_DISLIKES_DESCRIPTION = 0x6983684F
    MODIFY_LIKES = 0xE462A7EF
    MODIFY_DISLIKES = 0x416EDB91
    MODIFY_LIKES_DISLIKES_DESCRIPTION = 0x879965E3
    # Tokens: {0.String} (Trait Display Name) {1.String} (Trait Id)
    ADDED_TRAIT_TITLE = 0x93730BD2
    # Tokens: {0.SimFirstName} (Sim) {1.String} (Trait Display Name) {2.String} (Trait Id) {3.String} (Trait Tuning Name)
    ADDED_TRAIT_DESCRIPTION = 0xD1F44152
    # Tokens: {0.String} (Trait Display Name) {1.String} (Trait Id)
    FAILED_TO_ADD_TRAIT_TITLE = 0x4DD52072
    # Tokens: {0.SimFirstName} (Sim) {1.String} (Trait Display Name) {2.String} (Trait Id) {3.String} (Trait Tuning Name)
    FAILED_TO_ADD_TRAIT_DESCRIPTION = 0xB5C879F2
    REMOVE_TRAITS = 0xF6CBA3F4
    # Tokens: {0.String} (Trait Display Name) {1.String} (Trait Id)
    REMOVED_TRAIT_TITLE = 0xDA729790
    # Tokens: {0.SimFirstName} (Sim) {1.String} (Trait Display Name) {2.String} (Trait Id) {3.String} (Trait Tuning Name)
    REMOVED_TRAIT_DESCRIPTION = 0x07FF910B
    # Tokens: {0.String} (Trait Display Name) {1.String} (Trait Id) {2.String} (Trait Tuning Name) from {3.SimFirstName} (Sim)
    ARE_YOU_SURE_YOU_WANT_TO_REMOVE_TRAIT = 0x7C089D5A
    # Tokens: {0.String} (Trait Display Name) {1.String} (Trait Id) {2.String} (Trait Tuning Name) to {3.SimFirstName} (Sim)
    ARE_YOU_SURE_YOU_WANT_TO_ADD_TRAIT = 0xA494A1AA

    SET_PERSONALITY_TRAITS = 0x20CCE602
    # Tokens: {0.String} (Max Num Of Personality Traits)
    SET_PERSONALITY_TRAITS_MAX = 0x84DD2C14
    SET_PERSONALITY_TRAITS_TITLE = 0xF148D57D
    # Tokens: {0.SimFirstName} (Sim)
    SET_PERSONALITY_TRAITS_DESCRIPTION = 0x8DEFA22D

    # Buffs
    BUFFS = 0xDBA32451
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

    SAVE_AND_EXIT_TO_MENU_REQUIRED = 0x896D523A
    PLEASE_SAVE_AND_EXIT_TO_MAIN_MENU = 0x0D338EEF

    # Statistics
    STATISTICS = 0xFB3848F4
    SET_STATISTIC_VALUES = 0x73907A39
    SET_COMMODITY_VALUES = 0x3BB472F6

    # Perks
    PERKS = 0x0654798C
    ADD_PERKS = 0x53B29CE1
    REMOVE_PERKS = 0x8F06BCCA
    VAMPIRE_POWERS = 0x5571C741
    VAMPIRE_WEAKNESSES = 0x1AE2D67E
    WITCH_POWERS = 0x54609AF8
    WEREWOLF_ABILITIES = 0x93E187E0
    WEREWOLF_QUEST_ABILITIES = 0xCDBFD2FA
    ALREADY_UNLOCKED_THIS_PERK = 0xABE82D88
    CONFLICTING_PERKS_ALREADY_UNLOCKED = 0x6A3EF7B1
    REQUIRED_PERKS_ARE_NOT_UNLOCKED = 0x63FA8D57
    PERK_NOT_UNLOCKED = 0xD41EA441

    # Walk Styles
    WALK_STYLE = 0x2CD79C11

    LIFESTYLES = 0xC4250FB5
    SET_LIFESTYLE_VALUES = 0x21423828
    TWO_LIFESTYLE_TYPES_DESCRIPTION = 0x25ACF2E5
    ONE_LIFESTYLE_TYPE_DESCRIPTION = 0xE269B782

    # Whims
    WHIMS = 0xC477C771
    ADD_WHIMS = 0xE7F175E4
    # Tokens: {0.String} (Whim Type)
    ADD_WHIMS_WHIM_TYPE = 0x3A114AA0
    CHOOSE_A_WHIM_SLOT = 0x480733CE
    APPLY_WHIMSET = 0x5989570A

    REMOVE_WHIMS = 0xDF9B6F03
    # Tokens: {0.String} (Whim Display Name) {1.String} (Whim Id)
    REMOVED_WHIM_TITLE = 0x7712390B
    # Tokens: {0.SimFirstName} (Sim) {1.String} (Whim Display Name) {2.String} (Whim Id) {3.String} (Whim Tuning Name)
    REMOVED_WHIM_DESCRIPTION = 0x87C14A22
    # Tokens: {0.String} (Whim Display Name) {1.String} (Whim Id) {2.String} (Whim Tuning Name) from {3.SimFirstName} (Sim)
    ARE_YOU_SURE_YOU_WANT_TO_REMOVE_WHIM = 0xC27F4DC7
    # Tokens: {0.String} (Whim Display Name) {1.String} (Whim Id) {2.String} (Whim Tuning Name) to {3.SimFirstName} (Sim)
    ARE_YOU_SURE_YOU_WANT_TO_ADD_WHIM = 0xC14E7DBD
