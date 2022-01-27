import subprocess

subprocess.call(r"python -m PyInstaller -F --noconsole --hidden-import babel.numbers --add-data C:\\Users\\k90009968\AppData\\Local\\Programs\\Python\\Python39\\tcl\\tix8.4.3;tcl\\tix8.4.3 main.py")