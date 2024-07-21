"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from careers.career_tuning import Career, TunableCareerTrack
from controlmenu.dialogs.modify_sim_data.modify_career.enums.string_ids import CMSimModifyCareerStringId
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.sims.common_career_utils import CommonCareerUtils
from sims4communitylib.utils.sims.common_sim_career_utils import CommonSimCareerUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMManageCareersSimOp(CMSingleSimOperation):
    """Manage a specific career of a Sim."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_manage_career'

    # noinspection PyMissingOrEmptyDocstring
    def run(self, sim_info: SimInfo, on_completed: Callable[[bool], None] = CommonFunctionUtils.noop) -> bool:
        def _reopen() -> None:
            self.run(sim_info, on_completed=on_completed)

        def _on_close() -> None:
            on_completed(False)

        option_dialog = CommonChooseObjectOptionDialog(
            CMSimModifyCareerStringId.MANAGE_CAREERS,
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
            from controlmenu.dialogs.modify_sim_data.modify_career.modify_career_dialog import CMModifyCareerDialog
            CMModifyCareerDialog(sim_info, _career, on_close=_reopen, on_previous=on_completed).open()

        career_tracker = CommonSimCareerUtils.get_career_tracker(sim_info)
        if career_tracker is None:
            on_completed(False)
            return False

        sim = CommonSimUtils.get_sim_instance(sim_info)
        for (career_uid, career) in career_tracker.careers.items():
            career_guid = CommonCareerUtils.get_career_guid(career)
            if career_guid is None:
                self.log.format_with_message('Missing career id for Career.', career=career)
                continue
            try:
                start_track: TunableCareerTrack = career.start_track
                display_name = CommonLocalizationUtils.combine_localized_strings((start_track.get_career_name(sim), career.__class__.__name__), separator=CommonLocalizedStringSeparator.SPACE_PARENTHESIS_SURROUNDED)

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
                            icon=icon
                        ),
                        on_chosen=_on_option_chosen
                    )
                )
            except Exception as ex:
                self.log.format_error_with_message('Failed to display career.', career=career, career_name=career.__class__.__name__, career_id=career_guid, exception=ex)

        if not option_dialog.has_options():
            self.log.format_with_message('No careers available for the Sim!', sim=sim_info)
            on_completed(False)
            return False
        option_dialog.show(sim_info=sim_info, sort_options=True)
        return True
