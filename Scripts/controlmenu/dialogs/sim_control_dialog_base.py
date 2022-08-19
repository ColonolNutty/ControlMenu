"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from controlmenu.logging.has_cm_class_log import HasCMClassLog


class CMSimControlDialogBase(HasCMClassLog):
    """ A control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(
        self,
        sim_info: SimInfo,
        on_close: Callable[[], None] = None,
        on_previous: Callable[[], None] = None
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
    def description(self) -> Union[int, str, LocalizedString]:
        """The description of the dialog."""
        return 0

    @property
    def include_previous_button(self) -> bool:
        """Determine if the previous button should be included on the first page of the dialog."""
        return True

    @property
    def per_page(self) -> int:
        """The number of options per page."""
        return 10

    def open(self, **__) -> None:
        """ Open the dialog. """
        def _reopen() -> None:
            self.open(**__)

        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        def _on_previous() -> None:
            if any(__):
                self.open()
                return
            if self._on_previous is not None:
                self._on_previous()

        option_dialog = CommonChooseButtonOptionDialog(
            self.mod_identity,
            self.title,
            self.description,
            include_previous_button=self.include_previous_button,
            on_previous=_on_previous,
            on_close=_on_close,
            per_page=self.per_page
        )

        if not self._setup_dialog(option_dialog, _on_close, _on_previous, _reopen, **__):
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
        reopen: Callable[[], None],
        **__
    ) -> bool:
        raise NotImplementedError()
