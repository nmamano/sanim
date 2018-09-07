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
        for line in sobjects:
            for sobject in line:
                self.play(Write(sobject.vline))


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
                res.append([line])
    return res

def get_sobjects(raw_sobjects):
    res = []
    for line in raw_sobjects:
        res.append([])
        num_sobjects = len(line)
        if num_sobjects == 1:
            max_width = SCREEN_WIDTH
        else:
            max_width = (SCREEN_WIDTH-HORIZONTAL_SEPARATOR*(num_sobjects+1))/num_sobjects
        for raw_sobject in line:
            wait_for_input = True
            if raw_sobject[0] == '>':
                wait_for_input = False
                raw_sobject = raw_sobject[1:]
            res[-1].append(SObject(raw_sobject, max_width, wait_for_input))
    return res

class SObject():

    def __init__(self, text, max_width, wait_for_input):
        self.text = text
        self.max_width = max_width
        self.type = text.split()[0]
        self.content = text[len(self.type)+1:]
        self.wait_for_input = wait_for_input
        self.time_stamp = None #this will be updated later

        if self.type == 'TITLE':
            self.vline = makeTitle(self.content, max_width)
        elif self.type == 'DEF':
            self.vline = makeDef(self.content, max_width)
        elif self.type == '-':
            self.vline = makeBullet(self.content, max_width)
        elif self.type == '*':
            self.vline = makePlaneLine(self.content, max_width)
        elif self.type == 'SCENE':
            self.vline = makeScene(self.content, max_width)
        elif self.type == 'IMAGE':
            self.vline = makeImage(self.content, max_width)
        else:
            sys.exit('unexpected type')

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
