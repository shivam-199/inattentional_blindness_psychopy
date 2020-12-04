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


SCOPES = []
# clientID = "646209918312-dclpaepauatium46t8tg3ap3d1s8i1j3.apps.googleusercontent.com"
# clientSecret = "PEjWU1F-yAd5tjdgVs-t6aSn"
# sheetId = "16C6nZTZhbpzijuF0ighzySsWBnlcuVRpXm-rT7NdeUA"

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
# response_list = [str(datetime.datetime(2020, 12, 4, 12, 20, 27, 306320)), 'shivam Chaudhary', 'shivamc021999@gmail.com', '9133013490', '21', 'Male', False, '15', 'Yes', 'Above', 'X', 'Grey', 11, '11', 'Yes', 'Above', 'X', 'Green', 6, '13', 'Yes', 'Above', 'X', 'Grey', 6]
# print(response_list)
save_data_to_sheet(response_list)
window.close()
