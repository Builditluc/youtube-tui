import sys
import glob
import os


class methods:
    def __init__(self, description, name):
        self.description = description
        self.name = name

def watch_video(url, method):
    pass

def get_methods():
    os.chdir("runners")
    
    fileset = [file for file in glob.glob("*.py", recursive=False)]
    
    file_names = []

    for i in fileset:
        file_names.append(i.split(".")[0])
        exec("import " + i)
    return file_names 
        
print(get_methods())
