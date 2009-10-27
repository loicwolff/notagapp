from distutils.core import setup
import py2exe

setup(windows=[{"script":"NoTagApp.py",
                "icon_resources":[(1, "resource/NoTagApp.ico")]}])

