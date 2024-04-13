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

email_processor = EmailProcessor()

"""
Yo, this can be used for getting in other email folders, for more
information, look at the top of the comments in email_proccessor class
"""
spam_processor = EmailProcessor("SPAM")


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



#Displays Emails to scan, only displays up to 10 emails.  
#The number arguments is for the pagination for the page
def email_page(number_for_pagination):
    clear_window()
    
    # get email info
    subject = email_processor.get_subject()
    sender = email_processor.get_sender()
    body = email_processor.get_body()
    userAccount = email_processor.get_userAccount()
   
    '''
    Delete this comment later:
    Hey Audry,

    Can you make the buttons maybe like radio buttons, this way it can be organized like this:

    if (Emailbutton clicked):
        subject = email_processor.get_subject()
        sender = email_processor.get_sender()
        body = email_processor.get_body()
        userAccount = email_processor.get_userAccount()
    if (Spambutton clicked):
        subject = spam_processor.get_subject()
        sender = spam_processor.get_sender()
        body = spam_processor.get_body()
        userAccount = email_processor.get_userAccount()
    if (TrashButton clicked):
        subject = trash_processor.get_subject()
        sender = trash_processor.get_sender()
        body = trash_processor.get_body()
        userAccount = email_processor.get_userAccount()

    This way we wont have to re-write all the code (hopefully)

    '''




    # define logout bar
    logout_frame = customtkinter.CTkFrame(app)
    logout_frame.pack(fill='x', padx=10, pady=5)
    account_label = customtkinter.CTkLabel(logout_frame, text="Account: " + userAccount)
    account_label.pack(side="left", padx=10)
    logout = customtkinter.CTkButton(logout_frame, text="Logout of Gmail", command= logout_method)
    logout.pack(side = "right", padx=10, pady=10)


    email_header_data = list(zip(sender, subject)) # data to send to EmailList component (thumbnail-type quick list of emails)
    email_list = EmailList(app, emails = email_header_data, fg_color="transparent") 
    email_list.pack(side="left", padx=10)

    global email_frame # container frame for specific email user is viewing
    email_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    email_frame.pack(side="left", padx=10)

    scan_button = customtkinter.CTkButton(email_frame, text="Scan email", command=lambda: email_action(email_list.get_selected())) # scan_button calls email_action, which currently pulls email info and displays is in email_viewer
    scan_button.pack(side="bottom", padx=10)

    global email_viewer
    email_viewer = customtkinter.CTkFrame(email_frame, width = 300, border_color="gray10", border_width=2, fg_color="transparent", height = 270)
    email_viewer.pack(side="left", padx=10, pady=5)


#here is the evaluation of the email scan (work in progress)
def email_action(email_num):

    subject = email_processor.get_subject()
    sender = email_processor.get_sender()   
    body = email_processor.get_body()    
    userAccount = email_processor.get_userAccount()

    email_data = {'subject' : subject[email_num], 'sender' : sender[email_num], 'body' : body[email_num], 'user' : userAccount[email_num]}

    global email_viewer
    email_viewer.pack_forget() # remove previous email_viewer pane (displaying previous email)
    global email_frame
    email_viewer = EmailView(email_frame, email = email_data, width = 300, border_color="gray10", border_width=2, fg_color="transparent", height = 270) # create new email_viewer pane (displaying current email)
    email_viewer.pack(side="left", padx=10, pady=5)


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

