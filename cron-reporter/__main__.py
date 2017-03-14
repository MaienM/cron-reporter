#!/bin/env python3

import argparse
import subprocess
import sys

# Create the argument parser
parser = argparse.ArgumentParser(description='Cron helper')
parser.add_argument('command', nargs='+', help='the command to run')

# Parse the arguments
args = parser.parse_args()

# Run the command
proc = subprocess.Popen(
    args.command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
proc.wait()
if proc.returncode != 0:
    print(proc.stdout.read().decode('utf-8'), end='')
    sys.exit(proc.returncode)
