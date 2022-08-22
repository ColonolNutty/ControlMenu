"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from controlmenu.commonlib.utils.common_sim_pregnancy_utils import CMSimPregnancyUtils
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.pregnancy.operations.clear_pregnancy import CMClearPregnancyOp
from controlmenu.dialogs.modify_sim_data.pregnancy.operations.create_pregnancy import CMCreatePregnancyOp
from controlmenu.dialogs.modify_sim_data.pregnancy.operations.induce_labor import CMInduceLaborOp
from controlmenu.dialogs.modify_sim_data.pregnancy.operations.set_pregnancy_speed import CMSetPregnancySpeedOp
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.settings.setting_utils import CMSettingUtils


class CMPregnancyDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_pregnancy_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.PREGNANCY

    @property
    def description(self) -> Union[int, str, LocalizedString]:
        """The title of the dialog."""
        if CommonSimPregnancyUtils.is_pregnant(self._sim_info):
            pregnancy_tracker: PregnancyTracker = self._sim_info.pregnancy_tracker
            if not pregnancy_tracker:
                return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_IS_NOT_PREGNANT, tokens=(self._sim_info,))
            if not pregnancy_tracker._offspring_data:
                pregnancy_tracker.create_offspring_data()
            strings_list = list()
            pregnancy_progress = CommonSimPregnancyUtils.get_pregnancy_progress(self._sim_info)
            pregnancy_progress_string = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.PREGNANCY_PROGRESS_PERCENTAGE, tokens=(str(pregnancy_progress),))
            strings_list.append(pregnancy_progress_string)
            other_parent_sim_info = CommonSimPregnancyUtils.get_pregnancy_partner(self._sim_info)
            if other_parent_sim_info is not None:
                strings_list.append(CommonLocalizationUtils.create_localized_string(
                    CMSimControlMenuStringId.OTHER_PARENT,
                    tokens=(
                        other_parent_sim_info,
                    )
                ))
            number_of_babies = CMSimPregnancyUtils.get_number_of_babies(self._sim_info)
            number_of_babies_string = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.NUMBER_OF_BABIES, tokens=(str(number_of_babies),))
            strings_list.append(number_of_babies_string)
            baby_details = list()
            for baby_data in CMSimPregnancyUtils.get_babies_gen(self._sim_info):
                self.log.format_info_with_message('Sim has baby data.', baby_data=baby_data, baby_data_type=type(baby_data), baby_data_dir=dir(baby_data))
                from sims4communitylib.enums.common_species import CommonSpecies
                # noinspection PyTypeChecker
                species_string_id = CommonSpecies.convert_to_localized_string_id(CommonSpecies.get_species(baby_data))
                gender_string_id = CommonGender.convert_to_localized_string_id(CommonGender.convert_from_vanilla(baby_data.gender))
                baby_details.append(
                    CommonLocalizationUtils.combine_localized_strings(
                        (
                            species_string_id,
                            gender_string_id
                        ),
                        separator=CommonLocalizedStringSeparator.COMMA_SPACE
                    )
                )
            baby_details = tuple(baby_details)
            baby_details_text = CommonLocalizationUtils.combine_localized_strings(baby_details, separator=CommonLocalizedStringSeparator.COMMA_SPACE_AND)
            baby_details_string = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.BABY_DETAILS, tokens=(baby_details_text,))
            strings_list.append(baby_details_string)

            if not strings_list:
                return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_HAS_NO_PREGNANCY_DATA, tokens=(self._sim_info,))

            return CommonLocalizationUtils.combine_localized_strings(
                tuple(strings_list),
                separator=CommonLocalizedStringSeparator.NEWLINE
            )
        return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.SIM_IS_NOT_PREGNANT, tokens=(self._sim_info,))

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        is_pregnant = CommonSimPregnancyUtils.is_pregnant(self._sim_info)

        can_produce_pregnancy = CommonSimPregnancyUtils.has_permission_for_pregnancies(self._sim_info)

        create_pregnancy_disabled_text = None
        if is_pregnant:
            create_pregnancy_disabled_text = CMSimControlMenuStringId.SIM_IS_ALREADY_PREGNANT
        elif not can_produce_pregnancy:
            create_pregnancy_disabled_text = CMSimControlMenuStringId.SIM_IS_UNABLE_TO_CREATE_PREGNANCY
        elif not CommonHouseholdUtils.has_free_household_slots(self._sim_info):
            create_pregnancy_disabled_text = CMSimControlMenuStringId.TOO_MANY_SIMS_IN_HOUSEHOLD_ALREADY

        option_dialog.add_option(
            CommonDialogButtonOption(
                'CreatePregnancy',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.CREATE_PREGNANCY,
                    disabled_text_identifier=create_pregnancy_disabled_text,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _operation_run(CMCreatePregnancyOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'SetPregnancySpeed',
                None,
                CommonDialogResponseOptionContext(
                    CommonStringId.STRING_COLON_SPACE_STRING,
                    text_tokens=(
                        CMSimControlMenuStringId.SET_PREGNANCY_SPEED,
                        str(CMSettingUtils.get_pregnancy_speed_modifier()),
                    )
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetPregnancySpeedOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'InduceLabor',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.INDUCE_LABOR,
                    disabled_text_identifier=CMSimControlMenuStringId.SIM_IS_NOT_PREGNANT if not is_pregnant else None,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _operation_run(CMInduceLaborOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ClearPregnancy',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.CLEAR_PREGNANCY,
                    disabled_text_identifier=CMSimControlMenuStringId.SIM_IS_NOT_PREGNANT if not is_pregnant else None,
                    disabled_text_tokens=(self._sim_info,)
                ),
                on_chosen=lambda *_, **__: _operation_run(CMClearPregnancyOp())
            )
        )
        return True
