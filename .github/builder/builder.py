from subprocess import check_call
from os import mkdir, listdir
from os.path import isdir, splitext, exists
from shutil import rmtree
from json import load as json_load
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote as url_quote
from const import PROFILE_TRANSLATIONS, PROFILE_IGNORE_KEYS, SLICER_PROFILE_DIR, SLICER_DIR, SLICER_REPO, SLICER_BRANCH, PROFILE_VALUE_DEFAULTS

def translate_profile_key(key: str) -> str:
    return PROFILE_TRANSLATIONS.get(key, key)

def remap_repo_type(typ):
    if typ == "printer":
        return "machine"
    return typ

def clone_slicer():
    if isdir(SLICER_PROFILE_DIR):
        check_call(["git", "pull"], cwd=SLICER_DIR)
    else:
        rmtree("./tmp", ignore_errors=True)
        mkdir("./tmp")
        check_call(["git", "clone", "--depth", "1", "--branch", SLICER_BRANCH, SLICER_REPO, SLICER_DIR])


@dataclass
class ProfileDiff:
    key: str
    left: Any
    right: Any

class RepoProfile:
    def __init__(self, local: bool, profile_type: str, folder: str, file: str):
        self.local = local
        self.type = profile_type

        self.folder = folder
        self.file = file

        preview_file = f"{splitext(file)[0]}.jpg"
        if exists(f"{self.folder}/{preview_file}"):
            self.preview = preview_file
        else:
            self.preview = None

        with open(f"{self.folder}/{self.file}", "rb") as f:
            self.data = json_load(f)

        self.name = self.data["name"]
        self.base = self.data.get("inherits", None)

    def merge(self, other: "RepoProfile") -> None:
        """
        Merge another profile into this one without overwriting any existing values
        """

        for key, value in other.data.items():
            if key in self.data:
                continue
            self.data[key] = value

    def diff(self, other: "RepoProfile") -> list[ProfileDiff]:
        res = []
        for key, value in self.data.items():
            if key in PROFILE_IGNORE_KEYS:
                continue

            other_value = other.data.get(key, PROFILE_VALUE_DEFAULTS.get(key, [""]))

            if value != other_value:
                res.append(ProfileDiff(key, value, other_value))
        return res

PROFILE_REGISTRY = {
    "filament": {},
    "printer": {},
    "process": {},
}

def load_profile_dir(dir: str, profile_type: str, local: bool) -> None:
    for file in listdir(dir):
        if not file.endswith(".json"):
            continue

        profile = RepoProfile(local, profile_type, dir, file)
        if profile.name in PROFILE_REGISTRY[profile_type]:
            raise ValueError(f"Duplicate profile name {profile.name} for type {profile_type}")
        PROFILE_REGISTRY[profile_type][profile.name] = profile

def load_profile_fully(profile: RepoProfile) -> None:
    if profile.base is None:
        return

    if profile.base not in PROFILE_REGISTRY[profile.type]:
        raise ValueError(f"Profile {profile.name} has unknown base {profile.base}")

    base_profile = PROFILE_REGISTRY[profile.type][profile.base]
    load_profile_fully(base_profile)
    profile.merge(base_profile)

def compare_profile_to_base(profile: RepoProfile) -> list[ProfileDiff]:
    if profile.base is None:
        return []

    # This will also load the base profile fully
    # and verify it exists
    # therefor we only need this line
    load_profile_fully(profile)

    return profile.diff(PROFILE_REGISTRY[profile.type][profile.base])

def format_diff_item(item: Any, key: str) -> str:
    if isinstance(item, list) and len(item) == 1:
        item = item[0]

    if not isinstance(item, str):
        item = f"{item}"

    item = item.replace('\r', '').replace('\n', '<br>').strip()
    
    if key.endswith('_gcode'):
        item = f"<pre><code>{item}</code></pre>" 

    return item

def format_diff(diff: ProfileDiff) -> str:
    return f"| {translate_profile_key(diff.key)} | {format_diff_item(diff.left, diff.key)} | {format_diff_item(diff.right, diff.key)} |"

def build_profile_view(profile: RepoProfile) -> str:
    diffs = compare_profile_to_base(profile)
    diff_table = "\n".join([format_diff(diff) for diff in diffs])

    test_print_link = f"[{profile.preview}]({url_quote(profile.preview)})" if profile.preview else "N/A"

    return f"""## {profile.name}

This profile is based on "{profile.base}".

Profile: [{profile.file}]({url_quote(profile.file)})

Test print: {test_print_link}

### Differences

| Option | This | Base |
|--------|------|------|
{diff_table}
"""

def get_profile_types() -> list[str]:
    return list(PROFILE_REGISTRY.keys())

def load_all_profiles() -> None:
    for profile_type in PROFILE_REGISTRY.keys():
        load_profile_dir(f"{profile_type}", profile_type, True)
        load_profile_dir(f"{SLICER_PROFILE_DIR}/{remap_repo_type(profile_type)}", profile_type, False)

def build_profile_list_view(profile_type: str) -> str:
    res = []
    profiles = PROFILE_REGISTRY[profile_type]
    for profile in profiles.values():
        if not profile.local:
            continue
        res.append(build_profile_view(profile))
    return "\n".join(res)
