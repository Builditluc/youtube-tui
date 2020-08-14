from .runner_class import runner_class
class mpv(runner_class):
    title = "Opens the video with mpv, no args."
    requires = ["mpv"]
    def run(self, url: str):
        self.subprocess_run(["mpv", url], self.requires)