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

        # Variables for the size of the tab
        self.width = 0
        self.height = 0

        # The items the user can scroll through
        self.scrollable_items = []

        # Variables for the Scrolling
        self.current_line = 0
        self.max_lines = self.height

        self.top_line = 0
        self.bottom_line = len(self.scrollable_items)

        # Variables for the scroll direction
        self.scroll_up = -1
        self.scroll_down = 1

        # Variables for the translation of coords
        self.translate_x = lambda x: x
        self.translate_y = lambda y: y

        # Variables for the cursor position
        self.cursor_x = self.cursor_y = 0

        # Variables for the border
        self.has_border = False

        # The title of the tab
        self.title = "New Tab"
        self.show_title = False
        self.show_cursor = False

    def check_keys(self, key_pressed):
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

    def scroll(self, direction):
        """
        Scrolling the window when pressing up/down arrow keys
        :param direction: The direction of the Scrolling (Up or Down)
        """
        # next cursor position after Scrolling
        next_line = self.current_line + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.scroll_up) and (self.top_line > 0 and self.current_line == 0):
            self.top_line += direction
            return

        # Down direction overflow
        # next cursor position touches the max lines,
        # but absolute position of max lines could not touch the bottom
        if (direction == self.scroll_down) and (next_line == self.max_lines) \
                and (not self.top_line + self.max_lines >= self.bottom_line):
            self.top_line += direction
            return

        # Scroll down
        # next cursor position is above max lines,
        # but absolute position of next cursor could not touch the bottom
        if (direction == self.scroll_down) and (next_line < self.max_lines) \
                and (self.top_line + next_line < self.bottom_line):
            self.current_line = next_line
            return

        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.scroll_up) and (self.top_line > 0 or self.current_line):
            self.current_line = next_line
            return

    def translate(self, y_coord, x_coord):
        """
        Translates the coordinates to another point
        :param y_coord: The y coord of the new point
        :param x_coord: The x coord of the new point
        """
        self.translate_x = lambda x: x + x_coord
        self.translate_y = lambda y: y + y_coord

    def draw_text(self, y_coord, x_coord, text, color_code):
        self.parent.draw_text(self.translate_y(y_coord), self.translate_x(x_coord), text, color_code)

    def get_color(self, name):
        return self.parent.get_color(name)


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
        self.height, self.width = self.stdscr.getmaxyx()

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
        self.check_keys();
        self._tab_check_keys()

        self.update();
        self._tab_update()

        # Clear the Screen
        self.stdscr.erase()

        self._tab_draw_border()
        self.late_update();
        self._tab_late_update()

        self._tab_move_cursor()

        # Refreshing the Screen at the end of the Frame
        self._update_screen()

    def _tab_update(self):
        # Iterate through every tab and call the update function
        for tab in self.tabs:
            tab[1].update()

    def _tab_late_update(self):
        # Iterate through every tab and call the late update function 
        for tab in self.tabs:
            tab[1].late_update()

    def _tab_check_keys(self):
        # Iterate through every tab and if the tab
        # is the current call its check keys function
        for tab in self.tabs:
            if tab[0] == self.current_tab:
                tab[1].check_keys(self.key_pressed)
                return

    def _tab_draw_border(self):
        # Iterate through every tab and draw
        # a border if needed
        for tab in self.tabs:
            if tab[1].has_border:
                # Draw the horizontal lines
                self.draw_text(tab[1].translate_y(0), tab[1].translate_x(0),
                               "\u2501" * tab[1].width, self.get_color("text"))
                self.draw_text(tab[1].translate_y(tab[1].height), tab[1].translate_x(0),
                               "\u2501" * tab[1].width, self.get_color("text"))

                # Draw the vertical lines
                for i in range(1, tab[1].height):
                    self.draw_text(tab[1].translate_y(i), tab[1].translate_x(0),
                                   "\u2503" + " " * (tab[1].width - 1) + "\u2503", self.get_color("text"))

                # Draw the edges
                self.draw_text(tab[1].translate_y(0), tab[1].translate_x(0), "\u250F",
                               self.get_color("text"))
                self.draw_text(tab[1].translate_y(0), tab[1].translate_x(tab[1].width), "\u2513",
                               self.get_color("text"))
                self.draw_text(tab[1].translate_y(tab[1].height), tab[1].translate_x(0), "\u2517",
                               self.get_color("text"))
                self.draw_text(tab[1].translate_y(tab[1].height), tab[1].translate_x(tab[1].width), "\u251B",
                               self.get_color("text"))
            if tab[1].show_title:
                # Draw the title
                title_color = "text"
                if tab[0] == self.current_tab:
                    title_color = "highlighted"

                self.draw_text(tab[1].translate_y(0), tab[1].translate_x(2),
                               tab[1].title, self.get_color(title_color))

    def _tab_move_cursor(self):
        # Iterate through every tab and move
        # the cursor if the tab is selected
        for tab in self.tabs:
            if tab[0] == self.current_tab:
                self.stdscr.move(
                    tab[1].translate_y(tab[1].cursor_y),
                    tab[1].translate_x(tab[1].cursor_x)
                )
                return

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
        pair_number = len(self._colors) + 1
        curses.init_pair(pair_number, text_color, bg_color)
        self._colors.append([name, pair_number])

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

    def add_tab(self, tab: Tab, is_current: bool):
        """
        Adds a tab to the window
        :param tab: The tab that will be added to the window
        :param is_current: If the Tab should be the current tab of the window
        """
        tab_number = len(self.tabs)
        self.tabs.append([tab_number, tab])

        if is_current:
            self.current_tab = tab_number

    def get_tab(self, tab_numer):
        """
        Gets the tab with the tab number
        :param tab_number: The number of the tab
        :return: If a tab was found the tab otherwise None
        """
        # Iterate trough every tab and compare the tab numbers
        for tab in self.tabs:
            if tab[0] == tab_numer:
                return tab[1]

        return None

    def select_next_tab(self):
        """
        Selects the next tab of the window
        """
        current_tab_number = self.current_tab

        # If the current tab is the last tab,
        # select the first
        if current_tab_number == len(self.tabs) - 1:
            self.current_tab = 0
            return

        # Increase the current number by one
        self.current_tab += 1

        # If the selected tab wants to hide the cursor,
        # hide it
        selected_tab: Tab = self.get_tab(self.current_tab)
        if selected_tab.show_cursor:
            self.set_cursor_state(1)
        else:
            self.set_cursor_state(0)
            self.stdscr.move(0, 0)

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
