import curses.ascii
import npyscreen


class Search_widget(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class Video_list_widget(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLine


class Youtube_form(npyscreen.FormBaseNew):
    def create(self):
        super(__class__, self).create()
        self.cycle_widgets = True

        key_handlers = {
            "^Q" : self.exit_func
        }
        self.add_handlers(key_handlers)

        y, x = self.useable_space()

        search_bar: Search_widget = self.add(Search_widget, name="Search", rely=1, max_height=3)
        search_bar.entry_widget.handlers.update({curses.ascii.NL:self.start_search})

        video_list: Video_list_widget = self.add(Video_list_widget, name="Home Page", rely=5)
        video_list.values = ["Test1", "Test2", "Test3"]

    def while_editing(self, widget):
        pass

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def start_search(self, _input):
        pass

    def exit_func(self, _input):
        exit(0)

class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", Youtube_form, name="Youtube-TUI")


if __name__ == '__main__':
    youtubeApp = Application().run()
    print("Finished running youtube-tui, yay.")
