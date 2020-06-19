#!/usr/bin/env python3
import argparse
import re
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description='Calculate space savings of fdupes')
    parser.add_argument('infile', metavar='file', type=str,nargs=1, help='the input file for reading')
    return parser.parse_args()

if __name__=='__main__':
    args = parse_args()
    with open(args.infile[0], 'r') as f:
        lines = f.readlines()
    digitsmatch = re.compile(r'(^[0-9]+) bytes each:')

    reducible = 0
    numbytes = 0
    for ll in lines:
        digits = digitsmatch.match(ll)  # regex match for integer starting a line
        if digits:
            reducible -= 2*numbytes  # account for blank line separating duplicates
            numbytes = np.uint64(digits.group(1))  # number of bytes each instance of a duplicate file is
        else:
            reducible += numbytes  # accumulate
    print("fdupes can save %d bytes, or %.2fG." % (reducible, reducible / 1024 / 1024 / 1024))
