"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sims_option_dialog import \
    CommonPremadeChooseSimsOptionDialog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.modinfo import ModInfo


class CMSpawnSimsAtTargetLocationInteraction(CommonImmediateSuperInteraction):
    """CMSpawnSimsAtTargetLocationInteraction(*_, **__)

    Open a dialog and Spawn the selected Sims at the target location.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_spawn_sims_at_target_location'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None:
            cls.get_log().debug('Failed, Target was invalid.')
            return TestResult.NONE
        location = CommonObjectLocationUtils.get_location(interaction_target)
        if location is None:
            cls.get_log().debug('Failed, No Location for target.')
            return TestResult.NONE
        cls.get_log().debug('Success, can spawn sims at target location.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        target_location = CommonObjectLocationUtils.get_location(interaction_target)

        def _on_submit(chosen_sim_info_list: Tuple[SimInfo]) -> None:
            if chosen_sim_info_list is None or not chosen_sim_info_list:
                return
            for chosen_sim_info in chosen_sim_info_list:
                # noinspection PyBroadException
                try:
                    if CommonAgeUtils.is_baby(chosen_sim_info):
                        from sims.baby.baby_utils import create_and_place_baby
                        create_and_place_baby(chosen_sim_info, position=target_location.transform.translation, routing_surface=target_location.routing_surface)
                    else:
                        CommonSimSpawnUtils.spawn_sim(chosen_sim_info, location=target_location)
                except:
                    pass

        def _is_not_spawned(_sim_info: SimInfo):
            return CommonSimUtils.get_sim_instance(_sim_info) is None

        dialog = CommonPremadeChooseSimsOptionDialog(
            CMStringId.CHOOSE_SIMS_TO_SPAWN,
            0,
            include_sim_callback=_is_not_spawned,
            instanced_sims_only=False,
            mod_identity=self.mod_identity
        )
        if not dialog.has_options():
            return False
        # Sort the Sims in the dialog by their name.
        dialog._internal_dialog._rows = tuple(sorted(dialog._internal_dialog._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
        dialog.show(on_submit=_on_submit, max_selectable=dialog.option_count)
        return True
