from settings import ASISTEN_SPEACH_LANGUAGE, ASISTENT_NAME, USER_FIRST_NAME
import random

translated = {
    'EN':{
        "tts":[
            f"Hellow mister, im {ASISTENT_NAME} im artifical asistent", f"Good day mister {USER_FIRST_NAME},...", "What can you help ?"
        ],
        "stt":[
            "Good by mister", "Good night", "By by"
        ],
        "tst":[
            ""
        ],
        "calendar":{
            '1':'January',   '2':'February',
            '3':'March',    '4':'April',
            '5':'May',      '6':'June',
            '7':'July',     '8':'August',
            '9':'September','10':'October',
            '11':'November', '12':'December'}
    },
    "RU":{
        "tts":[
            'c возвращением Мистер','какие планы на сегодня','чем мы занимаемся сегодня',
            'чудный день, не так ли','рад снова тебя видеть','привет'
        ],
        "stt":[
            'до новых встреч мистер','скоро увидимся','до свидания'
        ],
        "calendar":{
            '1':'января',   '2':'февраля',
            '3':'марта',    '4':'апреля',
            '5':'мая',      '6':'июня',
            '7':'июля',     '8':'августа',
            '9':'сентября','10':'октября',
            '11':'ноября', '12':'декабря'}
    }}

class Example:

    def RandomTranslateText(self, tts: bool=False, stt: bool=False):
        if ASISTEN_SPEACH_LANGUAGE == 'en':
            if tts:
                return translated["EN"]["tts"][random.randint(0, 2)]
            if stt:
                return translated["EN"]['stt'][random.randint(0, 2)]
            
        if ASISTEN_SPEACH_LANGUAGE == 'ru':
            if tts:
                return translated['RU']['tts'][random.randint(0, 4)]
            if stt:
                return translated['RU']['stt'][random.randint(0, 2)]
          

    def Calendar(self):
        if ASISTEN_SPEACH_LANGUAGE == 'en':
            return translated["EN"]['calendar']
        elif ASISTEN_SPEACH_LANGUAGE == 'ru':
            return translated['RU']['calendar']
        

# if __name__=='__main__':
#     print(MultiplaySpeach(tts=True))