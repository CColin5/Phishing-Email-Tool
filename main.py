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

from email_processor import EmailProcessor
email_processor = EmailProcessor()


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
#The number arguments is for the pagnation for the page
def email_page(number_for_pagnation):
    clear_window()
    

    subject = email_processor.get_subject()
    
    sender = email_processor.get_sender()
    
    body = email_processor.get_body()
    
    userAccount = email_processor.get_userAccount()

   
    logout_frame = customtkinter.CTkFrame(app)
    logout_frame.pack(fill='x', padx=10, pady=5)

    account_label = customtkinter.CTkLabel(logout_frame, text="Account: " + userAccount, fg_color="black")
    account_label.pack(side="left", padx=10)
    


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
        # print(body[i])
        # Create a frame for each email
        email_frame = customtkinter.CTkFrame(app)
        email_frame.pack(fill='x', padx=10, pady=5)
        
        # Label for the email
        email_label = customtkinter.CTkLabel(email_frame, text="Sender: " + sender[i] + " \nSubject: " + subject[i], fg_color="black")
        email_label.pack(side="left", padx=10)
        
        # Button for the email
        email_button = customtkinter.CTkButton(email_frame, text="Open and Scan", command=lambda i=i: email_action(i))
        email_button.pack(side="right", padx=10)

        


#here is the evaluation of the email scan (work in progress)
def email_action(email_num):
    clear_window()


    subject = email_processor.get_subject()
    
    sender = email_processor.get_sender()
    
    body = email_processor.get_body()
    
    userAccount = email_processor.get_userAccount()



    email_frame = customtkinter.CTkFrame(app)
    email_frame.pack(fill='x', padx=10, pady=5)

    # Label for the email
    email_label = customtkinter.CTkLabel(email_frame, text="Sender: " + sender[email_num] + " \nSubject: " + subject[email_num], fg_color="black")
    email_label.pack(side="left", padx=10)

    body_label = customtkinter.CTkLabel(email_frame, text="Body: " + body[email_num], fg_color="black")
    body_label.pack(side="left", padx=10)
        




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

