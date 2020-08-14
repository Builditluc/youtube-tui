import string
import curses
import curses.ascii
from base import Tab
from backend import search


class Search_bar(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        # The search string
        self.search_string = ""
        self.search_string_x = self.search_string_y = 1

        self.has_border = True
        self.show_cursor = True

    def check_keys(self, key_pressed):
        if key_pressed < 0:
            return

        # When the user has pressed a ascii key,
        # update the search string
        if any(chr(key_pressed) in sublist for sublist in [string.ascii_letters, string.digits, string.punctuation]) or key_pressed == curses.ascii.SP:
            self.search_string += chr(key_pressed)
            return

        # When the user hast pressed the delete key,
        # remove the last character of the search string
        if key_pressed in [curses.ascii.BS, curses.KEY_BACKSPACE, 127]:
            self.search_string = self.search_string[:len(self.search_string) - 1]
            return

        # When the user has pressed the return key,
        # search for the current string in youtube
        if key_pressed in (curses.KEY_ENTER, 10):
            self.parent.yt_videos = search(self.search_string)
            self.parent.videos_tab.scrollable_items = self.parent.yt_videos
            self.search_string = ""

    def update(self):
        # Calculate new cursor positions for the tab
        self.cursor_x = self.search_string_x + len(self.search_string)
        self.cursor_y = self.search_string_y

    def late_update(self):
        # Draw the search string
        self.draw_text(self.search_string_y, self.search_string_x, self.search_string, self.get_color("text"))
