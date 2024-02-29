"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from controlmenu.enums.trait_ids import CMTraitId
from controlmenu.modinfo import ModInfo


class _CMAutoApplyTraits:
    """ Auto apply traits. """

    def _try_apply_traits(self, sim_info: SimInfo):
        if not CommonTraitUtils.has_trait(sim_info, CMTraitId.CONTROL_MENU_MAIN):
            CommonTraitUtils.add_trait(sim_info, CMTraitId.CONTROL_MENU_MAIN)
        if CommonSpeciesUtils.is_human(sim_info):
            CommonTraitUtils.remove_traits(
                sim_info,
                (
                    CMTraitId.CONTROLLABLE_LARGE_DOG_SIM,
                    CMTraitId.CONTROLLABLE_SMALL_DOG_SIM,
                    CMTraitId.CONTROLLABLE_CAT_SIM,
                    CMTraitId.CONTROLLABLE_FOX_SIM,
                    CMTraitId.CONTROLLABLE_HORSE_SIM
                )
            )
            if CommonTraitUtils.has_trait(sim_info, CMTraitId.CONTROLLABLE_HUMAN_SIM):
                return
            CommonTraitUtils.add_trait(sim_info, CMTraitId.CONTROLLABLE_HUMAN_SIM)
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            CommonTraitUtils.remove_traits(
                sim_info,
                (
                    CMTraitId.CONTROLLABLE_HUMAN_SIM,
                    CMTraitId.CONTROLLABLE_SMALL_DOG_SIM,
                    CMTraitId.CONTROLLABLE_CAT_SIM,
                    CMTraitId.CONTROLLABLE_FOX_SIM,
                    CMTraitId.CONTROLLABLE_HORSE_SIM
                )
            )
            if CommonTraitUtils.has_trait(sim_info, CMTraitId.CONTROLLABLE_LARGE_DOG_SIM):
                return
            CommonTraitUtils.add_trait(sim_info, CMTraitId.CONTROLLABLE_LARGE_DOG_SIM)
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            CommonTraitUtils.remove_traits(
                sim_info,
                (
                    CMTraitId.CONTROLLABLE_HUMAN_SIM,
                    CMTraitId.CONTROLLABLE_LARGE_DOG_SIM,
                    CMTraitId.CONTROLLABLE_CAT_SIM,
                    CMTraitId.CONTROLLABLE_FOX_SIM,
                    CMTraitId.CONTROLLABLE_HORSE_SIM
                )
            )
            if CommonTraitUtils.has_trait(sim_info, CMTraitId.CONTROLLABLE_SMALL_DOG_SIM):
                return
            CommonTraitUtils.add_trait(sim_info, CMTraitId.CONTROLLABLE_SMALL_DOG_SIM)
        elif CommonSpeciesUtils.is_cat(sim_info):
            CommonTraitUtils.remove_traits(
                sim_info,
                (
                    CMTraitId.CONTROLLABLE_HUMAN_SIM,
                    CMTraitId.CONTROLLABLE_LARGE_DOG_SIM,
                    CMTraitId.CONTROLLABLE_SMALL_DOG_SIM,
                    CMTraitId.CONTROLLABLE_FOX_SIM,
                    CMTraitId.CONTROLLABLE_HORSE_SIM
                )
            )
            if CommonTraitUtils.has_trait(sim_info, CMTraitId.CONTROLLABLE_CAT_SIM):
                return
            CommonTraitUtils.add_trait(sim_info, CMTraitId.CONTROLLABLE_CAT_SIM)
        elif CommonSpeciesUtils.is_fox(sim_info):
            CommonTraitUtils.remove_traits(
                sim_info,
                (
                    CMTraitId.CONTROLLABLE_HUMAN_SIM,
                    CMTraitId.CONTROLLABLE_LARGE_DOG_SIM,
                    CMTraitId.CONTROLLABLE_SMALL_DOG_SIM,
                    CMTraitId.CONTROLLABLE_CAT_SIM,
                    CMTraitId.CONTROLLABLE_HORSE_SIM
                )
            )
            if CommonTraitUtils.has_trait(sim_info, CMTraitId.CONTROLLABLE_FOX_SIM):
                return
            CommonTraitUtils.add_trait(sim_info, CMTraitId.CONTROLLABLE_FOX_SIM)
        elif CommonSpeciesUtils.is_horse(sim_info):
            CommonTraitUtils.remove_traits(
                sim_info,
                (
                    CMTraitId.CONTROLLABLE_HUMAN_SIM,
                    CMTraitId.CONTROLLABLE_LARGE_DOG_SIM,
                    CMTraitId.CONTROLLABLE_SMALL_DOG_SIM,
                    CMTraitId.CONTROLLABLE_CAT_SIM,
                    CMTraitId.CONTROLLABLE_FOX_SIM
                )
            )
            if CommonTraitUtils.has_trait(sim_info, CMTraitId.CONTROLLABLE_HORSE_SIM):
                return
            CommonTraitUtils.add_trait(sim_info, CMTraitId.CONTROLLABLE_HORSE_SIM)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cm_auto_apply_traits_on_sim_spawned(event_data: S4CLSimSpawnedEvent):
    sim_info = event_data.sim_info
    _CMAutoApplyTraits()._try_apply_traits(sim_info)
