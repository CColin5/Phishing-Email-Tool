#These are imports from https://www.youtube.com/watch?v=7E3NNxeXiys
#import: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import base64
import email

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


import tkinter
import customtkinter
#from loginProcess import LoginProcess
#import imaplib, email
from email.header import decode_header
import os
import webbrowser

"""
Youtube videos used
1. https://www.youtube.com/watch?v=7E3NNxeXiys - this is about using python to read emails
2. https://www.youtube.com/watch?v=NI9LXzo0UY0 - this is about building a modern gui project

"""



#Used this for the clear function https://www.codeease.net/programming/python/python-tkinter-clear-frame

#Methods
# Function to clear the window
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()



#Login page created

def login_To_Account_Page():
    clear_window()
    title = customtkinter.CTkLabel(app, text="Welcome to Phishing Detector")
    title.pack(padx=10, pady=10)

    #Log in button
    login = customtkinter.CTkButton(app, text="Login to Gmail", command=lambda: myEmails())
    login.pack(padx=10, pady=100)

#Displays Emails to scan, only displays up to 10 emails.  
#The number arguments is for the pagnation for the page
def email_page(number_for_pagnation):
    clear_window()
    for i in range(number_for_pagnation*10 + 0, number_for_pagnation*10 + 11):
        print(i)
        label = customtkinter.CTkLabel(app, text="Sender:" + sender[i]+" Subject:"+subject[i], fg_color="black")
        label.pack(padx=10, pady=10)


# This is from the youtube video #1
#This is for authenticating the user

#This is for storing the user information
subject = []
sender = []
body = []


#This is for authenticating the user and grabbing data

def myEmails():
    creds=None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        




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

    try:
        service = build('gmail', 'v1', credentials = creds)
        result = service.users().messages().list(userId='me').execute()
        messages = result.get('messages')
        for i in messages:
            txt = service.users().messages().get(userId='me', id=i['id']).execute()
            payload = txt['payload']
            headers = payload['headers']
            for i in headers:
                if i['name'] == 'Subject':
                    subject.append(i['value'])
                if i['name'] == 'From':
                    sender.append(i['value'])
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace('-', '+').replace('_','/')
                decode_data = base64.b64decode(data)
                body.append(decode_data)
        email_page(0)
    except HttpError as error:
        print('An error occurred: (error)')
    except Exception as e:
        print(e)







#sytem settings (grabs light mode or dark mode)
customtkinter.set_appearance_mode("System")

#set the default color theme
customtkinter.set_default_color_theme("blue")


#Our app frame (size, title, etc)
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Phishing Email Detector")

'''
Dont need these anymore, because I have 2Auth
#region This Section Is for Gathering the user's Gmail
#adding UI Elements
title = customtkinter.CTkLabel(app, text="Please type in your gmail")
title.pack(padx=10, pady=10)

#link input Section
#this gets the input -- This is a usable variable------
gmail_var = tkinter.StringVar()

#this is where the user types in information
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=gmail_var)
link.pack(padx=10, pady=10)

#endregion

#region This Section Is for Gathering the user's Password
#adding UI Elements
title = customtkinter.CTkLabel(app, text="Password")
title.pack(padx=10, pady=10)

#link input Section
#this gets the input -- This is a usable variable------
password_var = tkinter.StringVar()

#this is where the user types in information
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=password_var)
link.pack(padx=10, pady=10)
#endregion
'''






#Initialized login page
login_To_Account_Page()

# Run App
app.mainloop()