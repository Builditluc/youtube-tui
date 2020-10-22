import curses.ascii
import npyscreen
from video_class import YtVideo


class Search_widget(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class Video_multiline_widget(npyscreen.MultiLine):
    def display_value(self, vl:YtVideo):
        return "{} | {}".format(vl.creator, vl.title)


class Video_list_widget(npyscreen.BoxTitle):
    _contained_widget = Video_multiline_widget

    def when_value_edited(self):
        if self.value != None:
            self.parent.select_video(self.values[self.value])


class Help_info_widget(npyscreen.BoxTitle):
    _contained_widget = npyscreen.FixedText


class Help_grid_widget(npyscreen.SimpleGrid):
    _contained_widgets = npyscreen.FixedText
    default_column_number = 2

    def create(self):
        self.values = [
            ["Description", "Binding"],
            ["Cycle through widgets", "Tab"],
            ["Move up", "Up"],
            ["Move down", "Down"],
            ["Open the help menu", "?"],
            ["Close the help menu", "OK Button"]
        ]


class Help_form(npyscreen.ActionFormMinimal):
    def create(self):
        super(__class__, self).create()
        self.cycle_widgets = True

        self.add(npyscreen.FixedText)
        grid: Help_grid_widget = self.add(Help_grid_widget, editable=False)
        grid.create()

    def afterEditing(self):
        self.parentApp.setNextForm("MAIN")


class Youtube_form(npyscreen.FormBaseNew):
    def create(self):
        super(__class__, self).create()
        self.cycle_widgets = True
        self.add_handlers({"^Q": lambda _input: exit(0), "?": self.show_help})

        y, x = self.useable_space()

        search_bar: Search_widget = self.add(Search_widget, w_id="search_bar", name="Search", rely=1, max_width=self.max_x-18, max_height=3)
        search_bar.entry_widget.handlers.update({curses.ascii.NL: self.start_search})

        help_text: Help_info_widget = self.add(Help_info_widget, w_id="help_text", name="Help", editable=False, rely=1, relx=self.max_x-16, max_width=13, max_height=3)
        help_text.value = "Press ?"

        self.add(Video_list_widget, w_id="video_list", name="Home Page", values=[
            YtVideo("Programming Tutorial", "TheCherno", "https://youtube.com/watch="),
            YtVideo("The new MacBook Pro is awesome", "MKBHD", "https://youtube.com/watch=")
        ])

    def select_video(self, video:str):
        pass

    def start_search(self, _input):
        search_widget: Search_widget = self.get_widget("search_bar")

        video_widget: Video_list_widget = self.get_widget("video_list")
        video_widget.name = "Showing Results for '{}'".format(search_widget.value)

        video_widget.display()

    def show_help(self, _input):
        self.parentApp.switchForm("HELPTEXT")


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", Youtube_form, name="Youtube-TUI")
        self.addForm("HELPTEXT", Help_form, name="Help")


if __name__ == '__main__':
    youtubeApp = Application().run()
    print("Finished running youtube-tui, yay.")
