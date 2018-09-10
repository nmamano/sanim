import inspect
import os

from constants import ANIMATIONS_DIR, SANIM_AUX_FILE


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

def get_sanim_source_dir():
    if not in_sanim_mode():
        sys.exit("shouldn't ask for sanim source dir if not in sanim mode")

    #get folder of this file
    utils_path = os.path.dirname(os.path.realpath(__file__))
    # print('utils_path', utils_path)
    #remove the /utils part to get the manim folder
    parts = utils_path.split(os.path.sep)
    # print('parts', parts)
    parts = parts[:-1]
    # print('parts', parts)
    manim_path = os.path.join(*parts)
    manim_path = "C:\\"+manim_path[2:] #not sure the join above misses one bar??
    # print('manim_path', manim_path)
    #get the path from manim to the input sanim file
    parts = get_sanim_source_file_name().split('/')
    # print('parts:',parts)
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
