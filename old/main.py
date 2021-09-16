from dearpygui.core import *
from dearpygui.simple import *
from YTConverter.old.resources.themes import check_theme, set_default_style
from YTConverter.old.resources.languages import check_language, get_langdata
from YTConverter.old.resources.all_variables import *
from YTConverter.old.resources.settings import load_settings
import time
import youtube_dl
import os
import logging

logging.basicConfig(level=logging.INFO)

dlpath = 'downloads'
colors = {'red': [190, 58, 58, 255], 'green': [80, 190, 58, 255]}


class Show:
    def __init__(self):
        pass

    def reverse_download_checkbox(self, sender, data):
        show_item(IsReverseCheckbox)
        show_item('checkbox_same_line')


class Hide:
    def __init__(self):
        pass

    def reverse_download_checkbox(self, sender, data):
        hide_item(IsReverseCheckbox)
        hide_item('checkbox_same_line')


class Close:
    def __init__(self):
        pass

    def settings_popup(self, sender, data):
        close_popup(SettingsPopup)

    def download_popup(self, sender, data):
        close_popup(DownloadPopup)
        configure_item(AbortDownloadButton, label=get_langdata()['DownloadPopup']['AbortDownloadButton']['Label0'])


class Tools:
    def __init__(self):
        pass

    def _start_download(self, sender, data):
        run_async_function(self.wait, data=None)
        url = get_value(YouTubeURLInput)
        if url == '':
            set_value(name=DownloadStatusText, value=get_langdata()['DownloadPopup']['StatusText']['Label1'])
            return
        else:
            try:
                youtube_dl.YoutubeDL({'extract_flat': True, 'quiet': True}).extract_info(url, download=False)
            except youtube_dl.DownloadError:
                set_value(name=DownloadStatusText, value=f"{url} {get_langdata()['DownloadPopup']['StatusText']['Label2']}")
                return

        folder_name = get_value(FolderNameInput)
        archive_name = folder_name
        if folder_name == '':
            info = youtube_dl.YoutubeDL({'extract_flat': True, 'quiet': True}).extract_info(url, download=False)
            if 'entries' in info:
                folder_name = info['title']
            else:
                folder_name = info['title']
            archive_name = folder_name
        else:
            pass

        NEWLINE = True
        DOWNLOAD_ARCHIVE = f"{dlpath}/{folder_name}/archive/{folder_name}_archive.txt"
        OUTPUTPLAYLIST = f'{dlpath}/{folder_name}/%(playlist_index)s. %(artist)s - %(track)s.%(ext)s'
        OUTPUTVIDEO = f'{dlpath}/{folder_name}/%(title)s.%(ext)s'
        POSTPROCESSORS = [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'}]
        POSTPROCESSORS_ARGS = ['-id3v2_version', '3', '-metadata', f"album={folder_name}"]
        FORMAT = 'bestaudio[ext=m4a]'
        WRITETHUMBNAIL = True
        PLAYLISTREVERSE = get_value(IsReverseCheckbox)
        PREFER_FFMPEG = True
        VERBOSE = True
        KEEPVIDEO = False
        CACHEDIR = False
        HLSPREFER = True
        NO_OVERWRITES = False
        NO_PLAYLIST = not get_value(IsPlaylistCheckbox)

        def ytdl_opts():
            if get_value(IsPlaylistCheckbox):
                return {
                    'progress_with_newline': NEWLINE,
                    'download_archive': DOWNLOAD_ARCHIVE,
                    'outtmpl': OUTPUTPLAYLIST,
                    'postprocessors': POSTPROCESSORS,
                    'postprocessor_args': POSTPROCESSORS_ARGS,
                    'format': FORMAT,
                    'writethumbnail': WRITETHUMBNAIL,
                    'playlistreverse': PLAYLISTREVERSE,
                    'prefer_ffmpeg': PREFER_FFMPEG,
                    'verbose': VERBOSE,
                    'keepvideo': KEEPVIDEO,
                    'cachedir': CACHEDIR,
                    'hls_prefer_native': HLSPREFER,
                    'nooverwrites': NO_OVERWRITES,
                    'noplaylist': NO_PLAYLIST
                }
            else:
                return {
                    'progress_with_newline': NEWLINE,
                    'download_archive': DOWNLOAD_ARCHIVE,
                    'outtmpl': OUTPUTVIDEO,
                    'postprocessors': POSTPROCESSORS,
                    'postprocessor_args': POSTPROCESSORS_ARGS,
                    'format': FORMAT,
                    'writethumbnail': WRITETHUMBNAIL,
                    'playlistreverse': PLAYLISTREVERSE,
                    'prefer_ffmpeg': PREFER_FFMPEG,
                    'verbose': VERBOSE,
                    'keepvideo': KEEPVIDEO,
                    'cachedir': CACHEDIR,
                    'hls_prefer_native': HLSPREFER,
                    'nooverwrites': NO_OVERWRITES,
                    'noplaylist': NO_PLAYLIST
                }

        try:
            os.mkdir(f'{dlpath}/{folder_name}')
        except FileExistsError:
            pass
        try:
            os.mkdir(f'{dlpath}/{folder_name}/archive')
        except FileExistsError:
            pass
        ytdl = youtube_dl.YoutubeDL(ytdl_opts())
        ytdl.extract_info(url, download=True)
        os.startfile(os.path.realpath(f'{dlpath}/{folder_name}'))
        set_value(name=DownloadStatusText, value=get_langdata()['DownloadPopup']['StatusText']['Label3'])

    def start_download(self, sender, data):
        set_value(name=DownloadStatusText, value=get_langdata()['DownloadPopup']['StatusText']['Label4'])
        logging.info(msg=run_async_function(self._start_download, data=None, return_handler=AsycronFunc().configure_AbortDownloadButton))

    def wait(self, sender, data):
        time.sleep(0)

    def print_check(self, sender, data):
        logging.info(msg='Print Check')

    def check_is_playlist_checkbox(self, sender, data):
        if get_value(IsPlaylistCheckbox):
            Show().reverse_download_checkbox(sender, data)
        else:
            Hide().reverse_download_checkbox(sender, data)
            set_value(IsReverseCheckbox, False)


class Settings:
    def __init__(self):
        pass

    def SetPositionDownloadMenueWindow(self, sender, data):
        if does_item_exist(DownloadMenueWindow):
            main_width = get_item_width(PrimaryWindow)
            main_height = get_item_height(PrimaryWindow)
            DownloadMenue_width = get_item_width(DownloadMenueWindow)
            DownloadMenue_height = get_item_height(DownloadMenueWindow)
            set_window_pos(DownloadMenueWindow, int((main_width / 2 - DownloadMenue_width / 2)),
                           int((main_height / 2 - DownloadMenue_height / 2)))
        else:
            set_render_callback(None)

    def SetPositionSettingsPopup(self, sender, data):
        if does_item_exist(SettingsPopup):
            main_width = get_item_width(PrimaryWindow)
            main_height = get_item_height(PrimaryWindow)
            Settings_width = get_item_width(SettingsPopup)
            Settings_height = get_item_height(SettingsPopup)
            set_window_pos(SettingsPopup, int((main_width / 2 - Settings_width / 2)),
                           int((main_height / 2 - Settings_height / 2)))
        else:
            set_render_callback(None)

    def SetPositionDownloadPopup(self, sender, data):
        if does_item_exist(DownloadPopup):
            main_width = get_item_width(PrimaryWindow)
            main_height = get_item_height(PrimaryWindow)
            Download_width = get_item_width(DownloadPopup)
            Download_height = get_item_height(DownloadPopup)
            set_window_pos(DownloadPopup, int((main_width / 2 - Download_width / 2)),
                           int((main_height / 2 - Download_height / 2)))
        else:
            set_render_callback(None)


class AsycronFunc:
    def __init__(self):
        pass

    def configure_AbortDownloadButton(self, sender, data):
        configure_item(AbortDownloadButton, label=get_langdata()['DownloadPopup']['AbortDownloadButton']['Label1'])


class Main(Show, Hide, Close, Tools, Settings, AsycronFunc):
    def __init__(self):
        super().__init__()

    with window(name=DownloadMenueWindow, no_title_bar=True, autosize=True, no_resize=True, no_close=True, no_collapse=True, no_move=True):
        set_render_callback(Settings().SetPositionDownloadMenueWindow)
        # adds everything
        add_input_text(name=FolderNameInput, width=400, parent=DownloadMenueWindow)
        add_input_text(name=YouTubeURLInput, width=400, parent=DownloadMenueWindow)
        add_checkbox(name=IsPlaylistCheckbox, callback=Tools().check_is_playlist_checkbox, parent=DownloadMenueWindow)
        add_same_line(name='checkbox_same_line', parent=DownloadMenueWindow)
        add_checkbox(name=IsReverseCheckbox, parent=DownloadMenueWindow)
        add_button(name=StartDownloadButton, callback=Tools().start_download, parent=DownloadMenueWindow)
        add_same_line(parent=DownloadMenueWindow)
        add_button(name=OpenSettingsButton, parent=DownloadMenueWindow)
        # hide everything
        hide_item(IsReverseCheckbox)
        hide_item('checkbox_same_line')

    with popup(name=SettingsPopup, popupparent=OpenSettingsButton, modal=True, mousebutton=mvMouseButton_Left, width=600, height=500, parent=DownloadMenueWindow):
        add_combo(name=ThemesCombo, items=['Default', 'Light', 'Cherry', 'Grey', 'Custom [NOT AVAILABLE]'], default_value='Default', width=200, callback=check_theme, parent=SettingsPopup)
        add_combo(name=LanguagesCombo, items=['English', 'German (Deutsch)'], default_value='English', width=200, callback=check_language, parent=SettingsPopup)
        with tree_node(name=CustomColorNode, parent=SettingsPopup):
            hide_item(CustomColorNode)
            add_slider_int3(name='RGB_Slider', min_value=0, max_value=255, default_value=[30, 155, 90],
                            callback=None, show=False)
        with tree_node(name=SettingsAboutNode, parent=SettingsPopup):
            pass
        add_button(name=CloseSettingsButton, callback=Close().settings_popup, parent=SettingsPopup)

    with popup(name=DownloadPopup, popupparent=StartDownloadButton, modal=True, mousebutton=mvMouseButton_Left, width=600, height=500, parent=DownloadMenueWindow):
        add_text(name=DownloadStatusText, default_value=get_langdata()['DownloadPopup']['StatusText']['Label0'], parent=DownloadPopup)
        with tree_node(name=DownloadDetailNode, parent=DownloadPopup):
            pass
        add_text(name='                                                                 ', parent=DownloadPopup)
        add_button(name=AbortDownloadButton, callback=Close().download_popup, parent=DownloadPopup)


def start_dpg():
    def LoadSettings(sender, data):
        load_settings()
        check_theme(sender, data)
        check_language(sender, data)
        set_default_style()
    add_additional_font('resources/fonts/arial_narrow_7.ttf', 15)
    set_main_window_title(title='YouTube Downloader by Snosh')
    with window(name=PrimaryWindow, ):
        pass
    set_start_callback(LoadSettings)
    start_dearpygui(primary_window=PrimaryWindow)


start_dpg()
