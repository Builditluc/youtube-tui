"""
The main file for the youtube-tui
"""
import sys
from base import Application
from backend import driver
from load_config import get_shortcuts
from youtube_tui_window import Youtube_tui
from help_menu import Help_menu

if __name__ == "__main__":

    app: Application = Application()
    app.config = get_shortcuts()

    youtube_tui = Youtube_tui(app.stdscr, app)
    help_menu = Help_menu(app.stdscr, app)

    app.add_window(help_menu, "help")
    app.set_main_window(youtube_tui)

    """try:
        app.run()
    except BaseException as ex:
        print(ex)
        try:
            driver.close()
            print("\nDriver was closed")
        except:
            print("\nDriver was already closed")"""

    app.run()
    sys.exit()