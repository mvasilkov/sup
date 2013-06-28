#!/usr/bin/env python
"""Sup /b/
"""
from __future__ import print_function
import json
import os
import subprocess
import sys

try:
    from fabric.colors import blue as started_color, red as stopped_color
except ImportError:
    started_color = lambda a: a
    stopped_color = lambda a: a

SUP = os.path.expanduser("~/.sup")
SUP_FMT = SUP + "/%s"


def list_files():
    for not_used, not_used, files in os.walk(SUP):
        return tuple(filter(lambda f: f.endswith(".json"), files))
    return ()


def list_processes():
    return subprocess.check_output(("ps", "-A"))


def sup_all(commands):
    proc = list_processes()
    for cmd, params in commands.iteritems():
        started = params["process"] in proc
        print(started_color("(started)") if started
              else stopped_color("(stopped)"), cmd)


def main():
    commands = {}
    for f in list_files():
        obj = json.loads(open(SUP_FMT % f).read())
        commands.update(obj)
    if len(sys.argv) == 1:
        sup_all(commands)

if __name__ == "__main__":
    if os.path.isdir(SUP):
        main()
    else:
        print("There is no ~/.sup")
