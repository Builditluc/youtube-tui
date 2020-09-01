from .runner_class import runner_class
class vlc(runner_class):
    title = "Opens the video with vlc, no args."
    requires = ["vlc"]
    def run(self, url: str):
         self.subprocess_run(["vlc", url], self.requires)