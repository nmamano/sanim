#!/usr/bin/env python

from big_ol_pile_of_manim_imports import *

# To watch one of these scenes, run the following:
# python extract_scene.py file_name <SceneName> -p
#
# Use the flat -l for a faster rendering at a lower
# quality, use -s to skip to the end and just show
# the final frame, and use -n <number> to skip ahead
# to the n'th animation of a scene.

class KnightTest(Scene):
    CONFIG = {
    "plane_kwargs" : {
        "color" : RED_B
        },
    "point_charge_loc" : 0.5*RIGHT-1.5*UP,
    }
    def construct(self):
        svg_file = os.path.join(
            SVG_IMAGE_DIR,
            "knight.svg"
        )
        knight = SVGMobject(file_name=svg_file)
        svg_file = os.path.join(
            SVG_IMAGE_DIR,
            "stick_man.svg"
        )
        other = SVGMobject(file_name=svg_file)
        self.add(knight)
        knight.generate_target()
        knight.move_to((UP+LEFT+LEFT))
        self.play(MoveToTarget(knight))
        knight.generate_target()
        knight.move_to((UP+RIGHT+RIGHT))
        self.play(MoveToTarget(knight))
        self.play(Transform(knight,other))
        self.wait()
