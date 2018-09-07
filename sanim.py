#!/usr/bin/env python

from big_ol_pile_of_manim_imports import *

SCREEN_WIDTH = 14
HORIZONTAL_SEPARATOR = 1

class Sanim(Scene):

    def construct(self):
        source_file = "sanim_input.txt"
        input_lines = open(source_file).read().splitlines()
        raw_sobjects = get_raw_sobjects(input_lines)
        sobjects = get_sobjects(raw_sobjects)
        arrange_sobjects(sobjects)
        sobject_list = []
        for line in sobjects:
            if type(line) is list:
                sobject_list += line
            else:
                sobject_list.append(line)
        i = 0
        while i < len(sobject_list):
            sobjs_to_play = [sobject_list[i]]
            while not sobject_list[i].wait_for_input:
                i += 1
                sobjs_to_play.append(sobject_list[i])
            i += 1
            self.play(*[Write(sobject) for sobject in sobjs_to_play])


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
                line.to_edge(LEFT)
            prev_obj = line
        else:
            if prev_obj is None:
                sys.exit('bug')
            is_first = True
            for sobj in line:
                if is_first:
                    sobj.next_to(prev_obj.get_corner(DOWN+LEFT), DOWN)
                    sobj.to_edge(LEFT)
                    is_first = False
                else:
                    sobj.next_to(prev_obj.get_edge_center(RIGHT),RIGHT)

                prev_obj = sobj


class SObject(VGroup):

    def __init__(self, text, max_width, wait_for_input):
        self.text = text
        self.max_width = max_width
        self.SOtype = text.split()[0]
        self.content = text[len(self.SOtype)+1:]
        self.wait_for_input = wait_for_input
        self.time_stamp = None #this will be updated later

        if self.SOtype == 'TITLE':
            self.vline = makeTitle(self.content, max_width)
        elif self.SOtype == 'DEF':
            self.vline = makeDef(self.content, max_width)
        elif self.SOtype == '-':
            self.vline = makeBullet(self.content, max_width)
        elif self.SOtype == '*':
            self.vline = makePlaneLine(self.content, max_width)
        elif self.SOtype == 'SCENE':
            self.vline = makeScene(self.content, max_width)
        elif self.SOtype == 'IMAGE':
            self.vline = makeImage(self.content, max_width)
        else:
            sys.exit('unexpected type')
        super().__init__(self.vline)

def makeTitle(content, width):
    return TextMobject(content);

def makeDef(content, width):
    term = content.split()[0]
    definition = content[len(term)+1:]
    return TextMobject('- '+term+': '+definition)

def makeBullet(content, width):
    return TextMobject('- '+content)

def makePlaneLine(content, width):
    return TextMobject(content)

def makeScene(content, width):
    return TextMobject('not implemented')

def makeImage(content, width):
    return TextMobject('not implemented')
