"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMRemoveAllOccultsOp(S4CMSingleSimOperation):
    """Remove All Occult Types from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.mermaid import S4CMMermaidRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.skeleton import S4CMSkeletonRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.vampire import S4CMVampireRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.witch import S4CMWitchRemoveOp
        from sims4controlmenu.dialogs.modify_sim_data.modify_occult.operations.alien import S4CMAlienRemoveOp
        S4CMAlienRemoveOp().run(sim_info)
        S4CMMermaidRemoveOp().run(sim_info)
        S4CMSkeletonRemoveOp().run(sim_info)
        S4CMVampireRemoveOp().run(sim_info)
        S4CMWitchRemoveOp().run(sim_info)
        on_completed(True)
        return True
