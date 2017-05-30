#!/bin/env python3

import argparse
import datetime
import os.path
import subprocess
import sys
import tempfile

import fasteners

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
    '-l',
    '--lock',
    action='store_true',
    default=False,
    help='only allow one instance of this command to run at the same time',
)
parser.add_argument(
    '--lockfile',
    type=str,
    help='the lockfile path to use (default: based on command)'
)
parser.add_argument(
    'command',
    nargs='+',
    help='the command to run',
)

# Parse the arguments
args = parser.parse_args()

# Lockfile
if args.lock:
    if not args.lockfile:
        args.lockfile = os.path.join(
            tempfile.gettempdir(),
            '{}.lock'.format(args.command[0].split()[0])
        )
    lock = fasteners.InterProcessLock(args.lockfile)
    if not lock.acquire(blocking=False):
        print('could not acquire lock ({}), aborting'.format(args.lockfile))
        sys.exit(1)
elif args.lockfile:
    parser.error('--lockfile requires --lock')

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
