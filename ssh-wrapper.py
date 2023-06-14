#!/usr/bin/env python3

import os
import sys
from pathlib import Path


if __name__ == "__main__":
    # build args
    args = []
    if len(sys.argv) < 2:
        args.append("ssh")
    else:
        args.append(sys.argv[1])

    stem = Path(sys.argv[0]).stem
    args.append(
        {
            "ssh-xacc": "xacchead",
            "ssh-socks": "ssocks",
        }[stem]
    )

    if len(sys.argv) > 2:
        args.extend(sys.argv[2:])

    # build envs
    envs = os.environ.copy()
    envs["SSH_ASKPASS"] = "/home/shenjm/.local/bin/sshaskpass.py"
    envs["SSH_ASKPASS_REQUIRE"] = "force"
    if not envs.get("DISPLAY"):
        print("DISPLAY not set, set to :0", file=sys.stderr)
        envs["DISPLAY"] = ":0"

    # run
    os.execvpe(args[0], args, envs)
