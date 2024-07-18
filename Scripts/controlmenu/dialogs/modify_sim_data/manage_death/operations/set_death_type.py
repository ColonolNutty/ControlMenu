"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

import services
from event_testing import test_events
from interactions.utils.death import DeathTracker
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.common_death_types import CommonDeathType
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_death_utils import CommonSimDeathUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CMSetDeathTypeOp(CMSingleSimOperation):
    """Revive ghost Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_death_type'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _on_close() -> None:
            on_completed(True)

        def _on_chosen(_: str, new_death_type: CommonDeathType):
            if new_death_type is None:
                _on_close()
                return
            self.log.format_with_message('Chose new death type', new_death_type=new_death_type)
            for (_death_type, _ghost_trait) in DeathTracker.DEATH_TYPE_GHOST_TRAIT_MAP.items():
                CommonTraitUtils.remove_trait(sim_info, _ghost_trait)
            death_tracker = CommonSimDeathUtils.get_death_tracker(sim_info)
            vanilla_death_type = CommonDeathType.convert_to_vanilla(new_death_type)
            ghost_trait = DeathTracker.DEATH_TYPE_GHOST_TRAIT_MAP.get(vanilla_death_type)
            if ghost_trait is not None:
                CommonTraitUtils.add_trait(sim_info, ghost_trait)
            death_tracker._death_type = vanilla_death_type
            sim_info.resend_death_type()
            services.get_event_manager().process_event(test_events.TestEvent.SimDeathTypeSet, sim_info=sim_info)
            _on_close()

        current_death_type = CommonSimDeathUtils.get_death_type(sim_info)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimControlMenuStringId.SET_DEATH_TYPE_NAME,
            CMSimControlMenuStringId.SET_DEATH_TYPE_DESCRIPTION,
            description_tokens=(current_death_type.name,),
            on_close=_on_close,
            mod_identity=self.mod_identity,
        )

        for death_type in CommonDeathType.values:
            title = death_type.name
            icon = CommonIconUtils.load_unfilled_circle_icon()
            if death_type == current_death_type:
                title = CommonLocalizationUtils.create_localized_string(title, text_color=CommonLocalizedStringColor.GREEN)
                icon = CommonIconUtils.load_filled_circle_icon()

            option_dialog.add_option(
                CommonDialogSelectOption(
                    death_type.name,
                    death_type,
                    CommonDialogOptionContext(
                        title,
                        0,
                        is_selected=death_type == current_death_type,
                        is_enabled=death_type != current_death_type,
                        icon=icon
                    ),
                    on_chosen=_on_chosen
                )
            )

        if not option_dialog.has_options():
            on_completed(False)
            return True

        option_dialog.show(
            sim_info=sim_info
        )
        return True
