import subprocess
class vlc:
    title = "Opens the video with vlc, no args."
    requires = ["vlc"]
    def run(self, url: str):
        subprocess.run(["vlc", url])