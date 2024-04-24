#https://customtkinter.tomschimansky.com/documentation/windows/toplevel
#code came from this website

#https://platform.openai.com/docs/guides/text-generation/json-mode

import os
os.environ['OPENAI_API_KEY'] = ''


from openai import OpenAI
import customtkinter
import openai

class generativeAIWindow(customtkinter.CTkToplevel):
    def __init__(self, email: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.title("Email Information")

        email_info = (f"Sender: {email['sender']}\nSubject: {email['subject']}\n- - - - - - -\nBody: \n{email['body']}")

        label = customtkinter.CTkLabel(self, text = "Email Information", font = ("arial", 20))
        label.pack(side = "top")
        scrollable = customtkinter.CTkScrollableFrame(self)
        scrollable.pack(fill="both", padx = 10, pady = 20)

        client = OpenAI()
        try:
            completion = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-0125:personal::9HY6hnpM",
                messages=[
                    {"role": "system", "content": "You are a phishing email detector. Analyze the following email and provide and display a threat level on a scale of 0 - 2. 0 being not phishing, 1 being not sure, and 2 being phishing. After that explain your reasoning with 1 or more explanations on why it is or not a phishing email."},
                    {"role": "user", "content": email_info}
                ])
            GPTtext = completion.choices[0].message.content
            email_label = customtkinter.CTkLabel(scrollable, text=GPTtext, wraplength=280, justify = "left")
            email_label.pack(side="top", padx=10, pady=10)
        except openai.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.APIError as e:
            print(f"API Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")