import customtkinter

class ScrollEmailList(customtkinter.CTkScrollableFrame):
    '''
    child component of EmailList, provides scrollable pane of user-defined number of emails
    '''
    def __init__(self, master, emails: list, **kwargs):
        super().__init__(master, **kwargs)

        self.selected_index = 0
        self.checkboxes = [] # stores the CTkCheckBox objects for each email (so checked/unchecked state can be updated later)

        for i in range(len(emails)):
            sender, subject = emails[i]
            
            email_frame = customtkinter.CTkFrame(self) # frame for each individual email ( looks nicer if they have their own frames )
            email_frame.pack(fill='x', padx=10, pady=5)

            text = customtkinter.StringVar(value=f"Sender: {sender}\nSubject: {subject}")
            checkbox = customtkinter.CTkCheckBox(email_frame, textvariable=text, command=lambda i=i: self.__set_selected_index(i), variable=customtkinter.BooleanVar(value=False), onvalue=True, offvalue=False)
            checkbox.pack(side="left", padx=10, pady=5)

            self.checkboxes.append(checkbox)

    def __set_selected_index(self, n) -> int:
        '''
        private function to update the index of the selected email & deselect the other checkboxes
        '''
        self.checkboxes[self.selected_index].deselect() # deselect previously selected index
        self.selected_index = n
        self.checkboxes[n].select()
        
    def get_selected_index(self) -> int:
        return self.selected_index
