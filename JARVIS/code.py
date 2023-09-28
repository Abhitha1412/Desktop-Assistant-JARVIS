import pyttsx3 # for speaking
import requests
import speech_recognition as sr
import datetime
import os
import json
import requests
import pywhatkit # for whatsapp msg
import time
import sys
import random
import webbrowser as wb
from bs4 import BeautifulSoup
from instaloader import instaloader
from requests import get # for ip address
import wikipedia
import pyautogui as py # for tab switching
import pygetwindow as gw # for minimizing and maximizing windows
from playsound import playsound # for playing sound
import psutil # for battery
from pywikihow import search_wikihow # to get how to do a work
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from Jarvisgui import Ui_MainWindow
#import cv2
#import face_recognition
#import numpy as np
import pyjokes
import PyPDF2

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty("rate",170)
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
def wish():
    hour = datetime.datetime.now().hour
    time = datetime.datetime.now().strftime("%I:%M %p")
    if hour > 0 and hour < 12:
        morning = 'good morning sir now the time is ' + ' ' + time
        speak(morning)
    elif hour >= 12 and hour < 16:
        afternoon = 'good afternoon sir now the time is ' + ' ' + time
        speak(afternoon)
    else:
        evening = 'good evening sir now the time is ' + ' ' + time
        speak(evening)
def playmusic():
    music_dir = 'C:\\Users\\harshith\\OneDrive\\Music'      
    songs = os.listdir(music_dir)
    print(songs) 
    rd=random.choice(songs)
    os.startfile(os.path.join(music_dir, rd))
def getNumber(person):
    person = person.strip().lower()
    print(person)
    try:
        with open('C:\\Users\\harshith\\Desktop\\5k2\\contacts.vcf', 'r',encoding='utf-8') as file:
            data = {}
            for line in file:
                if "FN:" in line:
                    name = str(line.split(":")[1][:-1]).strip().lower()                    
                elif "CELL" in line:
                    tel = str(line.split(":")[1][:-1]).strip()
                    if name not in data.keys():
                        if tel[:2] == '+91':
                            data[name] = tel
                        else:
                            tel = "+91" + tel[-10:]
                            data[name] = tel
            #file.close()
            return data[person.lower()]
    except FileNotFoundError:
        return "File not found"
    except KeyError:
        return "Person not found"

def sendMessage(mobileNumber, message):
    if mobileNumber.startswith("+"):
        pywhatkit.sendwhatmsg_instantly(mobileNumber, message)
    else:
        # Add country code if it is not already included
        phone_number = "+91" + mobileNumber[-10:]
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
def face_recog():
    print("Started")
    speak("Recognizing Face")
    path = os.getcwd() + "\owner"
    myList = os.listdir(path)
    images = []
    classNames = []
    curImg = cv2.imread(f'{path}/{myList[0]}')
    images.append(curImg)
    classNames.append(os.path.splitext(myList[0])[0])
    img = cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB)
    encodeListKnown = []
    encode = face_recognition.face_encodings(img)[0]
    encodeListKnown.append(encode)
    print("Recognition started")
    cap = cv2.VideoCapture(0)
    name = ""
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex]
                print("Welcome sir", name)
                break
        if name != "":
            speak("Welcome sir " + name)
            return 1
        else:
            return 0
cv2.destroyAllWindows() 
def open_app(query):
    py.keyDown('winleft')
    time.sleep(0.3)
    py.press('s')
    time.sleep(0.3)
    py.keyUp('winleft')
    time.sleep(0.3)
    py.write(query)
    time.sleep(0.3)
    py.press("enter")
def close_app(app_name):
    for proc in psutil.process_iter():
        if proc.name() == app_name:
            proc.kill()
    os.system("taskkill /f /im " + app_name + ".exe")
def minimize(query):
    print('entered')
    if "all" in query:
        speak("Minimizing all the opened windows")
        py.hotkey('winleft', 'd')
    elif "chrome" in query:
        chrome = gw.getWindowsWithTitle('Google Chrome')[0]
        chrome.minimize()
def maximize(query):
    if "all" in query:
        speak("Maximizing all the windows")
        py.hotkey('winleft', 'd')
    else:
        titleList = py.getAllTitles()
        titleList = [i for i in titleList if i != '']
        title = [i for i in titleList if (query in i.lower())]
        c = gw.getWindowsWithTitle(title[0])[0]
        c.maximize()
def remembered():
    remember = open("data.txt", "r")
    speak("You told me to remember that" + remember.read())
    print("You told me to remember that " + str(remember))
def battery():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    return percentage
def Pass(pass_inp):
    print(pass_inp)
    pass_inp.lower()
    password = "jarvis"

    passss  = str(password)

    if passss==str(pass_inp):
        speak("Access Granted.")
    else:
        speak("Access Not Granted.")
def how_to_do():
    mainThreadObject = MainThread()
    speak('How to do mode is activated')
    while True:
        speak("Please tell me what do you want to know sir")
        how = mainThreadObject.takecommand()
        try:
            if "exit" in how or "close" in how:
                speak("Okay sir, how to do mode is closed")
                break
            else:
                how_to = search_wikihow(how, 1)
                assert len(how_to) == 1
                speak(how_to[0].summary)
        except Exception as e:
            speak("Sorry sir, ia am not able to find this")
def latestnews():
    api_dict = {"business" : "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=48f076e72ca3412da83628e892e3eb3a",
            "entertainment" : "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=48f076e72ca3412da83628e892e3eb3a",
            "health" : "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=48f076e72ca3412da83628e892e3eb3a",
            "science" :"https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=48f076e72ca3412da83628e892e3eb3a",
            "sports" :"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=48f076e72ca3412da83628e892e3eb3a",
            "technology" :"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=48f076e72ca3412da83628e892e3eb3a"
}
    content = None
    url = None
    speak("Which field news do you want, [business] , [health] , [technology], [sports] , [entertainment] , [science]")
    field = input("Type field news that you want: ")
    #field = self.takecommand()
    for key ,value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("url was found")
            break
        else:
            url = True
            
    if url is True:
        print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts :
        article = articles["title"]
        print(article)
        speak(article)
        news_url = articles["url"]
        print(f"for more info visit: {news_url}")

        #a = input("[press 1 to cont] and [press 2 to stop]")
        speak("press 1 to continue and press 2 to stop")
        a=input()
        if str(a) == "1":
            pass
        elif str(a) == "2":
            break
        
    speak("thats all")
def temp(search):
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"current {search} is {temp}")
def rememberthat(data):
    remember = open("data.txt", "w")
    remember.write(data)
    remember.close()
def pdf_reader():
    book = open('py3.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this book {pages} ")
    speak("sir please enter the page number i have to read")
    pg = int(input("please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
    def run(self):
        self.taskExecution()
    def takecommand(self):
        lr = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening..')
            lr.pause_threshold = 1
            audio = lr.listen(source)#, timeout=15, phrase_time_limit=7)
        try:
            print("Recognising..")
            query = lr.recognize_google(audio, language='en-in')    # query = ""
            #print("User said:", query)
            print(f"User said: {query}\n")
        except Exception as e:
            return ""
        query = query.lower()
        return query
    def run(self):
        if(True):
             self.taskExecution()#if(1)
             while True:
                query = self.takecommand()
                permission = self.takecommand()
                if "wake up" or "are you there" or "hello" in permission:
                    self.taskExecution()
                elif "good bye" in permission:
                    speak("thanks for using me sir, have a good day")
                    sys.exit()
        else:
            speak("You are not the registered person!")
    def taskExecution(self):
        wish()
        speak('My name is Jarvis. How can i help you sir?')
        speak("This Particular File Is Password Protected .")
        speak("Kindly Provide The Password To Access .")
        passssssss = self.takecommand()
        Pass(passssssss)
        while True:
            try:
                self.query = self.takecommand()
                charge = battery()
                if charge <= 20:
                    playsound("jarvis_low_battery.mp3")
                if "open" in self.query:
                    self.query = self.query.replace("open", "")
                    open_app(self.query)
                elif "close" in self.query:
                    self.query = self.query.replace("close", "")
                    close_app(self.query.strip())
                elif "sleep" in self.query:
                    speak('Going to sleep sir, you can call me anytime you want..')
                    break
                elif 'the time' in self.query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                    speak(f"Sir, the time is {strTime}")
                elif "number" in self.query:
                    self.query = self.query.replace("number", "")
                    mobile = getNumber(self.query)
                    print( mobile)
                    speak(mobile)
                elif "ip address" in self.query:
                    ip = get("https://api.ipify.org").text
                    ipspeak = "Your IP address is" + ip
                    speak(ipspeak)
                elif "send" in self.query and "whatsapp" in self.query:
                    speak("Tell the name of the person")
                    personName = self.takecommand()
                    mobileNumber = getNumber(personName)
                    speak("Tell the message that you wanted to send")
                    message = self.takecommand()
                    sendMessage(mobileNumber, message)
                elif "wikipedia" in self.query:
                    speak("searching wikipedia...")
                    self.query = self.query.replace("wikipedia", " ")
                    result = wikipedia.summary(self.query, sentences=2)
                    speak(result)
                elif "youtube" in self.query and "play" in self.query:
                    print("Yes")
                    self.query = self.query.replace("play", '')
                    speak('Playing...')
                    pywhatkit.playonyt(self.query)
                elif 'open youtube' in self.query:
                    wb.open("youtube.com")

                elif 'search' in self.query:
                    self.query = self.query.replace('search', '')
                    speak('Searching...')
                    pywhatkit.search(self.query)
                elif "switch the window" in self.query or "switch window" in self.query:
                    py.keyDown("alt")
                    py.press("tab")
                    py.keyUp("alt")
                elif "switch" in self.query and "tab" in self.query:
                    py.keyDown("ctrl")
                    py.press("tab")
                    py.keyUp("ctrl")
                elif "minimise" in self.query:
                    self.query = self.query.replace("minimise", "")
                    minimize(self.query.strip())
                elif "maximize" in self.query:
                    self.query = self.query.replace("maximize", "")
                    maximize(self.query.strip())
                elif "windows" in self.query and 'running' in self.query:
                    s = gw.getAllTitles()
                    for i in s:
                        speak(i)
                elif 'open google' in self.query:
                    wb.open("google.com")
                elif 'open stackoverflow' in self.query:
                    wb.open("stackoverflow.com")  
                elif "how much power left" in self.query or "how much power we have" in self.query:
                    percentage = battery()
                    speak(f"sir our system have {percentage} percent battery")
                elif "activate how to do mode" in self.query:
                    how_to_do()
                elif "volume up" in self.query or "increase volume" in self.query:
                    py.press("volumeup")
                elif "volume down" in self.query or "decrease volume" in self.query:
                    py.press("volumedown")
                elif "mute" in self.query or "unmute" in self.query:
                    py.press("volumemute")
                elif "take" in self.query or "screenshot" in self.query:
                    speak("Please hold the screen for few seconds i am taking screenshot")
                    img = py.screenshot()
                    img.save("C:\\Users\\harshith\\OneDrive\\Pictures\\Screenshots\\ss1.jpg")
                    speak("i am done and i am ready for next work sir")
                elif "tell me a joke" in self.query:
                    joke = pyjokes.get_joke()
                    speak(joke)
                elif "shut down the system" in self.query:
                    os.system("shutdown /s /t 5")
                elif "restart the system" in self.query:
                    os.system("shutdown /r /t 5")
                elif "sleep the system" in self.query:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                elif "tell news" in self.query:
                    #speak("please wait sir, fetching the latest news")
                    news = latestnews()
                    self.ui.textBrowser.setText(news)
                    #latestnews()
                elif "photo" in self.query:
                    py.press("super")
                    py.typewrite("camera")
                    py.press("enter")
                    py.sleep(2)
                    speak("SMILE")
                    speak("enter")
                    py.press("enter")
                elif "where i am" in self.query or "where we are" in self.query:
                    speak("wait sir, let me check")
                    try:
                        ipAdd = requests.get('https://api.ipify.org').text
                        print(ipAdd)
                        url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                        geo_requests = requests.get(url)
                        geo_data = geo_requests.json()
                        city = geo_data['city']
                        country = geo_data['country']
                        speak(f"sir i am not sure, but i think we are in {city} city of {country} country")
                    except Exception as e:
                        speak("sorry sir, Due to network issue i am not able to find where are.")
                        pass
                elif "instagram profile" in self.query or "profile on instagram" in self.query:
                    speak("sir please enter the user name correctly.")
                    name = input("Enter username here:")
                    wb.open(f"www.instagram.com/{name}")
                    speak(f"Sir would you like to download profile picture of this account.")
                    condition = "yes" # self.takecommand().lower()
                    if "yes" in condition:
                        mod = instaloader.Instaloader()
                        mod.download_profile(name, profile_pic_only=True)
                        speak("i am done sir, profile picture is saved in our main folder. now i am ready for another command")
                    else:
                        pass
                elif "read pdf" in self.query:
                    from pdf import read_pdf                
                    read_pdf('C:\\Users\\harshith\\Desktop\\5k2\\abstract.pdf',2)
                    #pdf_reader()
                elif 'play music' in self.query:
                    playmusic()
                elif "remember that" in self.query:
                    
                    speak("What should I remember")
                    data = self.takecommand()
                    speak("You said me to remember that" + data)
                    print("You said me to remember that " + str(data))
                    rememberthat(data)
                    '''remember = open("data.txt", "w")
                    remember.write(data)
                    remember.close()'''
                elif "do you remember anything" in self.query:
                    remembered()                                   
                elif "temperature at" in self.query:
                    
                    self.query = self.query.replace("temperature at", "")
                    search = "temperature in" + self.query
                    temp(search)
                    '''url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div", class_="BNeawe").text
                    speak(f"current {search} is {temp}")'''
                elif "bye" in self.query:
                    break
            except Exception as e:
                pass
if __name__ == "__main__":
    startExecution = MainThread()
    from jarvisgui import Ui_MainWindow
    class Main(QMainWindow):
        def __init__(self):
            super().__init__()
            self.ui = Ui_MainWindow()
            
            #self.request_url = "https://api.example.com"
            #self.token = "ABC123"
            #config = EnvConfig(request_url='https://example.com/api', token='ABC123')
            self.ui.setupUi(self)
            self.ui.pushButton.clicked.connect(self.startTask)
            self.ui.pushButton_2.clicked.connect(self.close)

        def startTask(self):
            self.ui.movie = QtGui.QMovie("JARVIS.jpeg")
            self.ui.label.setMovie(self.ui.movie)
            self.ui.movie.start()
            startExecution.start()
    app = QApplication(sys.argv)
    jarvis = Main()
    jarvis.show()
    exit(app.exec_())
