"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple, Union, List

from event_testing.test_base import BaseTest
from event_testing.tests import TestList
from interactions import ParticipantType
from interactions.base.interaction import Interaction
from sims.sim import Sim
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from controlmenu.modinfo import ModInfo


from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils


class _CMIsNotAvailableInteractionTest(BaseTest):
    def __init__(self, *_, interaction_name: str = None, **__):
        super().__init__(*_, **__)
        self._interaction_name = interaction_name

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Any:
        return {'subjects': ParticipantType.Actor, 'targets': ParticipantType.TargetSim}

    def __call__(self, subjects: Tuple[Sim] = (), targets: Any = ()) -> Any:
        return CommonTestResult.FALSE


class _CMInteractionModification(CommonService, HasClassLog):
    """ Modifies interactions. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    @classmethod
    def add_test_globals_to_interactions(cls, interaction_ids: Tuple[Union[int, Interaction]], tests_to_add: Tuple[BaseTest]) -> bool:
        """add_test_globals_to_interactions(interaction_ids, tests_to_add)

        Add a test to the test globals of an interaction.

        :param interaction_ids: The interactions to modify.
        :type interaction_ids: Tuple[Union[int, Interaction]]
        :param tests_to_add: Tests to add.
        :type tests_to_add: Tuple[BaseTest]
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if not tests_to_add:
            return False
        success = False
        for interaction_id in interaction_ids:
            interaction_instance = CommonInteractionUtils.load_interaction_by_id(interaction_id)
            if interaction_instance is None:
                continue
            if hasattr(interaction_instance, 'test_globals'):
                tests_list = list(interaction_instance.test_globals)
            else:
                tests_list = list()
            for test_to_add in tests_to_add:
                tests_list.insert(0, test_to_add)
            interaction_instance.test_globals = TestList(tests_list)
            success = True
        return success

    def _block_vanilla_interactions(self) -> None:
        interaction_ids = (
            125129,  # reactions_Generic_Shocked_Strong
            125127,  # reaction_Generic_ShockedAggregate
            219897,  # idle_Buff_Cauldron_Potion_Immortality_ApplyVFX
        )
        for interaction_id in interaction_ids:
            interaction = CommonInteractionUtils.load_interaction_by_id(interaction_id)
            if interaction is None:
                continue
            interaction_name = CommonInteractionUtils.get_interaction_short_name(interaction) or interaction.__name__ or interaction.__class__.__name__
            tests_to_add: List[BaseTest] = [
                _CMIsNotAvailableInteractionTest(interaction_name=interaction_name)
            ]
            _CMInteractionModification.add_test_globals_to_interactions((interaction,), tuple(tests_to_add))

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _cm_block_interactions_on_zone_load(event_data: S4CLZoneLateLoadEvent) -> bool:
        if event_data.game_loaded:
            return False
        _CMInteractionModification()._block_vanilla_interactions()
        clothing_nude_buff_id = 128807  # buff_Clothing_Nude
        buff = CommonBuffUtils.load_buff_by_id(clothing_nude_buff_id)
        if buff is not None:
            buff.broadcaster = None
        return True
