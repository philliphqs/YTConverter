from flask import Flask, jsonify, request

from dearpygui.dearpygui import *

from ui import Window

import threading

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "result": "working"
    })


@app.route('/download')
def download():
    url = request.headers.get('url')
    Window.set_youtubelink()


def init_app():
    pass


def main():
    init_app()

    app.run(port=54230, debug=True)  # http://localhost:54230/


if __name__ == '__main__':
    main()
