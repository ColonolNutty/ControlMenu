"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from situations.situation_goal import SituationGoal
from whims.whim import Whim


class CMCommonWhimUtils(_HasS4CLClassLog):
    """Utilities for manipulating whims."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_whim_utils'

    @classmethod
    def get_whim_guid(cls, whim: Union[int, Whim]) -> Union[int, None]:
        """get_whim_guid(whim)

        Retrieve the GUID (Decimal Identifier) of a Whim.

        :param whim: The identifier or instance of a Whim.
        :type whim: Union[int, Whim]
        :return: The decimal identifier of the Whim or None if the Whim does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(whim, int):
            return whim
        return getattr(whim, 'guid64', None)

    @classmethod
    def get_whim_name(cls, whim: Whim) -> Union[str, None]:
        """get_whim_name(whim)

        Retrieve the Name of a Whim.

        :param whim: An instance of a Whim.
        :type whim: Whim
        :return: The name of a Whim or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if whim is None:
            return None
        # noinspection PyBroadException
        try:
            return whim.__name__ or whim.__class__.__name__
        except:
            # noinspection PyBroadException
            try:
                return whim.__class__.__name__
            except:
                return ''

    @classmethod
    def get_whim_description(cls, whim: Whim, goal: SituationGoal) -> Union[LocalizedString, None]:
        """get_whim_description(whim, goal)

        Retrieve the Description of a Whim.

        :param whim: An instance of a Whim.
        :type whim: Whim
        :param goal: The goal of the Whim.
        :type goal: SituationGoal
        :return: The name of a Whim or None if a problem occurs.
        :rtype: Union[LocalizedString, None]
        """
        if whim is None or goal is None:
            return None
        localization_tokens = goal.get_localization_tokens()
        description = whim.fluff_description
        if description is not None:
            return description(*localization_tokens)
        return None
