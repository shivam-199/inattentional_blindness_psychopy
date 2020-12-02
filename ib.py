import os
import sys

import numpy as np

import psychopy.visual
import psychopy.gui
import psychopy.core
import random
from ib_stimuli import experimental_setup, movement

window = psychopy.visual.Window(
    size=[800, 600],
    units="pix",
    fullscr=False,
)

clock = psychopy.core.Clock()

instructions = psychopy.visual.TextStim(
    win=window,
    wrapWidth=600,
)

instructions.text = """
Focus on the central square by default. \n
When the experiment starts count the number of times the red stimulus passes or touches the central line.\n
Press 'T' to continue or 'Q' to exit.
"""

instructions.draw()
window.flip()

trials = 16


blankScreen = psychopy.visual.Rect(
    win=window,
    units="pix",
    width="800",
    height="600",
    fillColor=[-1] * 3,
    lineColor=[-1] * 3,
)
keys = psychopy.event.waitKeys(keyList=["T", "t", "q", "Q"])
window.flip()
if "T" in keys or "t" in keys:
    for trial_index in range(1):
        '''
            per trial, 
            600ms frozen start screen, 
            8000ms of stimuli movement, 
            300ms frozen screen to facilitate ambiguous counting decisions
        '''
        print("Trial {}".format(trial_index))
        showObject = True
        slow = random.choice([True, False])  # Record in response
        clock.reset()
        while clock.getTime() < 0.6:
            blankScreen.draw()
            window.flip()
        clock.reset()
        whiteScreen, fixation, line, stimuli_list, unexpectedStim, stimPos = experimental_setup(window)
        pass_count = movement(stimuli_list, window, fixation, line, unexpectedStim, showObject)
        print(pass_count)
        clock.reset()
        window.flip()
        while clock.getTime() < 0.3:
            blankScreen.draw()
            window.flip()
        window.flip()

window.close()
