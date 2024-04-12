import customtkinter

from components.scroll_email_list import ScrollEmailList

class EmailView(customtkinter.CTkScrollableFrame):
    '''
    component to display any email information. Currently displays sender, subject, and body. Could use some TLC in the beauty department, a bit hideous at the moment
    '''
    def __init__(self, master, email: dict, **kwargs):
        super().__init__(master, **kwargs)

        email_label = customtkinter.CTkLabel(self, text=f"Sender: {email['sender']}\nSubject: {email['subject']}\n- - - - - - -\nBody: \n{email['body']}", compound="left", justify="left", anchor="w", wraplength=280)
        email_label.pack(side="top", padx=10, pady=10)

