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
        self.log.format_with_message('Removing relations to old family', new_sim=sim_info)
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)

        # Remove Blood Relations
        old_blood_siblings_sim_info_list = list()
        old_blood_family_sim_info_list = list()
        # Remove Blood Siblings
        with genealogy_caching():
            for sibling_sim_info in genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found blood sibling by blood. Removing them.', sim=sim_info, sibling=sibling_sim_info)
                old_blood_family_sim_info_list.append(sibling_sim_info)
                old_blood_siblings_sim_info_list.append(sibling_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(sim_info, sibling_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                CommonRelationshipUtils.remove_relationship_bit(sibling_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for sibling_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER, instanced_only=False):
            if sibling_sim_info in old_blood_family_sim_info_list:
                continue
            self.log.format_with_message('Found blood sibling through relationship bit. Removing them.', sim=sim_info, sibling=sibling_sim_info)
            old_blood_family_sim_info_list.append(sibling_sim_info)
            old_blood_siblings_sim_info_list.append(sibling_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, sibling_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
            CommonRelationshipUtils.remove_relationship_bit(sibling_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        old_blood_family_sim_info_list_temp = list(old_blood_family_sim_info_list)
        for blood_family_sim_info in old_blood_family_sim_info_list_temp:
            blood_family_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(blood_family_sim_info)
            with genealogy_caching():
                for blood_niece_nephew_sim_info in blood_family_genealogy_tracker.get_child_sim_infos_gen():
                    if blood_niece_nephew_sim_info in old_blood_family_sim_info_list:
                        continue
                    self.log.format_with_message('Found blood niece/nephew. Removing them.', sim=sim_info, niece_nephew=blood_niece_nephew_sim_info)
                    old_blood_family_sim_info_list.append(blood_niece_nephew_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(blood_niece_nephew_sim_info, sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, blood_niece_nephew_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Remove Blood Grandfather
        if CommonSimGenealogyUtils.has_father(sim_info):
            blood_grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
            if blood_grandfather_sim_info not in old_blood_family_sim_info_list:
                old_blood_family_sim_info_list.append(blood_grandfather_sim_info)
            self.log.format_with_message('Found father. Removing them.', sim=sim_info, father=blood_grandfather_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, blood_grandfather_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(blood_grandfather_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_father_relation(sim_info)

        # Remove Blood Grandmother
        if CommonSimGenealogyUtils.has_mother(sim_info):
            blood_grandmother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
            if blood_grandmother_sim_info not in old_blood_family_sim_info_list:
                old_blood_family_sim_info_list.append(blood_grandmother_sim_info)
            self.log.format_with_message('Found mother. Removing them.', sim=sim_info, mother=blood_grandmother_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, blood_grandmother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.remove_relationship_bit(blood_grandmother_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.remove_mother_relation(sim_info)

        for old_blood_family_sim_info in old_blood_family_sim_info_list:
            with genealogy_caching():
                for blood_child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Removing blood family from Child.', sim=blood_child_sim_info, blood_family=old_blood_family_sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(blood_child_sim_info, old_blood_family_sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, blood_child_sim_info)

        # Step Relations
        child_sim_info_list = list()
        alternate_parent_sim_info_list = list()
        with genealogy_caching():
            for blood_child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                if blood_child_sim_info not in child_sim_info_list:
                    child_sim_info_list.append(blood_child_sim_info)
                alternate_parent_sim_info = None
                if CommonSimGenealogyUtils.is_father_of(sim_info, blood_child_sim_info):
                    alternate_parent_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(blood_child_sim_info)
                if CommonSimGenealogyUtils.is_mother_of(sim_info, blood_child_sim_info):
                    alternate_parent_sim_info = CommonSimGenealogyUtils.get_father_sim_info(blood_child_sim_info)

                if alternate_parent_sim_info is not None:
                    if alternate_parent_sim_info in alternate_parent_sim_info_list:
                        continue
                    self.log.format_with_message('Found alternate parent.', sim=blood_child_sim_info, alternate_parent=alternate_parent_sim_info)
                    alternate_parent_sim_info_list.append(alternate_parent_sim_info)

        keep_family_sim_info_list = list()
        for old_blood_family_sim_info in old_blood_family_sim_info_list:
            for alternate_parent_sim_info in alternate_parent_sim_info_list:
                if alternate_parent_sim_info not in keep_family_sim_info_list:
                    keep_family_sim_info_list.append(alternate_parent_sim_info)
                alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(alternate_parent_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(alternate_parent_sim_info, old_blood_family_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alternate_parent_sim_info)

                alt_parent_siblings_sim_info_list = list()

                with genealogy_caching():
                    for alt_parent_child_sim_info in alternate_parent_genealogy_tracker.get_child_sim_infos_gen():
                        if alt_parent_child_sim_info not in keep_family_sim_info_list:
                            keep_family_sim_info_list.append(alt_parent_child_sim_info)
                        self.log.format_with_message('Found step nephew/niece relation. Removing', sim=alt_parent_child_sim_info, step_relation=old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_child_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_child_sim_info)

                with genealogy_caching():
                    for alt_parent_sibling_sim_info in alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                        if alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                            continue
                        if alt_parent_sibling_sim_info not in keep_family_sim_info_list:
                            keep_family_sim_info_list.append(alt_parent_sibling_sim_info)
                        self.log.format_with_message('Found step sibling relation. Removing', sim=alt_parent_sibling_sim_info, step_relation=old_blood_family_sim_info)
                        alt_parent_siblings_sim_info_list.append(alt_parent_sibling_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_sibling_sim_info)

                with genealogy_caching():
                    for alt_parent_grandparent_sim_info in alternate_parent_genealogy_tracker.get_grandparent_sim_ids_gen():
                        if alt_parent_grandparent_sim_info not in keep_family_sim_info_list:
                            keep_family_sim_info_list.append(alt_parent_grandparent_sim_info)
                        self.log.format_with_message('Found step grandparent relation. Removing', sim=alt_parent_grandparent_sim_info, step_relation=old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_grandparent_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_grandparent_sim_info)

                with genealogy_caching():
                    for alt_parent_parent_sim_info in alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                        if alt_parent_parent_sim_info not in keep_family_sim_info_list:
                            keep_family_sim_info_list.append(alt_parent_parent_sim_info)
                        self.log.format_with_message('Found step parent relation. Removing', sim=alt_parent_parent_sim_info, step_relation=old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_parent_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_parent_sim_info)

                for alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                    if alt_parent_sibling_sim_info not in keep_family_sim_info_list:
                        keep_family_sim_info_list.append(alt_parent_sibling_sim_info)
                    alt_parent_sibling_genealogy = CommonSimGenealogyUtils.get_genealogy_tracker(alt_parent_sibling_sim_info)
                    with genealogy_caching():
                        for alt_parent_sibling_child_sim_info in alt_parent_sibling_genealogy.get_child_sim_infos_gen():
                            self.log.format_with_message('Found cousin relation. Removing', sim=alt_parent_sibling_child_sim_info, step_relation=old_blood_family_sim_info)
                            CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_child_sim_info, old_blood_family_sim_info)
                            CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_sibling_child_sim_info)

        old_alternate_blood_sibling_parent_sim_info_list = list()
        for old_blood_sibling_sim_info in old_blood_siblings_sim_info_list:
            old_blood_sibling_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(old_blood_sibling_sim_info)
            with genealogy_caching():
                for blood_siblings_child_sim_info in old_blood_sibling_genealogy_tracker.get_child_sim_infos_gen():
                    alternate_blood_sibling_parent_sim_info = None
                    if CommonSimGenealogyUtils.is_father_of(old_blood_sibling_sim_info, blood_siblings_child_sim_info):
                        alternate_blood_sibling_parent_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(blood_siblings_child_sim_info)
                    if CommonSimGenealogyUtils.is_mother_of(old_blood_sibling_sim_info, blood_siblings_child_sim_info):
                        alternate_blood_sibling_parent_sim_info = CommonSimGenealogyUtils.get_father_sim_info(blood_siblings_child_sim_info)

                    if alternate_blood_sibling_parent_sim_info is not None:
                        if alternate_blood_sibling_parent_sim_info in alternate_parent_sim_info_list:
                            continue
                        self.log.format_with_message('Found alternate parent for blood sibling.', sim=blood_siblings_child_sim_info, alternate_parent=alternate_blood_sibling_parent_sim_info)
                        old_alternate_blood_sibling_parent_sim_info_list.append(alternate_blood_sibling_parent_sim_info)

        for old_blood_alt_parent_sibling_sim_info in old_alternate_blood_sibling_parent_sim_info_list:
            self.log.format_with_message('Found unrelated step sibling relation. Removing', sim=sim_info, step_relation=old_blood_alt_parent_sibling_sim_info)
            alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(old_blood_alt_parent_sibling_sim_info)
            CommonSimGenealogyUtils.remove_family_relations_with(old_blood_alt_parent_sibling_sim_info, sim_info)
            CommonSimGenealogyUtils.remove_family_relations_with(sim_info, old_blood_alt_parent_sibling_sim_info)

            alt_parent_siblings_sim_info_list = list()

            with genealogy_caching():
                for alt_parent_child_sim_info in alternate_parent_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found unrelated step nephew/niece relation. Removing', sim=alt_parent_child_sim_info, step_relation=sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_child_sim_info, sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(sim_info, alt_parent_child_sim_info)

            with genealogy_caching():
                for alt_parent_sibling_sim_info in alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                    if alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                        continue
                    self.log.format_with_message('Found unrelated step sibling relation. Removing', sim=alt_parent_sibling_sim_info, step_relation=sim_info)
                    alt_parent_siblings_sim_info_list.append(alt_parent_sibling_sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_sim_info, sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(sim_info, alt_parent_sibling_sim_info)

            with genealogy_caching():
                for alt_parent_grandparent_sim_info in alternate_parent_genealogy_tracker.get_grandparent_sim_ids_gen():
                    self.log.format_with_message('Found unrelated step grandparent relation. Removing', sim=alt_parent_grandparent_sim_info, step_relation=sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_grandparent_sim_info, sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(sim_info, alt_parent_grandparent_sim_info)

            with genealogy_caching():
                for alt_parent_parent_sim_info in alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                    self.log.format_with_message('Found unrelated step parent relation. Removing', sim=alt_parent_parent_sim_info, step_relation=sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_parent_sim_info, sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(sim_info, alt_parent_parent_sim_info)

            for alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                alt_parent_sibling_genealogy = CommonSimGenealogyUtils.get_genealogy_tracker(alt_parent_sibling_sim_info)
                with genealogy_caching():
                    for alt_parent_sibling_child_sim_info in alt_parent_sibling_genealogy.get_child_sim_infos_gen():
                        self.log.format_with_message('Found unrelated cousin relation. Removing', sim=alt_parent_sibling_child_sim_info, step_relation=sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_child_sim_info, sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(sim_info, alt_parent_sibling_child_sim_info)

        for child_sim_info in child_sim_info_list:
            for old_blood_alt_parent_sibling_sim_info in old_alternate_blood_sibling_parent_sim_info_list:
                alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(old_blood_alt_parent_sibling_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(old_blood_alt_parent_sibling_sim_info, child_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(child_sim_info, old_blood_alt_parent_sibling_sim_info)

                alt_parent_siblings_sim_info_list = list()

                with genealogy_caching():
                    for alt_parent_child_sim_info in alternate_parent_genealogy_tracker.get_child_sim_infos_gen():
                        self.log.format_with_message('Found unrelated step nephew/niece relation. Removing', sim=alt_parent_child_sim_info, step_relation=child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_child_sim_info, child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(child_sim_info, alt_parent_child_sim_info)

                with genealogy_caching():
                    for alt_parent_sibling_sim_info in alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                        if alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                            continue
                        self.log.format_with_message('Found unrelated step sibling relation. Removing', sim=alt_parent_sibling_sim_info, step_relation=child_sim_info)
                        alt_parent_siblings_sim_info_list.append(alt_parent_sibling_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_sim_info, child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(child_sim_info, alt_parent_sibling_sim_info)

                with genealogy_caching():
                    for alt_parent_grandparent_sim_info in alternate_parent_genealogy_tracker.get_grandparent_sim_ids_gen():
                        self.log.format_with_message('Found unrelated step grandparent relation. Removing', sim=alt_parent_grandparent_sim_info, step_relation=child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_grandparent_sim_info, child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(child_sim_info, alt_parent_grandparent_sim_info)

                with genealogy_caching():
                    for alt_parent_parent_sim_info in alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                        self.log.format_with_message('Found unrelated step parent relation. Removing', sim=alt_parent_parent_sim_info, step_relation=child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_parent_sim_info, child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(child_sim_info, alt_parent_parent_sim_info)

                for alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                    alt_parent_sibling_genealogy = CommonSimGenealogyUtils.get_genealogy_tracker(alt_parent_sibling_sim_info)
                    with genealogy_caching():
                        for alt_parent_sibling_child_sim_info in alt_parent_sibling_genealogy.get_child_sim_infos_gen():
                            self.log.format_with_message('Found unrelated cousin relation. Removing', sim=alt_parent_sibling_child_sim_info, step_relation=child_sim_info)
                            CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_child_sim_info, child_sim_info)
                            CommonSimGenealogyUtils.remove_family_relations_with(child_sim_info, alt_parent_sibling_child_sim_info)

        self.log.format_with_message('Done removing relations to old family', new_sim=sim_info)
        return True

    def _add_new_relation(self, parent_sim_info: SimInfo, new_child_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding new mother to Sim', sim=new_child_sim_info, parent_sim=parent_sim_info)
        # Add new Mother
        CommonSimGenealogyUtils.set_as_mother_of(parent_sim_info, new_child_sim_info)
        self.log.format_with_message('Done adding new mother', sim=new_child_sim_info, parent=parent_sim_info)
        return True
