import npyscreen

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
