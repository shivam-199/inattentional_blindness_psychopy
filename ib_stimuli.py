import psychopy.visual
import psychopy.gui
import psychopy.core
import random
import sys
import math
import numpy as np

stimuli_count = 8
clock = psychopy.core.Clock()


def movement(stimuli_list, window, fixation, line, unexpectedStim, showObject=False, slow=False):
    clock.reset()
    i = 0
    speed_of_stimuli = 3
    low_speed_of_object = 2.25
    high_speed_of_object = 4.5
    object_speed = low_speed_of_object if slow else high_speed_of_object
    pass_count = 0

    while clock.getTime() < 8:
        if showObject:
            unexpectedStim.pos = [unexpectedStim.pos[0] - object_speed, unexpectedStim.pos[1]]
            unexpectedStim.draw()
        for textStim in stimuli_list:
            stim = textStim["stim"]
            if 1.5 >= stim.pos[1] >= -1.5:  # and stim.color == "#0000FF":
                print("pass")
                pass_count += 1
            if stim.pos[0] >= 390:
                textStim["x_dir"] *= -1
            elif stim.pos[0] <= -390:
                textStim["x_dir"] *= -1
            elif stim.pos[1] >= 290:
                textStim["y_dir"] *= -1
            elif stim.pos[1] <= -290:
                textStim["y_dir"] *= -1

            stim.pos = [stim.pos[0] + speed_of_stimuli * textStim["x_dir"], stim.pos[1] + speed_of_stimuli * textStim["y_dir"]]
            stim.size = 2
            stim.draw()
            fixation.draw()
            line.draw()
        window.flip()
        i += 1
    window.flip()
    return pass_count


def experimental_setup(window):
    # creating a white background
    whiteScreen = psychopy.visual.Rect(
        win=window,
        units="pix",
        width="800",
        height="600",
        fillColor=[1] * 3,
        lineColor=[1] * 3,
    )
    window.color = [1, 1, 1]
    stimuli_list = []

    # horizontal line
    line = psychopy.visual.Line(
        win=window,
        start=(-400, 0),
        end=(400, 0),
        lineColor=[-1] * 3
    )

    # fixation square
    fixation = psychopy.visual.Rect(
        win=window,
        units="pix",
        width="10",
        height="10",
        fillColor=[-1] * 3,
        lineColor=[-1] * 3,
    )

    # generating unexpected object
    stimPos = random.choice([-1, 1])
    unexpectedStim = psychopy.visual.TextStim(
        win=window,
        text="X",
        color="#E4E4E4",
        pos=[390, 15 * stimPos]
    )

    # generating text stimuli
    for i in range(stimuli_count):
        text = "T" if i % 2 == 0 else "L"
        color = "#0000FF" if i < stimuli_count/2 else "#FF0000"
        textDict = {
            # "slope": random.uniform(0, sys.maxsize),
            # "intercept": random.uniform(-290, 290),
            "x_dir": random.choice([-1, 1]),
            "y_dir": random.choice([-1, 1]),
            "stim": psychopy.visual.TextStim(
                win=window,
                text=text,
                color=color,
                pos=[random.uniform(-380, 380), random.uniform(-280, 280)],

            )
        }
        stimuli_list.append(textDict)
    return whiteScreen, fixation, line, stimuli_list, unexpectedStim, stimPos
