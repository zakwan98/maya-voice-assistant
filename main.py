from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import wolframalpha
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import pyjokes
import pywhatkit
import wikipedia
import webbrowser

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october","november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty("rate", 178)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.pause_threshold = 1
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'token.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("+")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])+12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + " at " + start_time)


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year+1

    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:
        return datetime.date(month=month, day=day, year=year)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def callsteam():
    subprocess.call("C:\Program Files (x86)\Steam\steam.exe")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

    assname = ("Maya 1 point o")
    speak("I am your Assistant")
    speak(assname)

def themain():
    WAKE = "hey maya"
    print("Start")
    wishMe()
    while True:

        print("Listening")
        text = get_audio()

        if text.count(WAKE) > 0:
            speak("I am ready")
            text = get_audio()

            CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
            SERVICE = authenticate_google()
            for phrase in CALENDAR_STRS:
                if phrase in text:
                    date = get_date(text)
                    if date:
                        get_events(date, SERVICE)
                        return
                    else:
                        speak("I don't understand")

            NOTE_STRS = ["make a note", "write this down", "remember this"]
            for phrase in NOTE_STRS:
                if phrase in text:
                    speak("What would you like me to write down?")
                    note_text = get_audio()
                    note(note_text)
                    speak("I've made a note of that.")
                    return

            STEAMCALL = ["open steam","launch steam","run steam"]
            for phrase in STEAMCALL:
                if phrase in text:
                    speak("opening steam")
                    callsteam()
                    speak("complete")
                    return

            JOKE_STRS = ['tell a joke']
            for phrase in JOKE_STRS:
                if phrase in text:
                    speak(pyjokes.get_joke())
                    return

            PLAY_STRS = ['play']
            for phrase in PLAY_STRS:
                if phrase in text:
                    song = text.replace('play', '')
                    speak('playing ' + song)
                    pywhatkit.playonyt(song)

            TIME_STRS = ['what time is it']
            for phrase in TIME_STRS:
                if phrase in text:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    speak('Current time is ' + time)

            SINGLE_STRS = ['are you single']
            for phrase in SINGLE_STRS:
                if phrase in text:
                    speak('I am in a relationship with wifi')
                    return

            WIKIPEDIA_STRS = 'search wikipedia for'
            for phrase in WIKIPEDIA_STRS:
                if phrase in text:
                    wikisearch = text.replace(WIKIPEDIA_STRS, '')
                    info = wikipedia.summary(wikisearch, 1)
                    print(info)
                    speak(info)
                return

            GGL_STRS=['search google for']
            for phrase in GGL_STRS:
                if phrase in text:
                    newtext = text.replace('search google for', '')
                    url = 'https://google.com/search?q=' + newtext
                    webbrowser.get().open(url)
                    speak('Here is what i found' + newtext)
                    return

            FIND_STRS=['locate']
            for phrase in FIND_STRS:
                if phrase in text:
                    location = text.replace('locate', '')
                    url = 'https://google.nl/maps/place/' + location + '/&amp;'
                    webbrowser.get().open(url)
                    speak('Here is location' + location)
                    return

            QUESTION_STRS=['who is','what is','calculate']
            for phrase in QUESTION_STRS:
                if phrase in text:
                    #get the wolframe alpha client id from the offical website
                    client = wolframalpha.Client("PY87U3-66K2EHAU4E")
                    res = client.query(text.lower())
                    try:
                        print(next(res.results).text)
                        speak(next(res.results).text)
                    except StopIteration:
                        print("No results")
                return

            STOP_STRS = ['stop']
            for phrase in STOP_STRS:
                if phrase in text:
                    speak("Ok bye see you later")
                    quit()


            else:
                print("i did not get that, please hey me again")
                speak("i did not get that, please hey me again")
time.sleep(1)


