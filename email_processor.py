
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import base64
import email

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# This is from the youtube video #1
#This is for authenticating the user

#This is for storing the user information


#This is for authenticating the user and for grabbing data


class EmailProcessor:
    def __init__(self):
        self.userAccount = ''
        self.subject = []
        self.sender = []
        self.body = []
        # Initialize any other properties you need

    def clear_data(self):
        """Clears all stored data."""
        self.userAccount = ''
        self.subject = []
        self.sender = []
        self.body = []

    def auth_and_load_emails(self):
            # cancel_button = customtkinter.CTkButton(app, text="Cancel", command=logout_method)
        # cancel_button.pack(pady=10)  # Adjust layout parameters as necessary

        creds=None
        #if the user is authenticated then skip to storing data
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # if the user is not authenticated then get the user to login and store the user's authentication token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials.json', SCOPES)
                
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        #This is for grabbing the user's emails
        try:
            service = build('gmail', 'v1', credentials = creds)
            result = service.users().messages().list(userId='me').execute()
            messages = result.get('messages')
            for i in messages:
                txt = service.users().messages().get(userId='me', id=i['id']).execute()
                payload = txt['payload']
                headers = payload['headers']
                for i in headers:  
                    if i['name'] == 'To':
                        self.userAccount = (i['value'])
                    if i['name'] == 'Subject':
                        self.subject.append(i['value'])
                    if i['name'] == 'From':
                        self.sender.append(i['value'])
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace('-', '+').replace('_','/')
                decode_data = base64.b64decode(data)
                
                #This allows us to print out the decoded data (converts to string)
                self.body.append(decode_data.decode('utf-8'))
            # email_page(0)
        except HttpError as error:
            print('An error occurred: (error)')
        except Exception as e:
            print(e)

    def get_userAccount(self):
        return self.userAccount
    def get_subject(self):
        return self.subject
    def get_sender(self):
        return self.sender
    def get_body(self):
        return self.body



        
