"""
The main file for the youtube-tui
"""
import curses
import curses.ascii
import string
from base import Application, Window, Tab

class Videos(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.has_border = True

class Search_bar(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        # The search string
        self.search_string = ""
        self.search_string_x = self.search_string_y = 1

        self.has_border = True

    def check_keys(self, key_pressed):
        if key_pressed < 0:
            return

        # When the user has pressed a ascii key,
        # update the search string
        if chr(key_pressed) in string.printable:
            self.search_string += chr(key_pressed)

        # When the user hast pressed the delete key,
        # remove the last character of the search string
        if key_pressed in [curses.ascii.BS, curses.KEY_BACKSPACE]:
            self.search_string = self.search_string[:len(self.search_string)-1]

    def late_update(self):
        # Draw the search string
        self.draw_text(self.search_string_y, self.search_string_x, self.search_string, self.get_color("text"))

class Youtube_tui(Window):
    def __init__(self, stdscr, application):
        super(__class__, self).__init__(stdscr, application)

        # Initializing the variable for the title
        self.title = "Youtube-TUI"
        self.title_x = self.title_y = 0

        # Adding the Search Bar to the Window and select it
        search_trans_x = 0
        search_trans_y = 1

        self.search_tab = Search_bar(self)
        self.search_tab.translate(search_trans_y, search_trans_x)

        self.search_tab.width = self.width - (search_trans_x + 1)
        self.search_tab.height = 2

        self.add_tab(self.search_tab, True)

        # Adding the Videos Tab to the Window
        videos_trans_x = 0
        videos_trans_y = search_trans_y + (self.search_tab.height + 1)

        self.videos_tab = Videos(self)
        self.videos_tab.translate(videos_trans_y, videos_trans_x)

        self.videos_tab.width = self.width - (videos_trans_x + 1)
        self.videos_tab.height = curses.LINES - (videos_trans_y + 2)

        self.add_tab(self.videos_tab, False)

        self.init_colors()

    def init_colors(self):
        curses.start_color()

        # Initialize the color pairs and add them to the window
        self.add_color(curses.COLOR_WHITE, curses.COLOR_BLACK, "text")
        self.add_color(curses.COLOR_BLACK, curses.COLOR_WHITE, "highlighted")
        self.add_color(curses.COLOR_RED, curses.COLOR_BLACK, "title")

    def update(self):
        # Calculating the x coordinate of the title,
        # based on the width of the terminal and the length of the title itself
        self.title_x = int((self.width // 2) - (len(self.title) // 2) - (len(self.title) % 2))

    def late_update(self):
        # Draw the title onto the screen
        self.draw_text(self.title_y, self.title_x, self.title, self.get_color("title"))

if __name__ == "__main__":
    app: Application = Application()
    app.set_main_window(Youtube_tui(app.stdscr, app))
    app.run()
