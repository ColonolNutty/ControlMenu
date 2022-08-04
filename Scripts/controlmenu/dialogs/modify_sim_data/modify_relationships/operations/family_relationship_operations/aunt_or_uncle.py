"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.genealogy_tracker import genealogy_caching
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.utils.sims.common_sim_genealogy_utils import CommonSimGenealogyUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    CMSetSimAAsRelationToSimBOperation


class CMSetSimAAsAuntOrUncleToSimBOp(CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as an aunt or uncle of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_aunt_or_uncle'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_AUNT_UNCLE

    # noinspection PyMissingOrEmptyDocstring
    @property
    def opposite_relationship_bit_id(self) -> CommonRelationshipBitId:
        return CommonRelationshipBitId.FAMILY_NIECE_NEPHEW

    # noinspection PyMissingOrEmptyDocstring
    def get_disabled_text(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo) -> Union[LocalizedString, None]:
        if not CommonSimGenealogyUtils.has_mother(sim_info) and not CommonSimGenealogyUtils.has_father(sim_info):
            return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_NEEDS_TO_HAVE_MOTHER_OR_FATHER_BEFORE_YOU_CAN_ADD_UNCLES_OR_AUNTS_TO_THEM, tokens=(sim_info,))
        return super().get_disabled_text(new_aunt_or_uncle_sim_info, sim_info)

    def _update_family_tree(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_selected(_: str, operation: Any):
            if operation is None:
                on_completed(False)
                return
            operation(new_aunt_or_uncle_sim_info, sim_info, on_completed=on_completed)

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            CMSimControlMenuStringId.WHOSE_SIDE_OF_THE_FAMILY,
            0,
            on_previous=lambda: on_completed(False),
            on_close=lambda: on_completed(False),
            include_previous_button=True
        )

        if CommonSimGenealogyUtils.has_mother(sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Mother',
                    self._mothers_side,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.MOTHER
                    ),
                    on_chosen=_on_selected
                )
            )

        if CommonSimGenealogyUtils.has_father(sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Father',
                    self._fathers_side,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.FATHER
                    ),
                    on_chosen=_on_selected
                )
            )

        if not option_dialog.has_options():
            on_completed(False)
            return False

        option_dialog.show()
        return True

    def _fathers_side(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as aunt/uncle of Sim B on fathers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
            father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
            self._remove_old_relation(new_aunt_or_uncle_sim_info)
            self._add_new_relation(new_aunt_or_uncle_sim_info, sim_info, father_sim_info, mother_sim_info)
            self.log.format_with_message('Done setting Sim A as aunt/uncle of Sim B on fathers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as aunt/uncle on fathers side.', exception=ex)
            on_completed(False)
            return False
        return True

    def _mothers_side(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        try:
            self.log.format_with_message('Setting Sim A as aunt/uncle of Sim B on mothers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            mother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(sim_info)
            father_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
            self._remove_old_relation(new_aunt_or_uncle_sim_info)
            self._add_new_relation(new_aunt_or_uncle_sim_info, sim_info, mother_sim_info, father_sim_info)
            self.log.format_with_message('Done setting Sim A as aunt/uncle of Sim B on mothers side', sim_a=new_aunt_or_uncle_sim_info, sim_b=sim_info)
            on_completed(True)
        except Exception as ex:
            self.log.error('Failed to set as aunt/uncle on mothers side.', exception=ex)
            on_completed(False)
            return False
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

        # Step Relations
        old_blood_child_sim_info_list = list()
        alternate_parent_sim_info_list = list()
        with genealogy_caching():
            for blood_child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                if blood_child_sim_info not in old_blood_child_sim_info_list:
                    old_blood_child_sim_info_list.append(blood_child_sim_info)
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

        for old_blood_family_sim_info in old_blood_family_sim_info_list:
            with genealogy_caching():
                for blood_child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Removing blood family from Child.', sim=blood_child_sim_info, blood_family=old_blood_family_sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(blood_child_sim_info, old_blood_family_sim_info)
                    CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, blood_child_sim_info)

            for alternate_parent_sim_info in alternate_parent_sim_info_list:
                self.log.format_with_message('Removing unrelated step sibling.', sim=alternate_parent_sim_info, blood_family=old_blood_family_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(alternate_parent_sim_info, old_blood_family_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alternate_parent_sim_info)
                alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(alternate_parent_sim_info)

                alt_parent_siblings_sim_info_list = list()

                with genealogy_caching():
                    for alt_parent_child_sim_info in alternate_parent_genealogy_tracker.get_child_sim_infos_gen():
                        self.log.format_with_message('Found step nephew/niece relation. Removing', sim=alt_parent_child_sim_info, step_relation=old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_child_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_child_sim_info)

                with genealogy_caching():
                    for alt_parent_sibling_sim_info in alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                        if alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                            continue
                        self.log.format_with_message('Found step sibling relation. Removing', sim=alt_parent_sibling_sim_info, step_relation=old_blood_family_sim_info)
                        alt_parent_siblings_sim_info_list.append(alt_parent_sibling_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_sibling_sim_info)

                with genealogy_caching():
                    for alt_parent_grandparent_sim_info in alternate_parent_genealogy_tracker.get_grandparent_sim_ids_gen():
                        self.log.format_with_message('Found step grandparent relation. Removing', sim=alt_parent_grandparent_sim_info, step_relation=old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_grandparent_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_grandparent_sim_info)

                with genealogy_caching():
                    for alt_parent_parent_sim_info in alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                        self.log.format_with_message('Found step parent relation. Removing', sim=alt_parent_parent_sim_info, step_relation=old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_parent_sim_info, old_blood_family_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_family_sim_info, alt_parent_parent_sim_info)

                for alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
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

        for old_blood_child_sim_info in old_blood_child_sim_info_list:
            for old_blood_alt_parent_sibling_sim_info in old_alternate_blood_sibling_parent_sim_info_list:
                alternate_parent_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(old_blood_alt_parent_sibling_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(old_blood_alt_parent_sibling_sim_info, old_blood_child_sim_info)
                CommonSimGenealogyUtils.remove_family_relations_with(old_blood_child_sim_info, old_blood_alt_parent_sibling_sim_info)

                alt_parent_siblings_sim_info_list = list()

                with genealogy_caching():
                    for alt_parent_child_sim_info in alternate_parent_genealogy_tracker.get_child_sim_infos_gen():
                        self.log.format_with_message('Found unrelated step nephew/niece relation. Removing', sim=alt_parent_child_sim_info, step_relation=old_blood_child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_child_sim_info, old_blood_child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_child_sim_info, alt_parent_child_sim_info)

                with genealogy_caching():
                    for alt_parent_sibling_sim_info in alternate_parent_genealogy_tracker.get_siblings_sim_infos_gen():
                        if alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                            continue
                        self.log.format_with_message('Found unrelated step sibling relation. Removing', sim=alt_parent_sibling_sim_info, step_relation=old_blood_child_sim_info)
                        alt_parent_siblings_sim_info_list.append(alt_parent_sibling_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_sim_info, old_blood_child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_child_sim_info, alt_parent_sibling_sim_info)

                with genealogy_caching():
                    for alt_parent_grandparent_sim_info in alternate_parent_genealogy_tracker.get_grandparent_sim_ids_gen():
                        self.log.format_with_message('Found unrelated step grandparent relation. Removing', sim=alt_parent_grandparent_sim_info, step_relation=old_blood_child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_grandparent_sim_info, old_blood_child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_child_sim_info, alt_parent_grandparent_sim_info)

                with genealogy_caching():
                    for alt_parent_parent_sim_info in alternate_parent_genealogy_tracker.get_parent_sim_infos_gen():
                        self.log.format_with_message('Found unrelated step parent relation. Removing', sim=alt_parent_parent_sim_info, step_relation=old_blood_child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_parent_sim_info, old_blood_child_sim_info)
                        CommonSimGenealogyUtils.remove_family_relations_with(old_blood_child_sim_info, alt_parent_parent_sim_info)

                for alt_parent_sibling_sim_info in alt_parent_siblings_sim_info_list:
                    alt_parent_sibling_genealogy = CommonSimGenealogyUtils.get_genealogy_tracker(alt_parent_sibling_sim_info)
                    with genealogy_caching():
                        for alt_parent_sibling_child_sim_info in alt_parent_sibling_genealogy.get_child_sim_infos_gen():
                            self.log.format_with_message('Found unrelated cousin relation. Removing', sim=alt_parent_sibling_child_sim_info, step_relation=old_blood_child_sim_info)
                            CommonSimGenealogyUtils.remove_family_relations_with(alt_parent_sibling_child_sim_info, old_blood_child_sim_info)
                            CommonSimGenealogyUtils.remove_family_relations_with(old_blood_child_sim_info, alt_parent_sibling_child_sim_info)

        self.log.format_with_message('Done removing relations to old family', new_sim=sim_info)
        return True

    def _add_new_relation(self, aunt_or_uncle_sim_info: SimInfo, nephew_or_niece_sim_info: SimInfo, parent_of_nephew_or_niece_sim_info: SimInfo, other_parent_of_nephew_or_niece_sim_info: SimInfo) -> bool:
        self.log.format_with_message('Adding new aunt/uncle to Sim', sim=nephew_or_niece_sim_info, new_sim=aunt_or_uncle_sim_info)
        aunt_or_uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(aunt_or_uncle_sim_info)

        CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, parent_of_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
        CommonRelationshipUtils.add_relationship_bit(parent_of_nephew_or_niece_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        new_brother_or_sister_sim_info_list = list()
        parent_of_nephew_or_niece_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(parent_of_nephew_or_niece_sim_info)

        if other_parent_of_nephew_or_niece_sim_info is not None:
            self.log.format_with_message('Found other parent. Adding them.', sim=aunt_or_uncle_sim_info, parent=other_parent_of_nephew_or_niece_sim_info)
            new_brother_or_sister_sim_info_list.append(other_parent_of_nephew_or_niece_sim_info)
            CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, other_parent_of_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
            CommonRelationshipUtils.add_relationship_bit(other_parent_of_nephew_or_niece_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        new_niece_nephew_sim_info_list = list()
        with genealogy_caching():
            for new_nephew_or_niece_sim_info in parent_of_nephew_or_niece_genealogy_tracker.get_child_sim_infos_gen():
                if new_nephew_or_niece_sim_info in new_niece_nephew_sim_info_list:
                    continue
                new_niece_nephew_sim_info_list.append(new_nephew_or_niece_sim_info)
                self.log.format_with_message('Found niece/nephew. Adding them.', sim=aunt_or_uncle_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for new_nephew_or_niece_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(
            parent_of_nephew_or_niece_sim_info,
            CommonRelationshipBitId.FAMILY_SON_DAUGHTER,
            instanced_only=False
        ):
            if new_nephew_or_niece_sim_info in new_niece_nephew_sim_info_list:
                continue
            new_niece_nephew_sim_info_list.append(new_nephew_or_niece_sim_info)
            self.log.format_with_message('Found niece/nephew. Adding them.', sim=aunt_or_uncle_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
            CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Add Niece/Nephew
        with genealogy_caching():
            for new_nephew_or_niece_sim_info in parent_of_nephew_or_niece_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found nephew/niece. Adding them.', sim=aunt_or_uncle_sim_info, new_nephew=new_nephew_or_niece_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Add Brothers/Sisters
        with genealogy_caching():
            for new_brother_or_sister_sim_info in parent_of_nephew_or_niece_genealogy_tracker.get_siblings_sim_infos_gen():
                if new_brother_or_sister_sim_info in new_brother_or_sister_sim_info_list or new_brother_or_sister_sim_info is aunt_or_uncle_sim_info:
                    continue
                self.log.format_with_message('Found brother/sister. Adding them.', sim=aunt_or_uncle_sim_info, brother_sister=new_brother_or_sister_sim_info)
                new_brother_or_sister_sim_info_list.append(new_brother_or_sister_sim_info)
                if CommonRelationshipUtils.has_relationship_bit_with_sim(parent_of_nephew_or_niece_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING):
                    CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                    CommonRelationshipUtils.add_relationship_bit(new_brother_or_sister_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                else:
                    CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                    CommonRelationshipUtils.add_relationship_bit(new_brother_or_sister_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for new_brother_or_sister_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(
            parent_of_nephew_or_niece_sim_info,
            (CommonRelationshipBitId.FAMILY_BROTHER_SISTER, CommonRelationshipBitId.FAMILY_STEP_SIBLING),
            instanced_only=False
        ):
            if new_brother_or_sister_sim_info in new_brother_or_sister_sim_info_list or new_brother_or_sister_sim_info is aunt_or_uncle_sim_info:
                continue
            self.log.format_with_message('Found brother/sister. Adding them.', sim=aunt_or_uncle_sim_info, brother_sister=new_brother_or_sister_sim_info)
            new_brother_or_sister_sim_info_list.append(new_brother_or_sister_sim_info)
            if CommonRelationshipUtils.has_relationship_bit_with_sim(parent_of_nephew_or_niece_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING):
                CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.add_relationship_bit(new_brother_or_sister_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
            else:
                CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                CommonRelationshipUtils.add_relationship_bit(new_brother_or_sister_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        # Add Nephews
        for new_brother_or_sister_sim_info in new_brother_or_sister_sim_info_list:
            new_brother_sister_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_brother_or_sister_sim_info)
            with genealogy_caching():
                for new_nephew_or_niece_sim_info in new_brother_sister_genealogy_tracker.get_child_sim_infos_gen():
                    new_niece_nephew_sim_info_list.append(new_nephew_or_niece_sim_info)
                    self.log.format_with_message('Found niece/nephew. Adding them.', sim=aunt_or_uncle_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_nephew_or_niece_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                if new_nephew_or_niece_sim_info in new_niece_nephew_sim_info_list:
                    continue
                new_niece_nephew_sim_info_list.append(new_nephew_or_niece_sim_info)
                self.log.format_with_message('Found niece/nephew. Adding them.', sim=aunt_or_uncle_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            aunt_or_uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(aunt_or_uncle_sim_info)
            with genealogy_caching():
                for new_nephew_or_niece_sim_info in aunt_or_uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found niece/nephew. Adding them.', sim=new_brother_or_sister_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.add_relationship_bit(new_brother_or_sister_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_nephew_or_niece_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                self.log.format_with_message('Found niece/nephew. Adding them.', sim=new_brother_or_sister_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, new_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(new_brother_or_sister_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        for new_nephew_or_niece_sim_info in new_niece_nephew_sim_info_list:
            new_step_brother_or_sister_sim_info = None
            if CommonSimGenealogyUtils.is_mother_of(parent_of_nephew_or_niece_sim_info, new_nephew_or_niece_sim_info):
                new_step_brother_or_sister_sim_info = CommonSimGenealogyUtils.get_father_sim_info(new_nephew_or_niece_sim_info)

            if CommonSimGenealogyUtils.is_father_of(parent_of_nephew_or_niece_sim_info, new_nephew_or_niece_sim_info):
                new_step_brother_or_sister_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(new_nephew_or_niece_sim_info)

            if new_step_brother_or_sister_sim_info is not None:
                CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_step_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
                CommonRelationshipUtils.add_relationship_bit(new_step_brother_or_sister_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

            with genealogy_caching():
                for new_cousin_sim_info in aunt_or_uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found cousin. Adding them.', sim=new_cousin_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, new_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.add_relationship_bit(new_cousin_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    if new_step_brother_or_sister_sim_info is not None:
                        CommonRelationshipUtils.add_relationship_bit(new_cousin_sim_info, new_step_brother_or_sister_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                        CommonRelationshipUtils.add_relationship_bit(new_step_brother_or_sister_sim_info, new_cousin_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_cousin_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                self.log.format_with_message('Found cousin. Adding them.', sim=new_cousin_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, new_cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                CommonRelationshipUtils.add_relationship_bit(new_cousin_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)

        with genealogy_caching():
            for new_nephew_or_niece_sim_info in aunt_or_uncle_genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found niece/nephew. Adding them.', sim=parent_of_nephew_or_niece_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, parent_of_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(parent_of_nephew_or_niece_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

            for new_nephew_or_niece_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                self.log.format_with_message('Found niece/nephew. Adding them.', sim=parent_of_nephew_or_niece_sim_info, niece_nephew=new_nephew_or_niece_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_nephew_or_niece_sim_info, parent_of_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                CommonRelationshipUtils.add_relationship_bit(parent_of_nephew_or_niece_sim_info, new_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        # Add Grandparents
        if CommonSimGenealogyUtils.has_father(parent_of_nephew_or_niece_sim_info):
            new_grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(parent_of_nephew_or_niece_sim_info)
            CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_grandfather_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandfather_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_father_of(new_grandfather_sim_info, aunt_or_uncle_sim_info)

            with genealogy_caching():
                for new_grandchild_sim_info in aunt_or_uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found grandfather. Adding them.', sim=new_grandchild_sim_info, grandfather=new_grandfather_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_grandfather_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_grandfather_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    if CommonSimGenealogyUtils.is_father_of(aunt_or_uncle_sim_info, new_grandchild_sim_info):
                        CommonSimGenealogyUtils.set_as_fathers_father_of(new_grandfather_sim_info, new_grandchild_sim_info)
                    else:
                        CommonSimGenealogyUtils.set_as_mothers_father_of(new_grandfather_sim_info, new_grandchild_sim_info)

            for new_grandchild_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                self.log.format_with_message('Found grandfather. Adding them.', sim=new_grandchild_sim_info, grandfather=new_grandfather_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_grandfather_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_grandfather_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        if CommonSimGenealogyUtils.has_mother(parent_of_nephew_or_niece_sim_info):
            new_grandmother_sim_info = CommonSimGenealogyUtils.get_mother_sim_info(parent_of_nephew_or_niece_sim_info)
            CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_grandmother_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandmother_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)
            CommonSimGenealogyUtils.set_as_mother_of(new_grandmother_sim_info, aunt_or_uncle_sim_info)

            with genealogy_caching():
                for new_grandchild_sim_info in aunt_or_uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found grandmother. Adding them.', sim=new_grandchild_sim_info, grandmother=new_grandmother_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_grandmother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_grandmother_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)
                    if CommonSimGenealogyUtils.is_father_of(aunt_or_uncle_sim_info, new_grandchild_sim_info):
                        CommonSimGenealogyUtils.set_as_fathers_mother_of(new_grandmother_sim_info, new_grandchild_sim_info)
                    else:
                        CommonSimGenealogyUtils.set_as_mothers_mother_of(new_grandmother_sim_info, new_grandchild_sim_info)

            for new_grandchild_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                self.log.format_with_message('Found grandmother. Adding them.', sim=new_grandchild_sim_info, grandmother=new_grandmother_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_grandmother_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_grandmother_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        for new_grandparent_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(parent_of_nephew_or_niece_sim_info, CommonRelationshipBitId.FAMILY_PARENT, instanced_only=False):
            self.log.format_with_message('Found grandparent. Adding them.', sim=aunt_or_uncle_sim_info, grandparent_sim=new_grandparent_sim_info)
            CommonRelationshipUtils.add_relationship_bit(aunt_or_uncle_sim_info, new_grandparent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
            CommonRelationshipUtils.add_relationship_bit(new_grandparent_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

            with genealogy_caching():
                for child_sim_info in aunt_or_uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found child, Adding grandparent.', sim=child_sim_info, grandparent=new_grandparent_sim_info)
                    CommonRelationshipUtils.add_relationship_bit(child_sim_info, new_grandparent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                    CommonRelationshipUtils.add_relationship_bit(new_grandparent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

            # Handle Step Children of Aunt/Uncle
            for new_grandchild_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER, instanced_only=False):
                self.log.format_with_message('Found grandmother. Adding them.', sim=new_grandchild_sim_info, grandparent=new_grandparent_sim_info)
                CommonRelationshipUtils.add_relationship_bit(new_grandchild_sim_info, new_grandparent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                CommonRelationshipUtils.add_relationship_bit(new_grandparent_sim_info, new_grandchild_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

        self.log.format_with_message('Done adding new aunt/uncle', sim=nephew_or_niece_sim_info, new_sim=aunt_or_uncle_sim_info)
        return True
