""""
Simple classes for the youtube-tui Window and Application
"""

import curses
import time


class Tab:
    """
    Simple class for a tab
    """
    def __init__(self, parent):
        super(__class__, self).__init__()

        # Saves the Window of the tab in a variable
        self.parent = parent

    def check_keys(self):
        """
        This function will be called every frame but only
        when the tab is focussed
        """

    def update(self):
        """
        This function will be called every frame but only
        when the tab is focussed. Its called before the screen is cleared
        """

    def late_update(self):
        """
        This function will be called every frame but only
        when the tab is focussed. Its called after the screen is cleared
        """


class Window:
    """
    Simple class for a curses Window
    """

    def __init__(self, stdscr, application):
        super(__class__, self).__init__()

        # Saves the Screen of the Window and the parent application in a variable
        self.stdscr: curses.window = stdscr
        self.application: Application = application

        # Creating the variables of the size of the Window
        self.width = int
        self.height = int

        # Creating the variable for the Keyinput
        self.key_pressed = int

        # ALl of the tabs in the window
        self.tabs: [[int, Tab]] = []

        # The current tab
        self.current_tab = int

        # An array of the initializes colors
        self._colors: [[str, int]] = []

    def init_colors(self):
        """
        Function for initiating the colors of a Window.
        Must be called manually.
        """

    def update(self):
        """
        This function will be called every time the Window updates.
        Mostly, you will do calculations of coordinates for the drawing in here.
        """

    def late_update(self):
        """
        This function will be called every time after the update function.
        Mostly, you will draw things on the screen here.
        """

    def check_keys(self):
        """
        This function will be called every frame.
        """

    def window_update(self):
        """
        This function will be called from the Application and calls
        functions like update or lateUpdate.
        Do not change anything in here!
        """
        self.height, self.width = self.stdscr.getmaxyx()
        self.key_pressed = self.stdscr.getch()
        self.check_keys()

        self.update()

        # Clear the Screen
        self.stdscr.erase()

        self.late_update()

        # Refreshing the Screen at the end of the Frame
        self._update_screen()

    def _update_screen(self):
        """
        This function just refreshes the Screen.
        """
        self.stdscr.refresh()

    def draw_text(self, y_coord, x_coord, text, color_code):
        """
        This function draws text on the screen
        :param y_coord: The y-Coordinate
        :param x_coord: The x_coord-Coordinate
        :param text: The text that will be drawn at the Coordinates
        :param color_code: The Code of the Color Pair you want to use for the text
        """
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.attron(curses.color_pair(color_code))

        self.stdscr.addstr(y_coord, x_coord, text)

        self.stdscr.attroff(curses.A_BOLD)
        self.stdscr.attroff(curses.color_pair(color_code))

    def add_color(self, text_color, bg_color, name):
        """
        Inits a color pair in curses with a name. curses.init_colors must be called before this!
        :param text_color: Color of the Text
        :param bg_color: Color of the Background
        :param name: The name of the color
        """
        pair_number = len(self._colors)
        curses.init_pair(pair_number, text_color, bg_color)
        self._colors.append([name, int])

    def get_color(self, name):
        """
        Returns the pair number of a color pair with its name
        :param name: The name of the color pair
        :return: int - The pair number of the color pair. If -1 then the color pair could not be found
        """
        # Iterate through every color pair
        for color_pair in self._colors:
            if color_pair[0] == name:
                return color_pair[1]

        # If the color pair could not be found,
        # return -1
        return -1

    def add_tab(self, tab:Tab, is_current:bool):
        """
        Adds a tab to the window
        :param tab: The tab that will be added to the window
        :param is_current: If the Tab should be the current tab of the window
        """
        tab_number = len(self.tabs)
        self.tabs.append([tab_number, tab])

        if is_current:
            self.current_tab = tab_number

    def select_next_tab(self):
        """
        Selects the next tab of the window
        """
        current_tab_number = self.current_tab

        # If the current tab is the last tab,
        # select the first
        if current_tab_number == len(self.tabs):
            self.current_tab = 0
            return

        # Increase the current number by one
        self.current_tab += 1

    def select_previous_tab(self):
        """
        Selects the previous tab of the window
        """
        current_tab_number = self.current_tab

        # If the current tab is the first tab,
        # select the last
        if current_tab_number == 0:
            self.current_tab = len(self.tabs)
            return

        # Decrease the current number by one
        self.current_tab -= 1

    @staticmethod
    def set_cursor_state(state: int):
        """
        Changes the Cursor in the window
        :param state: 0 - Hides the Cursor
        :param state: 1 - Shows the Cursor
        :param state: 2 - Makes the Cursor highly visible
        """
        curses.curs_set(state)

    def exit(self):
        """
        This function will be called, when the program closes
        """


class Application:
    """
    Simple class for a application managing a window
    """
    colormode: bool
    no_delay: bool

    def __init__(self):
        super(__class__, self).__init__()
        time.sleep(0.5)

        # First, initiating the Screen and defining a variable for the MainWindow of the Application
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.window = None

        curses.noecho()
        curses.cbreak()

        # Check, if the terminal supports colors and activates the NoDelay mode, if enabled
        self.colormode = curses.has_colors()
        self.no_delay = True
        if self.no_delay:
            self.stdscr.nodelay(True)

    def set_main_window(self, window: Window):
        """
        This function sets the MainWindow of the application
        :param window: The Window
        """
        self.window = window

    def run(self, time_wait=0.015):
        """
        This function starts the Programm
        :param time_wait: Time to wait between the frame updates
        """
        while True:
            self.window.window_update()
            time.sleep(time_wait)
