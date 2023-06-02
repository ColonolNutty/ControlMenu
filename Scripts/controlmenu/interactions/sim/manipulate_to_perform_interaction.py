"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Any, Set, Union

from controlmenu.enums.string_identifiers import CMStringId
from controlmenu.modinfo import ModInfo
from controlmenu.settings.setting_utils import CMSettingUtils
from event_testing.results import TestResult
from interactions.aop import AffordanceObjectPair
from interactions.choices import ChoiceMenu, MenuItem
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.dialogs.premade_dialogs.common_premade_choose_sim_option_dialog import \
    CommonPremadeChooseSimOptionDialog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator
from sims4communitylib.utils.misc.common_game_client_utils import CommonGameClientUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from distributor.shared_messages import IconInfoData
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from server.pick_info import PickType, PickInfo
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class CMDebugManipulateToPerformInteractionInteraction(CommonImmediateSuperInteraction):
    """ Handles the Manipulate To... Perform Interaction interaction. """

    # noinspection SpellCheckingInspection
    _EXCLUDED_INTERACTION_NAME_SNIPPETS = {
        'terrain-create',
        'sim-stand',
        'dog_stand',
        'cat_stand',
        'cheat',
        'setuplot',
        'gohere',
        'terrain-teleport',
        'proxy',
        'debug',
        'forcemarriage',
        'socialpickersi',
        'solo_moveaway',
        'hospitalexambed',
        'generic_toilet',
        'generic_shower',
        'generic_bath',
        'generic_bubblebath',
        'generic_relaxingbath',
        'generic_bedundercovers',
        'generic_sittogether',
        'generic_sitintimate',
        'generic_watchintimate',
        'generic_bed_sleep',
        'generic_cook',
        'bed_getnear_fromsocial',
        'eat_to_clean_from_sit',
        'fridge_grabsnack_autotest'
    }

    # noinspection SpellCheckingInspection
    _EXCLUDED_DEBUG_INTERACTION_NAME_SNIPPETS = {
        'picker_relbit',
        'picker_trait',
        'picker_buff',
        'picker_grounding',
        'simray_frozen',
        'si_grimreaper',
        'si_sim_energyfailure',
        'ensembleinteractions',
        'goingoutsocials',
        'simpicker',
        'changeoutfitpicker_targetsim',
        'tobirthdaycake',
        'purchase_holidaytraditions',
        'aggregatesi_gohome',
        'autonomous',
        'death_',
        'solo_skeleton_add',
        'npc_choose_to_leave',
        'terrain_setup_garden',
        'piemenu',
        'object_hirenpc'
    }

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> Union[CommonModIdentity, None]:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'cm_debug_manipulate_to_perform_interaction'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> CommonTestResult:
        super_result = super().on_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)
        if not super_result:
            return super_result
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if interaction_target is None:
            cls.get_log().format_with_message('Failed, Target invalid.', target=interaction_target)
            return CommonTestResult.NONE

        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Dying Sims cannot order Sims around. The Active Sim is currently dying.')
        if CommonTypeUtils.is_terrain(interaction_target) or CommonTypeUtils.is_ocean(interaction_target) or CommonTypeUtils.is_swimming_pool(interaction_target):
            cls.get_log().debug('Target is terrain, ocean, or a swimming pool.')
        elif CommonTypeUtils.is_game_object(interaction_target):
            cls.get_log().debug('Target is an object.')

            def _get_top_level_object(target) -> bool:
                while target.parent is not None:
                    target = target.parent
                return target

            interaction_target = _get_top_level_object(interaction_target) or interaction_target
            cls.get_log().format(top_level_object=interaction_target)
        else:
            cls.get_log().debug('Failed, Target was not valid.')
            return CommonTestResult.NONE
        cls.get_log().debug('Success.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)

        def _on_sim_chosen(_picked_sim_info: SimInfo):
            self.log.format_with_message('Sim chosen, choosing interaction.', picked_sim=_picked_sim_info)
            self._show_interaction_menu(_picked_sim_info, interaction_target)

        self.log.debug('Opening dialog.')
        CommonPremadeChooseSimOptionDialog(
            title_identifier=CMStringId.CHOOSE_SIM,
            description_identifier=CMStringId.CHOOSE_SIM_TO_DO_INTERACTIONS,
            mod_identity=self.mod_identity,
            on_sim_chosen=_on_sim_chosen,
            instanced_sims_only=True
        ).show(sim_info)
        return CommonExecutionResult.TRUE

    def _show_interaction_menu(self, picked_sim_info: SimInfo, interaction_target: Any):
        exclude_interaction_name_snippets = (
            *self._EXCLUDED_INTERACTION_NAME_SNIPPETS,
            self.mod_identity.base_namespace.lower()
        )
        exclude_debug_interaction_name_snippets = (
            *self._EXCLUDED_DEBUG_INTERACTION_NAME_SNIPPETS,
            self.mod_identity.base_namespace.lower()
        )
        include_interaction_name_snippets = tuple()

        def _interaction_with_name(_interaction: Interaction) -> bool:
            _interaction_short_name = CommonInteractionUtils.get_interaction_short_name(_interaction)
            self.log.format_with_message('Checking interaction with short name: ', interaction_short_name=_interaction_short_name)
            for exclude in exclude_interaction_name_snippets:
                if exclude in _interaction_short_name.lower() and _interaction_short_name.lower() not in include_interaction_name_snippets:
                    self.log.debug('Failed, Interaction is invalid because name.')
                    return False
            self.log.debug('Success, Interaction is valid.')
            return True

        def _debug_interaction_with_name(_interaction: Interaction) -> bool:
            _interaction_short_name = CommonInteractionUtils.get_interaction_short_name(_interaction)
            self.log.format_with_message('Checking interaction with short name: ', interaction_short_name=_interaction_short_name)
            for exclude_debug in exclude_debug_interaction_name_snippets:
                if exclude_debug in _interaction_short_name.lower() and _interaction_short_name.lower() not in include_interaction_name_snippets:
                    self.log.debug('Failed, Interaction is invalid because debug name.')
                    return False
            self.log.debug('Success, Interaction is valid.')
            return True

        option_dialog = CommonChooseObjectOptionDialog(
            CMStringId.CHOOSE_INTERACTION,
            CMStringId.CHOOSE_INTERACTION_FOR_SIM_TO_PERFORM,
            title_tokens=(picked_sim_info,),
            description_tokens=(picked_sim_info,),
            mod_identity=self.mod_identity,
            per_page=20000
        )
        picked_sim = CommonSimUtils.get_sim_instance(picked_sim_info)
        picked_sim_interaction_context: InteractionContext = self.context.clone_for_sim(picked_sim)

        def _on_interaction_chosen(____: str, affordance_object_pair: AffordanceObjectPair):
            self.log.format_with_message('Chose AOP', aop=affordance_object_pair, affordance=affordance_object_pair.affordance)
            result = affordance_object_pair.execute(picked_sim_interaction_context)
            if result:
                self.log.format_with_message('Success, Sim will do the interaction!', result=result)
                CommonBasicNotification(
                    CMStringId.MANIPULATION_SUCCESS,
                    CMStringId.SIM_WILL_PERFORM_CHOSEN_INTERACTION,
                    description_tokens=(picked_sim_info,)
                ).show(icon=IconInfoData(obj_instance=picked_sim_info))
            else:
                self.log.format_with_message('Failed, could not tell Sim to do the interaction!', result=result)
                CommonBasicNotification(
                    CMStringId.MANIPULATION_FAILED,
                    CMStringId.SIM_WAS_UNABLE_TO_PERFORM_THE_CHOSEN_INTERACTION_REASON,
                    description_tokens=(picked_sim_info, result)
                ).show(icon=IconInfoData(obj_instance=picked_sim_info))

        include_callback = CommonFunctionUtils.run_predicates_as_one(
            (
                _interaction_with_name,
                _debug_interaction_with_name
            )
        )
        if CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            target_id = CommonSimUtils.get_sim_id(interaction_target)
        elif CommonTypeUtils.is_script_object(interaction_target):
            target_id = CommonObjectUtils.get_object_id(interaction_target)
        else:
            target_id = None

        pick: PickInfo = picked_sim_interaction_context.pick
        pick_position: CommonVector3 = pick.location if pick is not None else None
        x: float = pick_position.x if pick_position is not None else 0.0
        y: float = pick_position.y if pick_position is not None else 0.0
        z: float = pick_position.z if pick_position is not None else 0.0

        generated_choices_menu = self._generate_choices(
            picked_sim_info,
            target_id=target_id,
            pick_type=pick.pick_type if pick is not None else PickType.PICK_TERRAIN,
            x=x,
            y=y,
            z=z,
            lot_id=pick.lot_id if pick is not None else 0,
            level=pick.level if pick is not None else 0,
            preferred_objects=picked_sim_interaction_context.preferred_objects,
            is_routeable=True
        )
        if generated_choices_menu is None:
            self.log.debug('No interactions found.')
            CommonOkDialog(
                CMStringId.NO_INTERACTIONS_FOUND,
                0
            ).show()
            return

        for (option_id, menu_item) in generated_choices_menu.menu_items.items():
            menu_item: MenuItem = menu_item
            aop: AffordanceObjectPair = menu_item.aop
            interaction = aop.affordance
            if not include_callback(interaction):
                continue
            self.log.format_with_message('Showing interaction', interaction=interaction, allow_user_directed=interaction.allow_user_directed)
            # noinspection PyBroadException
            try:
                interaction_name = CommonInteractionUtils.get_interaction_display_name(interaction, tokens=(picked_sim, interaction_target))
                interaction_short_name = CommonInteractionUtils.get_interaction_short_name(interaction)
            except Exception as ex:
                # If the interaction explodes here, then it is probably something we couldn't run.
                self.log.format_error_with_message('Something went boom', interaction=interaction, exception=ex, throw=False)
                continue
            self.log.format(interaction=interaction, class_name=interaction.__name__, interaction_name=interaction_name, interaction_short_name=interaction_short_name)
            if not interaction_name or not interaction_short_name:
                self.log.format_with_message('Interaction had no name.', interaction=interaction)
                continue
            _display_name = interaction_name
            _description = interaction_short_name
            if aop.super_affordance is not None:
                super_affordance_name = CommonInteractionUtils.get_interaction_display_name(aop.super_affordance, tokens=(picked_sim, interaction_target))
                super_affordance_short_name = CommonInteractionUtils.get_interaction_short_name(aop.super_affordance)
                _display_name = CommonLocalizationUtils.combine_localized_strings((_display_name, super_affordance_name), separator=CommonLocalizedStringSeparator.SPACE_PARENTHESIS_SURROUNDED)
                _description = CommonLocalizationUtils.combine_localized_strings((_description, super_affordance_short_name), separator=CommonLocalizedStringSeparator.SPACE_PARENTHESIS_SURROUNDED)

            menu_item_result: TestResult = menu_item.result
            tooltip = menu_item_result.tooltip
            is_enabled = bool(menu_item_result)

            # noinspection PyBroadException
            try:
                localization_tokens = interaction.get_localization_tokens()
            except:
                localization_tokens = (picked_sim_info, interaction_target)

            option_dialog.add_option(
                CommonDialogSelectOption(
                    interaction_short_name,
                    aop,
                    CommonDialogOptionContext(
                        _display_name,
                        _description,
                        is_enabled=is_enabled,
                        tooltip_text_identifier=tooltip,
                        tooltip_tokens=localization_tokens
                    ),
                    on_chosen=_on_interaction_chosen
                )
            )

        if not option_dialog.has_options():
            self.log.debug('No interactions found.')
            CommonOkDialog(
                CMStringId.NO_INTERACTIONS_FOUND,
                0
            ).show()
            return

        if CMSettingUtils().perform_interaction_disclaimer_has_been_shown():
            self.log.debug('Showing interaction dialog.')
            option_dialog.show(sim_info=picked_sim_info, sort_options=True)
        else:
            def _on_acknowledged(_: Any) -> None:
                self.log.debug('Showing interaction dialog.')
                option_dialog.show(sim_info=picked_sim_info, sort_options=True)
                CMSettingUtils().flag_perform_interaction_disclaimer_as_shown()

            CommonOkDialog(
                CMStringId.DISCLAIMER,
                CMStringId.MANIPULATE_SIM_TO_PERFORM_DISCLAIMER_DESCRIPTION
            ).show(on_acknowledged=_on_acknowledged)

    def _generate_choices(
        self,
        chosen_sim_info: SimInfo,
        target_id: int = None,
        pick_type: PickType = PickType.PICK_TERRAIN,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        lot_id: int = 0,
        level: int = 0,
        preferred_objects: Set[Any] = None,
        is_routeable: bool = True
    ) -> Union[ChoiceMenu, None]:
        if target_id is None:
            return None
        zone = services.current_zone()
        client = CommonGameClientUtils.get_first_game_client()
        sim = CommonSimUtils.get_sim_instance(chosen_sim_info)
        shift_held = False
        choice_menu = ChoiceMenu(sim)
        pick_target = zone.find_object(target_id)
        if preferred_objects is None:
            preferred_objects = set()
        suppress_social_front_page = False
        import gsi_handlers.sim_handlers_log
        scoring_gsi_handler = {} if gsi_handlers.sim_handlers_log.pie_menu_generation_archiver.enabled else None
        if pick_type == PickType.PICK_PORTRAIT or pick_type == PickType.PICK_CLUB_PANEL:
            target_sim_info = CommonSimUtils.get_sim_info(target_id)
            object_info = services.object_manager().get(target_id)
            inventory_object_info = services.inventory_manager().get(target_id)
            if target_sim_info is None and object_info is None and inventory_object_info is None:
                return None
            if sim is None:
                return None
            picked_item_ids = {target_id}

            context = InteractionContext(sim, client.interaction_source, client.interaction_priority, client=client, target_sim_id=target_id)
            context.add_preferred_objects(preferred_objects)
            target = object_info or (inventory_object_info or sim)
            potential_interactions = list(sim.potential_relation_panel_interactions(target, context, picked_item_ids=picked_item_ids))
            choice_menu.add_potential_aops(target_sim_info, context, potential_interactions, scoring_gsi_handler)
        elif pick_type == PickType.PICK_SKEWER:
            target_sim_info = CommonSimUtils.get_sim_info(target_id)
            if target_sim_info is None:
                return None
            skewer_sim = target_sim_info.get_sim_instance()
            context = InteractionContext(skewer_sim, client.interaction_source, client.interaction_priority, client=client)
            context.add_preferred_objects(preferred_objects)
            potential_interactions = list(target_sim_info.sim_skewer_affordance_gen(context, picked_item_ids={chosen_sim_info.sim_id}))
            choice_menu.add_potential_aops(pick_target, context, potential_interactions, scoring_gsi_handler)
        elif pick_type == PickType.PICK_MANAGE_OUTFITS:
            context = InteractionContext(sim, client.interaction_source, client.interaction_priority, client=client)
            retail_manager = services.business_service().get_retail_manager_for_zone()
            potential_interactions = []
            if retail_manager is not None:
                potential_interactions = list(retail_manager.potential_manage_outfit_interactions_gen(context))
            choice_menu.add_potential_aops(pick_target, context, potential_interactions, scoring_gsi_handler)
        else:
            position = CommonVector3(x, y, z)
            from server_commands.interaction_commands import _get_targets_from_pick
            (pick_target, pick_type, potential_targets) = _get_targets_from_pick(sim, pick_target, pick_type, position, level, zone.id, lot_id, is_routeable, preferred_objects=preferred_objects)
            if pick_target is None:
                return
            interaction_parameters = client.get_interaction_parameters()
            if potential_targets:
                def _add_potential_object_aops(_potential_target, _routing_surface) -> PickInfo:
                    _pick = PickInfo(pick_type=pick_type, target=_potential_target, location=position, routing_surface=_routing_surface, lot_id=lot_id, level=level, alt=False, control=False, shift=False)
                    _context = InteractionContext(sim, client.interaction_source, client.interaction_priority, client=client, pick=_pick, shift_held=False)
                    _context.add_preferred_objects(preferred_objects)
                    potential_aops = list(_potential_target.potential_interactions(_context, **interaction_parameters))
                    choice_menu.add_potential_aops(_potential_target, _context, potential_aops, scoring_gsi_handler)
                    return _pick

                pick = None
                for (potential_target, routing_surface) in potential_targets:
                    if potential_target.is_sim:
                        suppress_social_front_page |= potential_target.should_suppress_social_front_page_when_targeted()
                    pick = _add_potential_object_aops(potential_target, routing_surface)

                if shift_held or sim is not None:
                    context = InteractionContext(sim, client.interaction_source, client.interaction_priority, client=client, pick=pick, shift_held=shift_held)
                    context.add_preferred_objects(preferred_objects)
                    sim.fill_choices_menu_with_si_state_aops(pick_target, context, choice_menu, scoring_gsi_handler)

                if len(choice_menu) == 0:
                    fire_service = services.get_fire_service()
                    if fire_service.fire_is_active:
                        fires = fire_service.get_fires_in_potential_targets(potential_targets)
                        if fires:
                            potential_target = fires[0]
                            _add_potential_object_aops(potential_target, potential_target.routing_surface)
        return choice_menu
