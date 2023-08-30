"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.infant import CMSetAgeInfantOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.adult import \
    CMSetAgeLengthMultiplierAdultOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.baby import \
    CMSetAgeLengthMultiplierBabyOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.child import \
    CMSetAgeLengthMultiplierChildOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.elder import \
    CMSetAgeLengthMultiplierElderOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.infant import \
    CMSetAgeLengthMultiplierInfantOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.teen import \
    CMSetAgeLengthMultiplierTeenOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.toddler import \
    CMSetAgeLengthMultiplierToddlerOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age_length_multipliers.operations.young_adult import \
    CMSetAgeLengthMultiplierYoungAdultOp
from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.settings.settings import CMSetting
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.dialogs.option_dialogs.common_choose_button_option_dialog import CommonChooseButtonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from controlmenu.dialogs.modify_sim_data.enums.string_identifiers import CMSimControlMenuStringId
from controlmenu.dialogs.sim_control_dialog_base import CMSimControlDialogBase
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.adult import CMSetAgeAdultOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.child import CMSetAgeChildOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.elder import CMSetAgeElderOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.teen import CMSetAgeTeenOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.toddler import CMSetAgeToddlerOp
from controlmenu.dialogs.modify_sim_data.modify_age.set_age.operations.young_adult import CMSetAgeYoungAdultOp
from controlmenu.dialogs.modify_sim_data.single_sim_operation import CMSingleSimOperation


class CMSetAgeLengthMultipliersDialog(CMSimControlDialogBase):
    """ The control dialog for Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_set_age_length_multipliers_dialog'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return CMSimControlMenuStringId.SET_AGE_LENGTH_MULTIPLIERS

    # noinspection PyMissingOrEmptyDocstring
    @property
    def description(self) -> Union[int, str, LocalizedString]:
        return CMSimControlMenuStringId.SET_AGE_LENGTH_MULTIPLIERS_DESCRIPTION

    def _setup_dialog(
        self,
        option_dialog: CommonChooseButtonOptionDialog,
        on_close: Callable[[], None],
        on_previous: Callable[[], None],
        reopen: Callable[[], None],
        **__
    ) -> bool:
        def _operation_run(operation: CMSingleSimOperation):
            def _on_operation_complete(_: bool) -> None:
                reopen()

            operation.run(self._sim_info, on_completed=_on_operation_complete)

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Baby',
                CommonAge.BABY,
                CommonDialogResponseOptionContext(
                    CommonStringId.BABY
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierBabyOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Infant',
                CommonAge.INFANT,
                CommonDialogResponseOptionContext(
                    CommonStringId.INFANT
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierInfantOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Toddler',
                CommonAge.TODDLER,
                CommonDialogResponseOptionContext(
                    CommonStringId.TODDLER
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierToddlerOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Child',
                CommonAge.CHILD,
                CommonDialogResponseOptionContext(
                    CommonStringId.CHILD
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierChildOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Teen',
                CommonAge.TEEN,
                CommonDialogResponseOptionContext(
                    CommonStringId.TEEN
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierTeenOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'YoungAdult',
                CommonAge.YOUNGADULT,
                CommonDialogResponseOptionContext(
                    CommonStringId.YOUNG_ADULT
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierYoungAdultOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Adult',
                CommonAge.ADULT,
                CommonDialogResponseOptionContext(
                    CommonStringId.ADULT
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierAdultOp())
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Elder',
                CommonAge.ELDER,
                CommonDialogResponseOptionContext(
                    CommonStringId.ELDER
                ),
                on_chosen=lambda *_, **__: _operation_run(CMSetAgeLengthMultiplierElderOp())
            )
        )
        return True
