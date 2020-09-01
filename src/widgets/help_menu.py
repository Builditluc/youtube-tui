import curses
from base import Tab

class Help_menu(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.title = "Help"

        self.has_border = True
        self.is_selectable = False
        self.show_title = True

    def late_update(self):
        self.draw_text(1, 1, "Type ?", self.get_color("title"))