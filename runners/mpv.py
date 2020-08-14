import subprocess
class mpv:
    title = "Opens the video with mpv, no args."
    requires = ["mpv"]
    def run(self, url: str):
        try:
            subprocess.run(["mpv", url])
        except FileNotFoundError:
            print("Did you install the dependencies: ")
            for i in self.requires:
                print(i)