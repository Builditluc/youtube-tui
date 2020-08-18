import curses
import curses.ascii
from base import Tab


class Cell(Tab):
    def __init__(self, parent, title: str, author: str, url: str):
        super(__class__, self).__init__(parent)

        self.title = title
        self.author = author
        self.url = url

        self.selected = False

        self.title_pos_y = 1
        self.title_pos_x = 2

        self.has_border = True
        self.show_cursor = False

    def update(self):
        # If the title is longer than the width of the cell,
        # show only a part of the title
        if len(self.title) >= self.width:
            self.title = self.title[:self.width - 5] + "..."

    def late_update(self):
        draw_color = "text"
        # If the cell is selected,
        # change the color
        if self.selected:
            draw_color = "highlighted"

        # Draw the title
        self.parent.parent.draw_text(self.translate_y(self.title_pos_y),
                                     self.translate_x(self.title_pos_x),
                                     self.title, self.get_color(draw_color))


class Videos(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.columns = 3
        self.grid = []

        self.scroll_left = -1
        self.scroll_right = 1
        self.horizontal_position = 0

        self.videos_x = self.videos_y = 1
        self.cell_width = self.cell_height = 4

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
        for y, line in enumerate(selected_rows):
            for x, cell in enumerate(line):
                if y == self.current_line and x == self.horizontal_position:
                    cell.selected = True

                self.parent._draw_border([0, cell])
                cell.late_update()

    def check_keys(self, key_pressed):
        # When the user has pressed the return key,
        # populate the video options tab with options for the selected video
        if key_pressed == self.parent.get_binding("select_video"):
            self.parent.voptions_tab.select_video(self.grid[self.top_line:self.top_line+self.max_lines][self.current_line][self.horizontal_position])
            return

        # When the user has pressed the up key,
        # call the scroll function
        if key_pressed == self.parent.get_binding("scroll_up"):
            self.scroll(self.scroll_up)
            return

        # When the user has pressed the down key,
        # call the scroll function
        if key_pressed == self.parent.get_binding("scroll_down"):
            self.scroll(self.scroll_down)
            return

        # When the user has pressed the left key,
        # call the horizontal scroll function
        if key_pressed == self.parent.get_binding("scroll_left"):
            self.scroll_horizontally(self.scroll_left)
            return

        # When the user has pressed the right key,
        # call the horizontal scroll function
        if key_pressed == self.parent.get_binding("scroll_right"):
            self.scroll_horizontally(self.scroll_right)
            return

    def scroll_horizontally(self, direction):
        # next cursor position after scrolling
        next_position = self.horizontal_position + direction

        # Scroll left
        # current cursor position or left position is greater or equal than 0
        if (direction == self.scroll_left) and (self.horizontal_position >= 0) and (next_position >= 0):
            self.horizontal_position = next_position
            return

        # Scroll right
        # absolute position of next cursor is not the right edge
        if (direction == self.scroll_right) and (next_position < self.columns):
            self.horizontal_position = next_position
            return

        # Left overflow
        # next cursor position is smaller than 0 and the current line is not the top
        if (direction == self.scroll_left) and (next_position < 0):
            self.horizontal_position = self.columns - 1
            self.scroll(self.scroll_up)
            return

        # Right overflow
        # next cursor position is over the right edge
        if (direction == self.scroll_right) and (next_position == self.columns):
            self.horizontal_position = 0
            self.scroll(self.scroll_down)
            return