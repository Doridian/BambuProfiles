PROFILE_TRANSLATIONS = {

}

PROFILE_VALUE_DEFAULTS = {
    "additional_cooling_fan_speed": ["0"],
    "bed_temperature_difference": ["10"],
    "enable_overhang_bridge_fan": ["1"],
    "filament_is_support": ["0"],
}

PROFILE_IGNORE_KEYS = set([
    "name",
    "from",
    "inherits",
    "instantiation",
    "filament_settings_id",
    "version",
    "compatible_printers",
    "compatible_printers_condition",
    "compatible_prints",
    "compatible_prints_condition",
])

SLICER_REPO = "https://github.com/bambulab/BambuStudio.git"
SLICER_BRANCH = "master"

SLICER_DIR = "./tmp/slicer"
SLICER_PROFILE_DIR = f"{SLICER_DIR}/resources/profiles/BBL"
