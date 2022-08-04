"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from event_testing.results import TestResult
from interactions import ParticipantType
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.modinfo import ModInfo


class CMSummonSimFromRelPanelInteraction(CommonImmediateSuperInteraction):
    """CMSummonSimFromRelPanelInteraction(*_, **__)

    Open a dialog and Summon the target Sim from the Relationship Panel to the Active Sim
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_spawn_sim_from_rel_panel'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if 'picked_item_ids' not in kwargs:
            cls.get_log().format_with_message('Failed, No picked targets.', kwargles=kwargs)
            return TestResult.NONE
        location = CommonObjectLocationUtils.get_location(interaction_sim)
        if location is None:
            cls.get_log().format_with_message('Failed, No Location for Sim.')
            return TestResult.NONE
        cls.get_log().format_with_message('Success, can spawn sim from rel panel.', sim_ids=kwargs['picked_item_ids'])
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        sim_location = CommonObjectLocationUtils.get_location(interaction_sim)

        # noinspection PyUnresolvedReferences
        picked_sim_info = CommonSimUtils.get_sim_info(self.get_participant(ParticipantType.PickedSim))

        if picked_sim_info is None:
            return False
        if CommonSimUtils.get_sim_instance(picked_sim_info) is not None:
            # Sim is spawned, so let's move them to the Active Sim.
            CommonSimLocationUtils.set_location(picked_sim_info, sim_location)
        else:
            # Sim is not spawned, so let's spawn them.
            if CommonAgeUtils.is_baby(picked_sim_info):
                from sims.baby.baby_utils import create_and_place_baby
                create_and_place_baby(picked_sim_info, position=sim_location.transform.translation, routing_surface=sim_location.routing_surface)
            else:
                CommonSimSpawnUtils.spawn_sim(picked_sim_info, location=sim_location)
        return True
