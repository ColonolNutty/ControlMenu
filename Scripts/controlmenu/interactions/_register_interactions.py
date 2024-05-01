"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from objects.script_object import ScriptObject
from sims.sim import Sim
from sims4communitylib.enums.affordance_list_ids import CommonAffordanceListId
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonInteractionHandler, CommonScriptObjectInteractionHandler
from sims4communitylib.services.resources.common_instance_manager_modification_registry import \
    CommonInstanceManagerModificationRegistry
from sims4communitylib.services.resources.modification_handlers.common_add_interactions_to_affordance_lists_handler import \
    CommonAddInteractionsToAffordanceListsModificationHandler
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from controlmenu.enums.interaction_identifiers import CMInteractionId


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ADD_TO_SIM_RELATIONSHIP_PANEL_INTERACTIONS)
class _CMSimControlMenuRelationshipPanelInteractionHandler(CommonInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int, ...] = (
            CMInteractionId.OPEN_SIM_CONTROL_MENU_FROM_REL_PANEL,
            CMInteractionId.OPEN_SIM_CONTROL_MENU_FROM_REL_PANEL_FROM_DEBUG
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: Sim, *_, **__) -> bool:
        return CommonTypeUtils.is_sim_or_sim_info(script_object)


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _CMObjectControlMenuInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int, ...] = (
            CMInteractionId.MANIPULATE_TO_PERFORM_INTERACTION,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return True


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_TERRAIN_LOAD)
class _CMDebugTerrainInteractionHandler(CommonInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int, ...] = (
            CMInteractionId.MANIPULATE_TO_PERFORM_INTERACTION,
        )
        return result


@CommonInstanceManagerModificationRegistry.register_modification_handler()
class _CMAddDebugInteractionsToAffordanceWhitelist(CommonAddInteractionsToAffordanceListsModificationHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interaction_ids(self) -> Tuple[CommonInt]:
        interaction_ids = [
            CMInteractionId.OPEN_SIM_CONTROL_MENU_FROM_DEBUG,
            CMInteractionId.OPEN_SIM_CONTROL_MENU_FROM_SIM,
            CMInteractionId.OPEN_SIM_CONTROL_MENU_FROM_REL_PANEL,
            CMInteractionId.OPEN_SIM_CONTROL_MENU_FROM_REL_PANEL_FROM_DEBUG,
            CMInteractionId.CHANGE_OUTFIT,
            CMInteractionId.CHANGE_OUTFIT_TO_NUDE,
            CMInteractionId.TELEPORT_CONTROLLED_SIM_TO_TARGET,
            CMInteractionId.TELEPORT_SIMS_TO_TARGET,
            CMInteractionId.SPAWN_SIMS_AT_TARGET,
            CMInteractionId.SUMMON_SIM_FROM_REL_PANEL,
            CMInteractionId.MANIPULATE_TO_PERFORM_INTERACTION,
        ]
        # noinspection PyTypeChecker
        return tuple(interaction_ids)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def affordance_list_ids(self) -> Tuple[int]:
        result: Tuple[int, ...] = (
            CommonAffordanceListId.DEBUG_AFFORDANCES,
        )
        return result
