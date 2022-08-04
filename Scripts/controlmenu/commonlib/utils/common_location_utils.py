"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services


class CMCommonLocationUtils:
    """Utilities for location. """
    @classmethod
    def set_maximum_sims_per_lot(cls, max_sims_count: int) -> None:
        """set_maximum_sims_per_lot(max_sims_count)

        Override the maximum number of Sims allowed on a lot at one time.

        :param max_sims_count: The maximum number of Sims to be allowed on a lot at one time.
        :type max_sims_count: int
        """
        sim_spawner_service = services.sim_spawner_service()
        sim_spawner_service.set_npc_soft_cap_override(max_sims_count)
        services.get_object_routing_service().set_object_routing_soft_cap_debug_override(max_sims_count)
        services.get_object_routing_service().set_object_routing_hard_cap_debug_override(max_sims_count)

    @classmethod
    def clear_lot_capacity_overrides(cls) -> None:
        """clear_lot_capacity_overrides(max_sims_count)

        Clear any changes to lot capacity.
        """
        sim_spawner_service = services.sim_spawner_service()
        sim_spawner_service.set_npc_soft_cap_override(None)
        object_routing_service = services.get_object_routing_service()
        object_routing_service.set_object_routing_soft_cap_debug_override(None)
        object_routing_service.set_object_routing_hard_cap_debug_override(None)
        object_routing_service.set_object_routing_soft_cap_threshold_debug_override(None)
