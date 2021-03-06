#!/usr/bin/env python3
"""Emulates wc -l using concurrent processes/threads."""

import sys
import os
from concurrent import futures


def count_lines(filename):
    """Open file, count newlines, then return (filename, line_count) tuple."""
    with open(filename, 'rb') as file_to_read:
        chunk_size = 8192
        line_count = 0
        while True:
            chunk = file_to_read.read(chunk_size)
            if chunk:
                line_count += chunk.count(b'\n')
            else:
                break
        return filename, line_count


def print_count(count, label):
    """Print a line count right-justified along with a label."""
    formatted_count = str(count).rjust(10)
    print("{} {}".format(formatted_count, label))


def main():
    """Takes directory as argument, returns number of newlines in all files in
    the that directory (non-recursively).
    """
    if len(sys.argv) < 2:
        dirname = '.'
        paths = [f for f in os.listdir(dirname)]
    else:
        dirname = os.path.abspath(sys.argv[1])
        paths = [os.path.join(dirname, f) for f in os.listdir(dirname)]
    filenames = [p for p in paths if os.path.isfile(p)]
    counts = {}
    # with futures.ThreadPoolExecutor(max_workers=len(filenames)) as executor:
    with futures.ProcessPoolExecutor(max_workers=len(filenames)) as executor:
        all_futures = [executor.submit(count_lines, f) for f in filenames]
        for future in futures.as_completed(all_futures):
            filename, count = future.result()
            counts[filename] = count
    ranked = sorted(counts, key=lambda k: -counts[k])
    for filename in ranked:
        print_count(counts[filename], filename)
    print_count(sum(counts.values()), "[TOTAL]")


if __name__ == "__main__":
    main()
