#!/usr/bin/env python

from big_ol_pile_of_manim_imports import *
import shutil

BACKGROUND = "#e6f3ff"
DEF_COLOR = "#991f00"
DEFAULT_RUNTIME = 0.8
FLUSH_RUNTIME = 0.8
#having some space between transitions allows the javascript to be more sloppy with the pausing times
#the transitions are set to be in the middle of the wait time between transitions
#eg, if there is a wait of 0.2s between transitions, then the player can run 0.1 longer than it should
#and it wuld not be noticed
WAIT_TIME = 0.2
FLUSH_WAIT_TIME = 0.2 #0.8 #same
#lines starting with this add text to the presentation
CONTENT_KEYWORDS = {"TITLE", "DEF", "-", "PLAIN"}

#lines starting with this give instructions about how to display the presentation
COMMAND_KEYWORDS = {"FLUSH"}

#modifiers are the only keywords that can appear before other keywords
#(and nowhere else)
MODIFIER_SYMBOLS = {">", "^"} #^ not implemented yet


#a line of text plus its line number in the source file
#it breaks it down into its basic components
class InputLine:
    def __init__(self, line_num, raw_content):
        #line_num is used to flush up to a certian line with the FLUSH keyword
        self.line_num = line_num
        #keep the original line intact just in case
        self.raw_content = raw_content[:]
        self.raw_input_elems = raw_content.split(';')
        self.input_elems = [InputElem(elem) for elem in self.raw_input_elems]
        self.output_content_elems = []
        for elem in self.input_elems:
            if elem.keyword == "TITLE":
                self.output_content_elems.append(TitleElem(elem))
            elif elem.keyword == "PLAIN":
                self.output_content_elems.append(PlainElem(elem))
            elif elem.keyword == "-":
                self.output_content_elems.append(BulletElem(elem))
            elif elem.keyword == "DEF":
                self.output_content_elems.append(DefElem(elem))

    def is_content_line(self):
        return self.output_content_elems != []

    def get_fade_out_actions(self):
        res = []
        for elem in self.output_content_elems:
            res += elem.get_fade_out_actions()
        return res

class InputElem:
    def __init__(self, raw_content):
        if ';' in raw_content:
            sys.exit('internal parsing error: input element cannot contain ";"')

        #keep the raw content just in case
        self.raw_content = raw_content[:]

        #parse modifiers
        self.modifiers = []
        i = 0
        while i < len(raw_content) and (raw_content[i] == ' ' or raw_content[i] in MODIFIER_SYMBOLS):
            if raw_content[i] in MODIFIER_SYMBOLS:
                self.modifiers.append(raw_content[i])
            i += 1
        while i < len(raw_content) and raw_content[i] == ' ':
            i += 1

        #parse keyword
        raw_content = raw_content[i:] #everything except modifiers and trailing white space
        potential_keyword = raw_content[:raw_content.find(' ')]
        if potential_keyword in CONTENT_KEYWORDS or potential_keyword in COMMAND_KEYWORDS:
            self.keyword = potential_keyword
            self.content = raw_content[raw_content.find(' ')+1:]
        else:
            #no keyword means that this is just plain text
            self.keyword = "PLAIN" #'fake' keyword introduced by us
            self.content = raw_content
            if self.content == '':
                self.modifiers.append('>') #never wait for empty input

        self.keyword_type = 'content' if self.keyword in CONTENT_KEYWORDS else 'command'

class OutputElem:
    def __init__(self, input_elem):
        self.input_elem = input_elem
        if '>' in input_elem.modifiers:
            self.wait_for_input = False
        else: self.wait_for_input = True

    def individual_play(self, scene):
        pass

    def get_play_actions(self):
        pass

    def individual_play_duration(self):
        pass

    def position_center_at(self, pos_mobj):
        pass

    def position_left_aligned(self, pos_mobj):
        pass

    def get_shift_center_at_actions(self, pos_mobj):
        pass

    def get_shift_left_aligned_actions(self, pos_mobj):
        pass

    def get_bottom_right_mobject(self):
        pass

    def get_fade_out_actions(self):
        pass

    def copy(self):
        pass

class TitleElem(OutputElem):
    def __init__(self, input_elem):
        super().__init__(input_elem)
        content = input_elem.content
        if content == '':
            sys.exit('empty title')
        self.run_time = 1.1+len(content)/200
        self.text = Title(content, scale_factor=1.3, color=BLACK, background_stroke_color=BACKGROUND)

    def copy(self):
        return TitleElem(self.input_elem)

    def individual_play(self, scene):
        scene.play(Write(self.text), run_time=self.run_time)

    def get_play_actions(self):
        return [Write(self.text)]

    def individual_play_duration(self):
        return self.run_time

    def position_center_at(self, pos_mobj):
        self.text.move_to(pos_mobj)

    def position_left_aligned(self, pos_mobj):
        self.text.center()
        self.text.to_edge(UP)

    def get_shift_center_at_actions(self, pos_mobj):
        return [ApplyMethod(self.text.move_to, pos_mobj)]

    def get_shift_left_aligned_actions(self, pos_mobj):
        sys.exit("not implemented")
        pos_title = TextMobject("aux") #used only for positioning
        pos_title.center()
        pos_title.to_edge(UP)
        return [ApplyMethod(self.text.move_to, pos_title, alignment=LEFT)]

    def get_bottom_right_mobject(self):
        return self.text

    def get_fade_out_actions(self):
        return [FadeOut(self.text)]

class PlainElem(OutputElem):
    def __init__(self, input_elem):
        super().__init__(input_elem)
        content = input_elem.content
        if content == '':
            self.text = TextMobject("aux") #this is never displayed but allows the empty object to
                                           #be positioned and return its position,
                                           #which can be useful since empty elems occupy space anyway
            self.run_time = 0
            self.is_empty = True
        else:
            self.text = TextMobject(content, color=BLACK, background_stroke_color=BACKGROUND)
            self.run_time = 0.6+len(content)/150
            self.is_empty = False

    def copy(self):
        return PlainElem(self.input_elem)

    def individual_play(self, scene):
        if self.is_empty:
            return
        scene.play(Write(self.text), run_time=self.run_time)

    def get_play_actions(self):
        if self.is_empty:
            return []
        return [Write(self.text)]

    def individual_play_duration(self):
        return self.run_time

    def position_center_at(self, pos_mobj):
        self.text.move_to(pos_mobj)

    def position_left_aligned(self, pos_mobj):
        self.text.move_to(pos_mobj)
        self.text.to_edge(LEFT)

    def get_shift_center_at_actions(self, pos_mobj):
        if self.is_empty:
            return []
        return [ApplyMethod(self.text.move_to, pos_mobj)]

    def get_shift_left_aligned_actions(self, pos_mobj):
        if self.is_empty:
            return []
        pos_text = TextMobject("aux") #used only for positioning
        pos_text.move_to(pos_mobj)
        pos_text.to_edge(LEFT)
        return [ApplyMethod(self.text.move_to, pos_text)]

    def get_bottom_right_mobject(self):
        return self.text

    def get_fade_out_actions(self):
        if self.is_empty:
            return []
        return [FadeOut(self.text)]

class BulletElem(OutputElem):
    def __init__(self, input_elem):
        super().__init__(input_elem)
        content = input_elem.content
        if content == '':
            sys.exit("empty bullet item")
        self.text = BulletedItem(content, color=BLACK, background_stroke_color=BACKGROUND)
        self.run_time = 0.6+len(content)/150

    def copy(self):
        return BulletElem(self.input_elem)

    def individual_play(self, scene):
        scene.play(Write(self.text), run_time=self.run_time)

    def get_play_actions(self):
        return [Write(self.text)]

    def individual_play_duration(self):
        return self.run_time

    def position_center_at(self, pos_mobj):
        self.text.move_to(pos_mobj)

    def position_left_aligned(self, pos_mobj):
        self.text.move_to(pos_mobj)
        self.text.to_edge(LEFT)

    def get_shift_center_at_actions(self, pos_mobj):
        return [ApplyMethod(self.text.move_to, pos_mobj)]

    def get_shift_left_aligned_actions(self, pos_mobj):
        pos_text = BulletedItem(self.input_elem.content) #used only for positioning
        pos_text.move_to(pos_mobj)
        pos_text.to_edge(LEFT)
        return [ApplyMethod(self.text.move_to, pos_text)]

    def get_bottom_right_mobject(self):
        return self.text

    def get_fade_out_actions(self):
        return [FadeOut(self.text)]

class DefElem(OutputElem):
    def __init__(self, input_elem):
        super().__init__(input_elem)
        content = input_elem.content[:]
        #parse content to extract term and definition
        content = content.lstrip() #removes leading whitespace
        if content[0] != '"':
            sys.exit('invalid use of DEF. syntax: DEF "term" definition')
        content = content[1:]
        if not '"' in content:
            sys.exit('invalid use of DEF. syntax: DEF "term" definition')
        self.term_text = content[:content.find('"')]
        self.defi_text = content[content.find('"')+1:]
        self.defi_text.lstrip()
        if self.term_text == '':
            sys.exit('empty term in DEF')
        if self.defi_text == '':
            sys.exit('empty definition in DEF')

        self.term = TextMobject('\\textbf{'+self.term_text+'}:',background_stroke_color=BACKGROUND, alignment="")
        self.term.set_color(DEF_COLOR)
        self.defi = TextMobject(self.defi_text,color=BLACK, background_stroke_color=BACKGROUND, alignment="")
        #res.buff = LARGE_BUFF #not sure why this was here

        self.term_run_time = 0.5
        self.in_between_time = 0.1
        self.defi_run_time = 0.6+len(self.defi_text)/150

    def copy(self):
        return DefElem(self.input_elem)

    def individual_play(self, scene):
        scene.play(Write(self.term), run_time=self.term_run_time)
        scene.wait(self.in_between_time)
        scene.play(Write(self.defi), run_time=self.defi_run_time)

    def get_play_actions(self):
        return [Write(self.term), Write(self.defi)]

    def individual_play_duration(self):
        return self.term_run_time + self.in_between_time + self.defi_run_time

    def position_center_at(self, pos_mobj):
        self.term.move_to(pos_mobj)
        self.defi.next_to(self.term, RIGHT)
        self.defi.align_to(self.term, UP)

    def position_left_aligned(self, pos_mobj):
        self.term.move_to(pos_mobj)
        self.term.to_edge(LEFT)
        self.defi.next_to(self.term, RIGHT)
        self.defi.align_to(self.term, UP)

    def get_shift_center_at_actions(self, pos_mobj):
        pos_term = TextMobject(self.term_text, alignment = "") #used for positioning
        pos_defi = TextMobject(self.defi_text, alignment = "") #used for positioning
        pos_term.move_to(pos_mobj)
        pos_defi.next_to(pos_term, RIGHT)
        pos_defi.align_to(pos_term, UP)
        return [ApplyMethod(self.term.move_to, pos_term), ApplyMethod(self.defi.move_to, pos_defi)]

    def get_shift_left_aligned_actions(self, pos_mobj):
        pos_term = TextMobject(self.term_text, alignment = "") #used for positioning
        pos_defi = TextMobject(self.defi_text, alignment = "") #used for positioning
        pos_term.move_to(pos_mobj)
        pos_term.to_edge(LEFT)
        pos_defi.next_to(pos_term, RIGHT)
        pos_defi.align_to(pos_term, UP)
        return [ApplyMethod(self.term.move_to, pos_term), ApplyMethod(self.defi.move_to, pos_defi)]

    def get_bottom_right_mobject(self):
        return self.defi

    def get_fade_out_actions(self):
        return [FadeOut(self.term), FadeOut(self.defi)]

def display_animation_buffer(anim_buffer, scene, time_stamps):
    if len(anim_buffer) == 0:
        return
    if len(anim_buffer) == 1:
        elem = anim_buffer[0]
        elem.individual_play(scene)
    else:
        actions = []
        for elem in anim_buffer:
            actions += elem.get_play_actions()
        scene.play(*actions, run_time=DEFAULT_RUNTIME)

    anim_buffer.clear()

    time_stamps.append(scene.current_scene_time+WAIT_TIME/2)
    scene.wait(WAIT_TIME)

def add_elem_to_anim_buffer(elem, anim_buffer, scene, time_stamps):
    if elem.wait_for_input:
        display_animation_buffer(anim_buffer, scene, time_stamps)
    anim_buffer.append(elem)

def get_top_left_pos():
    res = TextMobject("aux") #used only for its positioninig
    res.to_corner(TOP+LEFT, buff=MED_SMALL_BUFF)
    return res

def animate_content_line(line, curr_pos, anim_buffer, scene, time_stamps):
    elems = line.output_content_elems
    if len(elems) == 1:
        elem = elems[0]
        elem.position_left_aligned(curr_pos)
        curr_pos.move_to(elem.get_bottom_right_mobject().get_edge_center(DOWN))
        add_elem_to_anim_buffer(elem, anim_buffer, scene, time_stamps)
    else:
        num_elems = len(elems)
        i = 1
        for elem in elems:
            curr_pos.to_edge(LEFT, buff=0)
            curr_pos.shift(RIGHT*(curr_pos.get_edge_center(LEFT)-curr_pos.get_center()))
            curr_pos.shift(i*2*FRAME_X_RADIUS*RIGHT/(num_elems+1))
            elem.position_center_at(curr_pos)
            i += 1
            add_elem_to_anim_buffer(elem, anim_buffer, scene, time_stamps)
        curr_pos.move_to(elems[-1].get_bottom_right_mobject().get_edge_center(DOWN))

    curr_pos.shift(DOWN*0.5)

def get_shift_actions(line, curr_pos):
    elems = line.output_content_elems
    res = []
    if len(elems) == 0:
        return []
    if len(elems) == 1:
        elem = elems[0]
        #actions = get_shift_left_aligned_actions(curr_pos)
        res += elem.get_shift_left_aligned_actions(curr_pos)
        elem_copy = elem.copy()
        elem_copy.position_left_aligned(curr_pos)
        curr_pos.move_to(elem_copy.get_bottom_right_mobject().get_edge_center(DOWN))
    else:
        num_elems = len(elems)
        i = 1
        for elem in elems:
            curr_pos.to_edge(LEFT, buff=0)
            curr_pos.shift(RIGHT*(curr_pos.get_edge_center(LEFT)-curr_pos.get_center()))
            curr_pos.shift(i*2*FRAME_X_RADIUS*RIGHT/(num_elems+1))
            res += elem.get_shift_center_at_actions(curr_pos)
            i += 1
        elem_copy = elems[-1].copy()
        elem_copy.position_center_at(curr_pos)
        curr_pos.move_to(elem_copy.get_bottom_right_mobject().get_edge_center(DOWN))

    curr_pos.shift(DOWN*0.5)
    return res


def animate_lines(lines, scene):
    flush_index = 0 #starting line to flush when using flush
    animation_buffer = []
    scene.wait(WAIT_TIME)
    time_stamps = [WAIT_TIME/2] #for the web
    curr_pos = get_top_left_pos()
    for line in lines:
        #scene.play(Write(curr_pos))
        if line.is_content_line():
            animate_content_line(line, curr_pos, animation_buffer, scene, time_stamps)
        else:
            elems = line.input_elems
            if len(elems) == 0:
                sys.exit("empty line")
            if len(elems) > 1:
                sys.exit("more than one command in a line")
            elem = elems[0]
            if elem.keyword == 'FLUSH':
                display_animation_buffer(animation_buffer, scene, time_stamps) #leftover stuff
                flush_line_num = int(elem.content)
                curr_line_num = line.line_num
                if flush_line_num > curr_line_num:
                    sys.exit("cannot flush beyond the current line")
                fade_out_actions = []
                while lines[flush_index].line_num < flush_line_num:
                    if lines[flush_index].is_content_line():
                        fade_out_actions += lines[flush_index].get_fade_out_actions()
                    flush_index += 1
                curr_pos = get_top_left_pos()
                shift_actions = []
                i = flush_index
                while lines[i].line_num < curr_line_num:
                    shift_actions += get_shift_actions(lines[i], curr_pos)
                    i += 1
                scene.play(*fade_out_actions, *shift_actions, run_time=FLUSH_RUNTIME)

                time_stamps.append(scene.current_scene_time+FLUSH_WAIT_TIME/2)
                scene.wait(FLUSH_WAIT_TIME)

            else:
                sys.exit("unknown command")
    display_animation_buffer(animation_buffer, scene, time_stamps) #leftover stuff
    return time_stamps

#note that the first line has index 1 (because my editor starts counting at 1...)
def input_to_lines(source_file):
    input_lines = open(source_file).read().splitlines()
    res = []
    i = 1
    for line in input_lines:
        if line == "":
            pass
            # sys.exit("empty line "+str(i))
        else:
            res.append(InputLine(i, line))
        i += 1
    return res


class Sanim(Scene):
    CONFIG = {
        "camera_config": {"background_color": BACKGROUND}
    }
    def construct(self):
        with open(SANIM_AUX_FILE, "r") as sanim_file:
                source_file = sanim_file.read()
        lines = input_to_lines(source_file)
        print("finished parsing")
        time_stamps = animate_lines(lines, self)
        source_folder = get_sanim_source_dir()
        web_info_file = os.path.join(source_folder,SANIM_TIME_STAMPS_FILE)
        with open(web_info_file, 'w') as web_file:
            web_file.write("var timeStamps = "+str([round(stmp, 4) for stmp in time_stamps])+"\n")
        source_html = os.path.join(get_main_manim_dir(), SANIM_HTML_FILE)
        dest_html = os.path.join(source_folder, SANIM_LOCAL_HTML_FILE)
        shutil.copyfile(source_html, dest_html)
