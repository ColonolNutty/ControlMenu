"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from controlmenu.dialogs.modify_sim_data.modify_motives.enums.string_ids import CMSimModifyMotivesStringId
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4.localization import LocalizationHelperTuning
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.common_statistic_category import CommonStatisticCategory
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_motive_utils import CommonSimMotiveUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from statistics.commodity_tracker import CommodityTracker


class CMModifyMotivesSimOp(CMSingleSimOperation):
    """Modify Motives of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_modify_motives_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimModifyMotivesStringId.MODIFY_MOTIVES,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_input_setting_changed(_motive_id: int, new_level: float, outcome: CommonChoiceOutcome):
            if new_level is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen()
                return
            self.log.format_with_message('Setting motive level for Sim.', _motive_id=_motive_id, new_level=new_level)
            self.modify_motive(_motive_id, sim_info, new_level)
            _reopen()

        sim = CommonSimUtils.get_sim_instance(sim_info)
        commodity_tracker: CommodityTracker = sim_info.commodity_tracker
        added_motive_ids = list()
        for commodity in commodity_tracker.get_all_commodities():
            categories = set(commodity.get_categories()) & {CommonStatisticCategory.MOTIVE_COMMODITIES}
            if not categories:
                continue
            motive_id = getattr(commodity, 'guid64', None)
            if motive_id is None or motive_id in added_motive_ids:
                continue
            try:
                self.verbose_log.format_with_message('Attempting to display motive', motive=commodity, motive_id=motive_id, sim=sim_info)

                current_motive_level = CommonSimMotiveUtils.get_motive_level(sim_info, motive_id)
                stat_name = getattr(commodity, 'stat_name', None)
                # noinspection PyUnresolvedReferences
                if stat_name and commodity.stat_name.hash is not 0:
                    # noinspection PyUnresolvedReferences
                    display_name = commodity.stat_name
                else:
                    motive_name = (hasattr(commodity, '__name__') and commodity.__name__) or (hasattr(commodity, '__class__') and hasattr(commodity.__class__, '__name__') and commodity.__class__.__name__) or str(commodity)
                    motive_name = motive_name[0].upper() + motive_name[1:]
                    display_name = LocalizationHelperTuning.get_raw_text(motive_name)

                if hasattr(commodity, 'stat_name_overrides'):
                    stat_name_overrides = commodity.stat_name_overrides
                    if stat_name_overrides is not None:
                        for (trait, override_display_name) in stat_name_overrides.items():
                            if CommonTraitUtils.has_trait(sim_info, trait):
                                display_name = override_display_name
                                break

                if commodity.commodity_states:
                    current_state = commodity.get_current_state_info()
                    if current_state is None:
                        self.verbose_log.format_with_message(f'Failed, no current state for motive {commodity}')
                        continue
                else:
                    current_state = None
                try:
                    state_name = current_state.ui_name
                    if state_name is not None:
                        display_name = LocalizationHelperTuning.get_name_value_pair(commodity.stat_name, state_name)
                except:
                    pass

                if not commodity.visible:
                    display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_SPACE_PAREN_STRING, tokens=(display_name, CMSimControlMenuStringId.HIDDEN))

                display_name = CommonLocalizationUtils.create_localized_string(CMSimControlMenuStringId.STRING_COLON_SPACE_STRING, tokens=(display_name, str(current_motive_level)))
                if current_state is not None:
                    description = current_state.data_description

                    if hasattr(current_state, '_data_description_overrides')\
                            and hasattr(current_state, 'data_description_overrides')\
                            and current_state.data_description_overrides:
                        for data_override in current_state.data_description_overrides:
                            trait = data_override.key
                            override_description = data_override.value
                            if CommonTraitUtils.has_trait(sim_info, trait):
                                description = override_description
                                break

                    icon = current_state.icon or CommonIconUtils.load_question_mark_icon()
                    self.log.enable()
                    self.log.format_with_message('Got other things', description=description, description_dir=dir(description))
                    self.log.disable()
                    description = description.hash
                else:
                    description = 0
                    icon = CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                option_dialog.add_option(
                    CommonDialogInputFloatOption(
                        motive_id,
                        current_motive_level,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            description_tokens=(sim_info,),
                            icon=icon
                        ),
                        dialog_description_identifier=CMSimModifyMotivesStringId.ENTER_A_VALUE_BETWEEN_MIN_AND_MAX_FOR_MOTIVE,
                        dialog_description_tokens=(str(commodity.min_value), str(commodity.max_value), str(current_motive_level)),
                        min_value=commodity.min_value,
                        max_value=int(commodity.max_value),
                        on_chosen=_on_input_setting_changed
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display motive.', motive=commodity, motive_name=(hasattr(commodity, '__name__') and commodity.__name__) or (hasattr(commodity, '__class__') and hasattr(commodity.__class__, '__name__') and commodity.__class__.__name__) or 'Unknown Motive Name', motive_id=motive_id, exception=ex)

        if not option_dialog.has_options():
            self.log.format_with_message('No motives available for the Sim!')
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    def modify_motive(self, motive_id: int, sim_info: SimInfo, new_value: float):
        """modify_motive(motive_id, sim_info, new_value)

        Sets a motive to a new value.

        .. note:: This function is useful for mods that manage their own stat values. This way they are informed of a change to the motive.

        :param motive_id:
        :param sim_info:
        :param new_value:
        """
        CommonSimMotiveUtils.set_motive_level(sim_info, motive_id, new_value)
