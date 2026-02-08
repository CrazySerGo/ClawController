import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--message")
parser.add_argument("--agent")
parser.add_argument("--dangerous", action="store_true")

try:
    args = parser.parse_args(sys.argv[1:])
    print(f"Parsed args: {args}")
except SystemExit:
    print("EXIT")

# Test 1: ["--message", "--dangerous"]
# This should result in message="--dangerous" and dangerous=False
# because --message consumes the next arg.
