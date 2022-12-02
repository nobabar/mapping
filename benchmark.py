import argparse
import json
import sys
import time
from random import choice


import matplotlib.pyplot as plt
import numpy as np

import bwt
import bwts
import isbwt
import sabwt


parser = argparse.ArgumentParser()

parser.add_argument(
    "-m",
    "--methods",
    nargs="+",
    default=["bwt", "bwts", "isbwt", "sabwt"],
    help="methods to benchmark",
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
    "-r",
    "--reps",
    type=int,
    default=100,
    help="number of repetitions for each sequence length",
)


def generate_seq(length):
    return "".join(choice("ACGT") for _ in range(length))


def benchmark_transform(n, rep, f):
    print(f"Benchmarking {f.__name__} for {rep} sequences of length {n}")
    start_time = time.time()
    timepoints = []
    for _ in range(rep):
        b = f(generate_seq(n))
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
        for method in args.methods:
            runtimes[length][method] = {}
            runtimes[length][method]["timepoints"] = benchmark_transform(
                length, args.reps, functions[method]
            )
            runtimes[length][method]["median"] = np.median(
                runtimes[length][method]["timepoints"]
            )
            runtimes[length][method]["mean"] = np.mean(
                runtimes[length][method]["timepoints"]
            )
            runtimes[length][method]["std"] = np.std(
                runtimes[length][method]["timepoints"]
            )

        # myrange = (0, max(runtimes[length]["bwt"]["timepoints"]) * 1.1)

        # plt.figure()

        # for method in methods:
        #     plt.hist(
        #         runtimes[length][method]["timepoints"],
        #         bins=100,
        #         alpha=0.5,
        #         edgecolor="black",
        #         linewidth=1.2,
        #         label=method,
        #         range=myrange,
        #     )

        # plt.legend(loc="upper right")reps
        # plt.savefig(f"benchmark_{length}.svg", format="svg")

    with open("runtimes.json", "w") as fp:
        json.dump(runtimes, fp)
