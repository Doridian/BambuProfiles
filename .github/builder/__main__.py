#!/usr/bin/env python3

from builder import clone_slicer, load_all_profiles, get_profile_types, build_profile_list_view

def main() -> None:
    clone_slicer()
    load_all_profiles()

    for profile_type in get_profile_types():
        view = build_profile_list_view(profile_type)
        with open(f"./{profile_type}/README.md", "wb") as f:
            f.write(b"# ")
            f.write(profile_type.title().encode('utf-8'))
            f.write(b" profiles\n\n")
            f.write(view.encode('utf-8'))

if __name__ == "__main__":
    main()
