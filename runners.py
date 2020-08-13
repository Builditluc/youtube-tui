import sys
import glob
import os

class methods:
    def __init__(self, title, name):
        self.title = title
        self.name = name

def get_python_files(dir: str):
    output = []
    fileset = os.listdir(dir)
    for file in fileset:
        path, extension = os.path.splitext(file)
        if extension == ".py" and not path.startswith("__"):
            output.append(path)
    return output

def get_methods():
    file_names = []
    for i in get_python_files("runners"):
        exec("import runners." + i)
        file_names.append(methods(eval("runners." + i + "." + i + ".title"), i))   
    return file_names

#print(get_methods())


def watch_video(url, method: methods):
    return eval("runners." + method.name + "." + method.name + ".run(" + url + ")")

watch_video("'https://www.youtube.com/watch?v=mf5SZ5Q7fMo'", methods("", "mpv"))