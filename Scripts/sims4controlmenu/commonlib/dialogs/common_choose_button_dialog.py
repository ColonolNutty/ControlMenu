"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

import sims4.commands
from typing import Tuple, Any, Callable, Union, Iterator

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.commonlib.dialogs.common_ui_dialog_response import CommonUiDialogResponse
from sims4controlmenu.commonlib.dialogs.common_ui_response_dialog import CommonUiResponseDialog
from sims4controlmenu.modinfo import ModInfo
from ui.ui_dialog import UiDialogOption


class CommonChooseButtonDialog(CommonDialog):
    """CommonChooseButtonDialog(\
        title_identifier,\
        description_identifier,\
        buttons,\
        title_tokens=(),\
        description_tokens=(),\
        mod_identity=None\
    )

    Create a dialog that prompts the player to choose a button.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_button_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_choose_button_dialog():

            def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
                pass

            buttons: Tuple[CommonUiDialogResponse] = (
                CommonUiDialogResponse(
                    1,
                    'Value 1',
                    text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE)
                ),
                CommonUiDialogResponse(
                    2,
                    'Value 2',
                    text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO)
                )
            )
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)

            active_sim_info = CommonSimUtils.get_active_sim_info()
            dialog = CommonChooseButtonDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                buttons,
                title_tokens=title_tokens,
                description_tokens=description_tokens,
            )
            dialog.show(
                on_chosen=_on_chosen,
                sim_info=active_sim_info
            )

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param buttons: The choices that can be chosen.
    :type buttons: Iterator[CommonUiDialogResponse]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_object_dialog'

    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        buttons: Iterator[CommonUiDialogResponse],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self._buttons = tuple(buttons)

    @property
    def buttons(self) -> Tuple[CommonUiDialogResponse]:
        """The buttons to display in the dialog.

        :return: A collection of buttons added to the dialog.
        :rtype: Tuple[CommonUiDialogResponse]
        """
        return self._buttons

    def add_button(self, button: CommonUiDialogResponse, *_, **__):
        """add_button(button, *_, **__)

        Add a button to the dialog.

        :param button: The button to add.
        :type button: CommonUiDialogResponse
        """
        try:
            self._buttons += (button,)
        except Exception as ex:
            self.log.error('add_row', exception=ex)

    def show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        dialog_options: UiDialogOption=0,
        sim_info: SimInfo=None
    ):
        """show(\
            on_chosen=CommonFunctionUtils.noop,\
            dialog_options=0,\
            sim_info=None,\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param on_chosen: A callback invoked upon the player choosing something from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Any, CommonChoiceOutcome], optional
        :param dialog_options: Options to apply to the dialog, such as removing the close button. Default is no options.
        :type dialog_options: UiDialogOption, optional
        :param sim_info: The Sim that will appear in the dialog image. The default Sim is the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        """
        try:
            return self._show(
                on_chosen=on_chosen,
                dialog_options=dialog_options,
                sim_info=sim_info
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(self.__class__.show.__name__), exception=ex)

    def _show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], bool]=CommonFunctionUtils.noop,
        dialog_options: UiDialogOption=0,
        sim_info: SimInfo=None
    ):
        def _on_chosen(choice: Any, outcome: CommonChoiceOutcome) -> bool:
            try:
                self.log.format_with_message('Choose button choice made.', choice=choice)
                result = on_chosen(choice, outcome)
                self.log.format_with_message('Finished handling choose object _show.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        _dialog = self.build_dialog(
            on_chosen=_on_chosen,
            dialog_options=dialog_options,
            sim_info=sim_info
        )
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    # noinspection PyMissingOrEmptyDocstring
    def build_dialog(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], bool]=CommonFunctionUtils.noop,
        dialog_options: UiDialogOption=0,
        sim_info: SimInfo=None
    ) -> Union[CommonUiResponseDialog, None]:
        self.log.format_with_message('Attempting to build dialog.', dialog_options=dialog_options)

        _dialog = self._create_dialog(
            dialog_options=dialog_options,
            sim_info=sim_info
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self.buttons) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

        def _on_chosen(dialog: CommonUiResponseDialog) -> bool:
            try:
                self.log.debug('Choice made.')
                if dialog.cancelled:
                    self.log.debug('Dialog cancelled.')
                    return on_chosen(None, CommonChoiceOutcome.CANCEL)
                if dialog.previous:
                    self.log.debug('Dialog previous.')
                    # noinspection PyTypeChecker
                    return on_chosen(None, 4)
                self.log.debug('Choice not made.')
                choice = dialog.get_response_value()
                self.log.format_with_message('Choice made.', choice=choice)
                result = on_chosen(choice, CommonChoiceOutcome.CHOICE_MADE)
                self.log.format_with_message('Finished handling choose object _on_chosen.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        self.log.debug('Adding always visible rows.')
        self._setup_dialog_rows(_dialog)

        self.log.debug('Adding listener.')
        _dialog.add_listener(_on_chosen)
        return _dialog

    def _setup_dialog_rows(
        self,
        _dialog: CommonUiResponseDialog
    ):
        for button in self.buttons:
            _dialog.add_response(button)

    def _create_dialog(
        self,
        dialog_options: UiDialogOption=0,
        sim_info: SimInfo=None
    ) -> Union[CommonUiResponseDialog, None]:
        try:
            self.log.debug('Building dialog without categories.')
            return CommonUiResponseDialog.TunableFactory().default(
                sim_info or CommonSimUtils.get_active_sim_info(),
                tuple(),
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@sims4.commands.Command('s4clib_testing.show_choose_button_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_button_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose button dialog.')

    def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

    try:
        buttons: Tuple[CommonUiDialogResponse] = (
            CommonUiDialogResponse(
                1,
                'Value 1',
                text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE)
            ),
            CommonUiDialogResponse(
                2,
                'Value 2',
                text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO)
            )
        )
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)

        active_sim_info = CommonSimUtils.get_active_sim_info()
        dialog = CommonChooseButtonDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            buttons,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
        )
        dialog.show(
            on_chosen=_on_chosen,
            sim_info=active_sim_info
        )
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
