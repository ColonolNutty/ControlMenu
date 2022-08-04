"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.collections import make_immutable_slots_class
from sims4.resources import Types
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_run import S4CLInteractionRunEvent
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.objects.common_object_state_utils import CommonObjectStateUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from controlmenu.modinfo import ModInfo


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cm_add_replace_water_interaction_with_clothes(event_data: S4CLZoneEarlyLoadEvent):
    if event_data.game_loaded:
        return True
    # laundry_WashTub_Values_Functions_Washing
    object_state_value = CommonObjectStateUtils.load_object_state_value_by_id(176817)
    if object_state_value is not None:
        # laundry_WashTub_Change_Water
        change_water_interaction = CommonInteractionUtils.load_interaction_by_id(176807)
        if change_water_interaction is not None and change_water_interaction not in object_state_value.super_affordances:
            object_state_value.super_affordances = (
                *object_state_value.super_affordances,
                change_water_interaction
            )
    # laundry_WashTub_WashClothes_Resume
    resume_laundry_interaction = CommonInteractionUtils.load_interaction_by_id(178682)
    if resume_laundry_interaction is not None:
        resume_laundry_interaction.allow_autonomous = True
        static_commodities = list(resume_laundry_interaction._static_commodities)
        static_commodities_immutable_class = make_immutable_slots_class(['desire', 'static_commodity'])
        tidy_commodity = CommonResourceUtils.load_instance(Types.STATIC_COMMODITY, 16440)
        new_static_commodity = {
            'desire': 1.0,
            'static_commodity': tidy_commodity
        }
        static_commodities.append(static_commodities_immutable_class(new_static_commodity))
        resume_laundry_interaction._static_commodities = tuple(static_commodities)
    return True


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cm_set_washtub_to_incomplete_state_upon_replace_water(event_data: S4CLInteractionRunEvent):
    # TODO: Add a do command to the interaction instead
    # Alternatively, update this to add a Loot Action to the interaction.
    interaction_id = CommonInteractionUtils.get_interaction_id(event_data.interaction)
    # laundry_WashTub_Change_Water
    if interaction_id != 176807:
        return True
    washtub = event_data.interaction.target
    # laundry_WashTub_Values_Functions_Washing
    if CommonObjectStateUtils.is_object_in_state(washtub, 176817):
        # laundry_WashTub_Load_Progress_Values_Incomplete
        CommonObjectStateUtils.set_object_state(washtub, 179511)
        # If the washtub has clothes in it when we replace its water, we want to ensure the clothes can be washed afterwards.
    return True
