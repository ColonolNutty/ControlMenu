"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
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


class CommonChooseResponseDialog(CommonDialog):
    """CommonChooseResponseDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        responses,\
        title_tokens=(),\
        description_tokens=()\
    )

    Create a dialog that prompts the player to choose a response.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_response_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_choose_response_dialog():

            def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
                pass

            responses: Tuple[CommonUiDialogResponse] = (
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
            dialog = CommonChooseResponseDialog(
                ModInfo.get_identity(),
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                responses,
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
    :param responses: The choices that can be chosen.
    :type responses: Iterator[CommonUiDialogResponse]
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
        return 's4cl_choose_response_dialog'

    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        responses: Iterator[CommonUiDialogResponse],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=()
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self._responses = tuple(responses)

    @property
    def responses(self) -> Tuple[CommonUiDialogResponse]:
        """The responses to display in the dialog."""
        return self._responses

    def add_response(self, response: CommonUiDialogResponse, *_, **__):
        """add_response(response, *_, **__)

        Add a response to the dialog.

        :param response: The response to add.
        :type response: CommonUiDialogResponse
        """
        try:
            self._responses += (response,)
        except Exception as ex:
            self.log.error('add_response', exception=ex)

    def show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        dialog_options: UiDialogOption=0,
        include_previous_button: bool=True,
        sim_info: SimInfo=None
    ):
        """show(\
            on_chosen=CommonFunctionUtils.noop,\
            on_previous=CommonFunctionUtils.noop,\
            dialog_options=0,\
            include_previous_button=True,\
            sim_info=None,\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param on_chosen: A callback invoked upon the player choosing something from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Any, CommonChoiceOutcome], optional
        :param on_previous: A callback performed when the previous response is chosen. Default is no operation.
        :type on_previous: Callable[[], None], optional
        :param dialog_options: Options to apply to the dialog, such as removing the close button. Default is no options.
        :type dialog_options: UiDialogOption, optional
        :param include_previous_button: If True, the Previous button will be appended to the end of the dialog. Default is True.
        :type include_previous_button: bool, optional
        :param sim_info: The Sim that will appear in the dialog image. The default Sim is the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        """
        try:
            return self._show(
                on_chosen=on_chosen,
                on_previous=on_previous,
                dialog_options=dialog_options,
                include_previous_button=include_previous_button,
                sim_info=sim_info
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(self.__class__.show.__name__), exception=ex)

    def _show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        dialog_options: UiDialogOption=0,
        include_previous_button: bool=True,
        sim_info: SimInfo=None
    ):
        def _on_chosen(choice: Any, outcome: CommonChoiceOutcome) -> None:
            try:
                self.log.format_with_message('Choice made.', choice=choice)
                on_chosen(choice, outcome)
                self.log.debug('Finished handling _show.')
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)

        _dialog = self.build_dialog(
            on_chosen=_on_chosen,
            on_previous=on_previous,
            dialog_options=dialog_options,
            include_previous_button=include_previous_button,
            sim_info=sim_info
        )
        if _dialog is None:
            self.log.error('An error occurred when building the dialog!')
            return
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    def build_dialog(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        dialog_options: Union[UiDialogOption, int]=0,
        include_previous_button: bool=True,
        sim_info: SimInfo=None
    ) -> Union[CommonUiResponseDialog, None]:
        """build_dialog(\
            on_chosen=CommonFunctionUtils.noop,\
            on_previous=CommonFunctionUtils.noop,\
            dialog_options=0,\
            include_previous_button=True,\
            sim_info=None\
        )

        Build the dialog.

        :param on_chosen: A callback performed when a choice is made. Default is no operation.
        :type on_chosen: Callable[[Any, CommonChoiceOutcome], None], optional
        :param on_previous: A callback performed when the previous response is chosen. Default is no operation.
        :type on_previous: Callable[[], None], optional
        :param dialog_options: Display options for the dialog, such as hiding the close button. Default is no display options.
        :type dialog_options: UiDialogOption, optional
        :param include_previous_button: If True, the Previous button will be appended to the end of the dialog. Default is True.
        :type include_previous_button: bool, optional
        :param sim_info: A Sim that will appear in the top left image when the dialog is shown. If set to None, the active Sim will be used. Default is None.
        :type sim_info: SimInfo, optional
        :return: The built dialog or None if a problem occurs.
        :rtype: Union[CommonUiResponseDialog, None]
        """
        self.log.format_with_message('Attempting to build dialog.', dialog_options=dialog_options)

        _dialog = self._create_dialog(
            dialog_options=dialog_options,
            include_previous_button=include_previous_button,
            sim_info=sim_info
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self.responses) == 0:
            raise AssertionError('No responses have been provided. Add responses to the dialog before attempting to display it.')

        def _on_chosen(dialog: CommonUiResponseDialog) -> None:
            try:
                if dialog.cancelled:
                    self.log.debug('Dialog cancelled.')
                    on_chosen(None, CommonChoiceOutcome.CANCEL)
                    return
                if dialog.previous:
                    self.log.debug('Dialog previous.')
                    on_previous()
                    return
                choice = dialog.get_response_value()
                self.log.format_with_message('Choice made.', choice=choice)
                on_chosen(choice, CommonChoiceOutcome.CHOICE_MADE)
                self.log.debug('Finished handling _on_chosen.')
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)

        self._setup_dialog(_dialog)

        self.log.debug('Adding listener.')
        _dialog.add_listener(_on_chosen)
        return _dialog

    def _setup_dialog(
        self,
        _dialog: CommonUiResponseDialog
    ):
        self.log.debug('Setting up dialog.')
        for response in self.responses:
            _dialog.add_response(response)

    def _create_dialog(
        self,
        dialog_options: UiDialogOption=0,
        include_previous_button: bool=True,
        sim_info: SimInfo=None
    ) -> Union[CommonUiResponseDialog, None]:
        try:
            self.log.debug('Creating dialog.')
            return CommonUiResponseDialog.TunableFactory().default(
                sim_info or CommonSimUtils.get_active_sim_info(),
                tuple(),
                include_previous_button=include_previous_button,
                dialog_options=dialog_options,
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@sims4.commands.Command('s4clib_testing.show_choose_response_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_response_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose response dialog.')

    def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

    try:
        responses: Tuple[CommonUiDialogResponse] = (
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
        dialog = CommonChooseResponseDialog(
            ModInfo.get_identity(),
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            responses,
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
