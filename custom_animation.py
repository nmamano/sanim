from manim_engine.big_ol_pile_of_manim_imports import *

# Custom animation for text with a unique reveal style
class CustomWrite(DrawBorderThenFill):
    CONFIG = {
        "rate_func": lambda t: smooth(1.5 * t - 0.5 * np.sin(t * np.pi)),
        "submobject_mode": "lagged_start",
        "stroke_color": "#333333",  # Darker stroke for better contrast
    }

    def __init__(self, mob_or_text, **kwargs):
        digest_config(self, kwargs)
        if isinstance(mob_or_text, str):
            mobject = TextMobject(mob_or_text)
        else:
            mobject = mob_or_text
        if "run_time" not in kwargs:
            self.establish_run_time(mobject)
        if "lag_factor" not in kwargs:
            if len(mobject.family_members_with_points()) < 4:
                min_lag_factor = 1
            else:
                min_lag_factor = 1.5
            self.lag_factor = max(self.run_time - 1, min_lag_factor)
        DrawBorderThenFill.__init__(self, mobject, **kwargs)

    def establish_run_time(self, mobject):
        num_subs = len(mobject.family_members_with_points())
        if num_subs < 15:
            self.run_time = 1.2  # Slightly slower for emphasis
        else:
            self.run_time = 2.2