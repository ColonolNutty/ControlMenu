"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Callable, Iterator, Tuple

from aspirations.aspiration_types import AspriationType
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from situations.situation_goal import SituationGoal
from whims.whim import Whim
from whims.whim_set import WhimSetBaseMixin


class CMCommonWhimUtils(_HasS4CLClassLog):
    """Utilities for manipulating whims."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_whim_utils'

    @classmethod
    def get_all_whim_sets_by_whim_generator(
        cls,
        whim: Union[int, Whim],
        include_whim_set_callback: Callable[[WhimSetBaseMixin], Union[bool, CommonExecutionResult, CommonTestResult]] = None
    ) -> Iterator[WhimSetBaseMixin]:
        """get_all_whim_sets_by_whim_generator(whim, include_whim_set_callback=None)

        Retrieve every Whim Set that contains a Whim.

        :param whim: The identifier or instance of a Whim.
        :type whim: Union[int, Whim]
        :param include_whim_set_callback: If the result of this callback is True, the Whim will be included in the results. If set to None, All Whims will be included.
        :type include_whim_set_callback: Callable[[Whim], bool], optional
        :return: An iterator of all Whim Sets that contain the specified Whim and match the `include_whim_set_callback` filter.
        :rtype: Iterator[WhimSetBaseMixin]
        """
        whim_instance = cls.load_whim_by_guid(whim)
        if whim_instance is None:
            return tuple()

        def _has_whim(_aspiration: WhimSetBaseMixin) -> bool:
            if hasattr(_aspiration, 'whims'):
                if whim_instance in _aspiration.whims:
                    return True
            return False

        include_whim_set_callback = CommonFunctionUtils.run_predicates_as_one((_has_whim, include_whim_set_callback))

        yield from cls.get_all_whim_sets_generator(include_whim_set_callback=include_whim_set_callback)

    @classmethod
    def get_all_whim_sets_generator(
        cls,
        include_whim_set_callback: Callable[[WhimSetBaseMixin], Union[bool, CommonExecutionResult, CommonTestResult]] = None
    ) -> Iterator[WhimSetBaseMixin]:
        """get_all_whim_sets_generator(include_whim_set_callback=None)

        Retrieve every Whim Set.

        :param include_whim_set_callback: If the result of this callback is True, the Whim will be included in the results. If set to None, All Whims will be included.
        :type include_whim_set_callback: Callable[[Whim], bool], optional
        :return: An iterator of all Whim Sets that contain the specified Whim and match the `include_whim_set_callback` filter.
        :rtype: Iterator[WhimSetBaseMixin]
        """
        for (aspiration_id, aspiration) in tuple(CommonResourceUtils.load_all_instances_as_guid_to_instance(Types.ASPIRATION, return_type=Whim).items()):
            if aspiration.aspiration_type != AspriationType.WHIM_SET:
                continue
            if include_whim_set_callback is None or include_whim_set_callback(aspiration):
                yield aspiration

    @classmethod
    def get_all_whims_generator(
        cls,
        include_whim_callback: Callable[[Whim], Union[bool, CommonExecutionResult, CommonTestResult]] = None
    ) -> Iterator[Whim]:
        """get_all_whims_generator(include_whim_callback=None)

        Retrieve every Whim.

        :param include_whim_callback: If the result of this callback is True, the Whim will be included in the results. If set to None, All Whims will be included.
        :type include_whim_callback: Callable[[Whim], bool], optional
        :return: An iterator of all Whims matching the `include_whim_callback` filter.
        :rtype: Iterator[Whim]
        """
        for (whim_id, whim) in tuple(CommonResourceUtils.load_all_instances_as_guid_to_instance(Types.WHIM, return_type=Whim).items()):
            if include_whim_callback is None or include_whim_callback(whim):
                yield whim

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
    def get_whimset_guid(cls, whimset: Union[int, WhimSetBaseMixin]) -> Union[int, None]:
        """get_whimset_guid(whimset)

        Retrieve the GUID (Decimal Identifier) of a Whimset.

        :param whimset: The identifier or instance of a Whimset.
        :type whimset: Union[int, WhimSetBaseMixin]
        :return: The decimal identifier of the Whimset or None if the Whimset does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(whimset, int):
            return whimset
        return getattr(whimset, 'guid64', None)

    @classmethod
    def get_whimset_whims(cls, whimset: WhimSetBaseMixin) -> Tuple[Whim]:
        """get_whimset_whims(whimset)

        Retrieve the Whims contained in a Whimset.

        :param whimset: An instance of a Whimset.
        :type whimset: WhimSetBaseMixin
        :return: The whims contained in the Whimset.
        :rtype: Tuple[Whim]
        """
        # noinspection PyUnresolvedReferences
        if not hasattr(whimset, 'whims') or not whimset.whims:
            return tuple()
        # noinspection PyUnresolvedReferences,PyTypeChecker
        return tuple([whim_class.whim for whim_class in whimset.whims])

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
                return 'Unknown Whim'

    @classmethod
    def get_whimset_name(cls, whimset: WhimSetBaseMixin) -> Union[str, None]:
        """get_whimset_name(whimset)

        Retrieve the Name of a Whimset.

        :param whimset: An instance of a Whimset.
        :type whimset: WhimSetBaseMixin
        :return: The name of a Whimset or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if whimset is None:
            return None
        # noinspection PyBroadException
        try:
            return whimset.__name__ or whimset.__class__.__name__
        except:
            # noinspection PyBroadException
            try:
                return whimset.__class__.__name__
            except:
                return 'Unknown Whimset'

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
        if hasattr(whim, 'fluff_description'):
            description = whim.fluff_description
            if description is not None:
                return description(*localization_tokens)
        return None

    @classmethod
    def load_whim_by_guid(cls, whim: Union[int, Whim]) -> Union[Whim, None]:
        """load_whim_by_guid(whim)

        Load an instance of a Whim by its identifier.

        :param whim: The identifier of a Whim.
        :type whim: Union[int, CommonWhimId, Whim]
        :return: An instance of a Whim matching the decimal identifier or None if not found.
        :rtype: Union[Whim, None]
        """
        if isinstance(whim, Whim):
            return whim
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            whim_instance = whim()
            if isinstance(whim_instance, Whim):
                # noinspection PyTypeChecker
                return whim
        except:
            pass
        # noinspection PyBroadException
        try:
            whim: int = int(whim)
        except:
            # noinspection PyTypeChecker
            whim: Whim = whim
            return whim

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.WHIM, whim)
