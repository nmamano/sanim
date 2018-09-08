#!/usr/bin/env python

from big_ol_pile_of_manim_imports import *

SCREEN_WIDTH = 14
HORIZONTAL_SEPARATOR = 1
BACKGROUND = "#cceeff"
DEF_COLOR = "#991f00"
class Sanim(Scene):
    CONFIG = {
        "camera_config": {"background_color": BACKGROUND}
    }
    def construct(self):
        source_file = "sanim_input2.txt"
        input_lines = open(source_file).read().splitlines()
        raw_sobjects = get_raw_sobjects(input_lines)
        sobjects = get_sobjects(raw_sobjects)
        arrange_sobjects(sobjects)
        self.play_animations(sobjects)

    def play_animations(self, sobjects):
        sobject_list = []
        for line in sobjects:
            if type(line) is list:
                sobject_list += line
            else:
                sobject_list.append(line)
        i = 0
        while i < len(sobject_list):
            if not sobject_list[i].visible:
                i += 1
                continue
            sobjs_to_play = [sobject_list[i]]
            i += 1
            while i < len(sobject_list) and not sobject_list[i].wait_for_input:
                if sobject_list[i].visible:
                    sobjs_to_play.append(sobject_list[i])
                i += 1
            self.play(*[Write(sobject) for sobject in sobjs_to_play], run_time=0.8)


def get_raw_sobjects(input_lines):
    res = []
    in_horizontal_group = False
    for line in input_lines:
        if line[0] == '(':
            if in_horizontal_group:
                sys.exit("found '(' inside '('")
            in_horizontal_group = True
            res.append([])
        elif line[0] == ')':
            if not in_horizontal_group:
                sys.exit("found ')' before '('")
            in_horizontal_group = False
        else:
            if in_horizontal_group:
                res[-1].append(line)
            else:
                res.append(line)
    return res

def get_sobjects(raw_sobjects):
    res = []
    for line in raw_sobjects:
        if type(line) is not list:
            if line[0] == '>':
                res.append(SObject(line[1:], SCREEN_WIDTH, False))
            else:
                res.append(SObject(line, SCREEN_WIDTH, True))
        else:
            res.append([])
            num_sobjects = len(line)
            max_width = (SCREEN_WIDTH-HORIZONTAL_SEPARATOR*(num_sobjects+1))/num_sobjects
            for raw_sobject in line:
                if raw_sobject[0] == '>':
                    res[-1].append(SObject(raw_sobject[1:], max_width, False))
                else:
                    res[-1].append(SObject(raw_sobject, max_width, True))
    return res

def arrange_sobjects(sobjects):
    prev_obj = None
    for line in sobjects:
        if type(line) is not list:
            if prev_obj is None:
                line.to_edge(UP)
            else:
                line.next_to(prev_obj.get_corner(DOWN+LEFT), DOWN)
                if prev_obj.SOtype == "TITLE":
                    line.shift(DOWN)

                if line.SOtype == '-':
                   line.to_edge(LEFT, buff = MED_LARGE_BUFF)
                else:
                   line.to_edge(LEFT, buff = MED_SMALL_BUFF)
            prev_obj = line
        else:
            if prev_obj is None:
                sys.exit('bug')
            is_first = True
            numItems = len(line)
            i = 1
            for sobj in line:
                if is_first:
                    sobj.next_to(prev_obj.get_corner(DOWN+LEFT), DOWN)
                    if prev_obj.SOtype == "TITLE":
                        line.shift(DOWN)
                    is_first = False
                else:
                    sobj.next_to(prev_obj.get_edge_center(RIGHT),RIGHT)
                sobj.to_edge(LEFT, buff=0)
                sobj.shift(-1*LEFT*(sobj.get_edge_center(LEFT)-sobj.get_center()))
                sobj.shift(i*2*FRAME_X_RADIUS*RIGHT/(numItems+1))
                i += 1
                prev_obj = sobj


class SObject(VGroup):

    def __init__(self, text, max_width, wait_for_input):
        self.text = text
        self.max_width = max_width
        self.SOtype = text.split()[0]
        self.content = text[len(self.SOtype)+1:]
        self.wait_for_input = wait_for_input
        self.time_stamp = None #this will be updated later
        self.visible = True

        if self.SOtype == 'TITLE':
            self.vline = makeTitle(self.content, max_width)
        elif self.SOtype == 'DEF':
            self.vline = makeDef(self.content, max_width)
        elif self.SOtype == '-':
            self.vline = makeBullet(self.content, max_width)
        elif self.SOtype == '*':
            if self.content == '':
                self.visible = False
                self.vline = makePlaneLine("no show", max_width)
            else:
                self.vline = makePlaneLine(self.content, max_width)
        elif self.SOtype == 'SCENE':
            self.vline = makeScene(self.content, max_width)
        elif self.SOtype == 'IMAGE':
            self.vline = makeImage(self.content, max_width)
        else:
            sys.exit('unexpected type '+self.SOtype)
        super().__init__(self.vline)

def makeTitle(content, width):
    res = Title(content, scale_factor=1.3, color=BLACK, background_stroke_color=BACKGROUND);
    return res;

def makeDef(content, width):
    if content[0] != '"':
        sys.exit('term defined should be within "')
    i = 2
    while content[i] != '"':
        i += 1

    term = content[1:i]
    definition = content[i+1:].lstrip()

    res = TextMobject('\\textbf{'+term+'}:',definition, color=BLACK, background_stroke_color=BACKGROUND)
    res.set_color_by_tex(term, DEF_COLOR)
    res.buff = LARGE_BUFF
    return res

def makeBullet(content, width):
    return BulletedItem(content, color=BLACK, background_stroke_color=BACKGROUND)

def makePlaneLine(content, width):
    if len(content) == 0:
        sys.exit("empty line")
    return TextMobject(content, color=BLACK, background_stroke_color=BACKGROUND)

def makeScene(content, width):
    return TextMobject('not implemented')

def makeImage(content, width):
    return TextMobject('not implemented')
