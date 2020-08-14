import subprocess
class runner_class:
    def subprocess_run(self, args: [str], requires: [str]):
        try:
            subprocess.run(args)
        except FileNotFoundError:
            print("Did you install the dependencies: ")
            for i in requires:
                print(i)