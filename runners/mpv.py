import subprocess
class mpv:
    title = "Opens the video with mpv, no args."
    requires = ["mpv"]
    def run(self, url: str):
        subprocess.run(["mpv", url])