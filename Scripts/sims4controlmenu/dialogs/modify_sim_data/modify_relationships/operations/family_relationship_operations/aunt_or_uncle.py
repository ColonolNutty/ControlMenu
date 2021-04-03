"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.genealogy_tracker import genealogy_caching
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.commonlib.dialogs.option_dialogs.options.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4controlmenu.commonlib.utils.common_sim_genealogy_utils import CommonSimGenealogyUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.modify_relationships.operations.family_relationship_operations.set_sim_a_relation_to_sim_b_operation import \
    S4CMSetSimAAsRelationToSimBOperation


class S4CMSetSimAAsAuntOrUncleToSimBOp(S4CMSetSimAAsRelationToSimBOperation):
    """Set Sim A as an aunt or uncle of Sim B"""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_set_aunt_or_uncle'

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
            return CommonLocalizationUtils.create_localized_string(S4CMSimControlMenuStringId.SIM_NEEDS_TO_HAVE_MOTHER_OR_FATHER_BEFORE_YOU_CAN_ADD_UNCLES_OR_AUNTS_TO_THEM, tokens=(sim_info, ))
        return super().get_disabled_text(new_aunt_or_uncle_sim_info, sim_info)

    def _update_family_tree(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_selected(_: str, operation: Any):
            if operation is None:
                on_completed(False)
                return
            operation(new_aunt_or_uncle_sim_info, sim_info, on_completed=on_completed)

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            S4CMSimControlMenuStringId.WHOSE_SIDE_OF_THE_FAMILY,
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
                        S4CMSimControlMenuStringId.MOTHER
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
                        S4CMSimControlMenuStringId.FATHER
                    ),
                    on_chosen=_on_selected
                )
            )

        if not option_dialog.has_options():
            on_completed(False)
            return False

        option_dialog.show()
        return True

    def _fathers_side(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
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

    def _mothers_side(self, new_aunt_or_uncle_sim_info: SimInfo, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
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
        self.log.format_with_message('Removing aunt/uncle relations to old family', new_sim=sim_info)
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        # Remove Brothers/Sisters
        brother_sister_sim_info_list = list()
        with genealogy_caching():
            for brother_sister_sim_info in genealogy_tracker.get_siblings_sim_infos_gen():
                self.log.format_with_message('Found brother/sister. Removing them.', sim=sim_info, brother_sister=brother_sister_sim_info)
                brother_sister_sim_info_list.append(brother_sister_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
                CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)

        for brother_sister_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, (CommonRelationshipBitId.FAMILY_BROTHER_SISTER, CommonRelationshipBitId.FAMILY_STEP_SIBLING), instanced_only=False):
            if brother_sister_sim_info in brother_sister_sim_info_list:
                continue
            self.log.format_with_message('Found brother/sister. Removing them.', sim=sim_info, brother_sister=brother_sister_sim_info)
            brother_sister_sim_info_list.append(brother_sister_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
            CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_BROTHER_SISTER)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, brother_sister_sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)
            CommonRelationshipUtils.remove_relationship_bit(brother_sister_sim_info, sim_info, CommonRelationshipBitId.FAMILY_STEP_SIBLING)

        # Remove Nephews
        for brother_sister_sim_info in brother_sister_sim_info_list:
            uncle_genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(brother_sister_sim_info)
            with genealogy_caching():
                for niece_nephew_sim_info in uncle_genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found niece/nephew. Removing them.', sim=sim_info, niece_nephew=niece_nephew_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, niece_nephew_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
                    CommonRelationshipUtils.remove_relationship_bit(niece_nephew_sim_info, sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        for niece_nephew_uncle_or_aunt_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, (CommonRelationshipBitId.FAMILY_NIECE_NEPHEW, CommonRelationshipBitId.FAMILY_AUNT_UNCLE), instanced_only=False):
            self.log.format_with_message('Found niece/nephew. Removing them.', sim=sim_info, niece_nephew_uncle_or_aunt=niece_nephew_uncle_or_aunt_sim_info)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, niece_nephew_uncle_or_aunt_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
            CommonRelationshipUtils.remove_relationship_bit(niece_nephew_uncle_or_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)
            CommonRelationshipUtils.remove_relationship_bit(niece_nephew_uncle_or_aunt_sim_info, sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
            CommonRelationshipUtils.remove_relationship_bit(sim_info, niece_nephew_uncle_or_aunt_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)

        with genealogy_caching():
            for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                self.log.format_with_message('Found Child of Sim. Updating them.', sim=sim_info, child=child_sim_info)
                for cousin_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN, instanced_only=False):
                    self.log.format_with_message('Found Cousin, removing them.', sim=child_sim_info, cousin=cousin_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(child_sim_info, cousin_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                    CommonRelationshipUtils.remove_relationship_bit(cousin_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_COUSIN)
                for aunt_or_uncle_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(child_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE, instanced_only=False):
                    self.log.format_with_message('Found Aunt/Uncle, removing them.', sim=child_sim_info, aunt_or_uncle=aunt_or_uncle_sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(child_sim_info, aunt_or_uncle_sim_info, CommonRelationshipBitId.FAMILY_AUNT_UNCLE)
                    CommonRelationshipUtils.remove_relationship_bit(aunt_or_uncle_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_NIECE_NEPHEW)

        if CommonSimGenealogyUtils.has_father(sim_info):
            grandfather_sim_info = CommonSimGenealogyUtils.get_father_sim_info(sim_info)
            self.log.format_with_message('Found father, removing father.', sim=sim_info, father=grandfather_sim_info)
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

        for grandparent_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, CommonRelationshipBitId.FAMILY_PARENT, instanced_only=False):
            self.log.format_with_message('Found grandparent. Removing them.', sim=sim_info, grandparent_sim=grandparent_sim_info)
            has_step_link = False
            with genealogy_caching():
                for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                    self.log.format_with_message('Found child, checking if has step link.', sim=child_sim_info, grandparent=grandparent_sim_info)
                    if CommonSimGenealogyUtils.is_mother_of(sim_info, child_sim_info):
                        if CommonSimGenealogyUtils.is_fathers_father_of(grandparent_sim_info, child_sim_info) or CommonSimGenealogyUtils.is_fathers_mother_of(grandparent_sim_info, child_sim_info):
                            self.log.format_with_message('Has step link. Keeping step grandparent relations.', sim=child_sim_info, grandparent=grandparent_sim_info)
                            has_step_link = True
                            break
                    if CommonSimGenealogyUtils.is_father_of(sim_info, child_sim_info):
                        if CommonSimGenealogyUtils.is_mothers_father_of(grandparent_sim_info, child_sim_info) or CommonSimGenealogyUtils.is_mothers_mother_of(grandparent_sim_info, child_sim_info):
                            self.log.format_with_message('Has step link. Keeping step grandparent relations.', sim=child_sim_info, grandparent=grandparent_sim_info)
                            has_step_link = True
                            break
                    self.log.format_with_message('No step link.', sim=child_sim_info, grandparent=grandparent_sim_info)

            if not has_step_link:
                with genealogy_caching():
                    for child_sim_info in genealogy_tracker.get_child_sim_infos_gen():
                        self.log.format_with_message('Found child, removing grandparent.', sim=child_sim_info, grandparent=grandparent_sim_info)
                        CommonRelationshipUtils.remove_relationship_bit(child_sim_info, grandparent_sim_info, CommonRelationshipBitId.FAMILY_GRANDPARENT)
                        CommonRelationshipUtils.remove_relationship_bit(grandparent_sim_info, child_sim_info, CommonRelationshipBitId.FAMILY_GRANDCHILD)

                CommonRelationshipUtils.remove_relationship_bit(sim_info, grandparent_sim_info, CommonRelationshipBitId.FAMILY_PARENT)
                CommonRelationshipUtils.remove_relationship_bit(grandparent_sim_info, sim_info, CommonRelationshipBitId.FAMILY_SON_DAUGHTER)

        self.log.format_with_message('Done removing old relations', new_sim=sim_info)
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
