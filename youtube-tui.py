"""
The main file for the youtube-tui
"""
import curses
import curses.ascii
from base import Application, Window
from backend import get_main_page, YtVideo
from widgets import search_bar, videos_list

class Youtube_tui(Window):
    def __init__(self, stdscr, application):
        super(__class__, self).__init__(stdscr, application)

        self.yt_videos: [YtVideo] = get_main_page()

        # Initializing the variable for the title
        self.title = "Youtube-TUI"
        self.title_x = self.title_y = 0

        # Adding the Search Bar to the Window and select it
        search_trans_x = 0
        search_trans_y = 1

        self.search_tab = search_bar.Search_bar(self)
        self.search_tab.translate(search_trans_y, search_trans_x)

        self.search_tab.width = self.width - (search_trans_x + 1)
        self.search_tab.height = 2

        self.add_tab(self.search_tab, True)

        # Adding the Videos Tab to the Window
        videos_trans_x = 0
        videos_trans_y = search_trans_y + (self.search_tab.height + 1)

        self.videos_tab = videos_list.Videos(self)
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

    def check_keys(self):
        # If the user pressed the Tab key,
        # switch the current tab
        if self.key_pressed == curses.ascii.TAB:
            self.select_next_tab()

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
