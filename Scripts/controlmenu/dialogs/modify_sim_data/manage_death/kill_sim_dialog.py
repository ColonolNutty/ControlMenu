"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.manage_death.operations.kill_sim import CMKillSimOp
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from sims4communitylib.enums.common_death_types import CommonDeathType
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.misc.common_text_utils import CommonTextUtils


class CMKillSimDialog(CMSimControlDialogBase):
    """ The control dialog for the Game Clock. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_change_weather_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) ->  Union[int, str, LocalizedString]:
        return CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.KILL_SIM, tokens=(self._sim_info,))

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
        def _operation_run(_: str, _death_type: CommonDeathType):
            def _on_operation_complete(_: CommonExecutionResult) -> None:
                on_close()

            CMKillSimOp(_death_type).run(self._sim_info, on_completed=_on_operation_complete)

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Random',
                CommonDeathType.get_random(),
                CommonDialogResponseOptionContext(
                    CommonStringId.S4CL_RANDOM,
                ),
                on_chosen=_operation_run
            )
        )

        # noinspection PyTypeChecker
        for death_type in CommonDeathType.values:
            if death_type in (
                CommonDeathType.NONE,
                CommonDeathType.MURPHY_BED,
                CommonDeathType.COW_PLANT,
                CommonDeathType.VENDING_MACHINE
            ):
                continue
            option_dialog.add_option(
                CommonDialogButtonOption(
                    death_type.name,
                    death_type,
                    CommonDialogResponseOptionContext(
                        CommonTextUtils.capitalize(death_type.name.replace('_', ' ').lower()),
                    ),
                    on_chosen=_operation_run
                )
            )
        return True
