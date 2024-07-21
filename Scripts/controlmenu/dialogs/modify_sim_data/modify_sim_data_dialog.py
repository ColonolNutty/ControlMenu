"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from controlmenu.dialogs.modify_sim_data.manage_death.manage_death_dialog import CMManageDeathDialog
from controlmenu.dialogs.modify_sim_data.modify_body.modify_body_dialog import CMModifyBodyDialog
from controlmenu.dialogs.modify_sim_data.modify_career.enums.string_ids import CMSimModifyCareerStringId
from controlmenu.dialogs.modify_sim_data.modify_career.modify_careers_dialog import CMModifyCareersDialog
from controlmenu.dialogs.modify_sim_data.modify_lifestyles.modify_lifestyles_dialog import CMModifyLifestylesDialog
from controlmenu.dialogs.modify_sim_data.modify_motives.enums.string_ids import CMSimModifyMotivesStringId
from controlmenu.dialogs.modify_sim_data.modify_motives.modify_motives_dialog import CMModifyMotivesDialog
from controlmenu.dialogs.modify_sim_data.modify_name.modify_name_dialog import CMModifyNameDialog
from controlmenu.dialogs.modify_sim_data.modify_perks.modify_perks_dialog import CMModifyPerksDialog
from controlmenu.dialogs.modify_sim_data.modify_statistics.modify_statistics_dialog import CMModifyStatisticsDialog
from controlmenu.dialogs.modify_sim_data.modify_walkstyles.modify_walk_style_dialog import CMModifyWalkStyleDialog
from controlmenu.dialogs.modify_sim_data.modify_whims.modify_whims_dialog import CMModifyWhimsDialog
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
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from statistics.trait_statistic import TraitStatisticGroup


class CMModifySimDataDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_modify_sim_data_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMStringId.SIM

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
                    CMSimControlMenuStringId.AGE,
                ),
                on_chosen=lambda *_, **__: CMModifyAgeDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyTraits',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.TRAITS,
                ),
                on_chosen=lambda *_, **__: CMModifyTraitsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyBuffs',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.BUFFS,
                ),
                on_chosen=lambda *_, **__: CMModifyBuffsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyNae',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.NAME,
                ),
                on_chosen=lambda *_, **__: CMModifyNameDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyCareer',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyCareerStringId.CAREER,
                ),
                on_chosen=lambda *_, **__: CMModifyCareersDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyMotives',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifyMotivesStringId.MOTIVES,
                ),
                on_chosen=lambda *_, **__: CMModifyMotivesDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyOccult',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.OCCULT,
                ),
                on_chosen=lambda *_, **__: CMModifyOccultDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyRelationships',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.RELATIONSHIPS,
                ),
                on_chosen=lambda *_, **__: CMModifyRelationshipsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifySkills',
                None,
                CommonDialogResponseOptionContext(
                    CMSimModifySkillsStringId.SKILLS,
                ),
                on_chosen=lambda *_, **__: CMModifySkillsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyPerks',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.PERKS,
                ),
                on_chosen=lambda *_, **__: CMModifyPerksDialog(self._sim_info, on_previous=reopen).open()
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

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyCurrency',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.CURRENCY,
                ),
                on_chosen=lambda *_, **__: CMModifyCurrencyDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyBody',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.BODY,
                ),
                on_chosen=lambda *_, **__: CMModifyBodyDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ManageDeath',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.DEATH,
                ),
                on_chosen=lambda *_, **__: CMManageDeathDialog(self._sim_info, on_previous=reopen).open()
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

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyStatistics',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.STATISTICS,
                ),
                on_chosen=lambda *_, **__: CMModifyStatisticsDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        if hasattr(TraitStatisticGroup, 'Lifestyle'):
            option_dialog.add_option(
                CommonDialogButtonOption(
                    'ModifyLifestyles',
                    None,
                    CommonDialogResponseOptionContext(
                        CMSimControlMenuStringId.LIFESTYLES,
                    ),
                    on_chosen=lambda *_, **__: CMModifyLifestylesDialog(self._sim_info, on_previous=reopen).open()
                )
            )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyWalkStyle',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.WALK_STYLE,
                ),
                on_chosen=lambda *_, **__: CMModifyWalkStyleDialog(self._sim_info, on_previous=reopen).open()
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'ModifyWhims',
                None,
                CommonDialogResponseOptionContext(
                    CMSimControlMenuStringId.WHIMS,
                ),
                on_chosen=lambda *_, **__: CMModifyWhimsDialog(self._sim_info, on_previous=reopen).open()
            )
        )
        return True
