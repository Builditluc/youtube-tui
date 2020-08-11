"""
The main file for the youtube-tui
"""
from base import Application, Window

class youtube_tui(Window):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

if __name__ == "__main__":
    app: Application = Application()
    app.set_main_window(youtube_tui(app.stdscr, app))
    app.run()