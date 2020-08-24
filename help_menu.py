import curses
import curses.ascii
import load_config
from base import Window

class Help_menu(Window):
    def __init__(self, stdscr, application):
        super(__class__, self).__init__(stdscr, application)

        self.help_items = [
            "Switch between tabs",
            "Search",
            "Select a Video",
            "Scroll Up",
            "Scroll Down",
            "Scroll Left",
            "Scroll Right",
            "Quit the program",
        ]

        self.set_cursor_state(0)
        self.init_colors()

    def init_colors(self):
        curses.start_color()
        self.add_color(curses.COLOR_WHITE, curses.COLOR_BLACK, "text")

    def check_keys(self):
        if self.key_pressed == ord("?"):
            self.application.switch_window("main")

    def late_update(self):
        description_x = 1
        binding_x = int(self.width/2)

        self.draw_text(1, description_x, "Description", self.get_color("text"))
        self.draw_text(1, binding_x, "Binding", self.get_color("text"))

        for y_offset, description in enumerate(self.help_items):
            self.draw_text(3 + y_offset, description_x, description, self.get_color("text"))

        for y_offset, binding in enumerate(self.application.config.items()):
            self.draw_text(3 + y_offset, binding_x, binding[1], self.get_color("text"))

        self.draw_text(5 + y_offset, description_x, "Press ? to close the menu", self.get_color("text"))