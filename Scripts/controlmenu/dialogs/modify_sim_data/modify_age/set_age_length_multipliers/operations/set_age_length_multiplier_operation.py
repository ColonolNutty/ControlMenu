"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.enums.string_identifiers import CMStringId
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CMSetAgeLengthMultiplierOp(CMSingleSimOperation):
    """Set the age length multiplier for an Age."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_age_length_multiplier'

    @property
    def age(self) -> CommonAge:
        """The age the multiplier is for."""
        raise NotImplementedError()

    @property
    def setting(self) -> str:
        """The setting being modified."""
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils

        def _on_input_setting_changed(setting_name: str, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            data_store.set_value_by_key(setting_name, setting_value)
            self._update_age_progress_for_all_sims()

            def _on_acknowledged(*_, **__) -> None:
                on_completed(True)

            CommonOkDialog(
                CMSimControlMenuStringId.SAVE_AND_EXIT_TO_MENU_REQUIRED,
                CMSimControlMenuStringId.PLEASE_SAVE_AND_EXIT_TO_MAIN_MENU,
                mod_identity=self.mod_identity
            ).show(on_acknowledged=_on_acknowledged)

        data_store = CMMainDataManagerUtils().get_main_mod_settings_data_store()
        CommonDialogInputFloatOption(
            self.setting,
            data_store.get_value_by_key(
                self.setting
            ),
            CommonDialogOptionContext(
                CommonStringId.STRING_COLON_SPACE_STRING,
                CommonStringId.STRING_SPACE_STRING,
                title_tokens=(
                    CMSimControlMenuStringId.SET_AGE_LENGTH_MULTIPLIER,
                    str(data_store.get_value_by_key(self.setting)),
                ),
                description_tokens=(
                    CMSimControlMenuStringId.SET_AGE_LENGTH_MULTIPLIER_DESCRIPTION,
                    CommonLocalizationUtils.create_localized_string(
                        CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(data_store.get_default_value_by_key(self.setting)),
                            '1.0',
                            '9999.0'
                        )
                    )
                )
            ),
            min_value=1.0,
            max_value=99999.0,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True

    def _update_age_progress_for_all_sims(self) -> None:
        def _has_age(__sim_info: SimInfo) -> bool:
            return CommonAge.get_age(__sim_info) == self.age

        for _sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=_has_age):
            _sim_info.update_age_callbacks()
