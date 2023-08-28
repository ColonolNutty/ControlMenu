"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from controlmenu.dialogs.game_world_dialog.weather.change_weather_dialog import CMChangeWeatherDialog
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.game_world_dialog.enums.string_identifiers import CMGameWorldControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_weather_utils import CommonWeatherUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator


class CMManageWeatherDialog(CMSimControlDialogBase):
    """ The control dialog for the Weather. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_manage_weather_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMGameWorldControlMenuStringId.WEATHER

    # noinspection PyMissingOrEmptyDocstring
    @property
    def description(self) -> Union[int, str, LocalizedString]:
        strings_list = [
            CMGameWorldControlMenuStringId.CURRENT_WEATHER,
        ]
        temperature = CommonWeatherUtils.get_current_temperature()
        strings_list.append(CommonLocalizationUtils.create_localized_string(
            CMGameWorldControlMenuStringId.TEMPERATURE,
            tokens=(
                temperature.name,
            )
        ))
        cloud_type = CommonWeatherUtils.get_weather_cloud_type()
        strings_list.append(CommonLocalizationUtils.create_localized_string(
            CMGameWorldControlMenuStringId.CLOUD_TYPE,
            tokens=(
                cloud_type.name,
            )
        ))
        thunder_or_lightning = CommonWeatherUtils.current_weather_contains_thunder_or_lightning()
        strings_list.append(CommonLocalizationUtils.create_localized_string(
            CMGameWorldControlMenuStringId.THUNDER_OR_LIGHTNING,
            tokens=(
                CommonStringId.S4CL_YES if thunder_or_lightning else CommonStringId.S4CL_NO,
            )
        ))
        return CommonLocalizationUtils.combine_localized_strings(
            tuple(strings_list),
            separator=CommonLocalizedStringSeparator.NEWLINE
        )

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        option_dialog.add_option(
            CommonDialogButtonOption(
                'ChangeWeather',
                None,
                CommonDialogResponseOptionContext(
                    CMGameWorldControlMenuStringId.CHANGE_WEATHER,
                ),
                on_chosen=lambda *_, **__: CMChangeWeatherDialog(self._sim_info, on_close=reopen).open()
            )
        )
        return True
