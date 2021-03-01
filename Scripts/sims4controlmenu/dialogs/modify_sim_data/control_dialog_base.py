"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4controlmenu.commonlib.dialogs.option_dialogs.common_choose_button_option_dialog import \
    CommonChooseButtonOptionDialog
from sims4controlmenu.modinfo import ModInfo


class S4CMSimControlDialogBase(HasClassLog):
    """ A control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(
        self,
        sim_info: SimInfo,
        on_close: Callable[[], None]=None,
        on_previous: Callable[[], None]=None
    ):
        super().__init__()
        self._sim_info = sim_info
        self._on_close = on_close
        self._on_previous = on_previous

    @property
    def title(self) -> int:
        """The title of the dialog."""
        raise NotImplementedError()

    @property
    def description(self) -> int:
        """The title of the dialog."""
        return 0

    @property
    def include_previous_button(self) -> bool:
        """Whether or not to include the previous button."""
        return True

    def open(self) -> None:
        """ Open the dialog. """
        def _reopen() -> None:
            self.open()

        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        def _on_previous() -> None:
            if self._on_previous is not None:
                self._on_previous()

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            self.title,
            self.description,
            include_previous_button=self.include_previous_button,
            on_previous=_on_previous,
            on_close=_on_close
        )

        if not self._setup_dialog(option_dialog, _on_close, _on_previous, _reopen):
            _on_previous()
            return

        if not option_dialog.has_options():
            _on_previous()
            return

        option_dialog.show(
            sim_info=self._sim_info
        )

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None]
    ) -> bool:
        raise NotImplementedError()
