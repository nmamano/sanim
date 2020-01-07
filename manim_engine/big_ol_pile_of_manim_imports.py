"""
I won't pretend like this is best practice, by in creating animations for a video,
it can be very nice to simply have all of the Mobjects, Animations, Scenes, etc.
of manim available without having to worry about what namespace they come from.

Rather than having a large pile of "from <module> import *" at the top of every such
script, the intent of this file is to make it so that one can just include
"from big_ol_pile_of_manim_imports import *".  The effects of adding more modules
or refactoring the library on current or older scene scripts should be entirely
addressible by changing this file.

Note: One should NOT import from this file for main library code, it is meant only
as a convenience for scripts creating scenes for videos.
"""


from manim_engine.constants import *
from manim_engine.animation.animation import *
from manim_engine.animation.composition import *
from manim_engine.animation.creation import *
from manim_engine.animation.indication import *
from manim_engine.animation.movement import *
from manim_engine.animation.numbers import *
from manim_engine.animation.rotation import *
from manim_engine.animation.specialized import *
from manim_engine.animation.transform import *
from manim_engine.animation.update import *
from manim_engine.camera.camera import *
from manim_engine.camera.mapping_camera import *
from manim_engine.camera.moving_camera import *
from manim_engine.camera.three_d_camera import *
from manim_engine.continual_animation.continual_animation import *
from manim_engine.continual_animation.from_animation import *
from manim_engine.continual_animation.numbers import *
from manim_engine.continual_animation.update import *
from manim_engine.mobject.coordinate_systems import *
from manim_engine.mobject.frame import *
from manim_engine.mobject.functions import *
from manim_engine.mobject.geometry import *
from manim_engine.mobject.matrix import *
from manim_engine.mobject.mobject import *
from manim_engine.mobject.number_line import *
from manim_engine.mobject.numbers import *
from manim_engine.mobject.probability import *
from manim_engine.mobject.shape_matchers import *
from manim_engine.mobject.svg.brace import *
from manim_engine.mobject.svg.drawings import *
from manim_engine.mobject.svg.svg_mobject import *
from manim_engine.mobject.svg.tex_mobject import *
from manim_engine.mobject.three_dimensions import *
from manim_engine.mobject.types.image_mobject import *
from manim_engine.mobject.types.point_cloud_mobject import *
from manim_engine.mobject.types.vectorized_mobject import *
from manim_engine.mobject.value_tracker import *
from manim_engine.for_3b1b_videos.common_scenes import *
from manim_engine.for_3b1b_videos.pi_creature import *
from manim_engine.for_3b1b_videos.pi_creature_animations import *
from manim_engine.for_3b1b_videos.pi_creature_scene import *
from manim_engine.once_useful_constructs.arithmetic import *
from manim_engine.once_useful_constructs.combinatorics import *
from manim_engine.once_useful_constructs.complex_transformation_scene import *
from manim_engine.once_useful_constructs.counting import *
from manim_engine.once_useful_constructs.fractals import *
from manim_engine.once_useful_constructs.graph_theory import *
from manim_engine.once_useful_constructs.light import *
from manim_engine.scene.graph_scene import *
from manim_engine.scene.moving_camera_scene import *
from manim_engine.scene.reconfigurable_scene import *
from manim_engine.scene.scene import *
from manim_engine.scene.sample_space_scene import *
from manim_engine.scene.graph_scene import *
from manim_engine.scene.scene_from_video import *
from manim_engine.scene.three_d_scene import *
from manim_engine.scene.vector_space_scene import *
from manim_engine.scene.zoomed_scene import *
from manim_engine.utils.bezier import *
from manim_engine.utils.color import *
from manim_engine.utils.config_ops import *
from manim_engine.utils.images import *
from manim_engine.utils.iterables import *
from manim_engine.utils.output_directory_getters import *
from manim_engine.utils.paths import *
from manim_engine.utils.rate_functions import *
from manim_engine.utils.simple_functions import *
from manim_engine.utils.sounds import *
from manim_engine.utils.space_ops import *
from manim_engine.utils.strings import *

# Non manim libraries that are also nice to have without thinking

import inspect
import itertools as it
import numpy as np
import operator as op
import os
import random
import re
import string
import sys
import math

from PIL import Image
from colour import Color
