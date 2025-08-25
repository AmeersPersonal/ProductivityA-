import datetime
import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from user import User

# If modifying these scopes, delete the file token.json.
# This scope allows full read/write access to Google Calendar.

class Calender():
    def __init__(self, user:User):
        self.user = user
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]

        # Get the directory of the current script
        self.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TOKEN_PATH = os.path.join(self.SCRIPT_DIR, self.user.get_uuid() +"_"+ "token.json")
        self.CREDENTIALS_PATH = os.path.join(self.SCRIPT_DIR, "credentials.json")

    def create_event(self, service, event_details):
        """
        Creates an event on the user's primary Google Calendar.

        Args:
            service: The authenticated Google Calendar API service object.
            event_details: A dictionary containing the event's data.
        
        Returns:
            The created event object from the API response.
        """
        try:
            # Call the Calendar API to insert the event.
            event = service.events().insert(calendarId='primary', body=event_details).execute()
            print(f"Event created: {event.get('htmlLink')}")
            return event
        except HttpError as error:
            print(f"An error occurred: {error}")

    def send_event(self, event):


        creds = None

        if os.path.exists(self.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_PATH, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

        try:
            # Build the service object for interacting with the Calendar API.
            service = build("calendar", "v3", credentials=creds)

            # Example event details


            # Create the event
            self.create_event(service, event)

        except HttpError as error:
            print(f"An error occurred: {error}")


    def get_event(self):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # We now use a full path to find the token.json file.
        if os.path.exists(self.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # The credentials.json file is downloaded from the Google Cloud Console.
                # We now use a full path to find the credentials.json file.
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_PATH, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
                try:
                    service  = build('calender', 'v3', credentials=creds)
                    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
                    events_result = service.events().list(calendarId='primary', timeMin=now,
                                                        maxResults=10, singleEvents=True,
                                                        orderBy='startTime').execute()
                    events = events_result.get('items', [])

                    output =[]

                    if not events:
                        print('No upcoming events found.')
                        return

                    # Print the start and summary of the upcoming events
                    for event in events:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        output.append(start)
                    return output
                except Exception as e:
                    print(e)

