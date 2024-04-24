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
        # print(email_info)


        client = OpenAI()
        try:
            completion = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-0125:personal::9HY6hnpM",
                messages=[
                    {"role": "system", "content": "You are a phishing email detector. Analyze the following email and provide and display a threat level on a scale of 0 - 2. 0 being not phishing, 1 being not sure, and 2 being phishing. After that explain your reasoning with 1 or more explanations on why it is or not a phishing email."},
                    {"role": "user", "content": email_info}
                ])
            GPTtext = completion.choices[0].message.content
            print(GPTtext)
        except openai.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.APIError as e:
            print(f"API Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # code form openai.com documentation
        # client = OpenAI()
        # try:
        #     response = client.chat.completions.create(
        #         model="gpt-3.5-turbo-0125",
        #         messages=[
        #             {"role": "system", "content": "You are a phishing email detector. Analyze the following email and provide and display a threat level on a scale of 0 - 2. 0 being not phishing, 1 being not sure, and 2 being phishing. After that explain your reasoning with 1 or more explanations on why it is or not a phishing email."},
        #             {"role": "user", "content": email_info}
            
        #     ])
        #     GPTtext = response.choices[0].message.content
        #     #self.label = customtkinter.CTkLabel(self, text=GPTtext, wraplength=280)
           

        #     email_label = customtkinter.CTkLabel(self, text=GPTtext, wraplength=280)
        #     email_label.pack(side="top", padx=10, pady=10)
        # except Exception as e:
        #     GPTtext = f"An error occurred: {e}"
        # print("API response content:", GPTtext)