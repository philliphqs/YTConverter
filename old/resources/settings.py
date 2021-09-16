from dearpygui.core import *
from dearpygui.simple import *
from YTConverter.old.resources.all_variables import *
from shutil import copyfile
import os
import json


def load_settings():
    if not os.path.isfile('resources/settings.json'):
        copyfile('resources/settings_preset.json', 'resources/settings.json')
    with open('resources/settings.json', 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    ThemeData = data['Settings']['Theme']
    LanguageData = data['Settings']['Language']
    set_value(ThemesCombo, value=ThemeData)
    set_value(LanguagesCombo, value=LanguageData)


def set_settings():
    if not os.path.isfile('resources/settings.json'):
        copyfile('resources/settings_preset.json', 'resources/settings.json')
    with open('resources/settings.json', 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        data['Settings']['Theme'] = get_value(ThemesCombo)
        data['Settings']['Language'] = get_value(LanguagesCombo)
        json.dump(data, open('resources/settings.json', 'w'), indent=2)
        load_settings()
