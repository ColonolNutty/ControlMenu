"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from controlmenu.dialogs.game_world_dialog.weather.operations.change_weather import CMChangeWeatherOp
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.game_world_dialog.enums.string_identifiers import CMGameWorldControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from sims4communitylib.enums.common_weather_event_ids import CommonWeatherEventId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_weather_utils import CommonWeatherUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.misc.common_text_utils import CommonTextUtils


class CMChangeWeatherDialog(CMSimControlDialogBase):
    """ The control dialog for the Weather. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_change_weather_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMGameWorldControlMenuStringId.CHANGE_WEATHER

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

    # noinspection PyMissingOrEmptyDocstring
    @property
    def per_page(self) -> int:
        return 8

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_previous_button(self) -> bool:
        return False

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(_: str, _weather_event_id: CommonWeatherEventId):
            def _on_operation_complete(_: bool) -> None:
                on_close()

            CMChangeWeatherOp(_weather_event_id).run(on_completed=_on_operation_complete)

        # noinspection PyTypeChecker
        for weather_event_id in CommonWeatherEventId.values:
            option_dialog.add_option(
                CommonDialogButtonOption(
                    weather_event_id.name,
                    weather_event_id,
                    CommonDialogResponseOptionContext(
                        CommonTextUtils.capitalize(weather_event_id.name.replace('_', ' ').lower()),
                    ),
                    on_chosen=_operation_run
                )
            )
        return True
