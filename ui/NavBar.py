import webbrowser

from resources.variables import *

import platform


def show():
    with menu_bar(label='NavBar', id=NavBar):
        file()
        edit()
        help_()
        about()

        add_spacing(count=48)

        vp_actions()


def file():
    with menu(label='File', id=FileMenu):
        add_menu_item(label='Exit', callback=stop_dearpygui)


def edit():
    with menu(label='Edit', id=EditMenu):
        add_menu_item(label='Settings')


def help_():
    with menu(label='Help', id=HelpMenu):
        add_menu_item(label='Report bug', callback=github_issue)


def about():
    with menu(label='About', id=AboutMenu):
        add_menu_item(label='GitHub Repo', callback=github_repo)


def vp_actions():
    add_menu_item(label='_', callback=minimize_viewport)
    add_menu_item(label='X', callback=stop_dearpygui)


def github_repo():
    webbrowser.open('https://github.com/philliphqs/YTConverter')


def github_issue():
    body = f'body=%23%23%23%23%20Description%0A' \
           f'%23%23%23%23%23%23%20...%0A' \
           f'%23%23%23%23%20Environment%0A' \
           f'%20*%20YTConverter%0A' \
           f'%20*%20Platform:%20{platform.system()}%0A' \
           f'%20*%20Arch:%20{platform.architecture()[0]}%0A' \
           f'%20*%20OS%20Version:%20{platform.version()}%0A' \
           f'%20*%20Python%20Version:%20{platform.python_version()}%0A' \
           f'%20*%20Proccesor:%20{platform.processor()}%0A' \
           f'%20*%20App%20Version:%200.0.1-alpha'

    webbrowser.open(url='https://github.com/philliphqs/ytconverter/issues/new?'+body)

