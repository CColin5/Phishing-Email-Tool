#These are imports from https://www.youtube.com/watch?v=7E3NNxeXiys
#import: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#If imports are not working ctrl+shift+p --> slect python interpeter. and pick a version that will resolve errors
#pip install openai

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



#Methods that create pages:


#Used this for the clear function https://www.codeease.net/programming/python/python-tkinter-clear-frame
# Function to clear the window
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()



#Login page for accounts 

def login_To_Account_Page():

    #clears the window
    clear_window()

    #uses customtkinter to create a label
    title = customtkinter.CTkLabel(app, text="Welcome to Phishing Detector")
    title.pack(padx=10, pady=10)

    #Log in button that sends the user's emails and processes them
    login = customtkinter.CTkButton(app, text="Login to Gmail", command=lambda: myEmails())
    login.pack(padx=10, pady=100)


# a logout button that will delete the user's token
def logout_method():
    clear_window()
    try:
        os.remove('token.json')
    except Exception as e:
        print(e)
    login_To_Account_Page()



#Displays Emails to scan, only displays up to 10 emails.  
#The number arguments is for the pagnation for the page
def email_page(number_for_pagnation):
    clear_window()
    
    logout_frame = customtkinter.CTkFrame(app)
    logout_frame.pack(fill='x', padx=10, pady=5)

    account_label = customtkinter.CTkLabel(logout_frame, text="Account: " + userAccount, fg_color="black")
    account_label.pack(side="left", padx=10)
    print(userAccount)


    # The user can log out here
    logout = customtkinter.CTkButton(logout_frame, text="Logout of Gmail", command= logout_method)
    logout.pack(padx=10, pady=10)

    # this gets the amount of emails that will desplay per page. Example: if there are 7 emails, only 7 will be desplayed. More than ten emails will result in only 10 emails being displayed
    if ((len(subject)- number_for_pagnation*10) > 10):
        email_amount_number = 10

        #create a next button to display the next 10 emails

    else:
        #this will display the remaining emails
        email_amount_number = len(subject)%10 

    #creates a frame of labels for to organize which email is which.
    for i in range(number_for_pagnation*10, number_for_pagnation*10 + email_amount_number):
        print(body[i])
        # Create a frame for each email
        email_frame = customtkinter.CTkFrame(app)
        email_frame.pack(fill='x', padx=10, pady=5)
        
        # Label for the email
        email_label = customtkinter.CTkLabel(email_frame, text="Sender: " + sender[i] + " \nSubject: " + subject[i], fg_color="black")
        email_label.pack(side="left", padx=10)
        
        # Button for the email
        email_button = customtkinter.CTkButton(email_frame, text="Open and Scan", command=lambda i=i: email_action(i))
        email_button.pack(side="right", padx=10)

        print(userAccount + "AHHHHHHHHHHHHHHHHHHHHHHHHHHHH")


#here is the evaluation of the email scan (work in progress)
def email_action(email_num):
    clear_window()
    email_frame = customtkinter.CTkFrame(app)
    email_frame.pack(fill='x', padx=10, pady=5)

    # Label for the email
    email_label = customtkinter.CTkLabel(email_frame, text="Sender: " + sender[email_num] + " \nSubject: " + subject[email_num], fg_color="black")
    email_label.pack(side="left", padx=10)

    body_label = customtkinter.CTkLabel(email_frame, text="Body: " + body[email_num], fg_color="black")
    body_label.pack(side="left", padx=10)
        










# This is from the youtube video #1
#This is for authenticating the user

#This is for storing the user information
subject = []
sender = []
body = []
userAccount = ''

#This is for authenticating the user and for grabbing data
def myEmails():

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
                print(i)
                if i['name'] == 'To':
                    userAccount = (i['value'])
                    print(i['value'] + "__________________________________")
                    print(userAccount+"AHHHHHHHHHHHHHHHHH")
                if i['name'] == 'Subject':
                    subject.append(i['value'])
                if i['name'] == 'From':
                    sender.append(i['value'])
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace('-', '+').replace('_','/')
                decode_data = base64.b64decode(data)
                
                #This allows us to print out the decoded data (converts to string)
                body.append(decode_data.decode('utf-8'))
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

#adds an image to the app
app.iconbitmap("images/PhishingDetector.ico")

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

