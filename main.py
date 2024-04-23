#These are imports from https://www.youtube.com/watch?v=7E3NNxeXiys
#import: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#If imports are not working ctrl+shift+p --> slect python interpeter. and pick a version that will resolve errors
#pip install openai

import tkinter
import customtkinter
from email.header import decode_header
import os
import webbrowser
from tkinter import PhotoImage

from components.email_list import EmailList
from components.email_view import EmailView
from email_processor import EmailProcessor

"""
Youtube videos used
1. https://www.youtube.com/watch?v=7E3NNxeXiys - this is about using python to read emails
2. https://www.youtube.com/watch?v=NI9LXzo0UY0 - this is about building a modern gui project

"""

email_processor = EmailProcessor()

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
    login = customtkinter.CTkButton(app, text="Login to Gmail", command=lambda: auth_and_loading_data())
    login.pack(padx=10, pady=100)

#This method is for loading data and determining if the user should be logged in    
def auth_and_loading_data():
    email_processor.auth_and_load_emails()
    if os.path.exists('token.json'):
        email_page(0)
    else:
        login_To_Account_Page()

# a logout button that will delete the user's token
def logout_method():
    clear_window()
    try:
        email_processor.clear_data()
        os.remove('token.json')
    except Exception as e:
        print(e)
    login_To_Account_Page()

def email_page(inbox: int):
    '''
    Displays emails in inbox
    inbox argument is an integer (0, 1, or 2) representing which inbox is being scanned
        0 : main
        1 : spam
        2 : trash
    '''
    clear_window()
    
    # get email info
    userAccount = email_processor.get_userAccount()
    subject = email_processor.get_subject()
    sender = email_processor.get_sender()

    # define logout bar
    logout_frame = customtkinter.CTkFrame(app)
    logout_frame.pack(fill='x', padx=10, pady=5)
    account_label = customtkinter.CTkLabel(logout_frame, text="Account: " + userAccount)
    account_label.pack(side="left", padx=10)
    logout = customtkinter.CTkButton(logout_frame, text="Logout of Gmail", command= logout_method)
    logout.pack(side = "right", padx=10, pady=10)

    inbox_select = customtkinter.CTkFrame(app)
    inbox_select.pack(side = "top", padx=10, pady=10)
    selected_inbox = customtkinter.IntVar(inbox_select, value = inbox)

    def inbox_filter():
        '''
        redefines email processor based on which inbox should be viewed & reloads email_page
        '''
        global email_processor
        match selected_inbox.get():
            case 1:
                email_processor = EmailProcessor("SPAM")
            case 2:
                email_processor = EmailProcessor("TRASH")
            case _:
                email_processor = EmailProcessor()
        auth_and_loading_data()
        email_page(selected_inbox.get())
    
    main_button = customtkinter.CTkRadioButton(inbox_select, variable = selected_inbox, value = 0, command = inbox_filter, text = "Main")
    spam_button = customtkinter.CTkRadioButton(inbox_select, variable = selected_inbox, value = 1, command = inbox_filter, text = "Spam")
    trash_button = customtkinter.CTkRadioButton(inbox_select, variable = selected_inbox, value = 2, command = inbox_filter, text = "Trash")
    main_button.pack(side="left", padx=5, pady=10)
    spam_button.pack(side="left", padx=5, pady=10)
    trash_button.pack(side="left", padx=5, pady=10)
    
    email_list = EmailList(app, emails = list(zip(sender, subject)), on_click = view_email, fg_color="transparent") 
    email_list.pack(side="left", padx=10)

    global email_frame # container frame for specific email user is viewing
    email_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    email_frame.pack(side="left", padx=10)

    scan_button = customtkinter.CTkButton(email_frame, text="Scan email", command=lambda: email_action(email_list.get_selected())) # scan_button calls email_action, which currently pulls email info and displays is in email_viewer
    scan_button.pack(side="bottom", padx=10)

    global email_viewer
    email_viewer = customtkinter.CTkFrame(email_frame, width = 300, border_color="gray10", border_width=2, fg_color="transparent", height = 270)
    email_viewer.pack(side="left", padx=10, pady=5)

def view_email(email_num):
    subject = email_processor.get_subject()
    sender = email_processor.get_sender()   
    body = email_processor.get_body()    
    userAccount = email_processor.get_userAccount()

    email_data = {'subject' : subject[email_num], 'sender' : sender[email_num], 'body' : body[email_num], 'user' : userAccount[email_num]}

    global email_viewer, email_frame
    email_viewer.pack_forget() # remove previous email_viewer pane (displaying previous email)
    email_viewer = EmailView(email_frame, email = email_data, width = 300, border_color="gray10", border_width=2, fg_color="transparent", height = 270) # create new email_viewer pane (displaying current email)
    email_viewer.pack(side="left", padx=10, pady=5)


def email_action(email_num):
    '''
    function for scanning email
    '''
    pass
    

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

#Initialized login page
login_To_Account_Page()

# Run App
app.mainloop()

