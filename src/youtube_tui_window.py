import curses
import curses.ascii
import sys
import threading
import load_config
from base import Window
from backend import get_main_page, YtVideo, close_driver
from widgets import search_bar, videos_list, voptions_field, help_menu, message_box


class Youtube_tui(Window):
    def __init__(self, stdscr, application):
        super(__class__, self).__init__(stdscr, application)

        self.yt_videos: [YtVideo] = []

        # Storing the config
        self.config = application.config

        # Initializing the variable for the title
        self.title = "Youtube-TUI"
        self.title_x = self.title_y = 0

        # Adding the Search Bar to the Window and select it
        search_trans_x = 0
        search_trans_y = 1

        self.search_tab = search_bar.Search_bar(self)
        self.search_tab.translate(search_trans_y, search_trans_x)

        self.search_tab.width = self.width - (search_trans_x + 11)
        self.search_tab.height = 2

        self.add_tab(self.search_tab, True)

        thread = threading.Thread(target=self.search_tab.start_search)
        thread.start()

        # Adding the Video Options Tab to the Window
        voptions_trans_x = 0
        voptions_trans_y = search_trans_y + (self.search_tab.height + 1)

        self.voptions_tab = voptions_field.VOptions(self)
        self.voptions_tab.translate(voptions_trans_y, voptions_trans_x)

        self.voptions_tab.width = 15
        self.voptions_tab.height = curses.LINES - (voptions_trans_y + 1)

        self.add_tab(self.voptions_tab, False)

        # Adding the Videos Tab to the Window
        videos_trans_x = voptions_trans_x + (self.voptions_tab.width + 1)
        videos_trans_y = search_trans_y + (self.search_tab.height + 1)

        self.videos_tab = videos_list.Videos(self)
        self.videos_tab.translate(videos_trans_y, videos_trans_x)

        self.videos_tab.width = self.width - (videos_trans_x + 1)
        self.videos_tab.height = curses.LINES - (videos_trans_y + 1)

        self.add_tab(self.videos_tab, False)

        # Adding the Help menu Tab to the window
        help_trans_x = self.width - 10
        help_trans_y = search_trans_y

        self.help_tab = help_menu.Help_menu(self)
        self.help_tab.translate(help_trans_y, help_trans_x)

        self.help_tab.width = self.width - (help_trans_x + 1)
        self.help_tab.height = self.search_tab.height

        self.add_tab(self.help_tab, False)

        self.init_colors()

    def __del__(self):
        close_driver()
        print("\nDriver was closed")
        sys.exit()

    def init_colors(self):
        curses.start_color()

        # Initialize the color pairs and add them to the window
        self.add_color(curses.COLOR_WHITE, curses.COLOR_BLACK, "text")
        self.add_color(curses.COLOR_BLACK, curses.COLOR_WHITE, "highlighted")
        self.add_color(curses.COLOR_RED, curses.COLOR_BLACK, "title")

    def check_keys(self):
        # If the user pressed the Tab key,
        # switch the current tab
        if self.key_pressed == self.get_binding("switch_tabs"):
            self.select_next_tab()

        # If the user pressed the quit key,
        # quit the program
        if self.key_pressed == self.get_binding("quit"):
            self.__del__()

        if self.key_pressed == ord("?"):
            self.application.switch_window("help")

    def update(self):
        # Calculating the x coordinate of the title,
        # based on the width of the terminal and the length of the title itself
        self.title_x = int((self.width // 2) - (len(self.title) // 2) - (len(self.title) % 2))

    def late_update(self):
        # Draw the title onto the screen
        self.draw_text(self.title_y, self.title_x, self.title, self.get_color("title"))

    def get_binding(self, name:str):
        return load_config.get_binding(name, self.config)
