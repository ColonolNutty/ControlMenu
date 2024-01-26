"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from traits.traits import Trait


class CMModifyWalkStyleDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_walk_style_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.WALK_STYLE

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        walk_style_ids = (
            9094,  # trait_WalkStyleDefault
            9095,  # trait_WalkStylePerky
            9096,  # trait_WalkStyleSnooty
            9293,  # trait_WalkStyleSwagger
            29593,  # trait_WalkStyleFeminine
            29594,  # trait_WalkStyleTough
            29600,  # trait_WalkStyleGoofy
            98757,  # trait_WalkStyleSleepy
            98760,  # trait_WalkStyleEnergetic
            155564,  # trait_WalkStyleCreepy
        )

        def _on_choose_walk_style(_: str, _walk_style_id: int):
            for style_id in walk_style_ids:
                CommonTraitUtils.remove_trait(self._sim_info, style_id)

            CommonTraitUtils.add_trait(self._sim_info, _walk_style_id)
            reopen()

        sim = CommonSimUtils.get_sim_info(self._sim_info)

        for walk_style_trait_id in walk_style_ids:
            trait: Trait = CommonTraitUtils.load_trait_by_id(walk_style_trait_id)
            if trait is None:
                continue

            # noinspection PyUnresolvedReferences
            display_name = trait.display_name(sim)
            if CommonTraitUtils.has_trait(self._sim_info, walk_style_trait_id):
                display_name = CommonLocalizationUtils.colorize(display_name, text_color=CommonLocalizedStringColor.GREEN)

            option_dialog.add_option(
                CommonDialogButtonOption(
                    str(trait),
                    walk_style_trait_id,
                    CommonDialogResponseOptionContext(
                        display_name,
                    ),
                    on_chosen=_on_choose_walk_style
                )
            )

        return True
