import inspect
import os
import sys

from manim_engine.constants import ANIMATIONS_DIR, SANIM_AUX_FILE


def add_extension_if_not_present(file_name, extension):
    # This could conceivably be smarter about handling existing differing extensions
    if(file_name[-len(extension):] != extension):
        return file_name + extension
    else:
        return file_name


def guarantee_existance(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_scene_output_directory(scene_class):
    file_path = os.path.abspath(inspect.getfile(scene_class))

    # TODO, is there a better way to do this?
    parts = file_path.split(os.path.sep)
    if "manim" in parts:
        sub_parts = parts[parts.index("manim") + 1:]
        file_path = os.path.join(*sub_parts)
    file_path = file_path.replace(".pyc", "")
    file_path = file_path.replace(".py", "")
    return guarantee_existance(os.path.join(ANIMATIONS_DIR, file_path))

def get_sanim_source_file_name():
    with open(SANIM_AUX_FILE, "r") as sanim_aux_file:
        return sanim_aux_file.read()

def in_sanim_mode():
    return get_sanim_source_file_name() != ''

def get_main_manim_dir():
    #get folder of this file
    utils_path = os.path.dirname(os.path.realpath(__file__))
    print(f"Debug - utils_path: {utils_path}")
    
    #remove the /utils part to get the manim folder
    parts = utils_path.split(os.path.sep)
    print(f"Debug - parts: {parts}")
    
    # Find the manim_engine directory
    try:
        manim_index = parts.index("manim_engine")
        parts = parts[:manim_index]
        print(f"Debug - parts after finding manim_engine: {parts}")
    except ValueError:
        print("Debug - Could not find manim_engine in path")
        # Fallback to removing last two parts
        parts = parts[:-2]
        print(f"Debug - parts after fallback: {parts}")
    
    # On Windows, handle the drive letter separately
    if os.name == 'nt' and len(parts) > 0 and parts[0].endswith(':'):
        drive = parts[0]
        parts = parts[1:]
        # Construct the path directly without using os.path.abspath
        manim_path = drive + os.sep + os.sep.join(parts)
    else:
        manim_path = os.sep.join(parts)
    
    print(f"Debug - Final manim_path: {manim_path}")
    return manim_path

def get_sanim_source_dir():
    if not in_sanim_mode():
        sys.exit("shouldn't ask for sanim source dir if not in sanim mode")
    manim_path = get_main_manim_dir()
    #get the path from manim to the input sanim file
    parts = get_sanim_source_file_name().replace('/', os.sep).split(os.sep)
    #but remove the file itself
    parts = parts[:-1]
    sub_path = os.path.join(*parts)
    res = os.path.join(manim_path, sub_path)
    return res

def get_movie_output_directory(scene_class, camera_config, frame_duration):
    if in_sanim_mode():
        return get_sanim_source_dir()

    directory = get_scene_output_directory(scene_class)
    sub_dir = "%dp%d" % (
        camera_config["pixel_height"],
        int(1.0 / frame_duration)
    )
    return guarantee_existance(os.path.join(directory, sub_dir))

def get_image_output_directory(scene_class, sub_dir="images"):
    if in_sanim_mode():
        return get_sanim_source_dir()

    directory = get_scene_output_directory(scene_class)
    return guarantee_existance(os.path.join(directory, sub_dir))
