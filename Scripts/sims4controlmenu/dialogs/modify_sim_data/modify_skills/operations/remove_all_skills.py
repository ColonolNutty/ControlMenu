"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any

from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4controlmenu.dialogs.modify_sim_data.modify_skills.enums.string_ids import S4CMSimModifySkillsStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation
from sims4controlmenu.enums.string_identifiers import S4CMStringId
from statistics.skill import Skill


class S4CMRemoveAllSkillsSimOp(S4CMSingleSimOperation):
    """Remove All Skills from a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cm_remove_all_skills_of_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_close() -> None:
            on_completed(False)

        def _on_yes_selected(_: Any):
            skill_manager = CommonResourceUtils.get_instance_manager(Types.STATISTIC)
            sim = CommonSimUtils.get_sim_instance(sim_info)
            for skill in skill_manager.get_ordered_types(only_subclasses_of=Skill):
                skill: Skill = skill
                if not CommonSimSkillUtils.has_skill(sim_info, skill):
                    continue
                CommonSimSkillUtils.remove_skill(sim_info, skill)

            CommonBasicNotification(
                S4CMSimModifySkillsStringId.REMOVED_ALL_SKILLS_TITLE,
                S4CMSimModifySkillsStringId.REMOVED_ALL_SKILLS_DESCRIPTION,
                title_tokens=(sim,),
                description_tokens=(sim,)
            ).show(icon=IconInfoData(obj_instance=sim))
            _on_close()

        def _on_no_selected(_: Any):
            _on_close()

        confirmation = CommonOkCancelDialog(
            S4CMStringId.CONFIRMATION,
            S4CMSimModifySkillsStringId.ARE_YOU_SURE_YOU_WANT_TO_REMOVE_ALL_SKILLS_FROM_SIM,
            description_tokens=(CommonSimUtils.get_sim_instance(sim_info),),
            ok_text_identifier=S4CMStringId.YES,
            cancel_text_identifier=S4CMStringId.NO,
            mod_identity=self.mod_identity
        )
        confirmation.show(on_ok_selected=_on_yes_selected, on_cancel_selected=_on_no_selected)
        return True
