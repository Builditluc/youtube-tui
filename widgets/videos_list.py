import curses
from base import Tab


class Cell(Tab):
    def __init__(self, parent, title: str, author: str, url: str):
        super(__class__, self).__init__(parent)

        self.title = title
        self.author = author
        self.url = url

        self.title_pos_y = 1
        self.title_pos_x = 2

        self.has_border = True
        self.show_cursor = False

    def update(self):
        # If the title is longer than the width of the cell,
        # show only a part of the title
        if len(self.title) >= self.width:
            self.title = self.title[:self.width - 4] + "..."

    def late_update(self):
        # Draw the title
        self.parent.parent.draw_text(self.translate_y(self.title_pos_y),
                                     self.translate_x(self.title_pos_x),
                                     self.title, self.get_color("text"))


class Videos(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.columns = 3
        self.grid = []

        self.videos_x = self.videos_y = 1
        self.cell_width = self.cell_height = 4

        self.current_line = 2
        self.title = "Home Page"

        self.has_border = True
        self.show_title = True

    def update(self):
        # Create/update the grid
        self.grid = []
        line = []
        for x, video in enumerate(self.parent.yt_videos):
            cell = Cell(self, video.title, video.creator, video.url)
            line.append(cell)

            if len(line) == 3:
                self.grid.append(line)
                line = []

        if line:
            self.grid.append(line)

        # translate the cells
        self.cell_width = int((self.width // self.columns) - 1)

        # Calculate the max lines and the bottom line
        self.max_lines = int((self.height // self.cell_height) - 1)
        self.bottom_line = len(self.grid)

        selected_rows = self.grid[self.top_line:self.top_line+self.max_lines]
        for y, line in enumerate(selected_rows):
            for x, cell in enumerate(line):
                cell.translate(
                    self.translate_y(((self.cell_height+ 1) * y) + 1),
                    self.translate_x(((self.cell_width + 1) * x) + 1)
                )
                # Apply the height and width to all cells
                cell.height = self.cell_height
                cell.width = self.cell_width

                # Call the update function
                cell.update()

        self.scrollable_items = self.grid


    def late_update(self):
        # Call the late update function of the cells
        selected_rows = self.grid[self.top_line:self.top_line+self.max_lines]
        for line in selected_rows:
            for cell in line:
                self.parent._draw_border([0, cell])
                cell.late_update()

        """# Draw the videos
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
        """

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
