"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.modify_sim_data.household.household_dialog import CMHouseholdDialog
from controlmenu.dialogs.modify_sim_data.modify_age.modify_age_dialog import CMModifyAgeDialog
from controlmenu.dialogs.modify_sim_data.modify_buffs.modify_buffs_dialog import CMModifyBuffsDialog
from controlmenu.dialogs.modify_sim_data.modify_currency.modify_currency_dialog import CMModifyCurrencyDialog
from controlmenu.dialogs.modify_sim_data.modify_occult.modify_sim_occult_dialog import CMModifyOccultDialog
from controlmenu.dialogs.modify_sim_data.modify_relationships.modify_relationships_dialog import \
    CMModifyRelationshipsDialog
from controlmenu.dialogs.modify_sim_data.modify_skills.enums.string_ids import CMSimModifySkillsStringId
from controlmenu.dialogs.modify_sim_data.modify_skills.modify_skills_dialog import CMModifySkillsDialog
from controlmenu.dialogs.modify_sim_data.modify_traits.modify_traits_dialog import CMModifyTraitsDialog
from controlmenu.dialogs.modify_sim_data.pregnancy.pregnancy_dialog import CMPregnancyDialog
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.settings.setting_utils import CMSettingUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils


class CMModifySimDataDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_sim_data_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMStringId.MODIFY_SIM_DATA

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyAge',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.MODIFY_AGE,
                ),
                on_chosen=lambda *_, **__: CMModifyAgeDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyTraits',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.MODIFY_TRAITS,
                ),
                on_chosen=lambda *_, **__: CMModifyTraitsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyBuffs',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.MODIFY_BUFFS,
                ),
                on_chosen=lambda *_, **__: CMModifyBuffsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyCurrency',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.MODIFY_CURRENCY,
                ),
                on_chosen=lambda *_, **__: CMModifyCurrencyDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyOccult',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.MODIFY_OCCULT,
                ),
                on_chosen=lambda *_, **__: CMModifyOccultDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyRelationships',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.MODIFY_RELATIONSHIPS,
                ),
                on_chosen=lambda *_, **__: CMModifyRelationshipsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifySkills',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifySkillsStringId.MODIFY_SKILLS,
                ),
                on_chosen=lambda *_, **__: CMModifySkillsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Household',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.HOUSEHOLD,
                ),
                on_chosen=lambda *_, **__: CMHouseholdDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        if CommonSimPregnancyUtils.has_permission_for_pregnancies(self._sim_info):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'Pregnancy',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.PREGNANCY,
                    ),
                    on_chosen=lambda *_, **__: CMPregnancyDialog(self._sim_info, on_previous=reopen).open()
                )
            )
        return True
