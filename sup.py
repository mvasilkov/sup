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


def sup_one(commands, cmd):
    if cmd in commands:
        proc = list_processes()
        started = commands[cmd]["process"] in proc
        print(started_color("(started)") if started
              else stopped_color("(stopped)"), cmd)
    else:
        print("Bad command")


def sup_mod(commands, cmd, action):
    if cmd not in commands:
        print("Bad command")
        return
    if action not in ("start", "stop"):
        print("Bad action")
        return
    proc = list_processes()
    started = commands[cmd]["process"] in proc
    if (action == "start" and started) or (action == "stop" and not started):
        print(started_color("(started)") if started
              else stopped_color("(stopped)"), cmd)
        return
    subprocess.call(commands[cmd][action], shell=True,
                    stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    sup_one(commands, cmd)


def sup_mod_all(commands, action):
    proc = list_processes()
    for cmd, params in commands.iteritems():
        started = params["process"] in proc
        if ((action == "start" and started) or
            (action == "stop" and not started)):
            print(started_color("(started)") if started
                  else stopped_color("(stopped)"), cmd)
            continue
        subprocess.call(commands[cmd][action], shell=True,
                        stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        sup_one(commands, cmd)


def main():
    commands = {}
    for f in list_files():
        obj = json.loads(open(SUP_FMT % f).read())
        commands.update(obj)
    if len(sys.argv) == 2:
        sup_one(commands, sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[1] in ("start", "stop") and sys.argv[2] == "all":
            sup_mod_all(commands, sys.argv[1])
        else:
            sup_mod(commands, sys.argv[1], sys.argv[2])
    else:
        sup_all(commands)

if __name__ == "__main__":
    if os.path.isdir(SUP):
        main()
    else:
        print("There is no ~/.sup")
