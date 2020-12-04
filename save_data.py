import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

SPREADSHEET_ID = '16C6nZTZhbpzijuF0ighzySsWBnlcuVRpXm-rT7NdeUA'
RANGE_NAME = 'Sheet1'
# API_KEY = "AIzaSyAUW2X6semz2OzVLyqtDOF5Qv8a9Pt08gI"


def save_data_to_sheet(data):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    values = [["Hello", "Hello", "Hello", "Hello", ["Hello", "Hello", "Hello", "Hello"]]]
    body = {
        "values": [data]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption="RAW", body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))

