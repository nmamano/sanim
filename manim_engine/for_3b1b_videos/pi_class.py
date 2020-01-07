import numpy as np
import warnings

from manim_engine.constants import *
from manim_engine.mobject.types.vectorized_mobject import VGroup
from manim_engine.for_3b1b_videos.pi_creature import PiCreature

class PiCreatureClass(VGroup):
    CONFIG = {
        "width" : 3,
        "height" : 2
    }

    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        for i in range(self.width):
            for j in range(self.height):
                pi = PiCreature().scale(0.3)
                pi.move_to(i*DOWN + j* RIGHT)
                self.add(pi)


