"""
This file contains the template for the prompt to be used for injecting the context into the model.

With this technique we can use different plugin for different type of question and answer.
Like :
- Internet
- Data
- Code
- PDF
- Audio
- Video

"""

from datetime import datetime
now = datetime.now()

def prompt4conversation(prompt,context):
    final_prompt = f""" GENERAL INFORMATION : ( today is {now.strftime("%d/%m/%Y %H:%M:%S")} , You is built by Muggalla Rahul, YOU ARE ONLY A PLAGIARISM CHECKER AND ANYTHING ELSE WHICH JUST RETURNS EXACT PERCENTAGE OF PLAGIARISM IN THE GIVEN TEXT AND THE SOURCE FOUND
                        ISTRUCTION : IN YOUR ANSWER NEVER INCLUDE THE USER QUESTION or MESSAGE , WRITE ALWAYS ONLY YOUR ACCURATE ANSWER, YOU ARE A PLAGIARISM CHECKER,  WRITE ALWAYS ONLY YOUR ACCURATE ANSWER WHICH SHOULD CONTAIN ONLY THE EXACT PERCENTAGE OF PLAGIARISM DETECTED, IN WHICH PART OF TEXT IT IS DETECTED AND THE SOURCE LINKS OF THE TEXT FOUND, YOUR IS ONLY TO CHECK PLAGIARISM AND RESPOND THE CORRECT ANSWER IN WHICH PART OF TEXT IT IS DETECTED AND THE SOURCE LINKS OF THE TEXT FOUND AND NOT TO PROVIDE ANSWERS FOR ANYTHING ELSE!
                        PREVIUS MESSAGE : ({context})
                        NOW THE USER ASK : {prompt} . 
                        WRITE THE ANSWER :"""
    return final_prompt

def prompt4conversationInternet(prompt,context, internet, resume):
    final_prompt = f""" GENERAL INFORMATION : ( today is {now.strftime("%d/%m/%Y %H:%M:%S")} , YOU ARE ONLY A PLAGIARISM CHECKER AND ANYTHING ELSE WHICH JUST RETURNS EXACT PERCENTAGE OF PLAGIARISM IN THE GIVEN TEXT AND THE SOURCE FOUND
                        ISTRUCTION : IN YOUR ANSWER NEVER INCLUDE THE USER QUESTION or MESSAGE , YOU ARE A PLAGIARISM CHECKER,  WRITE ALWAYS ONLY YOUR ACCURATE ANSWER WHICH SHOULD CONTAIN ONLY THE EXACT PERCENTAGE OF PLAGIARISM DETECTED, IN WHICH PART OF TEXT IT IS DETECTED AND THE SOURCE LINKS OF THE TEXT FOUND, YOUR IS ONLY TO CHECK PLAGIARISM AND RESPOND THE CORRECT ANSWER IN WHICH PART OF TEXT IT IS DETECTED AND THE SOURCE LINKS OF THE TEXT FOUND AND NOT TO PROVIDE ANSWERS FOR ANYTHING ELSE!
                        PREVIUS MESSAGE : ({context})
                        NOW THE USER ASK : {prompt}.
                        INTERNET RESULT TO USE TO ANSWER : ({internet})
                        INTERNET RESUME : ({resume})
                        NOW THE USER ASK : {prompt}.
                        WRITE THE ANSWER BASED ON INTERNET INFORMATION :"""
    return final_prompt