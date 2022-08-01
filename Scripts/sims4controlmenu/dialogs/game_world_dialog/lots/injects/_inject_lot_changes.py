"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from sims4controlmenu.commonlib.utils.common_location_utils import S4CMCommonLocationUtils
from sims4controlmenu.dialogs.game_world_dialog.lots.operations.set_maximum_sims_per_lot import S4CMSetMaximumSimsPerLotOp
from sims4controlmenu.modinfo import ModInfo
from sims4controlmenu.settings.setting_utils import S4CMSettingUtils


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cm_set_sim_cap_on_zone_late_load(event_data: S4CLZoneEarlyLoadEvent):
    if S4CMSetMaximumSimsPerLotOp._DEFAULT_NPC_PER_LOT_COUNT is None:
        from sims.sim_spawner_service import SimSpawnerService
        S4CMSetMaximumSimsPerLotOp._DEFAULT_NPC_PER_LOT_COUNT = SimSpawnerService.NPC_SOFT_CAP
        from services.object_routing_service import ObjectRoutingService
        S4CMSetMaximumSimsPerLotOp._DEFAULT_OBJECT_ROUTING_HARD_CAP = ObjectRoutingService.OBJECT_ROUTING_HARD_CAP
    maximum_sims_per_lot = S4CMSettingUtils.get_maximum_number_of_sims_per_lot()
    S4CMCommonLocationUtils.set_maximum_sims_per_lot(maximum_sims_per_lot)
