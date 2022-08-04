"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_integer_option import \
    CommonDialogInputIntegerOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from controlmenu.commonlib.utils.common_location_utils import CMCommonLocationUtils
from controlmenu.dialogs.game_world_dialog.enums.string_identifiers import CMGameWorldControlMenuStringId
from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.logging.has_cm_log import HasCMLog
from controlmenu.persistence.cm_data_manager_utils import CMMainDataManagerUtils
from controlmenu.settings.settings import CMSetting


class CMSetMaximumSimsPerLotOp(HasCMLog):
    """Set the maximum number of Sims per lot."""
    _DEFAULT_NPC_PER_LOT_COUNT = None
    _DEFAULT_OBJECT_ROUTING_HARD_CAP = None
    _DEFAULT_NPC_PER_LOT_MIN = 1
    _DEFAULT_NPC_PER_LOT_MAX = 9999

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_maximum_sims_per_lot'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        # noinspection PyUnusedLocal
        def _on_input_setting_changed(setting_name: str, setting_value: int, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                on_completed(True)
                return
            CMCommonLocationUtils.set_maximum_sims_per_lot(setting_value)
            data_store.set_value_by_key(CMSetting.MAXIMUM_SIMS_PER_LOT, setting_value)
            on_completed(True)

        data_store = CMMainDataManagerUtils().get_main_mod_settings_data_store()
        CommonDialogInputIntegerOption(
            self.mod_identity,
            CMSetting.MAXIMUM_SIMS_PER_LOT,
            data_store.get_value_by_key(
                CMSetting.MAXIMUM_SIMS_PER_LOT
            ),
            CommonDialogOptionContext(
                CommonStringId.STRING_COLON_SPACE_STRING,
                CommonStringId.STRING_SPACE_STRING,
                title_tokens=(
                    CMGameWorldControlMenuStringId.MAXIMUM_SIMS_PER_LOT_NAME,
                    str(data_store.get_value_by_key(CMSetting.MAXIMUM_SIMS_PER_LOT)),
                ),
                description_tokens=(
                    CMGameWorldControlMenuStringId.MAXIMUM_SIMS_PER_LOT_DESCRIPTION,
                    CommonLocalizationUtils.create_localized_string(
                        CMStringId.DEFAULT_MIN_MAX,
                        tokens=(
                            str(data_store.get_default_value_by_key(CMSetting.MAXIMUM_SIMS_PER_LOT)),
                            str(CMSetMaximumSimsPerLotOp._DEFAULT_NPC_PER_LOT_MIN),
                            str(CMSetMaximumSimsPerLotOp._DEFAULT_NPC_PER_LOT_MAX)
                        )
                    )
                )
            ),
            min_value=CMSetMaximumSimsPerLotOp._DEFAULT_NPC_PER_LOT_MIN,
            max_value=CMSetMaximumSimsPerLotOp._DEFAULT_NPC_PER_LOT_MAX,
            on_chosen=_on_input_setting_changed
        ).choose()
        return True
