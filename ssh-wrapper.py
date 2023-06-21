#!/usr/bin/env python3

import os
import sys


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: {} [ssh|scp|sftp|sshfs] [args]".format(sys.argv[0]))
        sys.exit(1)

    prog = "ssh"
    args = []

    if sys.argv[1] in ("ssh", "scp", "sftp", "sshfs"):
        prog = sys.argv[1]
        args = sys.argv[2:]
    else:
        args = sys.argv[1:]

    # build envs
    envs = os.environ.copy()
    if not envs.get("SSH_ASKPASS"):
        envs["SSH_ASKPASS"] = "sshaskpass.py"
    if not envs.get("SSH_ASKPASS_REQUIRE"):
        envs["SSH_ASKPASS_REQUIRE"] = "force"
    if not envs.get("DISPLAY"):
        envs["DISPLAY"] = ":0"

    # run
    print(prog, *args)
    os.execvpe(prog, [prog, *args], envs)
