"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.modify_occult.modify_occult_type_dialog import CMModifyOccultTypeDialog
from controlmenu.dialogs.modify_sim_data.modify_occult.operations.remove_all_occults import CMRemoveAllOccultsOp
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMModifyOccultDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_occult_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.MODIFY_OCCULT

    # noinspection PyMissingOrEmptyDocstring
    @property
    def per_page(self) -> int:
        return 5

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

        option_dialog.add_option(
            CommonDialogButtonOption(
                'RemoveAllOccults',
                CommonOccultType.NON_OCCULT,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.REMOVE_ALL_OCCULTS,
                ),
                on_chosen=lambda *_, **__: _operation_run(CMRemoveAllOccultsOp())
            ),
        )

        def _on_occult_type_chosen(_: str, _occult_type: CommonOccultType):
            CMModifyOccultTypeDialog(_occult_type, self._sim_info, on_previous=reopen).open()

        for occult_type in CommonOccultType.get_all(exclude_occult_types=(CommonOccultType.NON_OCCULT, CommonOccultType.NONE)):
            display_name = CommonOccultType.convert_to_localized_string_id(occult_type)
            if CommonSimOccultTypeUtils.is_occult_type(self._sim_info, occult_type):
                display_name = CommonLocalizationUtils.colorize(display_name, CommonLocalizedStringColor.GREEN)
            option_dialog.add_option(
                CommonDialogButtonOption(
                    occult_type.name,
                    occult_type,
                    CommonDialogResponseOptionContext(
                        display_name
                    ),
                    on_chosen=_on_occult_type_chosen
                )
            )
        return True
