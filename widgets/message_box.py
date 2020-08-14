from base import Tab


class Message_Box(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)
        self.show_cursor = False

        self.show = False
        self.message_title = ""
        self.message = ""

        self.message_x = self.message_y = 1

    def update(self):
        if self.show:
            self.has_border = True
            self.show_title = True

            self.title = self.message_title
        else:
            self.has_border = False
            self.show_title = False

            self.title = ""

    def late_update(self):
        if self.show:
            # Draw the message
            self.draw_text(self.message_y, self.message_x, self.message, self.get_color("text"))