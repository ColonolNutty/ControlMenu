"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union, Tuple, Any, Dict

from protocolbuffers.Localization_pb2 import LocalizedString
from relationships.relationship_bit import RelationshipBit
from relationships.relationship_track import RelationshipTrack
from relationships.tunable import BitTrackNode, _RelationshipTrackData2dLinkArrayElement
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sim_option_dialog import \
    CommonPremadeChooseSimOptionDialog
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4controlmenu.dialogs.modify_sim_data.enums.string_identifiers import S4CMSimControlMenuStringId
from sims4controlmenu.dialogs.modify_sim_data.single_sim_operation import S4CMSingleSimOperation


class S4CMRelationshipOption:
    """Used for displaying relationship options."""
    def __init__(self, display_name: LocalizedString, required_minimum: float):
        self.display_name = display_name
        self.required_minimum = required_minimum

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return '<{}: {}>'.format(self.display_name, self.required_minimum)


class S4CMSetRelationshipLevelOp(S4CMSingleSimOperation):
    """Set a relationship level between two Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    def _determine_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop) -> bool:
        def _on_chosen(chosen_sim_info: SimInfo) -> None:
            if chosen_sim_info is None:
                self.log.format_with_message('No Sim chosen.', sim=sim_info, chosen_sim=chosen_sim_info)
                on_completed(False)
                return
            self.run_with_sim(sim_info, chosen_sim_info, on_completed=on_completed)

        def _is_allowed(target_sim_info: SimInfo) -> bool:
            return self.can_run_with_sims(sim_info, target_sim_info)

        dialog = CommonPremadeChooseSimOptionDialog(
            S4CMSimControlMenuStringId.SET_RELATIONSHIP_WITH_WHO,
            0,
            title_tokens=(sim_info,),
            include_sim_callback=_is_allowed,
            instanced_sims_only=False,
            mod_identity=ModInfo.get_identity(),
            on_sim_chosen=_on_chosen,
            on_close=lambda: on_completed(False)
        )
        if not dialog.has_options():
            on_completed(False)
            return False
        # Sort the Sims in the dialog by their name.
        dialog._internal_dialog._rows = tuple(sorted(dialog._internal_dialog._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
        dialog.show(sim_info=sim_info)
        return True

    # noinspection PyMissingOrEmptyDocstring
    def can_run_with_sims(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        return super().can_run_with_sims(sim_info_a, sim_info_b) and sim_info_a is not sim_info_b and self._is_allowed_relationship_track(sim_info_a, sim_info_b)

    # noinspection PyMissingOrEmptyDocstring
    def run_with_sim(self, sim_info_a: SimInfo, sim_info_b: SimInfo, on_completed: Callable[[bool], None]=CommonFunctionUtils.noop):
        relationship_track_id = self._determine_relationship_track(sim_info_a, sim_info_b)
        if relationship_track_id == -1:
            self.log.format_with_message('No relationship track id found between Sims.', sim=sim_info_a, chosen_sim=sim_info_b)
            on_completed(False)
            return
        relationship_track = CommonResourceUtils.load_instance(Types.STATISTIC, relationship_track_id)
        if relationship_track is None:
            self.log.format_with_message('No relationship track found.', sim=sim_info_a, chosen_sim=sim_info_b)
            on_completed(False)
            return
        relationship_options = self._load_relationship_options(relationship_track)
        if not relationship_options:
            self.log.format_with_message('No relationship options found.', sim=sim_info_a, chosen_sim=sim_info_b)
            on_completed(False)
            return

        def _on_bit_chosen(_: Any, chosen_option: S4CMRelationshipOption):
            if _ is None or chosen_option is None:
                on_completed(False)
                return
            self.log.format_with_message('Chose relationship bit.', sim=sim_info_a, chosen_sim=sim_info_b, chosen_option=chosen_option, required_minimum=chosen_option.required_minimum)
            CommonRelationshipUtils.add_relationship_bit(sim_info_a, sim_info_b, CommonRelationshipBitId.HAS_MET)
            CommonRelationshipUtils.set_relationship_level_of_sims(sim_info_a, sim_info_b, relationship_track_id, chosen_option.required_minimum)
            on_completed(True)

        option_dialog = CommonChooseButtonOptionDialog(
            ModInfo.get_identity(),
            S4CMSimControlMenuStringId.CHOOSE_LEVEL,
            0,
            include_previous_button=True,
            on_previous=lambda: on_completed(False),
            on_close=lambda: on_completed(False)
        )
        for relationship_option in relationship_options:
            option_dialog.add_option(
                CommonDialogButtonOption(
                    relationship_option,
                    relationship_option,
                    CommonDialogResponseOptionContext(
                        relationship_option.display_name
                    ),
                    on_chosen=_on_bit_chosen
                )
            )

        if not option_dialog.has_options():
            on_completed(False)
            return

        option_dialog.show(sim_info=sim_info_a)

    def _load_relationship_options(self, relationship_track: RelationshipTrack) -> Tuple[S4CMRelationshipOption]:
        relationship_options: Dict[Any, S4CMRelationshipOption] = dict()
        for bit_set_item in relationship_track.bit_data.bit_set_list:
            if isinstance(bit_set_item, _RelationshipTrackData2dLinkArrayElement):
                for bit_set in bit_set_item.bit_set:
                    bit_set: BitTrackNode = bit_set
                    bit: RelationshipBit = bit_set.bit
                    # noinspection PyUnresolvedReferences
                    bit_display_name = bit.display_name
                    minimum_value = bit_set.add_value
                    relationship_options[bit_display_name] = S4CMRelationshipOption(bit_display_name, minimum_value)
            else:
                bit_set_item: BitTrackNode = bit_set_item
                bit: RelationshipBit = bit_set_item.bit
                # noinspection PyUnresolvedReferences
                bit_display_name = bit.display_name
                minimum_value = bit_set_item.add_value
                relationship_options[bit_display_name] = S4CMRelationshipOption(bit_display_name, minimum_value)
        if relationship_options:
            result: Tuple[S4CMRelationshipOption] = (
                S4CMRelationshipOption(S4CMSimControlMenuStringId.MAXIMUM, 100.0),
                S4CMRelationshipOption(S4CMSimControlMenuStringId.MINIMUM, -100.0),
                *relationship_options.values()
            )
            return result
        return tuple(relationship_options.values())

    def _is_allowed_relationship_track(self, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        return self._determine_relationship_track(sim_info_a, sim_info_b) != -1 and sim_info_a is not sim_info_b
