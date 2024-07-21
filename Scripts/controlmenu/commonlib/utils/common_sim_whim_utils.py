"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Dict, Tuple, Union

from controlmenu.commonlib.utils.common_whim_utils import CMCommonWhimUtils
from distributor.shared_messages import IconInfoData
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from whims.whim import Whim
from whims.whims_tracker import WhimsTracker, WhimType, TelemetryWhimEvents


class CMCommonSimWhimUtils(_HasS4CLClassLog):
    """Utilities for manipulating whims on Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_whim_utils'

    @classmethod
    def has_whim(cls, sim_info: SimInfo, whim: Union[int, Whim]) -> bool:
        """has_whim(sim_info, whim)

        Determine if a Sim has a Whim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param whim: The whim to check for.
        :type whim: Union[int, Whim]
        :return: True, if the Sim has the specified Whim. False, if not.
        :rtype: bool
        """
        whim_instance = CMCommonWhimUtils.load_whim_by_guid(whim)
        if whim_instance is None:
            return False
        whim_tracker = cls.get_whim_tracker(sim_info)
        return whim_tracker.is_whim_active(whim_instance)

    @classmethod
    def remove_whim(cls, sim_info: SimInfo, whim: Union[int, Whim]) -> CommonExecutionResult:
        """remove_whim(sim_info, whim)

        Remove a Whim from a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param whim: The whim to check for.
        :type whim: Union[int, Whim]
        """
        whim_instance = CMCommonWhimUtils.load_whim_by_guid(whim)
        if whim_instance is None:
            return CommonExecutionResult(False, reason=f'Whim not found by Guid {whim}')
        whim_tracker = cls.get_whim_tracker(sim_info)
        if whim_tracker is None:
            return CommonExecutionResult(False, reason=f'Target Sim {sim_info} did not have a Whim Tracker.')
        needs_update = False
        for whim_slot in cls.get_whim_slots(sim_info):
            if whim_slot.whim is whim_instance:
                whim_slot.clear(telemetry_event=TelemetryWhimEvents.CHEAT_CLEAR)
                needs_update = True
        if needs_update:
            whim_tracker._send_goals_update()
        return CommonExecutionResult.TRUE

    @classmethod
    def remove_whim_by_type(cls, sim_info: SimInfo, whim_type: WhimType) -> CommonExecutionResult:
        """remove_whim_by_type(sim_info, whim_type)

        Remove a Whim from a Sim by type.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param whim_type: The type of whim to remove.
        :type whim_type: WhimType
        """
        whim_tracker = cls.get_whim_tracker(sim_info)
        if whim_tracker is None:
            return CommonExecutionResult(False, reason=f'Target Sim {sim_info} did not have a Whim Tracker.')
        needs_update = False
        for whim_slot in cls.get_whim_slots(sim_info):
            if whim_slot.whim_type == whim_type:
                whim_slot.clear(telemetry_event=TelemetryWhimEvents.CHEAT_CLEAR)
                needs_update = True
                break
        if needs_update:
            whim_tracker._send_goals_update()
        return CommonExecutionResult.TRUE

    @classmethod
    def get_whims(cls, sim_info: SimInfo) -> Dict[WhimType, Whim]:
        """get_whims(sim_info)

        Retrieve Whims a Sim currently has active.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The current Whims on a Sim by Whim Type.
        :rtype: Dict[WhimType, Whim]
        """
        whims = dict()
        whim_tracker = cls.get_whim_tracker(sim_info)
        for whim_slot in whim_tracker._whim_slots:
            whim_type = whim_slot.whim_type
            if whim_slot.is_empty():
                whims[whim_type] = None
                continue
            whim = whim_slot.whim
            whims[whim_type] = whim
        return whims

    @classmethod
    def get_whim_slots(cls, sim_info: SimInfo) -> Tuple[WhimsTracker.WhimSlotData]:
        """get_whim_slots(sim_info)

        Retrieve the Whim slots of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The whim slots.
        :rtype: Tuple[WhimsTracker.WhimSlotData]
        """
        whim_tracker = cls.get_whim_tracker(sim_info)
        return tuple(whim_tracker._whim_slots)

    @classmethod
    def get_whim_tracker(cls, sim_info: SimInfo) -> WhimsTracker:
        """get_whim_tracker(sim_info)

        Retrieve the Tracker for Whims of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The Tracker for Whims of a Sim.
        :rtype: WhimsTracker
        """
        return sim_info.whim_tracker


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_whim',
    'Remove a whim from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('whim', 'Whim Id or Tuning Name', 'The decimal identifier or Tuning Name of the Whim to remove.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to remove the whim from.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.removewhim',
    )
)
def _common_remove_whim(output: CommonConsoleCommandOutput, whim: TunableInstanceParam(Types.WHIM), sim_info: SimInfo = None):
    if whim is None:
        return
    if sim_info is None:
        return
    output(f'Removing whim {whim} from Sim {sim_info}')
    result = CMCommonSimWhimUtils.remove_whim(sim_info, whim)
    if result:
        output(f'SUCCESS: Successfully removed whim {whim} from Sim {sim_info}: {result.reason}')
    else:
        output(f'FAILED: Failed to remove whim {whim} from Sim {sim_info}: {result.reason}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_whims',
    'Print a list of all whims on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to use.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printwhims',
    )
)
def _common_print_whims_on_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    log = CMCommonSimWhimUtils.get_log()
    try:
        log.enable()
        output(f'Attempting to print whims on Sim {sim_info}')
        whim_strings: List[str] = list()
        for (whim_type, whim) in CMCommonSimWhimUtils.get_whims(sim_info).items():
            whim_name = CMCommonWhimUtils.get_whim_name(whim)
            whim_id = CMCommonWhimUtils.get_whim_guid(whim)
            whim_strings.append(f'{whim_name} ({whim_id})')

        whim_strings = sorted(whim_strings, key=lambda x: x)
        sim_whims = ', '.join(whim_strings)
        text = ''
        text += f'Whims:\n{sim_whims}\n\n'
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        log.debug(f'{sim_info} Whims ({sim_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{sim_info} Whims ({sim_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info))
        )
    finally:
        log.disable()
