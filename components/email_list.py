import customtkinter

from components.scroll_email_list import ScrollEmailList

class EmailList(customtkinter.CTkFrame):
    '''
    EmailList component provides email selection and email list viewing functionality
    '''
    def __init__(self, master, emails:list, on_click, **kwargs):
        '''
        emails is zipped list of sender &
        '''
        super().__init__(master, **kwargs)

        self.emails_per_page = 10
        self.page_being_viewed = 0
        self.page = None

        def emails_per_page_select(choice):
            '''
            callback function for emails_per_page_dropdown combo box
            '''
            self.emails_per_page = int(choice)
            reload_list()

        def reload_list():
            '''
            refreshes list of emails, is called when either page changes or when number of emails per page changes
            '''
            start_index = self.emails_per_page*self.page_being_viewed
            end_index = start_index + self.emails_per_page
            email_data = emails[start_index:end_index]
            try:
                self.page.pack_forget() # remove page element from frame
            except AttributeError: # error is thrown when we try to forget page element before it has been initialized
                pass
            self.page = ScrollEmailList(self, email_data, on_click, start_index = start_index, width=300, height=200, corner_radius=0, fg_color="transparent")
            self.page.pack(fill='x', padx=10, pady=5)
        
        dropdown = customtkinter.CTkFrame(self, fg_color="transparent")
        dropdown.pack(side = "top", padx=10, pady=10)
        text = customtkinter.CTkLabel(dropdown, text=f"Retrieved {len(emails)} emails       |       per page: ", compound="left", justify="left", anchor="w")
        text.pack(side="left", padx=5, pady=10)

        # CHANGE VALUES OF DROPDOWN HERE - these are really small values mainly because my test email has like harly any emails in it
        emails_per_page_dropdown = customtkinter.CTkComboBox(dropdown, values=["2", "5", "10"], command=emails_per_page_select, state="readonly", justify="left", width=100)
        emails_per_page_dropdown.set("10")
        emails_per_page_dropdown.pack(side = "right", padx=10, pady=10)

        reload_list() # inserts up-to-date emails list

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(side = "bottom", padx=10, pady=10)

        def increment():
            '''
            called when user clicks "next" to go to next page
            '''
            new = self.page_being_viewed + 1
            max_page = len(emails)//(self.emails_per_page)
            self.page_being_viewed = max_page if new > max_page else new
            reload_list()

        def decrement():
            '''
            called when user clicks "prev" to go to previous page
            '''
            new = self.page_being_viewed - 1
            self.page_being_viewed = 0 if new < 0 else new
            reload_list()

        prev_button = customtkinter.CTkButton(self.button_frame, text = "prev", command = decrement, fg_color="gray10")
        prev_button.pack(side = "left", padx=10, pady=10)

        next_button = customtkinter.CTkButton(self.button_frame, text = "next", command = increment, fg_color="gray10")
        next_button.pack(side = "right", padx=10, pady=10)


    def get_selected(self):
        '''
        returns index of selected email
        '''
        return self.emails_per_page*self.page_being_viewed + self.page.get_selected_index()
