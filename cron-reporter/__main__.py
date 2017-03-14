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
result = subprocess.run(
    args.command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
if result.returncode != 0:
    print(result.stdout.decode('utf-8'), end='')
    sys.exit(result.returncode)
