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


class Youtube_form(npyscreen.FormBaseNew):
    def create(self):
        super(__class__, self).create()
        self.cycle_widgets = True
        self.add_handlers({"^Q": lambda _input: exit(0)})

        search_bar: Search_widget = self.add(Search_widget, w_id="search_bar", name="Search", rely=1, max_height=3)
        search_bar.entry_widget.handlers.update({curses.ascii.NL: self.start_search})

        self.add(Video_list_widget, w_id="video_list", name="Home Page", rely=5, values=[
            YtVideo("Programming Tutorial", "TheCherno", "https://youtube.com/watch="),
            YtVideo("The new MacBook Pro is awesome", "MKBHD", "https://youtube.com/watch=")
        ])

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def select_video(self, video:str):
        pass

    def start_search(self, _input):
        search_widget: Search_widget = self.get_widget("search_bar")

        video_widget: Video_list_widget = self.get_widget("video_list")
        video_widget.name = "Showing Results for '{}'".format(search_widget.value)

        video_widget.display()


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", Youtube_form, name="Youtube-TUI")


if __name__ == '__main__':
    youtubeApp = Application().run()
    print("Finished running youtube-tui, yay.")
