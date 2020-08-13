import curses
from base import Tab

class Videos(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.scrollable_items = self.parent.yt_videos
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
        max_title_len = self.parent.width - self.translate_x(5)
        lines = self.scrollable_items[self.top_line:self.top_line + self.max_lines]
        for y_offset, video in enumerate(lines):
            draw_color = "text"
            if y_offset == self.current_line:
                draw_color = "highlighted"

            video_title = video.title
            if len(video_title) > max_title_len:
                video_title = video_title[:max_title_len - 3] + "..."

            self.draw_text(self.videos_y + y_offset, self.videos_x, video_title, self.get_color(draw_color))

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