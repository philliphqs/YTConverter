import os

import pytube.exceptions
from pytube import YouTube, Playlist

from resources.variables import *

from ui import Tags


def download_youtube_video(sender, app_data):
    set_viewport_height(50)

    try:
        Tags.delete()
    except:
        pass

    if is_item_shown(OpenFileButton):
        hide_item(OpenFileButton)

    path = get_value(FolderInput)
    url = get_value(YouTubeLinkInput)
    format = get_value(FormatCombo)
    playlist = get_value(PlaylistCheckbox)

    def open_file_spec():
        open_file(path + '/' + yt.title + '.' + format)

    if playlist is True:
        download_youtube_playlist(path, url)

    yt = YouTube(url)

    if format == 'Format':
        set_value(StatusText, 'Choose a Format!')
    else:
        try:
            set_value(StatusText, 'Downloading "'+yt.title+'"')

            if format == 'mp3':
                download_youtube_mp3(yt, path, open_file_spec)
            elif format == 'mp4':
                download_youtube_mp4(yt, path, open_file_spec)

            set_value(FolderInput, path)

        except Exception as e:
            set_value(StatusText, e)
        except pytube.exceptions.RegexMatchError:
            set_value(StatusText, "Can't resolve URL!")


def open_file(path):
    os.system(f'"{path}"')


def download_youtube_mp3(yt, path, open_file_spec):
    yt.streams.filter(only_audio=True).first().download(output_path=path, filename=yt.title + '.mp3')
    set_value(StatusText, 'Finished')
    #set_viewport_height(370)

    show_item(OpenFileButton)
    set_item_callback(OpenFileButton, open_file_spec)

    #Tags.show()
    #Tags.update(title=yt.title, artist=yt.author, album=None, year=str(yt.publish_date)[0] + str(yt.publish_date)[1]
    #                                                               + str(yt.publish_date)[2] + str(yt.publish_date)[3],
    #            track=None, genre=None)
    set_value(FolderInput, path + '/' + yt.title + '.mp3')


def download_youtube_mp4(yt, path, open_file_spec):
    yt.streams.filter().get_highest_resolution().download(output_path=path, filename=yt.title + '.mp4')
    set_value(StatusText, 'Finished')
    show_item(OpenFileButton)
    set_item_callback(OpenFileButton, open_file_spec)

    set_value(FolderInput, path + '/' + yt.title + '.mp4')


def download_youtube_playlist(url, format):
    print('Playlist')
    playlist = Playlist(url)
    set_value(StatusText, 'Downloading "'+playlist.title+'" ('+len(playlist.videos)+')')

    for video in playlist.videos:
        print(video)
        yt = YouTube(video)
        #download_youtube_mp4()