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

        self.parent.parent.draw_text(self.translate_y(self.title_pos_y + 1),
                                     self.translate_x(self.title_pos_x),
                                     self.author, self.get_color("text"))


class Videos(Tab):
    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.videos_x = self.videos_y = 1
        self.cell_width = self.cell_height = 3

        self.title = "Home Page"

        self.has_border = True
        self.show_title = True

    def update(self):
        # Create/update the videos list
        self.videos_list = []
        for video in self.parent.yt_videos:
            cell = Cell(self, video.title, video.creator, video.url)
            self.videos_list.append(cell)

        # translate the cells
        self.cell_width = self.width - 2

        # Calculate the max lines and the bottom line
        self.max_lines = int((self.height // self.cell_height) - 1)
        self.bottom_line = len(self.videos_list)

        selected_cells = self.videos_list[self.top_line:self.top_line + self.max_lines]
        for y, cell in enumerate(selected_cells):
            cell.translate(
                self.translate_y(((self.cell_height + 1) * y) + 1),
                self.translate_x(1)
            )
            # Apply the height and width to the current cell
            cell.height = self.cell_height
            cell.width = self.cell_width

            # Call the update function of the cell
            cell.update()

        self.scrollable_items = self.videos_list

    def late_update(self):
        if not self.videos_list:
            self.draw_text(int(self.height//2), int(self.width//2), "Loading...", self.get_color("text"))
            return

        # Call the late update function of the cells
        selected_cells = self.videos_list[self.top_line:self.top_line + self.max_lines]
        for y, cell in enumerate(selected_cells):
            if y == self.current_line:
                cell.selected = True

            self.parent._draw_border([0, cell])
            cell.late_update()

    def check_keys(self, key_pressed):
        # When the user has pressed the return key,
        # populate the video options tab with options for the selected video
        if key_pressed == self.parent.get_binding("select_video"):
            self.parent.voptions_tab.select_video(
                self.videos_list[self.top_line:self.top_line + self.max_lines][self.current_line])
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