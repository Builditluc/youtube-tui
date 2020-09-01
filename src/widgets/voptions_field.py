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
        self.scrollable_items = self.options

        self.title = "Video Options"

        self.has_border = True
        self.show_title = True
        self.is_selectable = False

    def check_keys(self, key_pressed):
        if self.selected_video is None:
            return

        # If the user pressed down the up key,
        # scroll up
        if key_pressed == self.parent.get_binding("scroll_up"):
            self.scroll(self.scroll_up)

        # If the user pressed down the down key,
        # scroll down
        if key_pressed == self.parent.get_binding("scroll_down"):
            self.scroll(self.scroll_down)

    def update(self):
        self.max_lines = self.height - 1
        self.bottom_line = len(self.options)

        # If a video was selected,
        # make this tab selectable
        if self.selected_video is not None:
            self.is_selectable = True

        # If no video was selected and the tab is selectable,
        # make it non selectable
        if self.selected_video is None and self.is_selectable is True:
            self.is_selectable = False

    def late_update(self):
        # If a video was selected,
        # draw the options
        if self.selected_video is not None:
            # Draw the options
            for y_offset, option in enumerate(self.options[self.top_line:self.top_line+self.max_lines]):
                draw_color = "text"
                if y_offset == self.current_line:
                    draw_color = "highlighted"

                self.draw_text(self.options_y + y_offset, self.options_x, option.name, self.get_color(draw_color))

    def select_video(self, video: YtVideo):
        self.selected_video = video

    def deselect_video(self):
        self.selected_video = None