"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4controlmenu.commonlib.utils.common_sim_genealogy_utils import CommonSimGenealogyUtils


class S4CMFullFamily:
    """A Full Family"""

    def __init__(self, suffix: str='1') -> None:
        self._destroyed = False
        # Father 1 Side:
        self.grandfather_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandfather', last_name='One' + suffix)
        self.grandmother_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandmother', last_name='One' + suffix)
        self.uncle_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='One' + suffix)
        self.uncle_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='Two' + suffix)
        self.father_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Father', last_name='One' + suffix)
        self.cousin_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='One' + suffix)
        self.cousin_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Two' + suffix)
        self.cousin_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Three' + suffix)
        self.cousin_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Four' + suffix)

        # Father 2 Side:
        self.grandfather_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandfather', last_name='Two' + suffix)
        self.grandmother_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandmother', last_name='Two' + suffix)
        self.uncle_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='Three' + suffix)
        self.uncle_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='Four' + suffix)
        self.father_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Father', last_name='Two' + suffix)
        self.cousin_five: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Five' + suffix)
        self.cousin_six: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Six' + suffix)
        self.cousin_seven: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Seven' + suffix)
        self.cousin_eight: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Eight' + suffix)

        # Mother 1 Side:
        self.grandfather_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandfather', last_name='Three' + suffix)
        self.grandmother_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandmother', last_name='Three' + suffix)
        self.uncle_five: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='Five' + suffix)
        self.uncle_six: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='Six' + suffix)
        self.mother_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Mother', last_name='One' + suffix)
        self.cousin_nine: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Nine' + suffix)
        self.cousin_ten: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Ten' + suffix)
        self.cousin_eleven: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Eleven' + suffix)
        self.cousin_twelve: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Twelve' + suffix)

        # Mother 1 Side:
        self.grandfather_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandfather', last_name='Four' + suffix)
        self.grandmother_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandmother', last_name='Four' + suffix)
        self.uncle_seven: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='Seven' + suffix)
        self.uncle_eight: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Uncle', last_name='Eight' + suffix)
        self.mother_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Mother', last_name='Two' + suffix)
        self.cousin_thirteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Thirteen' + suffix)
        self.cousin_fourteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Fourteen' + suffix)
        self.cousin_fifteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Fifteen' + suffix)
        self.cousin_sixteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Sixteen' + suffix)

        # Aunt 1 Side:
        self.grandfather_five: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandfather', last_name='Five' + suffix)
        self.grandmother_five: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandmother', last_name='Five' + suffix)
        self.aunt_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Aunt', last_name='Two' + suffix)
        self.aunt_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Aunt', last_name='One' + suffix)
        self.cousin_seventeen: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Seventeen' + suffix)
        self.cousin_eighteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Eighteen' + suffix)

        # Aunt 3 Side:
        self.grandfather_six: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandfather', last_name='Six' + suffix)
        self.grandmother_six: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandmother', last_name='Six' + suffix)
        self.aunt_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Aunt', last_name='Three' + suffix)
        self.aunt_four: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Aunt', last_name='Four' + suffix)
        self.cousin_nineteen: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Nineteen' + suffix)
        self.cousin_twenty: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Cousin', last_name='Twenty' + suffix)

        # Children:
        self.child_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Child', last_name='One' + suffix)
        self.child_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Child', last_name='Two' + suffix)
        self.grand_child_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandchild', last_name='One' + suffix)
        self.grand_child_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Grandchild', last_name='Two' + suffix)
        self.step_child_one: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Step Child', last_name='One' + suffix)
        self.step_child_two: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Step Child', last_name='Two' + suffix)
        self.step_child_three: SimInfo = CommonSimSpawnUtils.create_human_sim_info(first_name='Step Child', last_name='Three' + suffix)

        self._setup_relationships()

    def _setup_relationships(self) -> None:
        if hasattr(self, '_destroyed') and getattr(self, '_destroyed', False):
            raise AssertionError('Full Family has already been destroyed!')

        # Father 1 Side:
        # Grandfather 1 (Parent of Father 1, Uncle 1, and Uncle 2, Step Parent of Mother 1, Mother 2, Aunt 3, Aunt 4, Uncle 5, 6, 7, and 8, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4, Step Grandparent of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20)
        # Grandmother 1 (Parent of Father 1, Uncle 1, and Uncle 2, Step Parent of Mother 1, Mother 2, Aunt 3, Aunt 4, Uncle 5, 6, 7, and 8, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4, Step Grandparent of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20)
        # Uncle 1 (Child of Grandfather 1 and Grandmother 1, Step Child of Grandfather 4, Grandfather 3, Grandfather 6, Grandmother 4, Grandmother 3, Grandmother 6, Sibling of Father 1 and Uncle 2, Step Sibling of Mother 1, Mother 2, Aunt 3, Aunt 4, Uncle 5, 6, 7, 8, Parent of Cousin 1 and Cousin 2, Uncle of Child 1, Child 2, Step Child 2, Cousin 3, and Cousin 4, Step Uncle of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20)
        # Uncle 2 (Child of Grandfather 1 and Grandmother 1, Step Child of Grandfather 4, Grandfather 3, Grandfather 6, Grandmother 4, Grandmother 3, Grandmother 6, Sibling of Father 1 and Uncle 1, Step Sibling of Mother 1, Mother 2, Aunt 4, Uncle 5, 6, 7, 8, Parent of Cousin 3 and Cousin 4, Uncle of Child 1, Child 2, Step Child 2, Cousin 1, and Cousin 2, Step Uncle of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20)
        # Father 1 (Child of Grandfather 1 and Grandmother 1, Step Child of Grandfather 4, Grandfather 3, Grandfather 6, Grandmother 4, Grandmother 3, Grandmother 6, Sibling of Uncle 1 and Uncle 2, Step Sibling of Aunt 3, Aunt 4, Uncle 5, 6, 7, 8, Parent of Child 1, Child 2, and Step Child 2, Step Parent of Step Child 1, Uncle of Cousin 1, 2, 3, and 4, Step Uncle of Cousin 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20)
        # Cousin 1 (Child of Uncle 1, Sibling of Cousin 2, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20, Grandchild of Grandfather 1 and Grandmother 1, Step Grandchild of Grandfather 3, Grandfather 4, Grandfather 6, Grandmother 3, Grandmother 4, and Grandmother 6, Nephew of Uncle 2 and Father 1, Step Nephew of Mother 1, Mother 2, Aunt 3, Aunt 4, Uncle 5, 6, 7, 8)
        # Cousin 2 (Child of Uncle 1, Sibling of Cousin 1, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20, Grandchild of Grandfather 1 and Grandmother 1, Step Grandchild of Grandfather 3, Grandfather 4, Grandfather 6, Grandmother 3, Grandmother 4, and Grandmother 6, Nephew of Uncle 2 and Father 1, Step Nephew of Mother 1, Mother 2, Aunt 3, Aunt 4, Uncle 5, 6, 7, 8)
        # Cousin 3 (Child of Aunt 3 and Uncle 2, Sibling of Cousin 4, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20, Grandchild of Grandfather 1, Grandfather 6, Grandmother 1, and Grandmother 6, Step Grandchild of Grandfather 3, Grandfather 4, Grandmother 3, and Grandmother 4, Nephew of Aunt 4, Uncle 1, and Father 1, Step Nephew of Mother 1, Mother 2, Uncle 5, 6, 7, 8)
        # Cousin 4 (Child of Aunt 3 and Uncle 2, Sibling of Cousin 3, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20, Grandchild of Grandfather 1, Grandfather 6, Grandmother 1, and Grandmother 6, Step Grandchild of Grandfather 3, Grandfather 4, Grandmother 3, and Grandmother 4, Nephew of Aunt 4, Uncle 1, and Father 1, Step Nephew of Mother 1, Mother 2, Uncle 5, 6, 7, 8)
        self._setup_father_one_side()

        # Father 2 Side:
        # Grandfather 2 (Parent of Father 2, Uncle 3, and Uncle 4, Step Parent of Mother 1, Uncle 5 and Uncle 6, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8, Step Grandparent of Child 1, Child 2, Cousin 9, 10, 11, and 12)
        # Grandmother 2 (Parent of Father 2, Uncle 3, and Uncle 4, Step Parent of Mother 1, Uncle 5 and Uncle 6, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8, Step Grandparent of Child 1, Child 2, Cousin 9, 10, 11, and 12)
        # Uncle 3 (Child of Grandfather 2 and Grandmother 2, Step Child of Grandfather 3 and Grandmother 3, Sibling of Father 2 and Uncle 4, Step Sibling of Mother 1, Uncle 5, and Uncle 6, Parent of Cousin 5 and Cousin 6, Uncle of Step Child 1, Cousin 7, and Cousin 8, Step Uncle of Child 1, Child 2, Cousin 9, 10, 11, and 12)
        # Uncle 4 (Child of Grandfather 2 and Grandmother 2, Step Child of Grandfather 3 and Grandmother 3, Sibling of Father 2 and Uncle 3, Step Sibling of Mother 1, Uncle 5, and Uncle 6, Parent of Cousin 7 and Cousin 8, Uncle of Step Child 1, Cousin 5, and Cousin 6, Step Uncle of Child 1, Child 2, Cousin 9, 10, 11, and 12)
        # Father 2 (Child of Grandfather 2 and Grandmother 2, Step Child of Grandfather 3 and Grandmother 3, Sibling of Uncle 3 and Uncle 4, Step Sibling of Uncle 5 and Uncle 6, Parent of Step Child 1, Step Parent of Child 1 and Child 2, Uncle of Cousin 5, 6, 7, and 8, Step Uncle of Child 1, Child 2, Cousin 9, 10, 11, and 12)
        # Cousin 5 (Child of Uncle 3, Sibling of Cousin 6, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 7, 8, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 4 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        # Cousin 6 (Child of Uncle 3, Sibling of Cousin 5, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 7, 8, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 4 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        # Cousin 7 (Child of Uncle 4, Sibling of Cousin 8, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 5, 6, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 3 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        # Cousin 8 (Child of Uncle 4, Sibling of Cousin 7, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 5, 6, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 3 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        self._setup_father_two_side()

        # Mother 1 Side:
        # Grandfather 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Step Parent of Father 1, Father 2, Uncle 1, 2, 3, and 4, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12, Step Grandparent of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        # Grandmother 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Step Parent of Father 1, Father 2, Uncle 1, 2, 3, and 4, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12, Step Grandparent of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        # Uncle 5 (Child of Grandfather 3 and Grandmother 3, Step Child of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Sibling of Mother 1 and Uncle 6, Step Sibling of Father 1, Father 2, Aunt 1, Aunt 2, Uncle 1, 2, 3, and 4, Parent of Cousin 11 and Cousin 12, Uncle of Child 1, Child 2, Step Child 1, Cousin 9, and Cousin 10, Step Uncle of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        # Uncle 6 (Child of Grandfather 3 and Grandmother 3, Step Child of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Sibling of Mother 1 and Uncle 5, Step Sibling of Father 1, Father 2, Aunt 2, Uncle 1, 2, 3, and 4, Parent of Cousin 9 and Cousin 10, Uncle of Child 1, Child 2, Step Child 1, Cousin 11, and Cousin 12, Step Uncle of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        # Mother 1 (Child of Grandfather 3 and Grandmother 3, Step Child of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, Grandmother 5, Sibling of Uncle 5 and Uncle 6, Step Sibling of Aunt 1, Aunt 2, Uncle 1, 2, 3, and 4, Parent of Child 1, Child 2, and Step Child 1, Step Parent of Step Child 2, Aunt of Cousin 9, 10, 11, and 12, Step Aunt of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        # Cousin 9 (Child of Uncle 6, Sibling of Cousin 10, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 17, and 18, Grandchild of Grandfather 3, Grandfather 5, Grandmother 3, and Grandmother 5, Step Grandchild of Grandfather 2, Grandfather 1, Grandmother 2, and Grandmother 1, Nephew of Aunt 2, Uncle 5, and Mother 1, Step Nephew of Father 1, Father 2, Uncle 1, 2, 3, and 4)
        # Cousin 10 (Child of Uncle 6, Sibling of Cousin 9, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 17, and 18, Grandchild of Grandfather 3, Grandfather 5, Grandmother 3, and Grandmother 5, Step Grandchild of Grandfather 2, Grandfather 1, Grandmother 2, and Grandmother 1, Nephew of Aunt 2, Uncle 5, and Mother 1, Step Nephew of Father 1, Father 2, Uncle 1, 2, 3, and 4)
        # Cousin 11 (Child of Uncle 5, Sibling of Cousin 12, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, and 18, Grandchild of Grandfather 3 and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Nephew of Uncle 6, and Mother 1, Step Nephew of Aunt 1, Aunt 2, Father 1, Father 2, Uncle 1, 2, 3, and 4)
        # Cousin 12 (Child of Uncle 5, Sibling of Cousin 11, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, and 18, Grandchild of Grandfather 3 and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Nephew of Uncle 6 and Mother 1, Step Nephew of Aunt 1, Aunt 2, Father 1, Father 2, Uncle 1, 2, 3, and 4)
        self._setup_mother_one_side()

        # Mother 2 Side:
        # Grandfather 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16, Step Grandparent of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        # Grandmother 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16, Step Grandparent of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        # Uncle 7 (Child of Grandfather 4 and Grandmother 4, Step Child of Grandfather 1 and Grandmother 1, Sibling of Mother 2 and Uncle 8, Step Sibling of Father 1, Uncle 1, and Uncle 2, Parent of Cousin 13 and Cousin 14, Uncle of Step Child 2, Cousin 15, and Cousin 16, Step Uncle of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        # Uncle 8 (Child of Grandfather 4 and Grandmother 4, Step Child of Grandfather 1 and Grandmother 1, Sibling of Mother 2 and Uncle 7, Step Sibling of Father 1, Uncle 1, and Uncle 2, Parent of Cousin 15 and Cousin 16, Uncle of Step Child 2, Cousin 13, and Cousin 14, Step Uncle of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        # Mother 2 (Child of Grandfather 4 and Grandmother 4, Step Child of Grandfather 1 and Grandmother 1, Sibling of Uncle 7 and Uncle 8, Step Sibling of Uncle 1, and Uncle 2, Parent of Step Child 2, Step Parent of Child 1 and Child 2, Aunt of Cousin 13, 14, 15, and 16, Step Aunt of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        # Cousin 13 (Child of Uncle 7, Sibling of Cousin 14, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 8 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        # Cousin 14 (Child of Uncle 7, Sibling of Cousin 13, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 8 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        # Cousin 15 (Child of Uncle 8, Sibling of Cousin 16, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 7 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        # Cousin 16 (Child of Uncle 8, Sibling of Cousin 15, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 7 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        self._setup_mother_two_side()

        # Aunt 1 Side:
        # Grandfather 5 (Parent of Aunt 1 and Aunt 2, Step Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Cousin 9, 10, 17, and 18, Step Grandparent of Child 1, Child 2, Step Child 1, Step Child 2, Cousin 11, 12)
        # Grandmother 5 (Parent of Aunt 1 and Aunt 2, Step Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Cousin 9, 10, 17, and 18, Step Grandparent of Child 1, Child 2, Step Child 1, Step Child 2, Cousin 11, 12)
        # Aunt 2 (Child of Grandfather 5 and Grandmother 5, Step Child of Grandfather 3 and Grandmother 3, Sibling of Aunt 1, Step Sibling of Mother 1, Uncle 5, and Uncle 6, Parent of Cousin 17 and Cousin 18, Aunt of Cousin 9 and Cousin 10, Step Aunt of Child 1, Child 2, Step Child 1, Step Child 2, Cousin 11, and Cousin 12)
        # Aunt 1 (Child of Grandfather 5 and Grandmother 5, Step Child of Grandfather 3, and Grandmother 3, Sibling of Aunt 2, Step Sibling of Mother 1 and Uncle 5, Parent of Cousin 9 and Cousin 10, Aunt of Cousin 17 and Cousin 18, Step Aunt of Child 1, Child 2, Step Child 1, Step Child 2, Cousin 11, and Cousin 12)
        # Cousin 17 (Child of Aunt 2, Sibling of Cousin 18, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 9, 10, 11, and 12, Grandchild of Grandfather 5 and Grandmother 5, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Aunt 1, Step Nephew of Mother 1, Uncle 5, and Uncle 6)
        # Cousin 18 (Child of Aunt 2, Sibling of Cousin 17, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 9, 10, 11, and 12, Grandchild of Grandfather 5 and Grandmother 5, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Aunt 1, Step Nephew of Mother 1, Uncle 5, and Uncle 6)
        self._setup_aunt_one_side()

        # Aunt 3 Side:
        # Grandfather 6 (Parent of Aunt 3 and Aunt 4, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Cousin 3, 4, 19, and 20, Step Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2)
        # Grandmother 6 (Parent of Aunt 3 and Aunt 4, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Cousin 3, 4, 19, and 20, Step Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2)
        # Aunt 3 (Child of Grandfather 6 and Grandmother 6, Step Child of Grandfather 1, and Grandmother 1, Sibling of Aunt 4, Step Sibling of Father 1 and Uncle 1, Parent of Cousin 3 and Cousin 4, Aunt of Cousin 19 and Cousin 20, Step Aunt of Child 1, Child 2, Step Child 2, Cousin 1, and Cousin 2)
        # Aunt 4 (Child of Grandfather 6 and Grandmother 6, Step Child of Grandfather 1 and Grandmother 1, Sibling of Aunt 3, Step Sibling of Father 1, Uncle 1, and Uncle 2, Parent of Cousin 19 and Cousin 20, Aunt of Cousin 3 and Cousin 4, Step Aunt of Child 1, Child 2, Step Child 2, Cousin 1, and Cousin 2)
        # Cousin 19 (Child of Aunt 4, Sibling of Cousin 20, Cousin of Child 1, Child 2, Step Child 2, and Cousin 1, 2, 3, and 4, Grandchild of Grandfather 6 and Grandmother 6, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Aunt 3, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        # Cousin 20 (Child of Aunt 4, Sibling of Cousin 19, Cousin of Child 1, Child 2, Step Child 2, and Cousin 1, 2, 3, and 4, Grandchild of Grandfather 6 and Grandmother 6, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Aunt 3, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        self._setup_aunt_three_side()

        # Children:
        # Child 1 (Child of Father 1 and Mother 1, Step Child of Father 2 and Mother 2, Sibling of Child 2, Step Child 1, and Step Child 2, Step Sibling of Step Child 3, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 4, Grandfather 5, Grandfather 6, Grandmother 2, Grandmother 4, Grandmother 5, and Grandmother 6, Nephew of Uncle 1, 2, 5, and 6, Step Nephew of Uncle 3, 4, 7, and 8)
        # Child 2 (Child of Father 1 and Mother 1, Step Child of Father 2 and Mother 2, Sibling of Child 1, Step Child 1, and Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 4, Grandfather 5, Grandfather 6, Grandmother 2, Grandmother 4, Grandmother 5, and Grandmother 6, Nephew of Uncle 1, 2, 5, and 6, Step Nephew of Uncle 3, 4, 7, and 8)
        # Grandchild 1 (Child of Child 2 and Step Child 3, Sibling of Grandchild 2, Grandchild of Mother 1 and Father 1, Step Grandchild of Father 2 and Mother 2, Nephew of Child 1, Step Nephew of Step Child 1 and Step Child 2)
        # Grandchild 2 (Child of Child 2 and Step Child 3, Sibling of Grandchild 1, Grandchild of Mother 1 and Father 1, Step Grandchild of Father 2 and Mother 2, Nephew of Child 1, Step Nephew of Step Child 1 and Step Child 2)
        # Step Child 1 (Child of Mother 1 and Father 2, Step Child of Father 1, Sibling of Child 1 and Child 2, Step Sibling of Step Child 2 and Step Child 3, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, and 18, Grandchild of Grandfather 2, Grandfather 3, Grandmother 2, and Grandmother 3, Step Grandchild of Grandfather 1, Grandfather 5, Grandmother 1, and Grandmother 5, Nephew of Uncle 3, 4, 5, and 6, Step Nephew of Uncle 1 and Uncle 2, Step Uncle of Grandchild 1 and Grandchild 2)
        # Step Child 2 (Child of Father 1 and Mother 2, Step Child of Mother 1, Sibling of Child 1 and Child 2, Step Sibling of Step Child 1 and Step Child 3, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20, Grandchild of Grandfather 1, Grandfather 4, Grandmother 1, and Grandmother 4, Step Grandchild of Grandfather 3, Grandfather 6, Grandmother 3, and Grandmother 6, Nephew of Uncle 1, 2, 7, and 8, Step Nephew of Uncle 5 and Uncle 6, Step Uncle of Grandchild 1 and Grandchild 2)
        # Step Child 3 (Step Child of Mother 1 and Father 1, Step Sibling Child 1, Step Child 1, and Step Child 2, Step Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Step Nephew of Uncle 1, 2, 5, and 6)
        self._setup_children()

    def _setup_father_one_side(self) -> None:
        # Grandfather 1 (Parent of Father 1, Uncle 1, and Uncle 2, Step Parent of Mother 1, Mother 2, Aunt 3, Aunt 4, Uncle 5, 6, 7, and 8, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4, Step Grandparent of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, and 16)
        # Grandmother 1 (Parent of Father 1, Uncle 1, and Uncle 2, Step Parent of Mother 1, Mother 2, Aunt 3, Aunt 4, Uncle 5, 6, 7, and 8, Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2, 3, and 4, Step Grandparent of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, and 16)
        grandparents_one_children = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        grandparents_one_step_children = (
            self.mother_one,
            self.mother_two,
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight,
            self.aunt_three,
            self.aunt_four
        )

        grandparents_one_grandchildren = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        grandparents_one_step_grandchildren = (
            self.step_child_one,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty,
            self.step_child_three
        )

        # Grandfather
        for child in grandparents_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_one, child)

        for step_child in grandparents_one_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_one, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_one_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_one, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_father_of(self.grandfather_one, grandchild)

        for step_grandchild in grandparents_one_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_one, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Grandmother
        for child in grandparents_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_one, child)

        for step_child in grandparents_one_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_one, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_one_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_one, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(self.grandmother_one, grandchild)

        for step_grandchild in grandparents_one_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_one, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Uncle 1 (Child of Grandfather 1 and Grandmother 1, Step Child of Grandfather 4, Grandfather 3, Grandmother 4, and Grandmother 3, Sibling of Father 1 and Uncle 2, Step Sibling of Mother 1, Mother 2, Uncle 5, 6, 7, 8, Parent of Cousin 1 and Cousin 2, Uncle of Child 1, Child 2, Step Child 2, Cousin 3, and Cousin 4, Step Uncle of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, and 16)
        uncle_one_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        uncle_one_step_parents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_four,
            self.grandmother_four,
            self.grandfather_six,
            self.grandmother_six
        )

        uncle_one_siblings = (
            self.father_one,
            self.uncle_two
        )

        uncle_one_step_siblings = (
            self.mother_one,
            self.mother_two,
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight,
            self.aunt_three,
            self.aunt_four
        )

        uncle_one_children = (
            self.cousin_one,
            self.cousin_two
        )

        uncle_one_nephews = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_three,
            self.cousin_four
        )

        uncle_one_step_nephews = (
            self.step_child_one,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty,
            self.step_child_three
        )

        for parent in uncle_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_one_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_one, child)

        for nephew in uncle_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_one_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_one, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 2 (Child of Grandfather 1 and Grandmother 1, Step Child of Grandfather 4, Grandfather 3, Grandmother 4, and Grandmother 3, Sibling of Father 1 and Uncle 1, Step Sibling of Mother 1, Mother 2, Uncle 5, 6, 7, 8, Parent of Cousin 3 and Cousin 4, Uncle of Child 1, Child 2, Step Child 2, Cousin 1, and Cousin 2, Step Uncle of Step Child 1, Cousin 9, 10, 11, 12, 13, 14, 15, and 16)
        uncle_two_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        uncle_two_step_parents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_four,
            self.grandmother_four,
            self.grandfather_six,
            self.grandmother_six
        )

        uncle_two_siblings = (
            self.father_one,
            self.uncle_one
        )

        uncle_two_step_siblings = (
            self.mother_one,
            self.mother_two,
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight,
            self.aunt_four
        )

        uncle_two_children = (
            self.cousin_three,
            self.cousin_four
        )

        uncle_two_nephews = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        uncle_two_step_nephews = (
            self.step_child_one,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.step_child_three
        )

        for parent in uncle_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_two_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_two_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_two, child)

        for nephew in uncle_two_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_two_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_two, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Father 1 (Child of Grandfather 1 and Grandmother 1, Step Child of Grandfather 4, Grandfather 3, Grandmother 4, and Grandmother 3, Sibling of Uncle 1 and Uncle 2, Step Sibling of Mother 2, Uncle 5, 6, 7, 8, Parent of Child 1, Child 2, and Step Child 2, Step Parent of Step Child 1, Uncle of Cousin 1, 2, 3, and 4, Step Uncle of Cousin 9, 10, 11, 12, 13, 14, 15, and 16)
        father_one_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        father_one_step_parents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_four,
            self.grandmother_four,
            self.grandfather_six,
            self.grandmother_six
        )

        father_one_siblings = (
            self.uncle_one,
            self.uncle_two
        )

        father_one_step_siblings = (
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight,
            self.aunt_three,
            self.aunt_four
        )

        father_one_children = (
            self.child_one,
            self.child_two,
            self.step_child_two
        )

        father_one_step_children = (
            self.step_child_one,
            self.step_child_three
        )

        father_one_grandchildren = (
            self.grand_child_one,
            self.grand_child_two
        )

        father_one_nephews = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        father_one_step_nephews = (
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        for parent in father_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in father_one_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in father_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in father_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in father_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.father_one, child)

        for step_child in father_one_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in father_one_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_father_of(self.father_one, grandchild)

        for nephew in father_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in father_one_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.father_one, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 1 (Child of Uncle 1, Sibling of Cousin 2, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Step Grandchild of Grandfather 3, Grandfather 4, Grandmother 3, and Grandmother 4, Nephew of Uncle 2 and Father 1, Step Nephew of Mother 1, Mother 2, Uncle 5, 6, 7, 8)
        cousin_one_parents = (
            self.uncle_one,
        )

        cousin_one_siblings = (
            self.cousin_two,
        )

        cousin_one_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_three,
            self.cousin_four,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        cousin_one_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_one_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_four,
            self.grandmother_four,
            self.grandfather_six,
            self.grandmother_six
        )

        cousin_one_uncles_and_aunts = (
            self.uncle_two,
            self.father_one
        )

        cousin_one_step_uncles_and_aunts = (
            self.mother_one,
            self.mother_two,
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight,
            self.aunt_three,
            self.aunt_four
        )

        for parent in cousin_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_one_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_one_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_one_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_one_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_one_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_one, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 2 (Child of Uncle 1, Sibling of Cousin 1, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 3, 4, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Step Grandchild of Grandfather 3, Grandfather 4, Grandmother 3, and Grandmother 4, Nephew of Uncle 2 and Father 1, Step Nephew of Mother 1, Mother 2, Uncle 5, 6, 7, 8)
        cousin_two_parents = (
            self.uncle_one,
        )

        cousin_two_siblings = (
            self.cousin_one,
        )

        cousin_two_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_three,
            self.cousin_four,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        cousin_two_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_two_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_four,
            self.grandmother_four,
            self.grandfather_six,
            self.grandmother_six
        )

        cousin_two_uncles_and_aunts = (
            self.uncle_two,
            self.father_one
        )

        cousin_two_step_uncles_and_aunts = (
            self.mother_one,
            self.mother_two,
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight,
            self.aunt_three,
            self.aunt_four
        )

        for parent in cousin_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_two_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_two_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_two_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_two_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_two_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_two, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 3 (Child of Uncle 2, Sibling of Cousin 4, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Step Grandchild of Grandfather 3, Grandfather 4, Grandmother 3, and Grandmother 4, Nephew of Uncle 1 and Father 1, Step Nephew of Mother 1, Mother 2, Uncle 5, 6, 7, 8)
        cousin_three_parents = (
            self.uncle_two,
            self.aunt_three
        )

        cousin_three_siblings = (
            self.cousin_four,
        )

        cousin_three_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_one,
            self.cousin_two,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        cousin_three_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_six,
            self.grandmother_six
        )

        cousin_three_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_three_uncles_and_aunts = (
            self.uncle_one,
            self.father_one,
            self.aunt_four
        )

        cousin_three_step_uncles_and_aunts = (
            self.mother_one,
            self.mother_two,
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight
        )

        for parent in cousin_three_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_three_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_three_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_three_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_three_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_three_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_three_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_three, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 4 (Child of Uncle 2, Sibling of Cousin 3, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 9, 10, 11, 12, 13, 14, 15, and 16, Grandchild of Grandfather 1 and Grandmother 1, Step Grandchild of Grandfather 3, Grandfather 4, Grandmother 3, and Grandmother 4, Nephew of Uncle 1 and Father 1, Step Nephew of Mother 1, Mother 2, Uncle 5, 6, 7, 8)
        cousin_four_parents = (
            self.aunt_three,
            self.uncle_two
        )

        cousin_four_siblings = (
            self.cousin_three,
        )

        cousin_four_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_one,
            self.cousin_two,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        cousin_four_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_six,
            self.grandmother_six
        )

        cousin_four_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_four_uncles_and_aunts = (
            self.uncle_one,
            self.father_one,
            self.aunt_four
        )

        cousin_four_step_uncles_and_aunts = (
            self.mother_one,
            self.mother_two,
            self.uncle_five,
            self.uncle_six,
            self.uncle_seven,
            self.uncle_eight
        )

        for parent in cousin_four_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_four_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_four_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_four_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_four_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_four_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_four_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_four, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_father_two_side(self) -> None:
        # Grandfather 2 (Parent of Father 2, Uncle 3, and Uncle 4, Step Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8, Step Grandparent of Child 1, Child 2, Cousin 9, 10, 11, 12)
        # Grandmother 2 (Parent of Father 2, Uncle 3, and Uncle 4, Step Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Step Child 1, Cousin 5, 6, 7, and 8, Step Grandparent of Child 1, Child 2, Cousin 9, 10, 11, 12)
        grandparents_two_children = (
            self.father_two,
            self.uncle_three,
            self.uncle_four
        )

        grandparents_two_step_children = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        grandparents_two_grandchildren = (
            self.step_child_one,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight
        )

        grandparents_two_step_grandchildren = (
            self.child_one,
            self.child_two,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        # Grandfather
        for child in grandparents_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_two, child)

        for step_child in grandparents_two_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_two, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_two_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_two, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_father_of(self.grandfather_two, grandchild)

        for step_grandchild in grandparents_two_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_two, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Grandmother
        for child in grandparents_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_two, child)

        for step_child in grandparents_two_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_two, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_two_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_two, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(self.grandmother_two, grandchild)

        for step_grandchild in grandparents_two_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_two, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Uncle 3 (Child of Grandfather 2 and Grandmother 2, Step Child of Grandfather 3 and Grandmother 3, Sibling of Father 2 and Uncle 4, Step Sibling of Mother 1, Uncle 5, and Uncle 6, Parent of Cousin 5 and Cousin 6, Uncle of Step Child 1, Cousin 7, and Cousin 8, Step Uncle of Child 1, Child 2, Cousin 9, 10, 11, and 12)
        uncle_three_parents = (
            self.grandfather_two,
            self.grandmother_two
        )

        uncle_three_step_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        uncle_three_siblings = (
            self.father_two,
            self.uncle_four
        )

        uncle_three_step_siblings = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        uncle_three_children = (
            self.cousin_five,
            self.cousin_six
        )

        uncle_three_nephews = (
            self.step_child_one,
            self.cousin_seven,
            self.cousin_eight
        )

        uncle_three_step_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        for parent in uncle_three_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_three_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_three_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_three_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_three, child)

        for nephew in uncle_three_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_three_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_three, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 4 (Child of Grandfather 2 and Grandmother 2, Step Child of Grandfather 3 and Grandmother 3, Sibling of Father 2 and Uncle 3, Step Sibling of Mother 1, Uncle 5, and Uncle 6, Parent of Cousin 7 and Cousin 8, Uncle of Step Child 1, Cousin 5, and Cousin 6, Step Uncle of Child 1, Child 2, Cousin 9, 10, 11, and 12)
        uncle_four_parents = (
            self.grandfather_two,
            self.grandmother_two
        )

        uncle_four_step_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        uncle_four_siblings = (
            self.father_two,
            self.uncle_three
        )

        uncle_four_step_siblings = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        uncle_four_children = (
            self.cousin_seven,
            self.cousin_eight
        )

        uncle_four_nephews = (
            self.step_child_one,
            self.cousin_five,
            self.cousin_six
        )

        uncle_four_step_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        for parent in uncle_four_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_four_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_four_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_four_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_four_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_four, child)

        for nephew in uncle_four_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_four_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_four, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Father 2 (Child of Grandfather 2 and Grandmother 2, Step Child of Grandfather 3 and Grandmother 3, Sibling of Uncle 3 and Uncle 4, Step Sibling of Uncle 5 and Uncle 6, Parent of Step Child 1, Step parent of Child 1 and Child 2, Uncle of Cousin 5, 6, 7, and 8, Step Uncle of Cousin 9, 10, 11, and 12)
        father_two_parents = (
            self.grandfather_two,
            self.grandmother_two
        )

        father_two_step_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        father_two_siblings = (
            self.uncle_three,
            self.uncle_four
        )

        father_two_step_siblings = (
            self.uncle_five,
            self.uncle_six
        )

        father_two_children = (
            self.step_child_one,
        )

        father_two_step_children = (
            self.child_one,
            self.child_two
        )

        father_two_nephews = (
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight
        )

        father_two_step_nephews = (
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        for parent in father_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in father_two_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in father_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in father_two_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in father_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.father_two, child)

        for step_child in father_two_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for nephew in father_two_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in father_two_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.father_two, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 5 (Child of Uncle 3, Sibling of Cousin 6, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 7, 8, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 4 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        cousin_five_parents = (
            self.uncle_three,
        )

        cousin_five_siblings = (
            self.cousin_six,
        )

        cousin_five_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        cousin_five_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_five_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_five_uncles_and_aunts = (
            self.uncle_four,
            self.father_two
        )

        cousin_five_step_uncles_and_aunts = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        for parent in cousin_five_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_five_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_five_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_five_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_five_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_five_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_five_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_five, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 6 (Child of Uncle 3, Sibling of Cousin 5, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 7, 8, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 4 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        cousin_six_parents = (
            self.uncle_three,
        )

        cousin_six_siblings = (
            self.cousin_five,
        )

        cousin_six_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        cousin_six_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_six_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_six_uncles_and_aunts = (
            self.uncle_four,
            self.father_two
        )

        cousin_six_step_uncles_and_aunts = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        for parent in cousin_six_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_six_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_six_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_six_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_six_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_six_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_six_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_six, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 7 (Child of Uncle 4, Sibling of Cousin 8, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 5, 6, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 3 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        cousin_seven_parents = (
            self.uncle_four,
        )

        cousin_seven_siblings = (
            self.cousin_eight,
        )

        cousin_seven_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_five,
            self.cousin_six,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        cousin_seven_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_seven_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_seven_uncles_and_aunts = (
            self.uncle_three,
            self.father_two
        )

        cousin_seven_step_uncles_and_aunts = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        for parent in cousin_seven_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_seven_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_seven_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_seven_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_seven_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_seven_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_seven_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seven, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 8 (Child of Uncle 4, Sibling of Cousin 7, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 5, 6, 9, 10, 11, and 12, Grandchild of Grandfather 2 and Grandmother 2, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Uncle 3 and Father 2, Step Nephew of Uncle 5 and Uncle 6)
        cousin_eight_parents = (
            self.uncle_four,
        )

        cousin_eight_siblings = (
            self.cousin_seven,
        )

        cousin_eight_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_five,
            self.cousin_six,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        cousin_eight_grandparents = (
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_eight_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_eight_uncles_and_aunts = (
            self.uncle_three,
            self.father_two
        )

        cousin_eight_step_uncles_and_aunts = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        for parent in cousin_eight_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_eight_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_eight_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_eight_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_eight_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_eight_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_eight_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eight, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_mother_one_side(self) -> None:
        # Grandfather 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Step Parent of Aunt 1, Aunt 2, Father 1, Father 2, Uncle 1, 2, 3, and 4, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12, Step Grandparent of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        # Grandmother 3 (Parent of Mother 1, Uncle 5, and Uncle 6, Step Parent of Aunt 1, Aunt 2, Father 1, Father 2, Uncle 1, 2, 3, and 4, Grandparent of Child 1, Child 2, Step Child 1, and Cousin 9, 10, 11, and 12, Step Grandparent of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        grandparents_three_children = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        grandparents_three_step_children = (
            self.aunt_one,
            self.aunt_two,
            self.father_one,
            self.father_two,
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four
        )

        grandparents_three_grandchildren = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        grandparents_three_step_grandchildren = (
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        # Grandfather
        for child in grandparents_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_three, child)

        for step_child in grandparents_three_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_three, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_three_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_three, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(self.grandfather_three, grandchild)

        for step_grandchild in grandparents_three_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_three, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Grandmother
        for child in grandparents_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_three, child)

        for step_child in grandparents_three_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_three, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_three_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_three, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(self.grandmother_three, grandchild)

        for step_grandchild in grandparents_three_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_three, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Uncle 5 (Child of Grandfather 3 and Grandmother 3, Step Child of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Sibling of Mother 1 and Uncle 6, Step Sibling of Father 1, Father 2, Aunt 1, Aunt 2, Uncle 1, 2, 3, and 4, Parent of Cousin 11 and Cousin 12, Uncle of Child 1, Child 2, Step Child 1, Cousin 9, and Cousin 10, Step Uncle of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        uncle_five_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        uncle_five_step_parents = (
            self.grandfather_two,
            self.grandfather_one,
            self.grandfather_five,
            self.grandmother_two,
            self.grandmother_one,
            self.grandmother_five
        )

        uncle_five_siblings = (
            self.mother_one,
            self.uncle_six
        )

        uncle_five_step_siblings = (
            self.father_one,
            self.father_two,
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four,
            self.aunt_one,
            self.aunt_two
        )

        uncle_five_children = (
            self.cousin_eleven,
            self.cousin_twelve
        )

        uncle_five_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_nine,
            self.cousin_ten
        )

        uncle_five_step_nephews = (
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_seventeen,
            self.cousin_eighteen,
            self.step_child_three
        )

        for parent in uncle_five_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_five_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_five_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_five_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_five_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_five, child)

        for nephew in uncle_five_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_five_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_five, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 6 (Child of Grandfather 3 and Grandmother 3, Step Child of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Sibling of Mother 1 and Uncle 5, Step Sibling of Father 1, Father 2, Aunt 2, Uncle 1, 2, 3, and 4, Parent of Cousin 9 and Cousin 10, Uncle of Child 1, Child 2, Step Child 1, Cousin 11, and Cousin 12, Step Uncle of Step Child 2, Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        uncle_six_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        uncle_six_step_parents = (
            self.grandfather_two,
            self.grandfather_one,
            self.grandfather_five,
            self.grandmother_two,
            self.grandmother_one,
            self.grandmother_five
        )

        uncle_six_siblings = (
            self.mother_one,
            self.uncle_five
        )

        uncle_six_step_siblings = (
            self.father_one,
            self.father_two,
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four,
            self.aunt_two
        )

        uncle_six_children = (
            self.cousin_nine,
            self.cousin_ten
        )

        uncle_six_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_eleven,
            self.cousin_twelve
        )

        uncle_six_step_nephews = (
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_seventeen,
            self.cousin_eighteen,
            self.step_child_three
        )

        for parent in uncle_six_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_six_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_six_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_six_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_six_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_six, child)

        for nephew in uncle_six_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_six_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_six, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Mother 1 (Child of Grandfather 3 and Grandmother 3, Step Child of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, Grandmother 5, Sibling of Uncle 5 and Uncle 6, Step Sibling of Aunt 1, Aunt 2, Uncle 1, 2, 3, and 4, Parent of Child 1, Child 2, and Step Child 1, Step Parent of Step Child 2, Aunt of Cousin 9, 10, 11, and 12, Step Aunt of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 17, and 18)
        mother_one_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        mother_one_step_parents = (
            self.grandfather_two,
            self.grandmother_two,
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_five,
            self.grandmother_five
        )

        mother_one_siblings = (
            self.uncle_five,
            self.uncle_six
        )

        mother_one_step_siblings = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four,
            self.aunt_one,
            self.aunt_two
        )

        mother_one_children = (
            self.child_one,
            self.child_two,
            self.step_child_one
        )

        mother_one_step_children = (
            self.step_child_two,
            self.step_child_three
        )

        mother_one_grandchildren = (
            self.grand_child_one,
            self.grand_child_two
        )

        mother_one_nephews = (
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        mother_one_step_nephews = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        for parent in mother_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in mother_one_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in mother_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in mother_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in mother_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.mother_one, child)

        for step_child in mother_one_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in mother_one_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_fathers_mother_of(self.mother_one, grandchild)

        for nephew in mother_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in mother_one_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.mother_one, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 9 (Child of Aunt 1 and Uncle 6, Sibling of Cousin 10, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 17, and 18, Grandchild of Grandfather 3, Grandfather 5, Grandmother 3, and Grandmother 5, Step Grandchild of Grandfather 2, Grandfather 1, Grandmother 2, and Grandmother 1, Nephew of Aunt 2, Uncle 5, and Mother 1, Step Nephew of Father 1, Father 2, Uncle 1, 2, 3, and 4)
        cousin_nine_parents = (
            self.aunt_one,
            self.uncle_six,
        )

        cousin_nine_siblings = (
            self.cousin_ten,
        )

        cousin_nine_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        cousin_nine_grandparents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_five,
            self.grandmother_five
        )

        cousin_nine_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_two,
            self.grandmother_two
        )

        cousin_nine_uncles_and_aunts = (
            self.aunt_two,
            self.uncle_five,
            self.mother_one
        )

        cousin_nine_step_uncles_and_aunts = (
            self.father_one,
            self.father_two,
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four
        )

        for parent in cousin_nine_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_nine_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_nine_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_nine_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_nine_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_nine_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_nine_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nine, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 10 (Child of Aunt 1 and Uncle 6, Sibling of Cousin 9, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 17, and 18, Grandchild of Grandfather 3, Grandfather 5, Grandmother 3, and Grandmother 5, Step Grandchild of Grandfather 2, Grandfather 1, Grandmother 2, and Grandmother 1, Nephew of Aunt 2, Uncle 5, and Mother 1, Step Nephew of Father 1, Father 2, Uncle 1, 2, 3, and 4)
        cousin_ten_parents = (
            self.aunt_one,
            self.uncle_six,
        )

        cousin_ten_siblings = (
            self.cousin_nine,
        )

        cousin_ten_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        cousin_ten_grandparents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_five,
            self.grandmother_five
        )

        cousin_ten_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_two,
            self.grandmother_two,
        )

        cousin_ten_uncles_and_aunts = (
            self.aunt_two,
            self.uncle_five,
            self.mother_one
        )

        cousin_ten_step_uncles_and_aunts = (
            self.father_one,
            self.father_two,
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four
        )

        for parent in cousin_ten_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_ten_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_ten_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_ten_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_ten_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_ten_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_ten_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_ten, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 11 (Child of Uncle 5, Sibling of Cousin 12, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, and 18, Grandchild of Grandfather 3 and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Nephew of Uncle 6, and Mother 1, Step Nephew of Aunt 1, Aunt 2, Father 1, Father 2, Uncle 1, 2, 3, and 4)
        cousin_eleven_parents = (
            self.uncle_five,
        )

        cousin_eleven_siblings = (
            self.cousin_twelve,
        )

        cousin_eleven_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        cousin_eleven_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_eleven_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_two,
            self.grandmother_two,
            self.grandfather_five,
            self.grandmother_five
        )

        cousin_eleven_uncles_and_aunts = (
            self.uncle_six,
            self.mother_one
        )

        cousin_eleven_step_uncles_and_aunts = (
            self.aunt_one,
            self.aunt_two,
            self.father_one,
            self.father_two,
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four
        )

        for parent in cousin_eleven_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_eleven_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_eleven_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_eleven_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_eleven_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_eleven_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_eleven_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eleven, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 12 (Child of Uncle 5, Sibling of Cousin 11, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, and 18, Grandchild of Grandfather 3 and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 1, Grandfather 5, Grandmother 2, Grandmother 1, and Grandmother 5, Nephew of Uncle 6 and Mother 1, Step Nephew of Aunt 1, Aunt 2, Father 1, Father 2, Uncle 1, 2, 3, and 4)
        cousin_twelve_parents = (
            self.uncle_five,
        )

        cousin_twelve_siblings = (
            self.cousin_eleven,
        )

        cousin_twelve_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.step_child_three,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        cousin_twelve_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_twelve_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_two,
            self.grandmother_two,
            self.grandfather_five,
            self.grandmother_five
        )

        cousin_twelve_uncles_and_aunts = (
            self.uncle_six,
            self.mother_one
        )

        cousin_twelve_step_uncles_and_aunts = (
            self.aunt_one,
            self.aunt_two,
            self.father_one,
            self.father_two,
            self.uncle_one,
            self.uncle_two,
            self.uncle_three,
            self.uncle_four
        )

        for parent in cousin_twelve_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_twelve_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_twelve_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_twelve_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_twelve_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_twelve_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_twelve_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twelve, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_mother_two_side(self) -> None:
        # Grandfather 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16, Step Grandparent of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        # Grandmother 4 (Parent of Mother 2, Uncle 7, and Uncle 8, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Step Child 2, Cousin 13, 14, 15, and 16, Step Grandparent of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        grandparents_four_children = (
            self.mother_two,
            self.uncle_seven,
            self.uncle_eight
        )

        grandparents_four_step_children = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        grandparents_four_grandchildren = (
            self.step_child_two,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        grandparents_four_step_grandchildren = (
            self.child_one,
            self.child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        # Grandfather
        for child in grandparents_four_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_four, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_four, child)

        for step_child in grandparents_four_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_four, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_four_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_four, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_father_of(self.grandfather_four, grandchild)

        for step_grandchild in grandparents_four_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_four, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Grandmother
        for child in grandparents_four_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_four, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_four, child)

        for step_child in grandparents_four_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_four, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_four_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_four, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(self.grandmother_four, grandchild)

        for step_grandchild in grandparents_four_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_four, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Uncle 7 (Child of Grandfather 4 and Grandmother 4, Step Child of Grandfather 1 and Grandmother 1, Sibling of Mother 2 and Uncle 8, Step Sibling of Father 1, Uncle 1, and Uncle 2, Parent of Cousin 13 and Cousin 14, Uncle of Step Child 2, Cousin 15, and Cousin 16, Step Uncle of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        uncle_seven_parents = (
            self.grandfather_four,
            self.grandmother_four
        )

        uncle_seven_step_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        uncle_seven_siblings = (
            self.mother_two,
            self.uncle_eight
        )

        uncle_seven_step_siblings = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        uncle_seven_children = (
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        uncle_seven_nephews = (
            self.step_child_two,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        uncle_seven_step_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        for parent in uncle_seven_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_seven_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_seven_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_seven_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_seven_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_seven, child)

        for nephew in uncle_seven_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_seven_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_seven, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Uncle 8 (Child of Grandfather 4 and Grandmother 4, Step Child of Grandfather 1 and Grandmother 1, Sibling of Mother 2 and Uncle 7, Step Sibling of Father 1, Uncle 1, and Uncle 2, Parent of Cousin 15 and Cousin 16, Uncle of Step Child 2, Cousin 13, and Cousin 14, Step Uncle of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        uncle_eight_parents = (
            self.grandfather_four,
            self.grandmother_four
        )

        uncle_eight_step_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        uncle_eight_siblings = (
            self.mother_two,
            self.uncle_seven
        )

        uncle_eight_step_siblings = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        uncle_eight_children = (
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        uncle_eight_nephews = (
            self.step_child_two,
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        uncle_eight_step_nephews = (
            self.child_one,
            self.child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        for parent in uncle_eight_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in uncle_eight_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in uncle_eight_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in uncle_eight_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in uncle_eight_children:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.uncle_eight, child)

        for nephew in uncle_eight_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in uncle_eight_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.uncle_eight, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Mother 2 (Child of Grandfather 4 and Grandmother 4, Step Child of Grandfather 1 and Grandmother 1, Sibling of Uncle 7 and Uncle 8, Step Sibling of Uncle 1, and Uncle 2, Parent of Step Child 2, Step Parent of Child 1 and Child 2, Aunt of Cousin 13, 14, 15, and 16, Step Aunt of Child 1, Child 2, Cousin 1, 2, 3, and 4)
        mother_two_parents = (
            self.grandfather_four,
            self.grandmother_four
        )

        mother_two_step_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        mother_two_siblings = (
            self.uncle_seven,
            self.uncle_eight
        )

        mother_two_step_siblings = (
            self.uncle_one,
            self.uncle_two
        )

        mother_two_children = (
            self.step_child_two,
        )

        mother_two_step_children = (
            self.child_one,
            self.child_two
        )

        mother_two_nephews = (
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        mother_two_step_nephews = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        for parent in mother_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in mother_two_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in mother_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in mother_two_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in mother_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.mother_two, child)

        for step_child in mother_two_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for nephew in mother_two_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in mother_two_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.mother_two, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 13 (Child of Uncle 7, Sibling of Cousin 14, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 8 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        cousin_thirteen_parents = (
            self.uncle_seven,
        )

        cousin_thirteen_siblings = (
            self.cousin_fourteen,
        )

        cousin_thirteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_thirteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_thirteen_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_thirteen_uncles_and_aunts = (
            self.uncle_eight,
            self.mother_two
        )

        cousin_thirteen_step_uncles_and_aunts = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        for parent in cousin_thirteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_thirteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_thirteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_thirteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_thirteen_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_thirteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_thirteen_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_thirteen, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 14 (Child of Uncle 7, Sibling of Cousin 13, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 15, and 16, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 8 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        cousin_fourteen_parents = (
            self.uncle_seven,
        )

        cousin_fourteen_siblings = (
            self.cousin_thirteen,
        )

        cousin_fourteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_fifteen,
            self.cousin_sixteen
        )

        cousin_fourteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_fourteen_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_fourteen_uncles_and_aunts = (
            self.uncle_eight,
            self.mother_two
        )

        cousin_fourteen_step_uncles_and_aunts = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        for parent in cousin_fourteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_fourteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_fourteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_fourteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_fourteen_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_fourteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_fourteen_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fourteen, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 15 (Child of Uncle 8, Sibling of Cousin 16, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 7 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        cousin_fifteen_parents = (
            self.uncle_eight,
        )

        cousin_fifteen_siblings = (
            self.cousin_sixteen,
        )

        cousin_fifteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        cousin_fifteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_fifteen_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_fifteen_uncles_and_aunts = (
            self.uncle_seven,
            self.mother_two
        )

        cousin_fifteen_step_uncles_and_aunts = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        for parent in cousin_fifteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_fifteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_fifteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_fifteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_fifteen_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_fifteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_fifteen_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_fifteen, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 16 (Child of Uncle 8, Sibling of Cousin 15, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 1, 2, 3, 4, 13, and 14, Grandchild of Grandfather 4 and Grandmother 4, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Uncle 7 and Mother 2, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        cousin_sixteen_parents = (
            self.uncle_eight,
        )

        cousin_sixteen_siblings = (
            self.cousin_fifteen,
        )

        cousin_sixteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_thirteen,
            self.cousin_fourteen
        )

        cousin_sixteen_grandparents = (
            self.grandfather_four,
            self.grandmother_four
        )

        cousin_sixteen_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_sixteen_uncles_and_aunts = (
            self.uncle_seven,
            self.mother_two
        )

        cousin_sixteen_step_uncles_and_aunts = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        for parent in cousin_sixteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_sixteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_sixteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_sixteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_sixteen_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_sixteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_sixteen_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_sixteen, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_aunt_one_side(self) -> None:
        # Grandfather 5 (Parent of Aunt 1 and Aunt 2, Step Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Cousin 9, 10, 17, and 18, Step Grandparent of Child 1, Child 2, Step Child 1, Cousin 11, 12)
        # Grandmother 5 (Parent of Aunt 1 and Aunt 2, Step Parent of Mother 1, Uncle 5, and Uncle 6, Grandparent of Cousin 9, 10, 17, and 18, Step Grandparent of Child 1, Child 2, Step Child 1, Cousin 11, 12)
        grandparents_five_children = (
            self.aunt_one,
            self.aunt_two
        )

        grandparents_five_step_children = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        grandparents_five_grandchildren = (
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        grandparents_five_step_grandchildren = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.cousin_eleven,
            self.cousin_twelve
        )

        # Grandfather
        for child in grandparents_five_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_five, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_five, child)

        for step_child in grandparents_five_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_five, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_five_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_five, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_father_of(self.grandfather_five, grandchild)

        for step_grandchild in grandparents_five_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_five, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Grandmother
        for child in grandparents_five_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_five, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_five, child)

        for step_child in grandparents_five_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_five, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_five_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_five, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(self.grandmother_five, grandchild)

        for step_grandchild in grandparents_five_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_five, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Aunt 2 (Child of Grandfather 5 and Grandmother 5, Step Child of Grandfather 3 and Grandmother 3, Sibling of Aunt 1, Step Sibling of Mother 1, Uncle 5, and Uncle 6, Parent of Cousin 17 and Cousin 18, Aunt of Cousin 9 and Cousin 10, Step Aunt of Child 1, Child 2, Step Child 1, Step Child 2, Cousin 11, and Cousin 12)
        aunt_two_parents = (
            self.grandfather_five,
            self.grandmother_five
        )

        aunt_two_step_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        aunt_two_siblings = (
            self.aunt_one,
        )

        aunt_two_step_siblings = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        aunt_two_children = (
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        aunt_two_nephews = (
            self.cousin_nine,
            self.cousin_ten
        )

        aunt_two_step_nephews = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.cousin_eleven,
            self.cousin_twelve
        )

        for parent in aunt_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in aunt_two_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_two, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in aunt_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in aunt_two_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_two, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in aunt_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.aunt_two, child)

        for nephew in aunt_two_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_two, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in aunt_two_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_two, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Aunt 1 (Child of Grandfather 5 and Grandmother 5, Step Child of Grandfather 3, and Grandmother 3, Sibling of Aunt 2, Step Sibling of Mother 1 and Uncle 5, Parent of Cousin 9 and Cousin 10, Aunt of Cousin 17 and Cousin 18, Step Aunt of Child 1, Child 2, Step Child 1, Step Child 2, Cousin 11, and Cousin 12)
        aunt_one_parents = (
            self.grandfather_five,
            self.grandmother_five
        )

        aunt_one_step_parents = (
            self.grandfather_three,
            self.grandmother_three
        )

        aunt_one_siblings = (
            self.aunt_two,
        )

        aunt_one_step_siblings = (
            self.mother_one,
            self.uncle_five
        )

        aunt_one_children = (
            self.cousin_nine,
            self.cousin_ten
        )

        aunt_one_nephews = (
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        aunt_one_step_nephews = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.cousin_eleven,
            self.cousin_twelve
        )

        for parent in aunt_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in aunt_one_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_one, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in aunt_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in aunt_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in aunt_one_children:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_one, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.aunt_one, child)

        for nephew in aunt_one_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_one, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in aunt_one_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_one, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 17 (Child of Aunt 2, Sibling of Cousin 18, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 9, 10, 11, and 12, Grandchild of Grandfather 5 and Grandmother 5, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Aunt 1, Step Nephew of Mother 1, Uncle 5, and Uncle 6)
        cousin_seventeen_parents = (
            self.aunt_two,
        )

        cousin_seventeen_siblings = (
            self.cousin_eighteen,
        )

        cousin_seventeen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        cousin_seventeen_grandparents = (
            self.grandfather_five,
            self.grandmother_five
        )

        cousin_seventeen_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_seventeen_uncles_and_aunts = (
            self.aunt_one,
        )

        cousin_seventeen_step_uncles_and_aunts = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        for parent in cousin_seventeen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seventeen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_seventeen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seventeen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_seventeen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seventeen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_seventeen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seventeen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_seventeen_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seventeen, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_seventeen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seventeen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_seventeen_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_seventeen, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 18 (Child of Aunt 2, Sibling of Cousin 17, Cousin of Child 1, Child 2, Step Child 1, Step Child 2, and Cousin 9, 10, 11, and 12, Grandchild of Grandfather 5 and Grandmother 5, Step Grandchild of Grandfather 3 and Grandmother 3, Nephew of Aunt 1, Step Nephew of Mother 1, Uncle 5, and Uncle 6)
        cousin_eighteen_parents = (
            self.aunt_two,
        )

        cousin_eighteen_siblings = (
            self.cousin_seventeen,
        )

        cousin_eighteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_one,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve
        )

        cousin_eighteen_grandparents = (
            self.grandfather_five,
            self.grandmother_five
        )

        cousin_eighteen_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three
        )

        cousin_eighteen_uncles_and_aunts = (
            self.aunt_one,
        )

        cousin_eighteen_step_uncles_and_aunts = (
            self.mother_one,
            self.uncle_five,
            self.uncle_six
        )

        for parent in cousin_eighteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eighteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_eighteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eighteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_eighteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eighteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_eighteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eighteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_eighteen_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eighteen, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_eighteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eighteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_eighteen_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_eighteen, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_aunt_three_side(self) -> None:
        # Grandfather 6 (Parent of Aunt 3 and Aunt 4, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Cousin 3, 4, 19, and 20, Step Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2)
        # Grandmother 6 (Parent of Aunt 3 and Aunt 4, Step Parent of Father 1, Uncle 1, and Uncle 2, Grandparent of Cousin 3, 4, 19, and 20, Step Grandparent of Child 1, Child 2, Step Child 2, Cousin 1, 2)
        grandparents_six_children = (
            self.aunt_three,
            self.aunt_four
        )

        grandparents_six_step_children = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        grandparents_six_grandchildren = (
            self.cousin_three,
            self.cousin_four,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        grandparents_six_step_grandchildren = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two
        )

        # Grandfather
        for child in grandparents_six_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_six, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.grandfather_six, child)

        for step_child in grandparents_six_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_six, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_six_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_six, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_father_of(self.grandfather_six, grandchild)

        for step_grandchild in grandparents_six_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandfather_six, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Grandmother
        for child in grandparents_six_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_six, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.grandmother_six, child)

        for step_child in grandparents_six_step_children:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_six, step_child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        for grandchild in grandparents_six_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_six, grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(self.grandmother_six, grandchild)

        for step_grandchild in grandparents_six_step_grandchildren:
            CommonRelationshipUtils.add_relationship_bit(self.grandmother_five, step_grandchild, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        # Aunt 3 (Child of Grandfather 6 and Grandmother 6, Step Child of Grandfather 1, and Grandmother 1, Sibling of Aunt 4, Step Sibling of Father 1 and Uncle 1, Parent of Cousin 3 and Cousin 4, Aunt of Cousin 19 and Cousin 20, Step Aunt of Child 1, Child 2, Step Child 2, Cousin 1, and Cousin 2)
        aunt_three_parents = (
            self.grandfather_six,
            self.grandmother_six
        )

        aunt_three_step_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        aunt_three_siblings = (
            self.aunt_four,
        )

        aunt_three_step_siblings = (
            self.father_one,
            self.uncle_one
        )

        aunt_three_children = (
            self.cousin_three,
            self.cousin_four
        )

        aunt_three_nephews = (
            self.cousin_nineteen,
            self.cousin_twenty
        )

        aunt_three_step_nephews = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two
        )

        for parent in aunt_three_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_three, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in aunt_three_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_three, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in aunt_three_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_three, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in aunt_three_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_three, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in aunt_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.aunt_three, child)

        for nephew in aunt_three_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_three, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in aunt_three_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_three, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Aunt 4 (Child of Grandfather 6 and Grandmother 6, Step Child of Grandfather 1 and Grandmother 1, Sibling of Aunt 3, Step Sibling of Father 1, Uncle 1, and Uncle 2, Parent of Cousin 19 and Cousin 20, Aunt of Cousin 3 and Cousin 4, Step Aunt of Child 1, Child 2, Step Child 2, Cousin 1, and Cousin 2)
        aunt_four_parents = (
            self.grandfather_six,
            self.grandmother_six
        )

        aunt_four_step_parents = (
            self.grandfather_one,
            self.grandmother_one
        )

        aunt_four_siblings = (
            self.aunt_three,
        )

        aunt_four_step_siblings = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        aunt_four_children = (
            self.cousin_nineteen,
            self.cousin_twenty
        )

        aunt_four_nephews = (
            self.cousin_three,
            self.cousin_four
        )

        aunt_four_step_nephews = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two
        )

        for parent in aunt_four_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_four, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in aunt_four_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_four, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in aunt_four_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_four, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in aunt_four_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_four, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for child in aunt_four_children:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_four, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.aunt_four, child)

        for nephew in aunt_four_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_four, nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for step_nephew in aunt_four_step_nephews:
            CommonRelationshipUtils.add_relationship_bit(self.aunt_four, step_nephew, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Cousin 19 (Child of Aunt 4, Sibling of Cousin 20, Cousin of Child 1, Child 2, Step Child 2, and Cousin 1, 2, 3, and 4, Grandchild of Grandfather 6 and Grandmother 6, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Aunt 3, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        cousin_nineteen_parents = (
            self.aunt_four,
        )

        cousin_nineteen_siblings = (
            self.cousin_twenty,
        )

        cousin_nineteen_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four
        )

        cousin_nineteen_grandparents = (
            self.grandfather_six,
            self.grandmother_six
        )

        cousin_nineteen_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_nineteen_uncles_and_aunts = (
            self.aunt_three,
        )

        cousin_nineteen_step_uncles_and_aunts = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        for parent in cousin_nineteen_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nineteen, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_nineteen_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nineteen, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_nineteen_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nineteen, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_nineteen_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nineteen, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_nineteen_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nineteen, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_nineteen_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nineteen, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_nineteen_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_nineteen, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Cousin 20 (Child of Aunt 4, Sibling of Cousin 19, Cousin of Child 1, Child 2, Step Child 2, and Cousin 1, 2, 3, and 4, Grandchild of Grandfather 6 and Grandmother 6, Step Grandchild of Grandfather 1 and Grandmother 1, Nephew of Aunt 3, Step Nephew of Father 1, Uncle 1, and Uncle 2)
        cousin_twenty_parents = (
            self.aunt_four,
        )

        cousin_twenty_siblings = (
            self.cousin_nineteen,
        )

        cousin_twenty_cousins = (
            self.child_one,
            self.child_two,
            self.step_child_two,
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
        )

        cousin_twenty_grandparents = (
            self.grandfather_six,
            self.grandmother_six
        )

        cousin_twenty_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one
        )

        cousin_twenty_uncles_and_aunts = (
            self.aunt_three,
        )

        cousin_twenty_step_uncles_and_aunts = (
            self.father_one,
            self.uncle_one,
            self.uncle_two
        )

        for parent in cousin_twenty_parents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twenty, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in cousin_twenty_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twenty, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for cousin in cousin_twenty_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twenty, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in cousin_twenty_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twenty, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in cousin_twenty_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twenty, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in cousin_twenty_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twenty, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in cousin_twenty_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.cousin_twenty, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def _setup_children(self) -> None:
        # Child 1 (Child of Father 1 and Mother 1, Step Child of Father 2 and Mother 2, Sibling of Child 2, Step Child 1, and Step Child 2, Step Sibling of Step Child 3, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 4, Grandfather 5, Grandfather 6, Grandmother 2, Grandmother 4, Grandmother 5, and Grandmother 6, Nephew of Uncle 1, 2, 5, and 6, Step Nephew of Uncle 3, 4, 7, and 8)
        child_one_parents = (
            self.father_one,
            self.mother_one
        )

        child_one_step_parents = (
            self.father_two,
            self.mother_two
        )

        child_one_siblings = (
            self.child_two,
            self.step_child_one,
            self.step_child_two,
        )

        child_one_step_siblings = (
            self.step_child_three,
        )

        child_one_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_seventeen,
            self.cousin_eighteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        child_one_grandparents = (
            self.grandfather_one,
            self.grandfather_three,
            self.grandmother_one,
            self.grandfather_three
        )

        child_one_step_grandparents = (
            self.grandfather_two,
            self.grandmother_two,
            self.grandfather_four,
            self.grandmother_four,
            self.grandfather_five,
            self.grandmother_five,
            self.grandfather_six,
            self.grandmother_six
        )

        child_one_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_five,
            self.uncle_six
        )

        child_one_step_uncles_and_aunts = (
            self.uncle_three,
            self.uncle_four,
            self.uncle_seven,
            self.uncle_eight
        )

        child_one_nephew_and_nieces = (
            self.grand_child_one,
            self.grand_child_two
        )

        for parent in child_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in child_one_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in child_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in child_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for cousin in child_one_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in child_one_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in child_one_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in child_one_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in child_one_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for nephew_or_niece in child_one_nephew_and_nieces:
            CommonRelationshipUtils.add_relationship_bit(self.child_one, nephew_or_niece, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Child 2 (Child of Father 1 and Mother 1, Step Child of Father 2 and Mother 2, Sibling of Child 1, Step Child 1, and Step Child 2, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20, Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Step Grandchild of Grandfather 2, Grandfather 4, Grandfather 5, Grandfather 6, Grandmother 2, Grandmother 4, Grandmother 5, and Grandmother 6, Nephew of Uncle 1, 2, 5, and 6, Step Nephew of Uncle 3, 4, 7, and 8)
        child_two_parents = (
            self.father_one,
            self.mother_one
        )

        child_two_step_parents = (
            self.father_two,
            self.mother_two
        )

        child_two_siblings = (
            self.child_one,
            self.step_child_one,
            self.step_child_two,
        )

        child_two_children = (
            self.grand_child_one,
            self.grand_child_two
        )

        child_two_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_seventeen,
            self.cousin_eighteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        child_two_grandparents = (
            self.grandfather_one,
            self.grandfather_three,
            self.grandmother_one,
            self.grandfather_three
        )

        child_two_step_grandparents = (
            self.grandfather_two,
            self.grandmother_two,
            self.grandfather_four,
            self.grandmother_four,
            self.grandfather_five,
            self.grandmother_five,
            self.grandfather_six,
            self.grandmother_six
        )

        child_two_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_five,
            self.uncle_six
        )

        child_two_step_uncles_and_aunts = (
            self.uncle_three,
            self.uncle_four,
            self.uncle_seven,
            self.uncle_eight
        )

        for parent in child_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in child_two_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in child_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for child in child_two_children:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(self.child_two, child)

        for cousin in child_two_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in child_two_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in child_two_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in child_two_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in child_two_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.child_two, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Grandchild 1 (Child of Child 2 and Step Child 3, Sibling of Grandchild 2, Grandchild of Mother 1 and Father 1, Step Grandchild of Father 2 and Mother 2, Nephew of Child 1, Step Nephew of Step Child 1 and Step Child 2)
        grand_child_one_parents = (
            self.child_two,
            self.step_child_three
        )

        grand_child_one_siblings = (
            self.grand_child_two,
        )

        grand_child_one_grandparents = (
            self.mother_one,
            self.father_one
        )

        grand_child_one_step_grandparents = (
            self.father_two,
            self.mother_two
        )

        grand_child_one_uncles_and_aunts = (
            self.child_one,
        )

        grand_child_one_step_uncles_and_aunts = (
            self.step_child_one,
            self.step_child_two
        )

        for parent in grand_child_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in grand_child_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for grandparent in grand_child_one_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_one, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in grand_child_one_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_one, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in grand_child_one_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in grand_child_one_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_one, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Grandchild 2 (Child of Child 2 and Step Child 3, Sibling of Grandchild 1, Grandchild of Mother 1 and Father 1, Step Grandchild of Father 2 and Mother 2, Nephew of Child 1, Step Nephew of Step Child 1 and Step Child 2)
        grand_child_two_parents = (
            self.child_two,
            self.step_child_three
        )

        grand_child_two_siblings = (
            self.grand_child_one,
        )

        grand_child_two_grandparents = (
            self.mother_one,
            self.father_one
        )

        grand_child_two_step_grandparents = (
            self.father_two,
            self.mother_two
        )

        grand_child_two_uncles_and_aunts = (
            self.child_one,
        )

        grand_child_two_step_uncles_and_aunts = (
            self.step_child_one,
            self.step_child_two
        )

        for parent in grand_child_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in grand_child_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for grandparent in grand_child_two_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_two, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in grand_child_two_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_two, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in grand_child_two_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in grand_child_two_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.grand_child_two, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        # Step Child 1 (Child of Mother 1 and Father 2, Step Child of Father 1, Sibling of Child 1 and Child 2, Step Sibling of Step Child 2 and Step Child 3, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, and 18, Grandchild of Grandfather 2, Grandfather 3, Grandmother 2, and Grandmother 3, Step Grandchild of Grandfather 1, Grandfather 5, Grandmother 1, and Grandmother 5, Nephew of Uncle 3, 4, 5, and 6, Step Nephew of Uncle 1 and Uncle 2, Step Uncle of Grandchild 1 and Grandchild 2)
        step_child_one_parents = (
            self.mother_one,
            self.father_two
        )

        step_child_one_step_parents = (
            self.father_one,
        )

        step_child_one_siblings = (
            self.child_one,
            self.child_two
        )

        step_child_one_step_siblings = (
            self.step_child_two,
            self.step_child_three
        )

        step_child_one_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_seventeen,
            self.cousin_eighteen
        )

        step_child_one_grandparents = (
            self.grandfather_two,
            self.grandmother_two,
            self.grandfather_three,
            self.grandmother_three
        )

        step_child_one_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_five,
            self.grandmother_five
        )

        step_child_one_uncles_and_aunts = (
            self.uncle_three,
            self.uncle_four,
            self.uncle_five,
            self.uncle_six
        )

        step_child_one_step_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two
        )

        step_child_one_step_nephew_and_nieces = (
            self.grand_child_one,
            self.grand_child_two
        )

        for parent in step_child_one_parents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in step_child_one_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in step_child_one_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in step_child_one_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for cousin in step_child_one_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in step_child_one_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in step_child_one_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in step_child_one_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in step_child_one_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_nephew_or_niece in step_child_one_step_nephew_and_nieces:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_one, step_nephew_or_niece, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Step Child 2 (Child of Father 1 and Mother 2, Step Child of Mother 1, Sibling of Child 1 and Child 2, Step Sibling of Step Child 1 and Step Child 3, Cousin of Cousin 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, and 20, Grandchild of Grandfather 1, Grandfather 4, Grandmother 1, and Grandmother 4, Step Grandchild of Grandfather 3, Grandfather 6, Grandmother 3, and Grandmother 6, Nephew of Uncle 1, 2, 7, and 8, Step Nephew of Uncle 5 and Uncle 6, Step Uncle of Grandchild 1 and Grandchild 2)
        step_child_two_parents = (
            self.father_one,
            self.mother_two
        )

        step_child_two_step_parents = (
            self.mother_one,
        )

        step_child_two_siblings = (
            self.child_one,
            self.child_two
        )

        step_child_two_step_siblings = (
            self.step_child_one,
            self.step_child_three
        )

        step_child_two_cousins = (
            self.cousin_one,
            self.cousin_two,
            self.cousin_three,
            self.cousin_four,
            self.cousin_five,
            self.cousin_six,
            self.cousin_seven,
            self.cousin_eight,
            self.cousin_nine,
            self.cousin_ten,
            self.cousin_eleven,
            self.cousin_twelve,
            self.cousin_thirteen,
            self.cousin_fourteen,
            self.cousin_fifteen,
            self.cousin_sixteen,
            self.cousin_nineteen,
            self.cousin_twenty
        )

        step_child_two_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_four,
            self.grandmother_four
        )

        step_child_two_step_grandparents = (
            self.grandfather_three,
            self.grandmother_three,
            self.grandfather_six,
            self.grandmother_six
        )

        step_child_two_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_seven,
            self.uncle_eight
        )

        step_child_two_step_uncles_and_aunts = (
            self.uncle_five,
            self.uncle_six
        )

        step_child_two_step_nephew_and_nieces = (
            self.grand_child_one,
            self.grand_child_two
        )

        for parent in step_child_two_parents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, parent, CommonRelationshipBitId.FAMILY_PARENT)

        for step_parent in step_child_two_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for sibling in step_child_two_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, sibling, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for step_sibling in step_child_two_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for cousin in step_child_two_cousins:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, cousin, CommonRelationshipBitId.FAMILY_COUSIN)

        for grandparent in step_child_two_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_grandparent in step_child_two_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for uncle_or_aunt in step_child_two_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_uncle_or_aunt in step_child_two_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for step_nephew_or_niece in step_child_two_step_nephew_and_nieces:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_two, step_nephew_or_niece, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Step Child 3 (Step Child of Mother 1 and Father 1, Step Sibling Child 1, Step Child 1, and Step Child 2, Step Grandchild of Grandfather 1, Grandfather 3, Grandmother 1, and Grandmother 3, Step Nephew of Uncle 1, 2, 5, and 6)
        step_child_three_step_parents = (
            self.mother_one,
            self.father_one
        )

        step_child_three_step_siblings = (
            self.child_one,
            self.step_child_one,
            self.step_child_two,
        )

        step_child_three_children = (
            self.grand_child_one,
            self.grand_child_two
        )

        step_child_three_step_grandparents = (
            self.grandfather_one,
            self.grandmother_one,
            self.grandfather_three,
            self.grandmother_three
        )

        step_child_three_step_uncles_and_aunts = (
            self.uncle_one,
            self.uncle_two,
            self.uncle_five,
            self.uncle_six
        )

        for step_parent in step_child_three_step_parents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_three, step_parent, CommonRelationshipBitId.FAMILY_PARENT)

        for child in step_child_three_children:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_three, child, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(self.step_child_three, child)

        for step_sibling in step_child_three_step_siblings:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_three, step_sibling, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        for step_grandparent in step_child_three_step_grandparents:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_three, step_grandparent, CommonRelationshipBitId.FAMILY_GRANDPARENT)

        for step_uncle_or_aunt in step_child_three_step_uncles_and_aunts:
            CommonRelationshipUtils.add_relationship_bit(self.step_child_three, step_uncle_or_aunt, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

    def destroy(self) -> None:
        """destroy()

        Destroy the family and delete all Sims.
        """
        CommonSimSpawnUtils.delete_sim(self.grandfather_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.father_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_four, cause='S4CM: testing cleanup')

        # Father 2 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.father_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_five, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_six, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_seven, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_eight, cause='S4CM: testing cleanup')

        # Mother 1 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_five, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_six, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.mother_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_nine, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_ten, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_eleven, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_twelve, cause='S4CM: testing cleanup')

        # Mother 1 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_seven, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.uncle_eight, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.mother_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_thirteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_fourteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_fifteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_sixteen, cause='S4CM: testing cleanup')

        # Aunt 1 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_five, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_five, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.aunt_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.aunt_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_seventeen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_eighteen, cause='S4CM: testing cleanup')

        # Aunt 1 Side:
        CommonSimSpawnUtils.delete_sim(self.grandfather_six, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grandmother_six, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.aunt_three, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.aunt_four, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_nineteen, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.cousin_twenty, cause='S4CM: testing cleanup')

        # Children:
        CommonSimSpawnUtils.delete_sim(self.child_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.child_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grand_child_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.grand_child_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.step_child_one, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.step_child_two, cause='S4CM: testing cleanup')
        CommonSimSpawnUtils.delete_sim(self.step_child_three, cause='S4CM: testing cleanup')

        # Father 1 Side:
        self.grandfather_one: SimInfo = None
        self.grandmother_one: SimInfo = None
        self.uncle_one: SimInfo = None
        self.uncle_two: SimInfo = None
        self.father_one: SimInfo = None
        self.cousin_one: SimInfo = None
        self.cousin_two: SimInfo = None
        self.cousin_three: SimInfo = None
        self.cousin_four: SimInfo = None
        
        # Father 2 Side:
        self.grandfather_two: SimInfo = None
        self.grandmother_two: SimInfo = None
        self.uncle_three: SimInfo = None
        self.uncle_four: SimInfo = None
        self.father_two: SimInfo = None
        self.cousin_five: SimInfo = None
        self.cousin_six: SimInfo = None
        self.cousin_seven: SimInfo = None
        self.cousin_eight: SimInfo = None
        
        # Mother 1 Side:
        self.grandfather_three: SimInfo = None
        self.grandmother_three: SimInfo = None
        self.uncle_five: SimInfo = None
        self.uncle_six: SimInfo = None
        self.mother_one: SimInfo = None
        self.cousin_nine: SimInfo = None
        self.cousin_ten: SimInfo = None
        self.cousin_eleven: SimInfo = None
        self.cousin_twelve: SimInfo = None
        
        # Mother 1 Side:
        self.grandfather_four: SimInfo = None
        self.grandmother_four: SimInfo = None
        self.uncle_seven: SimInfo = None
        self.uncle_eight: SimInfo = None
        self.mother_two: SimInfo = None
        self.cousin_thirteen: SimInfo = None
        self.cousin_fourteen: SimInfo = None
        self.cousin_fifteen: SimInfo = None
        self.cousin_sixteen: SimInfo = None
        
        # Aunt 1 Side:
        self.grandfather_five: SimInfo = None
        self.grandmother_five: SimInfo = None
        self.aunt_two: SimInfo = None
        self.aunt_one: SimInfo = None
        self.cousin_seventeen: SimInfo = None
        self.cousin_eighteen: SimInfo = None

        # Aunt 3 Side:
        self.grandfather_six: SimInfo = None
        self.grandmother_six: SimInfo = None
        self.aunt_three: SimInfo = None
        self.aunt_four: SimInfo = None
        self.cousin_nineteen: SimInfo = None
        self.cousin_twenty: SimInfo = None

        # Children:
        self.child_one: SimInfo = None
        self.child_two: SimInfo = None
        self.grand_child_one: SimInfo = None
        self.grand_child_two: SimInfo = None
        self.step_child_one: SimInfo = None
        self.step_child_two: SimInfo = None
        self.step_child_three: SimInfo = None

        setattr(self, '_destroyed', True)
