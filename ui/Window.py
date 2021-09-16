from tkinter import Tk, filedialog

from YTConverter.resources.variables import *

from YTConverter.ui import NavBar as NavBar_

from YTConverter.backend import youtube


def dragViewport():
    drag_deltas = get_mouse_drag_delta()
    viewport_current_pos = get_viewport_pos()
    set_viewport_pos([viewport_current_pos[0] + drag_deltas[0], viewport_current_pos[1] + drag_deltas[1]])


with handler_registry():
    add_mouse_drag_handler(callback=dragViewport)


def font_():
    with font_registry():
        add_font(file='resources/arial.ttf', size=13, default_font=True)


def font_poppins():
    with font_registry():
        add_font(file='resources/poppins.ttf', size=18)


def show():
    with window(label='YTConverter', id=MainWindow):
        NavBar_.show()
        content()

    set_item_font(last_item(), font=font_())

    viewport_init()
    start_dearpygui()


def viewport_init():
    vp = create_viewport()
    setup_dearpygui(viewport=vp)
    configure_viewport(0, height=50, width=600, x_pos=600, y_pos=200)

    minimize_viewport()

    set_viewport_title("YTConverter")
    set_viewport_always_top(True)
    set_viewport_resizable(True)
    # set_viewport_small_icon('')
    # set_viewport_large_icon('')
    # set_viewport_height()
    # set_viewport_width()
    set_viewport_decorated(False)
    set_primary_window(MainWindow, True)
    show_viewport(vp)


def content():
    width, height, channels, data = load_image('resources/icon_no_border.png')
    with texture_registry():
        image = add_static_texture(width, height, data)

    size = 100
    add_image(image, width=size, height=size)

    add_same_line()

    with child(autosize_x=True, height=size, border=False):
        add_spacing(count=4)
        add_button(label='Select Folder', callback=selectfolder)
        add_same_line()
        add_input_text(id=FolderInput, readonly=True, width=400)

        add_text('YouTube Link ')
        add_same_line()
        add_input_text(id=YouTubeLinkInput, uppercase=False, width=400)

        add_separator()

        # add_checkbox(label='Playlist', id=PlaylistCheckbox, default_value=False)
        # add_same_line()
        add_combo(items=['mp3', 'mp4'], default_value='Format', width=80, id=FormatCombo)

    add_separator()

    add_button(label='Download', width=582, callback=youtube.download_youtube_video)

    add_separator()

    add_text('Status: ')
    add_same_line()
    add_text(id=StatusText, default_value=None)
    add_same_line()
    add_button(label='Open', id=OpenFileButton, show=False)

    add_separator()


def selectfolder():
    Tk().withdraw()
    file_path = filedialog.askdirectory()
    DirString = file_path
    set_value(FolderInput, DirString)
