import subprocess
class mpv:
    description = "Open the video with mpv, no args."
    requires = ["mpv"]
    def run(self, url):
        subprocess.run(["mpv", url])