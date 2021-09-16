from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3

from YTConverter.resources.variables import *


def show():
    size = 150

    width, height, channels, data = load_image('resources/cover.png')
    with texture_registry():
        cover = add_static_texture(width, height, data)

    add_image(cover, width=size, height=size, parent=MainWindow, id=TagsCoverImage)
    add_same_line(parent=MainWindow, id=CoverTagsInputsSameLine)

    with child(id=TagsInputs, parent=MainWindow, border=False, autosize_x=True, height=size):
        add_text('Title     ')
        add_same_line()
        add_input_text(width=161, id=TitleInput)

        add_same_line()

        add_text('Artist')
        add_same_line()
        add_input_text(width=174, id=ArtistInput)

        add_text('Album ')
        add_same_line()
        add_input_text(width=378, id=AlbumInput)

        add_text('Year    ')
        add_same_line()
        add_input_text(width=50, hexadecimal=True, id=YearInput)

        add_same_line()

        add_text('Track')
        add_same_line()
        add_input_text(width=65, id=TrackInput)

        add_same_line()

        add_text('Genre')
        add_same_line()
        add_input_text(width=167, id=GenreInput)

        with child(id=12, autosize_x=True, height=81, border=True):
            pass

        add_button(label='Save', width=582, callback=update_tags, parent=MainWindow, id=TagsSaveButton)


def delete():
    delete_item(TagsInputs, children_only=True)
    delete_item(TagsInputs)
    delete_item(TagsCoverImage)
    delete_item(TagsSaveButton)
    delete_item(CoverTagsInputsSameLine)


def update(title, artist, album, year, track, genre):
    set_value(TitleInput, title)
    set_value(ArtistInput, artist)
    set_value(AlbumInput, album)
    set_value(YearInput, year)
    set_value(TrackInput, track)
    set_value(GenreInput, genre)


def update_tags():
    path = get_value(FolderInput)
    title = get_value(TitleInput)
    artist = get_value(ArtistInput)
    album = get_value(AlbumInput)
    year = get_value(YearInput)
    track = get_value(TrackInput)
    genre = get_value(GenreInput)

    # Read the ID3 tag or create one if not present
    try:
        tags = ID3(path)
    except ID3NoHeaderError:
        print('Adding ID3 header')
        set_value(StatusText, "Adding ID3 header")
        tags = ID3()

    tags['title'] = f'{title}'
    tags['artist'] = f'{artist}'
    tags['album'] = f'{album}'

    print('Saving File')
    set_value(StatusText, 'Saving File')
    tags.save(path)
    set_value(StatusText, 'Finished')
