from dearpygui.core import *
from dearpygui.simple import *
from YTConverter.old.resources.all_variables import *
from YTConverter.old.resources.settings import set_settings
import json


def set_lang(lang):
    with open(lang, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    # --- MainWindow ---
    FolderNameData = data['MainWindow']['FolderName']
    YouTubeURLData = data['MainWindow']['YouTubeURL']
    IsPlaylistData = data['MainWindow']['IsPlaylist']
    IsReverseData = data['MainWindow']['IsReverse']
    DownloadButtonData = data['MainWindow']['DownloadButton']
    SettingsButtonData = data['MainWindow']['SettingsButton']

    configure_item(FolderNameInput, label=FolderNameData['Label'], tip=FolderNameData['Tip'], hint=FolderNameData['Hint'])
    configure_item(YouTubeURLInput, label=YouTubeURLData['Label'], tip=YouTubeURLData['Tip'], hint=YouTubeURLData['Hint'])
    configure_item(IsPlaylistCheckbox, label=IsPlaylistData['Label'], tip=IsPlaylistData['Tip'])
    configure_item(IsReverseCheckbox, label=IsReverseData['Label'], tip=IsReverseData['Tip'])
    configure_item(StartDownloadButton, label=DownloadButtonData['Label'])
    configure_item(OpenSettingsButton, label=SettingsButtonData['Label'])

    # --- SettingsPopup ---
    ThemesComboData = data['SettingsPopup']['ThemesCombo']
    LanguagesComboData = data['SettingsPopup']['LanguageCombo']
    AboutNodeData = data['SettingsPopup']['AboutNode']
    CustomColorNodeData = data['SettingsPopup']['CustomColorNode']
    CloseSettingsButtonData = data['SettingsPopup']['CloseSettingsButton']

    configure_item(ThemesCombo, label=ThemesComboData['Label'])
    configure_item(LanguagesCombo, label=LanguagesComboData['Label'])
    configure_item(SettingsAboutNode, label=AboutNodeData['Label'])
    configure_item(CustomColorNode, label=CustomColorNodeData['Label'])
    configure_item(CloseSettingsButton, label=CloseSettingsButtonData['Label'])

    # --- DownloadPopup ---
    DownloadStatusTextData = data['DownloadPopup']['StatusText']
    DetailNodeData = data['DownloadPopup']['DetailNode']
    AbortDownloadButtonData = data['DownloadPopup']['AbortDownloadButton']

    configure_item(DownloadStatusText, default_value=DownloadStatusTextData['Label0'])
    configure_item(DownloadDetailNode, label=DetailNodeData['Label'])
    configure_item(AbortDownloadButton, label=AbortDownloadButtonData['Label0'])


def get_langdata():
    language = get_value(LanguagesCombo)
    if language == 'English':
        lang = 'resources/languages/en-gb.json'
    elif language == 'German (Deutsch)':
        lang = 'resources/languages/de-de.json'
    elif language is None:
        print('I got None language to check')
    with open(lang, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return data


def check_language(sender, data):
    language = get_value(LanguagesCombo)
    if language == 'English':
        set_lang(lang='resources/languages/en-gb.json')
    elif language == 'German (Deutsch)':
        set_lang(lang='resources/languages/de-de.json')
    elif language is None:
        print('I got None language to check')
    set_settings()
