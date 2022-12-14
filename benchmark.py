import argparse
import json
import sys
import time
from random import choice

import numpy as np
from memory_profiler import profile

import bwt
import bwts
import isbwt
import sabwt


parser = argparse.ArgumentParser()

parser.add_argument(
    "-a",
    "--algorithm",
    nargs="+",
    default=["bwt", "bwts", "isbwt", "sabwt"],
    choices=["bwt", "bwts", "isbwt", "sabwt"],
    help="algorithm to benchmark",
)
parser.add_argument(
    "-s",
    "--sequences",
    nargs="+",
    type=int,
    default=[100, 1000, 10000],
    help="list of sequence lengths to benchmark",
)

parser.add_argument(
    "-n",
    "--nreps",
    type=int,
    default=100,
    help="number of repetitions for each sequence length",
)

parser.add_argument(
    "-r",
    "--runtime",
    action="store_true",
    help="calculate and save runtimes",
)

parser.add_argument(
    "-m",
    "--memory",
    action="store_true",
    help="calculate and save memory profile",
)


def generate_seq(n):
    """
    Generate a random DNA sequence of length n

    Parameters
    ----------
    n : int
        length of the sequence

    Returns
    -------
    str
        random DNA sequence
    """
    return "".join(choice("ACGT") for _ in range(n))


def benchmark_transform(n, rep, f, mprofile):
    """
    Benchmark the transform function of a BWT class

    Parameters
    ----------
    n : int
        length of the sequence
    rep : int
        number of repetitions
    f : function
        transform function of a BWT class
    mprofile : bool
        whether to calculate memory profile

    Returns
    -------
    list
        list of runtimes
    """
    print(f"Benchmarking {f.__name__} for {rep} sequences of length {n}")
    timepoints = []
    start_time = time.time()
    for _ in range(rep):
        b = f(generate_seq(n))
        if mprofile:
            profile(b.transform())
        else:
            b.transform()
        timepoints.append(time.time() - start_time)
        start_time = time.time()
    # convert times to ms
    timepoints = list(map(lambda x: x * 1000, timepoints))
    return timepoints


if __name__ == "__main__":
    args = sys.argv[1:]
    args = parser.parse_args(args)

    runtimes = {}
    functions = {
        "bwt": bwt.bwt,
        "bwts": bwts.bwts,
        "sabwt": sabwt.sabwt,
        "isbwt": isbwt.isbwt,
    }

    for length in args.sequences:
        runtimes[length] = {}
        for algo in args.algorithm:
            runtimes[length][algo] = {}
            runtimes[length][algo]["timepoints"] = benchmark_transform(
                length, args.nreps, functions[algo], args.memory
            )
            runtimes[length][algo]["median"] = np.median(
                runtimes[length][algo]["timepoints"]
            )
            runtimes[length][algo]["mean"] = np.mean(
                runtimes[length][algo]["timepoints"]
            )
            runtimes[length][algo]["std"] = np.std(
                runtimes[length][algo]["timepoints"]
            )

    if args.runtime:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(f"results/runtimes_{timestr}.json", "w") as fp:
            json.dump(runtimes, fp)
