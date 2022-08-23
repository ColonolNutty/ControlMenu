"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, Iterator, Any

from controlmenu.logging.has_cm_class_log import HasCMClassLog
from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.utils.success_chance import SuccessChance
from sims4.resources import Types
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from ui.ui_dialog import CommandArgType


class CommonCommandArgumentType(CommonInt):
    """Argument types for commands."""
    PARTICIPANT = ...
    BOOL = ...
    STRING = ...
    FLOAT = ...
    INT = ...

    @classmethod
    def convert_to_vanilla(cls, value: 'CommonCommandArgumentType') -> CommandArgType:
        """convert_to_vanilla(value)

        Convert a value into the vanilla equivalent.

        :param value: An instance of CommonCommandArgumentType
        :type value: CommonCommandArgumentType
        :return: The specified CommonCommandArgumentType translated to CommandArgType or CommandArgType.ARG_TYPE_BOOL, if the value could not be translated.
        :rtype: CommandArgType
        """
        if isinstance(value, CommandArgType):
            return value

        mapping = {
            CommonCommandArgumentType.PARTICIPANT: CommandArgType.ARG_TYPE_BOOL,
            CommonCommandArgumentType.BOOL: CommandArgType.ARG_TYPE_BOOL,
            CommonCommandArgumentType.STRING: CommandArgType.ARG_TYPE_STRING,
            CommonCommandArgumentType.FLOAT: CommandArgType.ARG_TYPE_FLOAT,
            CommonCommandArgumentType.INT: CommandArgType.ARG_TYPE_INT,
        }
        return mapping.get(value, CommandArgType.ARG_TYPE_BOOL)


class CommonStaticCommodityDesireData:
    """
        Data about a static commodity and the desire level for a Sim to do it.
    """
    def __init__(self, static_commodity_identifier: int, desire: float = 1.0):
        self.static_commodity_identifier = static_commodity_identifier
        self.desire = desire


class CommonCommandArgumentData:
    """An argument for a command."""
    def __init__(self, argument_type: CommonCommandArgumentType, argument_value: Any) -> None:
        self.argument_type = argument_type
        self.argument_value = argument_value

    def to_tuning(self) -> Any:
        """Create a tuning out of the data."""
        from sims4.collections import make_immutable_slots_class
        arguments_one_data = dict()
        arguments_one_data.update({'arg_type': CommonCommandArgumentType.convert_to_vanilla(self.argument_type)})
        arguments_one_data.update({'argument': self.argument_value})
        argument_one_slots = {'arg_type', 'argument'}
        arguments_one_immutable_class = make_immutable_slots_class(argument_one_slots)
        return arguments_one_immutable_class(arguments_one_data)


class CommonCommandParticipantArgumentData(CommonCommandArgumentData):
    """An argument for a command."""
    def __init__(self, argument_value: ParticipantType) -> None:
        super().__init__(CommonCommandArgumentType.PARTICIPANT, argument_value)


class CommonCommandStringArgumentData(CommonCommandArgumentData):
    """An argument for a command."""
    def __init__(self, argument_value: str) -> None:
        super().__init__(CommonCommandArgumentType.STRING, argument_value)


class CommonCommandIntArgumentData(CommonCommandArgumentData):
    """An argument for a command."""
    def __init__(self, argument_value: int) -> None:
        super().__init__(CommonCommandArgumentType.INT, argument_value)


class CommonCommandFloatArgumentData(CommonCommandArgumentData):
    """An argument for a command."""
    def __init__(self, argument_value: float) -> None:
        super().__init__(CommonCommandArgumentType.FLOAT, argument_value)


class CommonInteractionBasicExtrasTiming(CommonInt):
    """Timing for a basic extras to run at."""
    AT_BEGINNING = ...
    AT_END = ...
    # ON_XEVT = ...


class CMCommonInteractionUtils(HasCMClassLog):
    """Utils."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_common_interaction_utils'

    @classmethod
    def add_static_commodities_to_interaction(cls, interactions: Iterator[Union[int, Interaction]], static_commodities: Iterator[CommonStaticCommodityDesireData]):
        """add_static_commodities_to_interaction(interactions, static_commodities)

        Add static commodities to interactions.

        :param interactions: The interactions to modify.
        :type interactions: Iterator[Union[int, Interaction]]
        :param static_commodities: The static commodities to add.
        :type static_commodities: Iterator[CommonStaticCommodityDesireData]
        """
        if not interactions:
            raise AssertionError('Attempted to add Static Commodities without specifying Interactions to modify.')
        if not static_commodities:
            raise AssertionError('Attempted to add Static Commodities without specifying Static Commodities to add!')
        from sims4.collections import make_immutable_slots_class
        for interaction in interactions:
            interaction_instance = CommonInteractionUtils.load_interaction_by_id(interaction)
            if interaction_instance is None:
                continue
            new_static_commodities = list(interaction_instance._static_commodities)
            static_commodities_immutable_class = make_immutable_slots_class(['desire', 'static_commodity'])
            for static_commodity in static_commodities:
                static_commodity_instance = CommonResourceUtils.load_instance(Types.STATIC_COMMODITY, static_commodity.static_commodity_identifier)
                if static_commodity_instance is None:
                    continue
                new_static_commodity = {
                    'desire': static_commodity.desire,
                    'static_commodity': static_commodity_instance
                }
                new_static_commodities.append(static_commodities_immutable_class(new_static_commodity))
            interaction_instance._static_commodities = tuple(new_static_commodities)

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def add_do_command_to_interactions(
        cls,
        interactions: Iterator[int],
        command_name: str,
        command_arguments: Iterator[CommonCommandArgumentData] = tuple(),
        timing: CommonInteractionBasicExtrasTiming = CommonInteractionBasicExtrasTiming.AT_END,
        # offset_time: Union[None, float] = None,
        # xevt_id: Union[None, int] = None
    ):
        """add_do_command_to_interactions(\
            interactions,\
            command_name,\
            command_arguments=tuple(),\
            timing=CommonInteractionBasicExtrasTiming.AT_END,\
        )

        Add a Do Command Basic Extras variant to interactions.

        :param interactions: A collection of interactions to modify.
        :type interactions: Iterator[int]
        :param command_name: Create a local `@Command(command, command_type=CommandType.Live)` method
        :param command_arguments: A collection of arguments to pass to the command upon it being invoked. Default is no arguments.
        :type command_arguments: Iterator[CommonCommandArgumentData], optional
        :param timing: When the command should be invoked. Default is at the End of the interaction.
        :type timing: CommonInteractionBasicExtrasTiming, optional
        """
        # :param parameter: The 1st argument. The 2nd argument will be 'ParticipantType.Actor'
        # :param offset_time: valid for 'at_beginning', it is recommended to use 'on_xevt' instead.
        # :param xevt_id:
        cls.get_log().format_with_message('add_do_command', interaction_ids=interactions, command_name=command_name, timing=timing)
        for interaction in interactions:
            interaction_instance = CommonInteractionUtils.load_interaction_by_id(interaction)
            if interaction_instance is None:
                continue
            cls.get_log().format_with_message('Processing', interaction_instance=interaction_instance, interaction=interaction)
            new_basic_extra = cls._create_do_command_basic_extras(command_name, command_arguments=command_arguments, timing=timing)
            new_basic_extras: Tuple = (new_basic_extra, )
            cls.get_log().format_with_message('New basic extras', new_basic_extra=new_basic_extra, tuned_values_attr=getattr(new_basic_extra, '_tuned_values', None))

            if getattr(interaction_instance, 'basic_extras', None):
                def _has_argument(_argument_value: str) -> bool:
                    for command_argument in command_arguments:
                        if command_argument.argument_value == _argument_value:
                            return True
                    return False

                cls.get_log().format_with_message('Got basic extras', basic_extras=interaction_instance.basic_extras)
                # Add the new command to 'basic_extras'
                for basic_extra in getattr(interaction_instance, 'basic_extras'):
                    if getattr(basic_extra, 'command', None) == command_name and _has_argument(getattr(basic_extra, 'argument', None)):
                        cls.get_log().format_with_message('Tuning already contains command', command_name=command_name, interaction_instance=interaction_instance)
                        continue
                    cls.get_log().format_with_message('Existing basic extras', basic_extra=basic_extra, tuned_values_attr=getattr(basic_extra, '_tuned_values', None))
                    new_basic_extras += (basic_extra, )

            setattr(interaction_instance, 'basic_extras', new_basic_extras)
            cls.get_log().format_with_message('New basic_extras', extras=getattr(interaction_instance, 'basic_extras', None))

    # t_at_beginning = 'at_beginning'
    # t_at_end = 'at_end'
    # t_on_xevt = 'on_xevt'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def _create_do_command_basic_extras(
        cls,
        command_name: str,
        command_arguments: Iterator[CommonCommandArgumentData] = tuple(),
        timing: CommonInteractionBasicExtrasTiming = CommonInteractionBasicExtrasTiming.AT_END,
        # offset_time: Union[None, float] = None,
        # xevt_id: Union[None, int] = None
    ):
        basic_extras = None
        if timing != CommonInteractionBasicExtrasTiming.AT_BEGINNING:
            offset_time = None

        try:
            from element_utils import CleanupType
            from sims4.collections import make_immutable_slots_class
            from ui.ui_dialog import CommandArgType
            import collections
            do_command_data = dict()
            do_command_slots = {'arguments', 'command', 'success_chance', 'timing'}

            do_command_data.update({'command': command_name})
            do_command_data.update({'success_chance': SuccessChance.ONE})

            argument_tunings = list()
            for command_argument in command_arguments:
                argument_tunings.append(command_argument.to_tuning())

            # arguments_one_data = dict()
            # arguments_one_data.update({'arg_type': CommandArgType.ARG_TYPE_STRING})
            # arguments_one_data.update({'argument': parameter})
            # argument_one_slots = {'arg_type', 'argument'}
            # arguments_one_immutable_class = make_immutable_slots_class(argument_one_slots)
            # arguments_one_tuning = arguments_one_immutable_class(arguments_one_data)

            # arguments_two = dict()
            # arguments_two.update({'arg_type': CommandArgType.ARG_TYPE_BOOL})
            # arguments_two.update({'argument': ParticipantType.Actor})
            # argument_two_slots = {'arg_type', 'argument'}
            # arguments_two_immutable_class = make_immutable_slots_class(argument_two_slots)
            # arguments_two_tuning = arguments_two_immutable_class(arguments_two)

            do_command_data.update({'arguments': tuple(argument_tunings)})

            timing_data = dict()
            timing_data.update({'criticality': CleanupType.OnCancel})
            # if offset_time:
            #     timing_data.update({'offset_time': offset_time})
            # else:
            #     timing_data.update({'offset_time': None})
            timing_data.update({'offset_time': None})
            timing_data.update({'supports_failsafe': None})
            timing_data.update({'timing': timing.name.lower()})
            timing_data.update({'xevt_id': None})
            # timing_data.update({'xevt_id': xevt_id})
            timing_slots = {'criticality', 'offset_time', 'supports_failsafe', 'timing', 'xevt_id'}
            timing_immutable_class = make_immutable_slots_class(timing_slots)
            timing_tuning = timing_immutable_class(timing_data)

            do_command_data.update({'timing': timing_tuning})

            do_command_class = make_immutable_slots_class(do_command_slots)
            do_command_tuning = do_command_class(do_command_data)

            from interactions.utils.tunable import DoCommand
            from sims4.tuning.tunable import TunableFactory
            basic_extras = TunableFactory.TunableFactoryWrapper(do_command_tuning, 'TunableDoCommand', DoCommand)

        except Exception as ex:
            cls.get_log().error('Failed to process', exception=ex)

        return basic_extras
