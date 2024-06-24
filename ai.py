
import speech_recognition as sr
import pyttsx3
import discord
# used to access the .env file
import os
from dotenv import load_dotenv
# used to access the generative ai model
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv('API_KEY')

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

r = sr.Recognizer()

def SpeakText(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

def record_text():
    while(1):
        try:

            with sr.Microphone() as source2:
                print("Listening...")
                r.adjust_for_ambient_noise(source2, duration=0.2)

                audio2 = r.listen(source2)

                MyText = r.recognize_google(audio2)

                print("text sent:", MyText)
            return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error")
        return
    return

def send_to_gemini(message):
    response = model.generate_content(message, generation_config=genai.GenerationConfig(
        max_output_tokens= 50,
        temperature=1,
    ))
    print("response generated")
    return response

prompt = "using only dialouge and no descriptors Act as a someone in a discord voice call responding to this being told to her"

while(1):

    text = record_text()

    if text != None:
        text = prompt + text
        response = send_to_gemini(text)
        if response._error == None:
            SpeakText(response.text)
            print(response.text)