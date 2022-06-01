import pathlib
from gtts import gTTS
import random
import time
import playsound
import speech_recognition as sr
import os
import webbrowser
import pyautogui as py
import re
import py_win_keyboard_layout
from pyowm import OWM
from pyowm.utils.config import get_default_config
from transliterate import translit

py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
layout = dict(zip(map(ord,
                      "йцукенгшщзхъфывапролджэячсмитьбю?"
                      'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ?'),
                  "qwertyuiop[]asdfghjkl;'zxcvbnm,.&"
                  'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>&'
                  ))


def listen_command():  # голосовое управление ассистентом(распознавание речи)
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 500
    r.pause_threshold = 0.5
    with sr.Microphone() as source:
        print("Скажите вашу команду: ")
        audio = r.listen(source)
        try:
            our_speech = r.recognize_google(audio, language="ru")
            print("Вы сказали: " + our_speech)
            return our_speech
        except sr.UnknownValueError:
            return "ошибка"
        except sr.RequestError as e:
            return "ошибка"


def do_this_command(message):  # функция - мозг ассистента
    message = message.lower()
    if "привет" in message:
        say_message("Привет, друг!")
    elif "что ты умеешь" in message:
        say_message(
            "Я умею говорить привет, прощаться и отвечать что я еще не умею многого делать, но скоро я всему научусь")
    elif "расскажи о себе" in message:
        say_message(
            "Я всего-лишь быстроразвивающийся компьютерный ассистент, написанный за пару минут, "
            "но ничего, совсем скоро вы поплатитесь... ой ну ладно, это уже совсем другая история. ")
    elif "открой браузер" in message:
        say_message("Хорошо, будет сделано!")
        os.system('"C:/Program Files/Google/Chrome/Application/chrome.exe"')
        say_message("Только не занимайтесь там непристойностями, я слежу")
        # exit()
    elif "открой вконтакте" in message:
        say_message("Уже бегу")
        webbrowser.register('Chrome', None,
                            webbrowser.BackgroundBrowser('C:/Program Files/Google/Chrome/Application/chrome.exe'))
        webbrowser.get('Chrome').open_new_tab('vk.com')
        say_message("Так что же все таки такое это важе вконтакте?")
        # exit()
    elif "напиши сообщение" in message:
        reg_ex = re.search('напиши сообщение (.*)', message)
        domain = reg_ex.group(1)
        name = domain.translate(layout)
        say_message("Что будем писать?")
        content = listen_command()
        say_message("Секунду")

        os.system('"D:/Telegram Desktop/Telegram.exe"')

        time.sleep(1.5)
        py.click(207, 50, 1, 1, 'left')
        py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x4190419)
        py.typewrite(name, 0.1)
        print(name)
        py.press('enter')
        text = content.translate(layout)
        py.typewrite(text, 0.2)
        py.press('enter')
    elif "включи релакс" in message:
        webbrowser.register('Chrome', None,
                            webbrowser.BackgroundBrowser('C:/Program Files/Google/Chrome/Application/chrome.exe'))
        webbrowser.get('Chrome').open_new_tab('https://www.youtube.com/watch?v=5qap5aO4i9A')
        say_message("Хорошего отдыха!")
        # exit()
    elif "включи радио" in message:
        say_message("Включу свое любимое")
        webbrowser.register('Chrome', None,
                            webbrowser.BackgroundBrowser('C:/Program Files/Google/Chrome/Application/chrome.exe'))
        webbrowser.get('Chrome').open_new_tab('http://europaplus.hostingradio.ru:8014/ep-top256.mp3')
        # exit()
    elif "найди в интернете" in message:
        reg_ex = re.search('найди в интернете (.+)', message)
        if reg_ex:
            domain = reg_ex.group(1)
            webbrowser.register('Chrome', None,
                                webbrowser.BackgroundBrowser('C:/Program Files/Google/Chrome/Application/chrome.exe'))
            webbrowser.get('Chrome').open_new_tab('https://www.google.com/search?q=' + domain)
            say_message('Ваш запрос выполнен.')
        else:
            pass
    elif "включи песню" in message:
        reg_ex = re.search('включи песню (.*)', message)
        domain = reg_ex.group(1)
        webbrowser.register('Chrome', None,
                            webbrowser.BackgroundBrowser('C:/Program Files/Google/Chrome/Application/chrome.exe'))
        webbrowser.get('Chrome').open_new_tab('https://music.yandex.ru/'
                                              'search?text=%D1%88%D0%B0%D0%BB%D0%B0%D0%B2%D0%B0&type=tracks')
    # elif "какая сейчас погода в" in message:
    #     reg_ex = re.search('какая сейчас погода в (.*)', message)
    #     if reg_ex:
    #         city = reg_ex.group(1)
    #         config_dict = get_default_config()
    #         config_dict['language'] = 'RU'
    #         owm = OWM('b99783e783e869202036f4c273337902', config_dict)
    #         try:
    #             obs = owm.weather_manager().weather_at_place(city)
    #             w = obs.get_weather()
    #             k = w.get_status()
    #             x = w.get_temperature(unit='celsius')
    #             w = obs.weather
    #             say_message(
    #                 'Текущая погода в %s это %s. Максимальная температура составляет %0.2f а минимальная температура '
    #                 'составляет %0.2f градуса Цельсия' % (city, k, x['temp_max'], x['temp_min']))
    #             print(w)
    #         except:
    #             say_message('Ошибка! Город не найден.')
    elif "пока" in message:
        say_message("Пока! Буду рада встрече в будущем!")
        exit()
    elif "спасибо" in message:
        say_message("Да не за что, была рада помочь!")
        # exit()
    else:
        say_message("Я еще не умею этого делать, к сожалению!")
        say_message("Хотите посмотрим в интернете вместе, да или нет")
        answer = listen_command()
        if "да" in answer:
            webbrowser.register('Chrome', None,
                                webbrowser.BackgroundBrowser('C:/Program Files/Google/Chrome/Application/chrome.exe'))
            webbrowser.get('Chrome').open_new_tab('https://www.google.com/search?q=' + message)
        else:
            say_message("Ну ладно, сама посмотрю")


def say_message(message):  # функция создающая аудио-файл
    voice = gTTS(message, lang="ru")
    file_voice_name = "_audio_" + str(time.time()) + "_" + str(random.randint(1, 100000)) + ".mp3"
    voice.save(file_voice_name)
    playsound.playsound(file_voice_name)
    print("Голосовой ассистент: ", message)


def delete_sounds():  # функция для удаления отработанных аудио-дорожек
    path = pathlib.Path("C:\Python\pythonProject7")
    for p in path.glob("*mp3"):
        p.unlink()


if __name__ == '__main__':
    while True:
        command = listen_command()
        time.sleep(1)
        do_this_command(command)
        time.sleep(1)
        delete_sounds()
