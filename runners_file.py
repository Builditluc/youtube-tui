import sys
import os
import subprocess

class methods:
    def __init__(self, title, name):
        self.title = title
        self.name = name


def _get_python_files_(dir: str):
    output = []
    fileset = os.listdir(dir)
    for file in fileset:
        path, extension = os.path.splitext(file)
        if extension == ".py" and not path.startswith("__"):
            output.append(path)
    return output


def get_methods():
    file_names = []
    for i in _get_python_files_("runners"):
        exec("import runners." + i)
        file_names.append(
            methods(eval("runners." + i + "." + i + ".title"), i))
    return file_names


def watch_video(url, method: methods):
    exec("import runners." + method.name)
    command = "runners." + method.name + \
        "." + method.name + "().run(" + url + ")"
    return eval(command)




#watch_video("'https://www.youtube.com/watch?v=dQw4w9WgXcQ'", methods("asdf", "mpv"))