import sys
import math

import numpy as np
import random
import win32api

import psychopy.visual
import psychopy.gui
import psychopy.core

stimuli_count = 8
clock = psychopy.core.Clock()


def stimuli_questions():
    response = {}
    while True:
        gui = psychopy.gui.Dlg(title="Personal Information", labelButtonOK="Submit", labelButtonCancel="Cancel")
        gui.addField("How many times did the red object touch/cross the middle line?")
        gui.addField("Did you notice anything other than the 8 letter?", choices=["", "Yes", "No"])
        gui.addText("Answer the below regardless of your previous answer.")
        gui.addField("Was the additional object above or below the line?", choices=["", "Above", "Below"])
        gui.addField("What was the shape of the object?", choices=["", "X", "O", "T", "L", "W"])
        gui.addField("What was the color of the object?", choices=["", "Red", "Green", "Blue", "Grey", "Black", "Cyan"])
        gui.show()
        if gui.OK:
            if "" in gui.data:
                win32api.MessageBox(0, "Please enter the required data.")
                continue
            response["pass_count_resp"] = gui.data[0]
            response["stimuli_seen"] = gui.data[1]
            response["stimuli_position"] = gui.data[2]
            response["stimuli_shape"] = gui.data[3]
            response["stimuli_color"] = gui.data[4]
        else:
            win32api.MessageBox(0, "Please enter the required data, exiting...")
            sys.exit("Please enter required data")
        break
    return response


def movement(stimuli_list, window, fixation, line, unexpectedStim, showObject=False, slow=False, trial=True):
    clock.reset()
    i = 0
    stimuli_trial_speed = 2.25
    stimuli_expt_speed = 4.5
    speed_of_stimuli = stimuli_trial_speed if trial else stimuli_expt_speed

    low_speed_of_object = 2.25
    high_speed_of_object = 4.5
    object_speed = low_speed_of_object if slow else high_speed_of_object

    pass_count = 0

    while clock.getTime() < 8:
        if showObject and clock.getTime() > 2.9:
            unexpectedStim.pos = [unexpectedStim.pos[0] - object_speed, unexpectedStim.pos[1]]
            unexpectedStim.draw()
        for textStim in stimuli_list:
            stim = textStim["stim"]
            if 1.5 >= stim.pos[1] >= -1.5 and stim.color == "#0000FF":
                pass_count += 1
            if stim.pos[0] >= 390:
                textStim["x_dir"] *= -1
            elif stim.pos[0] <= -390:
                textStim["x_dir"] *= -1
            elif stim.pos[1] >= 290:
                textStim["y_dir"] *= -1
            elif stim.pos[1] <= -290:
                textStim["y_dir"] *= -1

            # change the position of the stimuli
            stim.pos = [stim.pos[0] + speed_of_stimuli * textStim["x_dir"], stim.pos[1] + speed_of_stimuli * textStim["y_dir"]]
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
