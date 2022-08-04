"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_integer_option import \
    CommonDialogInputIntegerOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.settings.settings import CMSetting


class CMSetMaximumHouseholdSizeOp(CMSingleSimOperation):
    """Set the maximum household size."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_maximum_household_size_speed'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        from controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils

        def _on_input_setting_changed(setting_name: str, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            data_store.set_value_by_key(setting_name, setting_value)
            on_completed(True)

        data_store = CMMainDataManagerUtils().get_main_mod_settings_data_store()
        CommonDialogInputIntegerOption(
            self.mod_identity,
            CMSetting.MAXIMUM_HOUSEHOLD_SIZE,
            data_store.get_value_by_key(
                CMSetting.MAXIMUM_HOUSEHOLD_SIZE
            ),
            CommonDialogOptionContext(
                CommonStringId.STRING_COLON_SPACE_STRING,
                CommonStringId.STRING_SPACE_STRING,
                title_tokens=(
                    CMSimControlMenuStringId.SET_MAXIMUM_HOUSEHOLD_SIZE,
                    str(data_store.get_value_by_key(CMSetting.MAXIMUM_HOUSEHOLD_SIZE)),
                ),
                description_tokens=(
                    CMSimControlMenuStringId.SET_MAXIMUM_HOUSEHOLD_SIZE_DESCRIPTION,
                    CommonLocalizationUtils.create_localized_string(
                        CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(data_store.get_default_value_by_key(CMSetting.MAXIMUM_HOUSEHOLD_SIZE)),
                            '0.0',
                            '9999.0'
                        )
                    )
                )
            ),
            min_value=1,
            max_value=999999,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True
