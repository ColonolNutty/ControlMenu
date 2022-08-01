"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple, Union

from sims.outfits.outfit_enums import OutfitCategory
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_outfit_dialog import CommonChooseOutfitDialog
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMSwapToOutfitOp(S4CMSingleSimOperation):
    """Change a Sim to one of their outfits."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_set_current_outfit'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        try:
            def _on_chosen(choice: Union[Tuple[OutfitCategory, int], None], outcome: CommonChoiceOutcome) -> None:
                if choice is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                    on_completed(False)
                    return
                CommonOutfitUtils.set_current_outfit(sim_info, choice)
                on_completed(True)

            dialog = CommonChooseOutfitDialog(
                self.mod_identity,
                S4CMSimControlMenuStringId.CHANGE_OUTFIT,
                0
            )
            dialog.show(sim_info, on_chosen=_on_chosen)
        except Exception as ex:
            self.log.error('Error while attempting to build change outfit dialog.', exception=ex)
        return True
