import npyscreen

class Video_multiline_widget(npyscreen.MultiLine):
    def display_value(self, vl):
        return "{} | {}".format(vl.creator, vl.title)


class Video_list_widget(npyscreen.BoxTitle):
    _contained_widget = Video_multiline_widget

    def when_value_edited(self):
        if self.value != None:
            self.parent.select_video(self.values[self.value])