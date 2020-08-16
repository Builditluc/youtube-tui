import curses
from base import Tab
from backend import YtVideo


class Option:
    name = str
    command = str

    def __init__(self, _name, _command):
        self.name = _name
        self.command = _command


class VOptions(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.options: [Option, ] = [
            Option("Play", ""),
            Option("Download", "")
        ]
        self.options_x = self.options_y = 1

        self.selected_video: YtVideo = None

        self.title = "Video Options"

        self.has_border = True
        self.show_title = True
        self.is_selectable = False

    def late_update(self):
        # If a video was selected,
        # draw the options
        if self.selected_video is not None:
            # Draw the options
            for y_offset, option in enumerate(self.options):
                self.draw_text(self.options_y + y_offset, self.options_x, option.name, self.get_color("text"))

    def select_video(self, video: YtVideo):
        self.selected_video = video
