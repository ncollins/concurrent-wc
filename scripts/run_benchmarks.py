#!/usr/bin/env python3

"""Run me from the root repo directory"""

import os
import re
import sys
from subprocess import check_output
from typing import Mapping

BENCHMARKS_DIR = "./benchmarks"
BIN_DIR = "./bin"


def run_benchmark_once(wc_bin: str, directory: str) -> int:
    """
    Runs a `wc_bin` program on a given `directory`, returning the running time
    in milliseconds.
    """
    result = check_output([os.path.join(BIN_DIR, wc_bin), directory])
    time_ms = result.decode().split('\n')[-2]
    parsed = -1
    try:
        parsed = re.match(r'^Took\s+(\d+)ms$', time_ms)[1]
    except TypeError:
        print("could not parse timing info for {}".format(wc_bin))
    return int(parsed)


def run_benchmark(wc_bin: str, directory: str) -> int:
    """
    Runs a `wc_bin` program repeatedly on a given `directory`, returning the
    median running time in milliseconds.
    """
    all_runs = sorted([run_benchmark_once(wc_bin, directory) for _ in range(5)])
    return all_runs[len(all_runs) // 2]


def run_benchmarks(directory: str) -> Mapping[str, int]:
    """
    Runs all the wc programs on the given benchmark (`directory`), returning a
    mapping of program names to their running time, in milliseconds.
    """
    return {
        wc: run_benchmark(wc, directory)
        for wc in os.listdir(BIN_DIR)
        if wc.startswith('wc')
    }


def main():
    print(run_benchmarks(sys.argv[1]))


if __name__ == "__main__":
    main()