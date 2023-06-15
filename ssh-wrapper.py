#!/usr/bin/env python3

import os
import sys
from pathlib import Path


if __name__ == "__main__":
    # build args
    prog = "ssh"
    args = []

    if len(sys.argv) > 1 and sys.argv[1] in ("ssh", "scp", "sftp"):
        prog = sys.argv[1]
        args = sys.argv[2:]
    else:
        args = sys.argv[1:]

    dest = {
        "ssh-xacc": "xacchead",
        "ssh-socks": "ssocks",
    }[Path(sys.argv[0]).stem]

    # build envs
    envs = os.environ.copy()
    envs["SSH_ASKPASS"] = "/home/shenjm/.local/bin/sshaskpass.py"
    envs["SSH_ASKPASS_REQUIRE"] = "force"
    if not envs.get("DISPLAY"):
        print("DISPLAY not set, set to :0", file=sys.stderr)
        envs["DISPLAY"] = ":0"

    # run
    print(prog, dest, *args)
    os.execvpe(prog, [prog, dest, *args], envs)
