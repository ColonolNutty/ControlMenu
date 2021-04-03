"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.genealogy_tracker import genealogy_caching
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4controlmenu.commonlib.utils.common_sim_genealogy_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsMotherToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as a mother of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_set_mother'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_PARENT

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_SON_DAUGHTER

    @property
    def _display_name(self) -> int:
        return S4CMSimControlMenuStringId.MOTHER

    # noinspection PyMissingOrEmptyDocstring
    def has_relation(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        return super().has_relation(sim_info_a, sim_info_b) and CommonSimGenealogyUtils.is_mother_of(sim_info_a, sim_info_b)

    def _update_family_tree(self, parent_sim_info: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as mother of Sim B', parent=parent_sim_info, sim_b=sim_info_b)
            self._remove_old_relation(parent_sim_info)
            # self._add_new_relation(parent_sim_info, sim_info_b)
            self.log.format_with_message('Done setting Sim A as mother of Sim B', parent=parent_sim_info, sim_b=sim_info_b)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as mother.', exception=ex)
            on_completed(False)
        return True

    def _remove_old_relation(self, sim_info: SimInfo) -> bool:
        self.log.format_with_message('Removing parent relations to old family', new_sim=sim_info)
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        # Remove Brothers/Sisters
        brother_sister_sim_info_list = list()
        with genealogy_caching():
            for brother_sister_sim_info in genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found brother/sister. Removing them.', sim=sim_info, brother_sister=brother_sister_sim_info)
                if CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING):
                    continue
                brother_sister_sim_info_list.append(brother_sister_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for brother_sister_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER, instanced_only=False):
            if brother_sister_sim_info in brother_sister_sim_info_list:
                continue
            self.log.format_with_message('Found brother/sister. Removing them.', sim=sim_info, brother_sister=brother_sister_sim_info)
            brother_sister_sim_info_list.append(brother_sister_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
            CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        # Remove Nephews
        niece_and_nephews_sim_info_list = list()
        for brother_sister_sim_info in brother_sister_sim_info_list:
            uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(brother_sister_sim_info)
            with genealogy_caching():
                for niece_nephew_sim_info in uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found niece/nephew. Removing them.', sim=sim_info, niece_nephew=niece_nephew_sim_info)
                    niece_and_nephews_sim_info_list.append(niece_nephew_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, niece_nephew_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.remove_relationship_bit(niece_nephew_sim_info, sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        with genealogy_caching():
            for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                if not CommonSimGenealogyUtils.is_mother_of(sim_info, child_sim_info) and not CommonSimGenealogyUtils.is_father_of(sim_info, child_sim_info):
                    continue
                self.log.format_with_message('Found Child of Sim. Updating them.', sim=sim_info, child=child_sim_info)
                for cousin_sim_info in niece_and_nephews_sim_info_list:
                    self.log.format_with_message('Found Cousin, removing them.', sim=child_sim_info, cousin=cousin_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(child_sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.remove_relationship_bit(cousin_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

                for aunt_or_uncle_sim_info in brother_sister_sim_info_list:
                    self.log.format_with_message('Found Aunt/Uncle, removing them.', sim=child_sim_info, aunt_or_uncle=aunt_or_uncle_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(child_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(aunt_or_uncle_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        if CommonSimGenealogyUtils.has_father(sim_info):
            grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
            self.log.format_with_message('Found grandfather, removing father.', sim=sim_info, father=grandfather_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, grandfather_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(grandfather_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            with genealogy_caching():
                for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found child, removing grandfather.', sim=child_sim_info, grandfather=grandfather_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(child_sim_info, grandfather_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(grandfather_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    if CommonSimGenealogyUtils.is_fathers_father_of(grandfather_sim_info, child_sim_info):
                        CommonSimGenealogyUtils.remove_fathers_father_relation(child_sim_info)
                    if CommonSimGenealogyUtils.is_mothers_father_of(grandfather_sim_info, child_sim_info):
                        CommonSimGenealogyUtils.remove_mothers_father_relation(child_sim_info)
            CommonSimGenealogyUtils.remove_father_relation(sim_info)

        if CommonSimGenealogyUtils.has_mother(sim_info):
            grandmother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
            self.log.format_with_message('Found mother, removing mother.', sim=sim_info, mother=grandmother_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, grandmother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(grandmother_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            with genealogy_caching():
                for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found child, removing grandmother.', sim=child_sim_info, grandmother=grandmother_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(child_sim_info, grandmother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.remove_relationship_bit(grandmother_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    if CommonSimGenealogyUtils.is_fathers_mother_of(grandmother_sim_info, child_sim_info):
                        CommonSimGenealogyUtils.remove_fathers_mother_relation(child_sim_info)
                    if CommonSimGenealogyUtils.is_mothers_mother_of(grandmother_sim_info, child_sim_info):
                        CommonSimGenealogyUtils.remove_mothers_mother_relation(child_sim_info)
            CommonSimGenealogyUtils.remove_mother_relation(sim_info)

        self.log.debug('Done removing old mother')
        return True

    def _add_new_relation(self, parent_sim_info: SimInfo, new_child_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding new mother to Sim', sim=new_child_sim_info, parent_sim=parent_sim_info)
        # Add new Mother
        CommonSimGenealogyUtils.set_as_mother_of(parent_sim_info, new_child_sim_info)

        # Add new Uncles/Aunts
        uncle_aunt_sim_info_list = list()
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(parent_sim_info)
        with genealogy_caching():
            for uncle_aunt_sim_info in genealogy_tracker.get_siblings_sim_infos_gen():
                uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_child_sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(uncle_aunt_sim_info, new_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for uncle_aunt_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(parent_sim_info, (CommonRelationshipBitId.FAMILY_BROTHER_SISTER, CommonRelationshipBitId.FAMILY_STEP_SIBLING), instanced_only=False):
            if uncle_aunt_sim_info in uncle_aunt_sim_info_list:
                continue
            self.log.format_with_message('Found an uncle/aunt. Adding them as aunt/uncle to sim.', sim=new_child_sim_info, new_uncle=uncle_aunt_sim_info)
            uncle_aunt_sim_info_list.append(uncle_aunt_sim_info)
            CommonRelationshipUtils.add_relationship_bit(new_child_sim_info, uncle_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(uncle_aunt_sim_info, new_child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Remove Cousins
        for uncle_aunt_sim_info in uncle_aunt_sim_info_list:
            uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(uncle_aunt_sim_info)
            with genealogy_caching():
                for cousin_sim_info in uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found a cousin. Adding them as cousins to sim.', sim=new_child_sim_info, new_cousin=cousin_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_child_sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(cousin_sim_info, new_child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_child_sim_info)
        with genealogy_caching():
            for brother_sister_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                if brother_sister_sim_info is new_child_sim_info:
                    continue
                self.log.format_with_message('Found a brother/sister. Adding them as brother/sister to Sim.', sim=new_child_sim_info, brother_sister_sim=brother_sister_sim_info, father=father_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_child_sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                CommonRelationshipUtils.add_relationship_bit(brother_sister_sim_info, new_child_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        new_child_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_child_sim_info)
        with genealogy_caching():
            for child_sim_info in new_child_genealogy_tracker.get_child_sim_infos_gen():
                CommonRelationshipUtils.add_relationship_bit(child_sim_info, parent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(parent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                CommonSimGenealogyUtils.set_as_mothers_mother_of(parent_sim_info, child_sim_info)

        # Add new grandmother
        new_grandmother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(parent_sim_info)
        if new_grandmother_sim_info is not None:
            self.log.format_with_message('Found grandmother, adding them as grandmother to sim.', sim=new_child_sim_info, new_grandmother=new_grandmother_sim_info)
            CommonRelationshipUtils.add_relationship_bit(new_child_sim_info, new_grandmother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandmother_sim_info, new_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_mother_of(new_grandmother_sim_info, new_child_sim_info)

        # Add new grandfather
        new_grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(parent_sim_info)
        if new_grandfather_sim_info is not None:
            self.log.format_with_message('Found grandfather, adding them as grandfather to sim.', sim=new_child_sim_info, new_grandfather=new_grandfather_sim_info)
            CommonRelationshipUtils.add_relationship_bit(new_child_sim_info, new_grandfather_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandfather_sim_info, new_child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
            CommonSimGenealogyUtils.set_as_mothers_father_of(new_grandfather_sim_info, new_child_sim_info)

        self.log.format_with_message('Done adding new mother', sim=new_child_sim_info, parent=parent_sim_info)
        return True
