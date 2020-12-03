import os
import sys
import win32api

import numpy as np
import pandas as pd

import psychopy.visual
import psychopy.gui
import psychopy.core
import random

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from ib_stimuli import experimental_setup, movement, stimuli_questions


SCOPES = []
# clientID = "646209918312-dclpaepauatium46t8tg3ap3d1s8i1j3.apps.googleusercontent.com"
# clientSecret = "PEjWU1F-yAd5tjdgVs-t6aSn"
# sheetId = "16C6nZTZhbpzijuF0ighzySsWBnlcuVRpXm-rT7NdeUA"



response_dict = {}
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
        response_dict["Name"] = gui.data[0]
        response_dict["Email"] = gui.data[1]
        response_dict["Phone"] = gui.data[2]
        response_dict["Age"] = gui.data[3]
        response_dict["Gender"] = gui.data[4]
    else:
        win32api.MessageBox(0, "Please enter the required data, exiting...")
        sys.exit("Please enter required data")
    break

print(response_dict)

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
# response_df = pd.DataFrame(columns=["Name", "Email", "Phone", "Age", "Sex", "stimuli_slow",
#                                     "stimuli_above", "notice_additional", "shape_stimuli_res", "stimuli_color_res", "stimuli_above_res"])

blankScreen = psychopy.visual.Rect(
    win=window,
    units="pix",
    width="800",
    height="600",
    fillColor=[-1] * 3,
    lineColor=[-1] * 3,
)
slow = random.choice([True, False])  # Record in response
response_dict["stimuli_slow"] = slow

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
        print("Trial {}".format(trial_index))
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
        pass_count = movement(stimuli_list, window, fixation, line, unexpectedStim, showObject, slow, practice_trial)
        if trial_index == 10 or trial_index == 14 or trial_index == 15:
            response = stimuli_questions()
            response["pass_count_calc"] = pass_count
            if trial_index == 10:
                response_dict["critical_trial"] = response
            elif trial_index == 14:
                response_dict["divided_att_trial"] = response
            elif trial_index == 15:
                response_dict["full_att_trial"] = response

        clock.reset()
        window.flip()
        while clock.getTime() < 0.3:
            blankScreen.draw()
            window.flip()
        window.flip()

print(response_dict)
window.close()
