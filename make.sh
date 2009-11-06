#!/bin/bash

PYTHON="python2.5"
DEFAULT="NoTagApp.py"

case $1 in
  "build")
    #TODO: build for mac/win/linux
    python setup.py py2app;;
  "run")
    case $2 in
      "app")
        $PYTHON NoTagApp.py;;
      "main")
        $PYTHON MainFrame.py;;
      "pref")
        $PYTHON Preferences.py;;
      *)
        $PYTHON $DEFAULT;;
    esac;;
  "clean")
    #TODO: build for mac/win/linux
    rm -r build/ dist/;; 
  *)
    echo "usage: ./launch.sh build|run [app|main|pref]";;
esac
