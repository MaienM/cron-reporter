#!/bin/env python3

import argparse
import datetime
import subprocess
import sys

from timedeltatype import TimeDeltaType

# Create the argument parser
parser = argparse.ArgumentParser(description='Cron helper')
parser.add_argument(
    '-t',
    '--timeout',
    type=TimeDeltaType(),
    default=None,
    help='the timeout of the command',
)
parser.add_argument(
    'command',
    nargs='+',
    help='the command to run',
)

# Parse the arguments
args = parser.parse_args()
print(args)

# Run the command
proc = subprocess.Popen(
    args.command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

try:
    timeout = args.timeout and args.timeout.total_seconds() or None
    stdout, _ = proc.communicate(timeout=timeout)
except subprocess.TimeoutExpired:
    try:
        proc.kill()
    except OSError:
        # If the process exits between the timeout and the kill call, we'll get
        # this. We just ignore this and act as if the timeout was never hit.
        pass
    stdout, _ = proc.communicate()

# Print output, unless the process exited successfully
if proc.returncode != 0:
    print(stdout.decode('utf-8'), end='')
    sys.exit(proc.returncode)
