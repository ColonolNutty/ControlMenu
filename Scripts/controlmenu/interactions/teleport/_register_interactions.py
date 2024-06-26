"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from objects.script_object import ScriptObject
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonInteractionHandler, CommonScriptObjectInteractionHandler
from controlmenu.enums.interaction_identifiers import CMInteractionId
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_TERRAIN_LOAD)
class _CMTeleportTerrainInteractionHandler(CommonInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int, ...] = (
            CMInteractionId.TELEPORT_CONTROLLED_SIM_TO_TARGET,
            CMInteractionId.TELEPORT_SIMS_TO_TARGET,
        )
        return result


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _CMTeleportObjectControlMenuInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int, ...] = (
            CMInteractionId.TELEPORT_TARGET_TO_CONTROLLED_SIM,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return not CommonTypeUtils.is_sim_or_sim_info(script_object)
