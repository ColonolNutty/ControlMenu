from typing import Tuple

import services
from event_testing.resolver import SingleSimResolver
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.motives_enum import CommonMotiveId
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_motive_utils import CommonSimMotiveUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
import id_generator


class S4CMBecomeVampireOp:
    """Turn a Sim into a Vampire."""
    def run(self, sim_info: SimInfo) -> bool:
        """Run the operation."""
        if CommonOccultUtils.is_vampire(sim_info):
            return False
        # Buff_VampireCreation_StrangeThirst
        strange_thirst_buff = 149536
        # (From Becoming a Vampire)
        strange_thirst_buff_reason = 2119589990
        CommonBuffUtils.add_buff(sim_info, strange_thirst_buff, buff_reason=strange_thirst_buff_reason)
        CommonTraitUtils.add_trait(sim_info, CommonTraitId.OCCULT_VAMPIRE)
        CommonSimMotiveUtils.set_motive_level(sim_info, CommonMotiveId.VAMPIRE_THIRST, 0.0)
        CommonSimStatisticUtils.remove_statistic(sim_info, CommonStatisticId.BECOMING_VAMPIRE)
        # dialogDramaNode_IntroToVampire_Call1
        drama_node_id = 154434
        drama_node = CommonResourceUtils.load_instance(Types.DRAMA_NODE, drama_node_id)
        if drama_node is not None:
            uid = id_generator.generate_object_id()
            drama_node_instance = drama_node(uid)
            services.drama_scheduler_service().schedule_node(drama_node, SingleSimResolver(sim_info), specific_time=drama_node_instance.get_picker_schedule_time(), drama_inst=drama_node_instance)
        buffs_to_remove: Tuple[int] = (
            CommonBuffId.PLANT_SIMS_MAIN_VISIBLE,
            CommonBuffId.PLANT_SIMS_MAIN_VISIBLE_NPC,
            CommonBuffId.SPRING_CHALLENGE_PLANT_SIMS_NPC_ANGRY,
            CommonBuffId.SPRING_CHALLENGE_PLANT_SIMS_NPC_FLIRTY,
            CommonBuffId.SPRING_CHALLENGE_PLANT_SIMS_NPC_PLAYFUL,
            CommonBuffId.SPRING_CHALLENGE_PLANT_SIMS_NPC_SAD,
            CommonBuffId.SPRING_CHALLENGE_PLANT_SIMS_NPC_UNCOMFORTABLE,
            CommonBuffId.SPRING_CHALLENGE_PLANT_SIMS_NPC_BEANS_GIVEN,
            CommonBuffId.PLANT_SIMS_MOOD_AURAS_ANGRY,
            CommonBuffId.PLANT_SIMS_MOOD_AURAS_CONFIDENT,
            CommonBuffId.PLANT_SIMS_MOOD_AURAS_FLIRTY,
            CommonBuffId.PLANT_SIMS_MOOD_AURAS_PLAYFUL,
            CommonBuffId.PLANT_SIMS_MOOD_AURAS_SAD,
            CommonBuffId.PLANT_SIMS_MOOD_AURAS_UNCOMFORTABLE,
        )
        CommonBuffUtils.remove_buff(sim_info, *buffs_to_remove)
        CommonTraitUtils.remove_trait(sim_info, (
            CommonTraitId.IS_PLANT_SIM_NPC
        ))
        return True
