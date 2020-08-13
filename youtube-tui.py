"""
The main file for the youtube-tui
"""
import curses
import curses.ascii
import string
from base import Application, Window, Tab
#import backend

class yt_video:
    def __init__(self, title_arg, creator_arg, url_arg):
        #global title
        #global creator
        #global url
        self.title = title_arg
        self.creator = creator_arg
        self.url = url_arg

yt_videos = []
for i in range(0, 100):
    title = "Yt - Video No. {}".format(i)
    creator = "Yt - Creator No. {}".format(i)
    url = "https://youtube.com/watch?id={}".format(i)

    new = yt_video(title, creator, url)

    yt_videos.append(new)

#yt_videos = backend.get_main_page()

#backend.driver.close()

class Videos(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.scrollable_items = yt_videos
        self.videos_x = self.videos_y = 1

        self.current_line = 2
        
        self.has_border = True
        self.show_title = True
        

    def update(self):
        # Calculate the max lines and the bottom line
        self.max_lines = self.height - 1
        self.bottom_line = len(self.scrollable_items)

    def late_update(self):
        # Draw the videos
        lines = self.scrollable_items[self.top_line:self.top_line + self.max_lines]
        for y_offset, video in enumerate(lines):
            draw_color = "text"
            if y_offset == self.current_line:
                draw_color = "highlighted"

            self.draw_text(self.videos_y + y_offset, self.videos_x, video.title, self.get_color(draw_color))

    def check_keys(self, key_pressed):
        # When the user has pressed the up key,
        # call the scroll function
        if key_pressed == curses.KEY_UP:
            self.scroll(self.scroll_up)
            return

        # When the user has pressed the down key,
        # call the scroll function
        if key_pressed == curses.KEY_DOWN:
            self.scroll(self.scroll_down)
            return


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
        if any(chr(key_pressed) in sublist for sublist in [string.ascii_letters, string.digits, string.punctuation]):
            self.search_string += chr(key_pressed)
            return

        # When the user hast pressed the delete key,
        # remove the last character of the search string
        if key_pressed in [curses.ascii.BS, curses.KEY_BACKSPACE]:
            self.search_string = self.search_string[:len(self.search_string) - 1]
            return

        # When the user has pressed the return key,
        # search for the current string in youtube
        if key_pressed == curses.KEY_ENTER:
            #yt_videos = backend.search(self.search_string)
            pass

    def update(self):
        # Calculate new cursor positions for the tab
        self.cursor_x = self.search_string_x + len(self.search_string)
        self.cursor_y = self.search_string_y

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
