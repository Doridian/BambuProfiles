PROFILE_TRANSLATIONS = {

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
