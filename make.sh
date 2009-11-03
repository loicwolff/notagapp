#!/bin/bash

PYTHON="python2.5"
DEFAULT="NoTagApp.py"

case $1 in
  "build")
    #TODO: build for mac/win/linux
    $PYTHON setup_mac.py py2app -s --dist-dir='../dist' --bdist-base='../build/';;
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
    rm -r ../build/;
    rm -r ../dist/;;
  *)
    echo "usage: ./launch.sh build|run [app|main|pref]";;
esac
