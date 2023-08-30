from controlmenu.modinfo import ModInfo
from controlmenu.settings.setting_utils import CMSettingUtils
from sims.aging.aging_transition import AgingTransition
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AgingTransition, AgingTransition._get_age_duration_multiplier.__name__)
def _cm_override_get_age_duration_multiplier(original, self, sim_info: SimInfo):
    original_value = original(self, sim_info)
    multiplier = 1.0
    if CommonAgeUtils.is_baby(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_baby()
    elif CommonAgeUtils.is_infant(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_infant()
    elif CommonAgeUtils.is_toddler(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_toddler()
    elif CommonAgeUtils.is_child(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_child()
    elif CommonAgeUtils.is_teen(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_teen()
    elif CommonAgeUtils.is_young_adult(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_young_adult()
    elif CommonAgeUtils.is_adult(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_adult()
    elif CommonAgeUtils.is_elder(sim_info):
        multiplier = CMSettingUtils.AgeLength.get_age_length_multiplier_elder()
    return original_value * multiplier
