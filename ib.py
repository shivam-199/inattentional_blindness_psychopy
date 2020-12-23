import os
import sys
import win32api

import numpy as np
import pandas as pd
import datetime

import psychopy.visual
import psychopy.gui
import psychopy.core
import random

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from ib_stimuli import experimental_setup, movement, stimuli_questions
from save_data import save_data_to_sheet


response_list = []
response_list.append(str(datetime.datetime.now()))
while True:
    gui = psychopy.gui.Dlg(title="Personal Information", labelButtonOK="Confirm", labelButtonCancel="Exit")
    gui.addField("Name: ")
    gui.addField("Email: ")
    gui.addField("Phone: ")
    gui.addField("Age: ")
    gui.addField("Gender: ", choices=["", "Male", "Female", "Others"])
    gui.show()
    if gui.OK:
        if "" in gui.data:
            win32api.MessageBox(0, "Please fill all the fields.")
            continue
        for i in range(len(gui.data)):
            response_list.append(gui.data[i])
    else:
        win32api.MessageBox(0, "Please enter the required data, exiting...")
        sys.exit("Please enter required data")
    break

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
When the experiment starts, focus on the black square at the center of the screen. \n
There are a total of 16 trials, each trial separated by brief blank screens. You have to count the number of times the
red letters cross the central horizontal line in each trial. When asked to enter the count, enter the count of only
the previous trial. \n
Please note that the personal information collected will not be shared with any third party. \n
Participation in this study is voluntary, you can leave the experiment at any time in between. \n
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
slow = random.choice([True, False])  # Record in response
response_list.append(slow)

keys = psychopy.event.waitKeys(keyList=["T", "t", "q", "Q"])
window.flip()

if "T" in keys or "t" in keys:
    stimuli_pos = []
    for trial_index in range(trials):
        '''
            per trial,
            600ms frozen start screen,
            8000ms of stimuli movement,
            300ms frozen screen to facilitate ambiguous counting decisions
        '''
        # print("Trial {}".format(trial_index))
        practice_trial = True if trial_index < 3 else False

        clock.reset()
        while clock.getTime() < 0.6:
            blankScreen.draw()
            window.flip()
        clock.reset()
        whiteScreen, fixation, line, stimuli_list, unexpectedStim, stimPos = experimental_setup(window)
        if trial_index == 10 or trial_index == 14 or trial_index == 15:
            showObject = True
            stimuli_pos.append(stimPos)
        else:
            showObject = False
        if trial_index == 14:
            unexpectedStim.color = "#000000"
        else:
            unexpectedStim.color = "#E4E4E4"
        pass_count = movement(stimuli_list, window, fixation, line, unexpectedStim, showObject, slow, practice_trial)
        if trial_index == 10 or trial_index == 14 or trial_index == 15:
            response = stimuli_questions()
            response.append(pass_count)
            response_list += response

        clock.reset()
        window.flip()
        while clock.getTime() < 0.3:
            blankScreen.draw()
            window.flip()
        window.flip()

save_data_to_sheet(response_list)

thankYouScreen = psychopy.visual.TextStim(
    win=window,
    wrapWidth=600,
)
thankYouScreen.text = "Thank you for participating in this study!"
thankYouScreen.draw()
window.flip()
psychopy.event.waitKeys()

window.close()
