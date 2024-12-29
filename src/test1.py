import sys
from typing import List
import argparse
from pathlib import Path
import importlib
import bpy


def print_sys_paths():
    print("\nsys.paths__________________________")
    for path in sys.path:
        print(path)

def print_script_paths():
    print("\nscript_paths__________________________")
    for path in bpy.utils.script_paths():
        print(path)

def print_addons(title: str = "addons") -> None:
    print(f"\n{title}__________________________")
    addon: bpy.types.Addon
    for addon in bpy.context.preferences.addons:
        print(addon)
    print()


def priint_modules(prefix: str = '') -> None:
    print("\nmodules__________________________")
    for key in sys.modules:
        if not prefix or key.startswith(prefix):
            print(key)  # key is module name


def initialize_addon(addon_dir: str) -> None:
    addon_dir_path: Path = Path(addon_dir)
    if not addon_dir_path.exists():
        sys.exit(f"addon dir not found: {addon_dir}")
    if addon_dir not in sys.path:
        sys.path.append(addon_dir)

    for path in addon_dir_path.iterdir():
        if path.is_dir():
            print(f"found module dir: {path}")
    
    loaded_modules = set()
    modules = bpy.utils.modules_from_path(addon_dir, loaded_modules)
    for module in modules:
        addon_name = module.__name__
        print(f'<loading: {addon_name}>')
        importlib.reload(module)
        if addon_name not in bpy.context.preferences.addons:
            bpy.ops.preferences.addon_enable(module=addon_name)
            print(f"registered: {module}")


def main() -> None:
    parser = argparse.ArgumentParser(description='bpy addon initialize test')
    parser.add_argument('-a', '--addon_dir', type=str, help='addon dir')
    parser.add_argument('-o', '--output_dir', type=str, help='output dir')
    args = parser.parse_args()

    con: bpy = bpy.context
    print_script_paths()
    print_sys_paths()
    # priint_modules('bl_')
    print_addons("default addons")
    if args.addon_dir:
        initialize_addon(args.addon_dir)
    print_addons("current addons")


main()

