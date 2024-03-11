from vosk import Model, KaldiRecognizer
import pyaudio
from settings import *
import speech_recognition
import pyttsx3
import json
import os
import webbrowser
import wikipedia
import requests
import datetime
import random
from views import Example
import sys

datetimenow = datetime.datetime.now()


def SetupVoiceAsisten():
    "sintes text to speack"
    voices = TTsEngine.getProperty("voices")

    if ASISTEN_SPEACH_LANGUAGE == "ru":
        if ASISTENT_GENDER == 'Famale':
            TTsEngine.setProperty("voice", voices[2].id)
        else:
            TTsEngine.setProperty("voice", voices[1].id)

    elif ASISTEN_SPEACH_LANGUAGE == 'en':
        TTsEngine.setProperty("voice", voices[0].id)
    

def speach(text: str):
    "text to speak"
    TTsEngine.say(text)
    TTsEngine.runAndWait()


def Today( *input_today: tuple):
    
    def Time( text ):
        speach(f"сегодняшнее { text }:{ datetimenow.strftime('%H:%M ') }")
        return datetimenow.strftime("%H:%M:%S")
    
    def Date( text ):
        monthDICT = example.Calendar()
        
        day = str(datetimenow.day)
        month = str(datetimenow.month)
        year = str(datetimenow.year)

        for monthKEY in monthDICT.keys():
            if month in monthKEY:
                speach(f'сегодняшняя { text }, { day }  {monthDICT[month]}, {year}')
                return f"{day}.{month}.{year}"

            
    def Weather( text ):
        try:
            city = USER_CITY.lower()
            link_1 = "http://api.openweathermap.org/data/2.5/weather?q="
            link_2 = "&units=metric&APPID=6bab4d6713adbf3a428b1f2a7454395d"
            link = link_1 + city + link_2
            response = requests.get(link)
            if response.status_code == 200:
                JSONdata = response.json()
                temp = JSONdata['main']['temp']
                weather = JSONdata['weather'][0]['main']
                
                if weather == "Clear":
                    data = f"сегодняшняя { text } солнечная. { temp }.цельсия градусов"
            
                if weather == "Clouds":
                    data = f'сегодняшняя { text } облачная. { temp }.цельсия градусов'
                speach(data)
                return f"{text}:  { temp }`C"
            return f"status code: { response.status_code }"
        except: return "Not found conection error"

    if not input_today[0]: return
    for command in input_today[0]:
        if command not in [ 'время', 'час', 'времени' ]:
            if command not in [ 'дата', 'число' ]:
                if command not in [ 'погода' ]:
                    return
                else:
                    return Weather ( command )
            else:
                return Date ( command )
            
        else:
            return Time ( command)

    
def Play( *input_play: tuple ):

    def Musik():
        songs = os.listdir(PATH_MUSIK)
        count = len(songs)
        file = os.path.join(PATH_MUSIK, songs[ random.randint(0, count )])
        os.startfile(file)
        return f"Play musik: file({ file })"

    def YouTubeVideo( *args: tuple ):

        if not args[0]: return
        search = " ".join( args[0] )
        url = "https://www.youtube.com/results?search_query=" + search
        webbrowser.get().open(url)
        speach(f"анализ по запросу { search }")
        return f"search: { search }"

    if not input_play[0]: return
    if input_play[0][0] not in [ 'музыку', 'музыка', 'музыки' ]:
        if input_play[0][0] not in [ 'видео' ]:
            return "Command not found"
        else:
            return YouTubeVideo( input_play[0: len(input_play[0])])
    else:
        return Musik()


def Wikipedia( *search: tuple ):
    try:
        search = " ".join(search[0])
        wikipedia.set_lang(ASISTEN_SPEACH_LANGUAGE)
        page = wikipedia.page((search))
        page.html
        speach(page.summary)
        return f"Wikipedia: { page.title }"
    except:
        return "Conection error"


def Browser( *search: tuple):
    search = " ".join(search[0])
    try:
        webbrowser.open(f"https://www.google.com/search?q={ search }")
        speach(f"анализ по запросу { search }")
        return f"search: { search }"
    except:
        return "Conection error"
    

def StartFile( *filename: tuple ):
    for name_key in filename[0]:
        for file_key in commands['files']:

            if name_key in file_key:
                os.startfile(commands['files'][file_key])
                return f"start file:..."
            return "Command not fond"


def close( *args: tuple ):
    speach(example.RandomTranslateText(stt=True))
    sys.exit(1)

commands = {
    ('открой','Открой','войти','войди','зайти','зайди') :StartFile,
    ('ищи','кто','найди','Найди','найти') :Browser,
    ('сколько','Сколько','Который','какое','какой','сейчас','который','сегодняшний','сегодняшнее','сегодняшняя','сегодняшнюю') :Today,
    ('кто','расскажи','расскажи мне','Расскажи','Что','Кто','скажи') :Wikipedia,
    ('Выключи','Поставь','включи','поставь') :Play,
    ('пока', 'отключись', 'выключись', 'хватит', 'перестань', 'замолкни '): close,

    "files":{
        ('телеграф','телеграмм'):PATH_TELEGRAM,
        ('google','гугл','хром','кукол','гуго','угол','губы'):PATH_GOOGLE,
        ('YouTube','ютуб','юту'):PATH_YOUTUBE,
    },
}


def CMD(command: str = "", command_options: list = []):
    for key in commands.keys():
        if command in key:
            if command != "":
                print(f"{ASISTENT_NAME}:   {commands[ key ](command_options)}")
            return ""
        

def SintesText(text: str):
    voice_input = text.split(" ")
    command = voice_input[0]
    command_options = voice_input[1:]
    return command, command_options


def SpeachToTextOnPackeg():
    "oflayin recognition speack"
    text = ""
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=8000)
    stream.start_stream()
    while True:
        try:
            data = stream.read(400)
        except:
            return text
        finally:
            if len(data) == 0:
                break
            if res.AcceptWaveform(data):
                textj = json.loads(res.Result())
                text = textj['text']
                return text


def SpeachToTextOnOnlayin():
    "onlayin recognition speack"
    text = ""
    # recongizer.dynamic_energy_threshold = False
    # recongizer.energy_threshold = 1000
    # recongizer.pause_threshold = 0.5
    try:
        with micraphone as source:
            print("listening.......")
            recongizer.adjust_for_ambient_noise(micraphone, duration=2)
            try:
                audio = recongizer.listen(source, 5, 5)

            except speech_recognition.WaitTimeoutError:
                return "Can you check if your microphone is on, please?"
            try:
                text = recongizer.recognize_google(audio, language = ASISTENT_LANGUAGE).lower()
                return text
            
            except speech_recognition.UnknownValueError:
                return
            
            except speech_recognition.RequestError:
                return "Извините нет интернета пожалуйста подключить к интернету"
            
            finally:
                return text
    except:
        exit(1)


def main():
 
    while True:
        if ON_PATH_MODULE:
            listen = SpeachToTextOnPackeg()
        else:
            listen = SpeachToTextOnOnlayin()
        print(f"{USER_FIRST_NAME}:   {listen}")
        command, command_options = SintesText(listen)
        CMD(command, command_options)


if __name__=="__main__":
    
    if ON_PATH_MODULE:
        module = Model(MODULE)
        audio = pyaudio.PyAudio()
        res = KaldiRecognizer(module, 16000)

    if not ON_PATH_MODULE:
        recongizer = speech_recognition.Recognizer()
        micraphone = speech_recognition.Microphone(device_index=1)

    TTsEngine = pyttsx3.init("sapi5")
    example = Example()

    SetupVoiceAsisten()
    # speach(RandomTranslateText(tts=True))
    main()