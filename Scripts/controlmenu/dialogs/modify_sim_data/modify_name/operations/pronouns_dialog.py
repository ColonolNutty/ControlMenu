"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Dict

from protocolbuffers.S4Common_pb2 import SimPronoun
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_text_option import \
    CommonDialogInputTextOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils


class CMPronounsCase(CommonInt):
    """Pronouns Case."""
    SUBJECTIVE = 1
    OBJECTIVE = 2
    POSSESSIVE_DEPENDENT = 3
    POSSESSIVE_INDEPENDENT = 4
    REFLEXIVE = 5

    @classmethod
    def get_display_name(cls, pronouns_case: 'CMPronounsCase') -> int:
        """Display names of pronouns."""
        if pronouns_case == CMPronounsCase.SUBJECTIVE:
            return 0xCAD4DF2E
        if pronouns_case == CMPronounsCase.OBJECTIVE:
            return 0xBE2233AD
        if pronouns_case == CMPronounsCase.POSSESSIVE_DEPENDENT:
            return 0xCA3B975B
        if pronouns_case == CMPronounsCase.POSSESSIVE_INDEPENDENT:
            return 0xA712EAC8
        if pronouns_case == CMPronounsCase.REFLEXIVE:
            return 0xD21465D0
        # noinspection PyTypeChecker
        return pronouns_case.name

    @classmethod
    def get_display_description(cls, pronouns_case: 'CMPronounsCase') -> int:
        """Display description of pronouns."""
        if pronouns_case == CMPronounsCase.SUBJECTIVE:
            return 0xEB6E9505
        if pronouns_case == CMPronounsCase.OBJECTIVE:
            return 0x05E1AF5C
        if pronouns_case == CMPronounsCase.POSSESSIVE_DEPENDENT:
            return 0xA37B1075
        if pronouns_case == CMPronounsCase.POSSESSIVE_INDEPENDENT:
            return 0xD8FB4176
        if pronouns_case == CMPronounsCase.REFLEXIVE:
            return 0x92D85A65
        return 0

    @classmethod
    def get_default_pronoun(cls, pronouns_case: 'CMPronounsCase', gender: CommonGender) -> str:
        """Default pronouns."""
        if gender == CommonGender.MALE:
            if pronouns_case == CMPronounsCase.SUBJECTIVE:
                return 'he'
            if pronouns_case == CMPronounsCase.OBJECTIVE:
                return 'him'
            if pronouns_case == CMPronounsCase.POSSESSIVE_DEPENDENT:
                return 'his'
            if pronouns_case == CMPronounsCase.POSSESSIVE_INDEPENDENT:
                return 'his'
            if pronouns_case == CMPronounsCase.REFLEXIVE:
                return 'himself'
        elif gender == CommonGender.FEMALE:
            if pronouns_case == CMPronounsCase.SUBJECTIVE:
                return 'she'
            if pronouns_case == CMPronounsCase.OBJECTIVE:
                return 'her'
            if pronouns_case == CMPronounsCase.POSSESSIVE_DEPENDENT:
                return 'her'
            if pronouns_case == CMPronounsCase.POSSESSIVE_INDEPENDENT:
                return 'hers'
            if pronouns_case == CMPronounsCase.REFLEXIVE:
                return 'herself'
        else:
            if pronouns_case == CMPronounsCase.SUBJECTIVE:
                return 'they'
            if pronouns_case == CMPronounsCase.OBJECTIVE:
                return 'them'
            if pronouns_case == CMPronounsCase.POSSESSIVE_DEPENDENT:
                return 'their'
            if pronouns_case == CMPronounsCase.POSSESSIVE_INDEPENDENT:
                return 'theirs'
            if pronouns_case == CMPronounsCase.REFLEXIVE:
                return 'themself'
        return 'unknown'


class CMModifyPronounsOp(CMSingleSimOperation):
    """Modify the pronouns of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_pronouns'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.PRONOUNS

    # noinspection PyMissingOrEmptyDocstring
    @property
    def description(self) -> int:
        return CMSimControlMenuStringId.MODIFY_PRONOUNS_OF_A_SIM

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        current_pronouns = self._load_pronouns(sim_info._base)

        def _on_completed(result: bool) -> None:
            self._save_pronouns(sim_info._base, current_pronouns)
            on_completed(result)

        self._open_dialog(sim_info, current_pronouns, on_completed=_on_completed)
        return True

    def _open_dialog(self, sim_info: SimInfo, current_pronouns: Dict[CMPronounsCase, str], on_completed: Callable[[bool], None] = CommonFunctionUtils.noop):
        def _reopen() -> None:
            self._open_dialog(sim_info, current_pronouns, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(True)

        def _on_chosen(_pronouns_case: CMPronounsCase, new_value: str, outcome: CommonChoiceOutcome):
            self.log.format_with_message('Entered new pronoun value', pronouns_case=_pronouns_case, new_value=new_value)
            if outcome == CommonChoiceOutcome.ERROR:
                _reopen()
                return
            elif CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen()
                return
            current_pronouns[_pronouns_case] = new_value
            _reopen()

        option_dialog = CommonChooseObjectOptionDialog(
            self.title,
            self.description,
            on_close=_on_close,
            mod_identity=self.mod_identity,
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CMSimControlMenuStringId.SELECT_FROM_DEFAULT_PRONOUNS_NAME,
                    CMSimControlMenuStringId.SELECT_FROM_DEFAULT_PRONOUNS_DESCRIPTION,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=lambda *_, **__: self._select_default_pronoun(sim_info, current_pronouns, _reopen)
            )
        )

        gender = CommonGender.get_gender(sim_info)

        for pronouns_case in CMPronounsCase.values:
            current_value = current_pronouns.get(pronouns_case, CMPronounsCase.get_default_pronoun(pronouns_case, gender))
            title = CommonLocalizationUtils.combine_localized_strings(
                (CMPronounsCase.get_display_name(pronouns_case), current_value),
                separator=CommonLocalizedStringSeparator.SPACE
            )
            description_id = CMPronounsCase.get_display_description(pronouns_case)
            if description_id != 0:
                description = CommonLocalizationUtils.create_localized_string(
                    description_id,
                    tokens=(current_value,)
                )
            else:
                description = 0

            option_dialog.add_option(
                CommonDialogInputTextOption(
                    self.mod_identity,
                    pronouns_case,
                    current_value,
                    CommonDialogOptionContext(
                        title,
                        description
                    ),
                    on_chosen=_on_chosen,
                )
            )

        if not option_dialog.has_options():
            on_completed(False)
            return True

        option_dialog.show(
            sim_info=sim_info
        )

    def _select_default_pronoun(self, sim_info: SimInfo, current_pronouns: Dict[CMPronounsCase, str], on_close: Callable[[], None]):
        def _reopen() -> None:
            self._select_default_pronoun(sim_info, current_pronouns, on_close)

        def _on_close() -> None:
            on_close()

        def _on_chosen(_: str, chosen_gender: CommonGender):
            if chosen_gender is None:
                _on_close()
                return
            self.log.format_with_message('Chose default pronouns', gender=chosen_gender)
            for pronouns_case in CMPronounsCase.values:
                default_pronoun = CMPronounsCase.get_default_pronoun(pronouns_case, chosen_gender)
                current_pronouns[pronouns_case] = default_pronoun
            _reopen()

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.SELECT_FROM_DEFAULT_PRONOUNS_NAME,
            CMSimControlMenuStringId.SELECT_FROM_DEFAULT_PRONOUNS_DESCRIPTION,
            on_close=_on_close,
            mod_identity=self.mod_identity,
        )

        male_pronouns = [CMPronounsCase.get_default_pronoun(pronouns_case, CommonGender.MALE) for pronouns_case in CMPronounsCase.values]
        option_dialog.add_option(
            CommonDialogSelectOption(
                'HeHim',
                CommonGender.MALE,
                CommonDialogOptionContext(
                    CMSimControlMenuStringId.HE_HIM,
                    CommonLocalizationUtils.combine_localized_strings_with_comma_space_and(male_pronouns),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        female_pronouns = [CMPronounsCase.get_default_pronoun(pronouns_case, CommonGender.FEMALE) for pronouns_case in CMPronounsCase.values]
        option_dialog.add_option(
            CommonDialogSelectOption(
                'SheHer',
                CommonGender.FEMALE,
                CommonDialogOptionContext(
                    CMSimControlMenuStringId.SHE_HER,
                    CommonLocalizationUtils.combine_localized_strings_with_comma_space_and(female_pronouns),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        they_them_pronouns = [CMPronounsCase.get_default_pronoun(pronouns_case, CommonGender.INVALID) for pronouns_case in CMPronounsCase.values]
        option_dialog.add_option(
            CommonDialogSelectOption(
                'TheyThem',
                CommonGender.INVALID,
                CommonDialogOptionContext(
                    CMSimControlMenuStringId.THEY_THEM,
                    CommonLocalizationUtils.combine_localized_strings_with_comma_space_and(they_them_pronouns),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_chosen
            )
        )

        if not option_dialog.has_options():
            _on_close()
            return True

        option_dialog.show(
            sim_info=sim_info
        )

    def _load_pronouns(self, sim_info: SimInfo) -> Dict[CMPronounsCase, str]:
        sim_pronouns_data = dict()
        from protocolbuffers import S4Common_pb2
        pronouns_list = S4Common_pb2.SimPronounList()
        pronouns_list.MergeFromString(sim_info.pronouns)

        # noinspection PyUnresolvedReferences
        for sim_pronoun in pronouns_list.pronouns:  # RepeatedCompositeContainer
            sim_pronoun: SimPronoun = sim_pronoun
            # noinspection PyUnresolvedReferences
            pronoun = sim_pronoun.pronoun
            # noinspection PyUnresolvedReferences
            case = sim_pronoun.case
            pronoun_case = CommonResourceUtils.get_enum_by_int_value(case, CMPronounsCase, default_value=None)
            if pronoun_case is None:
                continue
            sim_pronouns_data[pronoun_case] = pronoun

        gender = CommonGenderUtils.get_gender(sim_info)

        for pronouns_case in CMPronounsCase.values:
            if pronouns_case not in sim_pronouns_data:
                sim_pronouns_data[pronouns_case] = CMPronounsCase.get_default_pronoun(pronouns_case, gender)
        return sim_pronouns_data

    def _save_pronouns(self, sim_info: SimInfo, new_pronouns: Dict[CMPronounsCase, str]):
        from protocolbuffers import S4Common_pb2
        pronouns_list = S4Common_pb2.SimPronounList()
        pronouns = list()
        # noinspection PyUnresolvedReferences
        for (pronoun_case, pronoun_text) in new_pronouns.items():  # RepeatedCompositeContainer
            pronoun = SimPronoun()
            pronoun.pronoun = pronoun_text
            pronoun.case = int(pronoun_case)
            pronouns.append(pronoun)

        # noinspection PyUnresolvedReferences
        pronouns_list.pronouns.extend(pronouns)
        sim_info.pronouns = pronouns_list.SerializeToString()
