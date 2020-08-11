"""
The main file for the youtube-tui
"""
import curses
from base import Application, Window, Tab


class Search_bar(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.scrollable_items.append(["##########"])
        self.scrollable_items.append(["##########"])
        self.scrollable_items.append(["##########"])
        self.scrollable_items.append(["##########"])

    def late_update(self):
        # Draw the scrollable items
        _x = _y = 0
        for item in self.scrollable_items:
            self.draw_text(_y, _x, item[0], self.get_color("text"))
            _y += 1


class Youtube_tui(Window):
    def __init__(self, stdscr, application):
        super(__class__, self).__init__(stdscr, application)

        # Initializing the variable for the title
        self.title = "Youtube-TUI"
        self.title_x = self.title_y = 0

        # Adding the Search Bar to the Window and select it
        self.add_tab(Search_bar(self), True)

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
