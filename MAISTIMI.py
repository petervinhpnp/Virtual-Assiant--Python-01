import pyttsx3 #library that converts text into speech using python
import datetime #date and time libraries
import speech_recognition as sr #pip install SpeechRecognition, and call the function as sr for sort form
import smtplib   #sending mail library
from mail_info import send_to_email, epwd, to  
from time import sleep
import wikipedia
from selenium import webdriver #search google but Im not using this one :v
from googlesearch import search
import pywhatkit
import webbrowser as wb
import wikipedia as googleScrap
from time import sleep
from newsapi import NewsApiClient #pip install newsapi-python
import clipboard #pip install clipboard
import os #operating system
import pyjokes #pip install pyjokes
import string
import psutil #pip install psutil (for checking CPU usage and battery) (I don't find it really interesting)
from nltk import word_tokenize
import requests

MAISTIMI = pyttsx3.init() #MAISTIMI is the name of the assistant i named, you can change it to anything you prefer.

def speak(audio):
    MAISTIMI.say(audio)
    MAISTIMI.runAndWait()

def getvoices(): #setting up system's voice sound
    voices = MAISTIMI.getProperty('voices')
    MAISTIMI.setProperty('voice', voices[1].id) #0 is male voice, 1 is female voice.

def greeting_time(): #greet according to time in 1 day
    hour = datetime.datetime.now().hour
    if (hour >= 5 and hour < 12):
        speak("Good morning!")
    elif (hour >= 12 and hour <= 17):
        speak("Good afternoon!")
    elif (hour > 17 and hour <= 21):
        speak("Good evening, Peter!")
    else:
        speak("Night, sir!")

def time(): # read out current time
    Time = datetime.datetime.now().strftime("%I:%M:%S") # hour, minutes, seconds
    speak("The current time is")
    speak(Time)

def date(): # read out current date
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)

    speak_day = {1:"1st", 2:"2nd", 3:"3rd", 4:"4th", 4:"4th", 5:"5th", 6:"6th", 7:"7th", 8:"8th", 9:"9th", 10:"11th", 12:"12th", 13:"13th",
    14:"14th", 15:"15th", 16:"16th", 17:"17th", 18:"18th", 19:"19th", 20:"20th", 21:"21st", 22:"22nd", 23:"23rd", 24:"24th", 25:"25th",
    26:"26th", 27:"27th", 28:"28th", 29:"29th", 30:"30th", 31:"31st"}

    speak_month = {1 : "January", 2 : "Febuary", 3 : "March", 4 : "April", 5 : "May", 6 : "June",
    7 : "July", 8 : "August", 9 : "September", 10 : "October", 11 : "November", 12 : "December"}
    speak("The date of today is")
    if day in speak_day:
        speak(speak_day[day]) #say the day in ordered pronunciation
    if month in speak_month:
        speak(speak_month[month]) #speak month correctly not just the number themselves
    speak(year)
    print(f"The date of today is: {day}/{month}/{year}")

def takeCommand(): #command is like for the big menu list!
    command = input("What do you want to do?\n")
    return command

def takeMicCommand():
    mic_input = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        mic_input.adjust_for_ambient_noise(source, duration = 0.5) #create a 0.5sec pause after hearing
        audio = mic_input.listen(source)
    try:
        print("Analyzing...")
        query = mic_input.recognize_google(audio, language='en-US', show_all= False)
        print(query)
    except Exception as e:
        print(e)
        speak("Please say again")
        return "None"
    return query


def searchGoogle():
    speak("What should I search?")
    while True:               
        try:
            search_data  = str(input("What should I search?\n")) # can use voice or typing searches
            if search_data == "stop": #stop this loop and exit it
                raise StopIteration
            speak("Searching... ")
            pywhatkit.search(search_data)
            sleep(3.5)
            speak("What else do you need to search?\n")
        except StopIteration:
            break

#Will do this 1 again (look up on Youtube)
# def sendMail(content):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(send_to_email, epwd)
#     server.sendmail(send_to_email, to, content)
#     server.close()
# sendMail()

def news():
    while True:
        try:
            newsapi = NewsApiClient(api_key = 'd7f0600a059249749a4d3e70a47c0483')
            speak("What news you want to hear about?")
            topic = takeMicCommand()
            # topic = takeCommand()
            if topic == "stop" or topic == "Stop":
                raise StopIteration
            data = newsapi.get_top_headlines(q = topic, language = 'en', page_size = 3)
            newsdata = data['articles']
            for x, y in enumerate(newsdata):
                print(f'{x}{y["description"]}')
                speak(f'{x}{y["description"]}')
        except StopIteration:
            break
        
def text2speech(): # read what i have copied to the clipboard (the latest ones in the list)
    text = clipboard.paste()
    print(text)
    speak(text)

if __name__ == '__main__':
    getvoices()
    greeting_time()
    wakeword = "buddy"  
    while True:
        command = takeCommand().lower()
        # command = takeMicCommand()
        command = word_tokenize(command)
        if wakeword in command:
            if "time" in command:
                time()

            elif "date" in command:
                date()

            elif "stop" in command:
                quit()
            
            elif 'weather' in command:
                city = input('Which place that you want to know about the weather? ')
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city},uk&APPID=0599e5fcf5a387d663cb811a6dcb65c4'
                res = requests.get(url)
                data = res.json()
                weather = data['weather'][0]['main']
                temp = data['main']['temp']
                desp = data['weather'][0]['description'] #description
                temp = round((temp - 32) * 5/9)
                print(weather)
                print(temp)
                print(desp)
                speak(f'Weather in {city} city is like')
                speak('Temperature: {} degree Celcius'.format(temp))
                speak('Weather is {}'.format(desp))

            elif 'Wikipedia' in command or 'WIKIPEDIA'in command or "wikipedia" in command: #searching and summary information by wikipedia
                    while True:
                        stop_list_keyword = ["stop", "stop wikipedia", "stop searching"]
                        try:
                            speak("What should I search")
                            search_data = input("What should I summary? \n")
                            if search_data in stop_list_keyword :
                                raise StopIteration
                            result = wikipedia.summary(search_data, sentences = 2) #summary sentences
                            print(result)
                            speak(result)
                        except StopIteration:
                            break

            elif "google search"in command or "Google search" in command or 'GOOGLE search' in command: # search by gg and open the browser
                searchGoogle()

            elif "youtube" in command or 'Youtube' in command or 'YOUTUBE' in command:
                speak("What do you want to see on Youtube?\n")
                while True:
                    try:
                        topic = takeCommand()
                        # topic = takeMicCommand()
                        if topic == "stop":
                            raise StopIteration
                        pywhatkit.playonyt(topic)
                        sleep(5)
                        speak("What else do you want to see?")

                    except StopIteration:
                        break

            elif 'News' in command or 'NEWS' in command or "news" in command:
                news()
                
            elif 'read' in command or 'Read' in command:
                text2speech()
            
    #opening application on this laptop
            # to use it, you should change it exactly in your computer files' paths. (those below are like examples)
            elif 'open code' in command:
                vscode_path = 'C:\\Users\\buriv\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
                os.startfile(vscode_path)
            elif 'open editing app' in command:
                powerdirector_path = 'C:\\2. Data for Asus\\1. EDITING SOFTWARE DOWNLOAD FILES\\PowerDirector21\\PDR.exe'
                os.startfile(powerdirector_path)
            elif 'open action' in command:
                action_path = 'C:\\Program Files (x86)\\Mirillis\\Action!\\Launcher.exe'
                os.startfile(action_path)
            elif 'open chatting app' in command:
                zalo_path = 'C:\\Users\\buriv\\AppData\\Local\\Programs\\Zalo\\Zalo.exe'
                os.startfile(zalo_path)
            elif 'open google' in command or 'open Google' in command:
                google_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                os.startfile(google_path)
            elif 'open modelling app' in command:
                freeCAD_path = 'C:\\Program Files\\FreeCAD 0.20\\bin\\FreeCAD.exe'
                os.startfile(freeCAD_path)
            elif 'open blender' in command or 'open Blender' in command:
                blender_path = 'C:\\Program Files\\Blender Foundation\\Blender 3.2\\Launcher.exe'
                os.startfile(blender_path)
    #above code section for opening application on this laptop
    #Opening 
            elif 'open my document' in command:
                os.system('explorer C:\\{}'.format(command.replace('Open','')))
            # elif 'open music' in command:
            #     os.system('explorer C:\\{}'.format(command.replace('Open','')))
            elif 'tell me a joke' in command: # generating a joke
                print(pyjokes.get_joke())
                speak(pyjokes.get_joke())
                
            elif ("stop program" in command) or ("hault" in command) or ("shut down" in command) or ("offline" in command): #stop the program (the biggest one) 
                exit()

                
# elif "google search" in command:
#     while True:
#         print("What do I should search?")
#         searchGoogle()
#         if search == "exit google":
#             break           
# elif "email" in command:
# try:
#     speak("What should be sent?")
#     content = takeMicCommand()
#     sendMail(content)
#     speak('Email has been sent')
# except Exception as e:
#     print(e)
#     speak("I was unable to send email")

