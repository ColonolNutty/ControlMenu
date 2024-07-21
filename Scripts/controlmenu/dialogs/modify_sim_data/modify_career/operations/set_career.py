"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple

from careers.career_tuning import Career, TunableCareerTrack, CareerLevel
from controlmenu.dialogs.modify_sim_data.modify_career.enums.string_ids import CMSimModifyCareerStringId
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.sims.common_career_track_utils import CommonCareerTrackUtils
from sims4communitylib.utils.sims.common_career_utils import CommonCareerUtils
from sims4communitylib.utils.sims.common_sim_career_utils import CommonSimCareerUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMSetCareerSimOp(CMSingleSimOperation):
    """Set Career of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_set_career_of_sim'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimModifyCareerStringId.SET_CAREER,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_option_chosen(_: str, _career: Career):
            if _career is None:
                _reopen()
                return
            self.log.format_with_message('Displaying career tracks career for Sim.', _career=_career, sim=sim_info)
            self._display_career_branches(sim_info, _career, _reopen, on_completed=on_completed)

        # noinspection PyTypeChecker
        non_playable_career_ids: Tuple[int] = (
            223698,  # University_BaseCareer
            231099,  # career_Batuu
            207004,  # career_OddJob
            209979,  # university_CourseSlot_A
            209984,  # university_CourseSlot_B
            209988,  # university_CourseSlot_C
            209989,  # university_CourseSlot_D
            260893,  # careers_VillagerHelp
            206791,  # careers_Adult_Freelancer_No_Agency
        )

        sim = CommonSimUtils.get_sim_instance(sim_info)
        for career in CommonResourceUtils.load_all_instance_values(Types.CAREER, return_type=Career):
            career_guid = CommonCareerUtils.get_career_guid(career)
            if career_guid is None:
                self.log.format_with_message('Missing career id for Career.', career=career)
                continue
            if career_guid in non_playable_career_ids:
                self.log.format_with_message('Career is not playable', career=career)
                continue
            if not CommonSimTypeUtils.is_non_player_sim(sim_info):
                if 'npc' in career.__name__.lower():
                    self.log.format_with_message('Career is for NPCs only', career=career)
                    continue
            try:
                self.log.format_with_message('Attempting to display career', career=career, skill_id=career_guid, sim=sim_info)
                if not career.is_valid_career(sim_info=sim_info, from_join=True):
                    self.log.format_with_message('Failed, Career is not available for Sim.', career=career, skill_id=career_guid, sim=sim_info)
                    continue

                start_track: TunableCareerTrack = career.start_track
                display_name = CommonLocalizationUtils.combine_localized_strings((start_track.get_career_name(sim), career.__name__), separator=CommonLocalizedStringSeparator.SPACE_PARENTHESIS_SURROUNDED)

                # noinspection PyUnresolvedReferences
                description = start_track.get_career_description(sim)
                # noinspection PyUnresolvedReferences
                icon = start_track.icon or CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()
                option_dialog.add_option(
                    CommonDialogSelectOption(
                        str(career_guid),
                        career,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=icon,
                            is_enabled=self._is_career_allowed_for_sim(sim_info, career)
                        ),
                        on_chosen=_on_option_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display career.', career=career, career_name=career.__name__, career_id=career_guid, exception=ex)

        if not option_dialog.has_options():
            self.log.format_with_message('No careers available for the Sim!', sim=sim_info)
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True

    def _is_career_allowed_for_sim(self, sim_info: SimInfo, career: Career) -> bool:
        career_id = CommonCareerUtils.get_career_guid(career)
        return sim_info is not None and career_id is not None

    def _display_career_branches(self, sim_info: SimInfo, career: Career, on_close: Callable[[], None], on_completed: Callable[[bool], None] = CommonFunctionUtils.noop):
        def _reopen() -> None:
            self._display_career_branches(sim_info, career, on_close=on_close, on_completed=on_completed)

        def _on_close() -> None:
            on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimModifyCareerStringId.CHOOSE_CAREER_BRANCH_TITLE,
            CMSimModifyCareerStringId.CHOOSE_CAREER_BRANCH_DESCRIPTION,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        def _on_career_track_chosen(_: str, _career_track: TunableCareerTrack):
            if not _career_track:
                _reopen()
                return
            self._display_career_levels(sim_info, career, _career_track, _reopen, on_completed=on_completed)

        sim = CommonSimUtils.get_sim_instance(sim_info)
        for career_track in CommonCareerUtils.get_all_career_tracks(career):
            try:
                career_track_id = CommonCareerTrackUtils.get_career_track_guid(career_track)
                # noinspection PyUnresolvedReferences
                icon = career_track.icon or CommonIconUtils.load_question_mark_icon()
                # MISSING ICON Identifier
                _MISSING_IMAGE_ICON_ID = 3526464109639239417
                if icon.instance == 0 or icon.instance == _MISSING_IMAGE_ICON_ID:
                    icon = CommonIconUtils.load_question_mark_icon()

                option_dialog.add_option(
                    CommonDialogSelectOption(
                        str(career_track_id),
                        career_track,
                        CommonDialogOptionContext(
                            career_track.get_career_name(sim),
                            career_track.get_career_description(sim),
                            icon=icon,
                        ),
                        on_chosen=_on_career_track_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display Career Branch', career_branch=career_track, exception=ex)

        if not option_dialog.has_options():
            _on_close()
            return
        option_dialog.show(sim_info=sim_info, sort_options=True)

    def _display_career_levels(self, sim_info: SimInfo, career: Career, career_track: TunableCareerTrack, on_close: Callable[[], None], on_completed: Callable[[bool], None] = CommonFunctionUtils.noop):
        def _on_close() -> None:
            on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimModifyCareerStringId.CHOOSE_CAREER_LEVEL_TITLE,
            CMSimModifyCareerStringId.CHOOSE_CAREER_LEVEL_DESCRIPTION,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=20000
        )

        sim = CommonSimUtils.get_sim_instance(sim_info)

        def _on_career_level_chosen(_: str, _career_level: CareerLevel):
            CommonSimCareerUtils.add_career(sim_info, career, remove_all_existing_careers=True, career_level=_career_level)
            on_completed(True)

        career_track_levels: Tuple[CareerLevel] = CommonCareerTrackUtils.get_career_levels(career_track)
        level = 1
        for _career_level in career_track_levels:
            try:
                # 'Level: {career level name}'
                career_level_id = getattr(_career_level, 'guid64', None)

                display_name = CommonLocalizationUtils.combine_localized_strings((_career_level.get_title(sim), str(level)), separator=CommonLocalizedStringSeparator.SPACE_PARENTHESIS_SURROUNDED)

                description = _career_level.title_description(sim)

                option_dialog.add_option(
                    CommonDialogSelectOption(
                        str(career_level_id),
                        _career_level,
                        CommonDialogOptionContext(
                            display_name,
                            description,
                            icon=CommonIconUtils.load_arrow_right_icon(),
                        ),
                        on_chosen=_on_career_level_chosen
                    )
                )
                level += 1
            except Exception as ex:
                self.log.format_error_with_message('Failed to display Career Level', career_level=_career_level, exception=ex)

        if not option_dialog.has_options():
            _on_close()
            return
        option_dialog.show(sim_info=sim_info, sort_options=True)
