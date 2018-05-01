from cx_Freeze import setup, Executable

base = None

executables = [Executable("MasterLauncher.py", base=base)]

packages = ["idna", "os", "PyQt5", "win32gui", "time", "atexit", "webbrowser",
            "atexit", "pycurl", "sys", "win32process", "urllib"]

incl_files = ["happy.png", "whale.jpg"]

options = {
    'build_exe': {
        'packages': packages,
        'include_files': incl_files
    },
}

setup(
    name="Focus Task",
    options=options,
    version="0.1",
    description='A productivity application that works by limiting multitasking to reduce switching costs',
    executables=executables
)
