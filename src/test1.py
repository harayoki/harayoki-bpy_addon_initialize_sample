import sys
import os
from typing import List
import argparse
from pathlib import Path
import numpy as np
import importlib

try:
    import bpy
except ImportError:
    sys.exit("this script is only run in blender environment")

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
    for addon in bpy.context.preferences.addons:  # addons: bpy_prop_collection
        print(addon.module)  # name
    print()


def print_modules(prefix: str = '') -> None:
    print("\nmodules__________________________")
    for key in sys.modules:
        if not prefix or key.startswith(prefix):
            print(key)  # key is module name


def initialize_addon(addon_dir: str, skip_if_registered: bool = False) -> None:
    """
    任意のアドオンディレクトリ内にあるアドオンを読み込む
    :param addon_dir: アドオンディレクトリ
    :param skip_if_registered: 指定すると既に登録されている場合は読み込まない
    """
    addon_dir_path: Path = Path(addon_dir)
    if not addon_dir or not addon_dir_path.exists():
        sys.exit(f"addon dir not found: '{addon_dir}'")

    # アドオンディレクトリをsys.pathに追加
    if addon_dir not in sys.path:
        sys.path.append(addon_dir)

    # アドオンファイルおよびアドオンディレクトリをデバッグ用に表示
    for p in addon_dir_path.iterdir():
        if p.is_dir():
            if (p / '__init__.py').exists():
                print(f"found addon dir: {p}")
        elif p.is_file():
            if p.suffix == '.py':
                print(f"found addon file: {p}")
    
    # アドオンの探索 アドオンファイルもアドオンディレクトリもmodulesとして発見される
    loaded_modules = set()
    modules = bpy.utils.modules_from_path(addon_dir, loaded_modules)

    # 見つかったアドオンの追加
    for module in modules:
        addon_name = module.__name__
        print(f"found addon file: {addon_name}")
        # すでに登録されている場合の処理
        registered = addon_name in bpy.context.preferences.addons
        if registered:
            if skip_if_registered:
                print(f"already registered: {addon_name}")
                continue
            else:
                bpy.ops.preferences.addon_disable(module=addon_name)
                print(f"unregister: {addon_name}")
        # アドオンソースの読み込み importlib を使う
        print(f'* ADDON LOADING: {addon_name}')
        importlib.reload(module)

        # アドオンを登録 直接 preferences.addons に追加はできない
        if addon_name not in bpy.context.preferences.addons:
            bpy.ops.preferences.addon_enable(module=addon_name)
            print(f"* ADDON REGISTERED: {module.__name__}")


def run() -> None:
    parser = argparse.ArgumentParser(description='bpy addon initialize test')
    parser.add_argument('-a', '--addon_dir', type=str, help='addon dir', default='')
    parser.add_argument('-t', '--test', action='store_true', help='テストアドオンを追加して実行する')
    addon_dir = ''
    if bpy.app.binary_path == '':
        args = parser.parse_args()
    elif bpy.app.background:
        print("background mode")
        if '--' in sys.argv:
            # blender background 起動時の引数を取得
            args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
        else:
            args = parser.parse_args([])
    else:
        # python script として実行された場合の引数を取得
        args = parser.parse_args()
    addon_dir = args.addon_dir
    if args.test:
        test_add_addon(addon_dir)
    else:
        main(addon_dir)


def main(addon_dir:str = '') -> None:
    print_script_paths()
    print_sys_paths()
    # priint_modules('bl_')
    print_addons("default addons")
    if addon_dir:
        initialize_addon(addon_dir)
        print_addons("current addons")


def test_add_addon(addon_dir:str = ''):
    if not addon_dir:
        addon_dir_path: Path = Path(__file__).parent.parent / 'addons'
        addon_dir = addon_dir_path.as_posix()
    if not os.path.exists(addon_dir):
        print(f"addon dir not found: {addon_dir}")
    else:
        main(addon_dir)
        bpy.ops.object.create_hello_world(text="こんにちわ Blender!!")


if bpy.app.binary_path == '':
    # コマンド実行時
    run()
elif bpy.app.background:
    # Blender background 起動時
    run()
else:
    # Blender内、スクリプトパネル等での実行時
    # main(addon_dir='addonsフォルダへのパス')
    # test_add_addon(addon_dir='addonsフォルダへのパス')
    main("******/addons")

