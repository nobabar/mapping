import json
import time
from random import choice

import matplotlib.pyplot as plt
import numpy as np

import bwt
import bwts
import isbwt
import sabwt


def generate_seq(length):
    return "".join(choice("ACGT") for _ in range(length))


def benchmark_transform(n, rep, f):
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


seq_lengths = [100, 1000, 10000, 100000]
reps = 1000


runtimes = {}
methods = {
    "bwt": bwt.bwt,
    "bwts": bwts.bwts,
    "sabwt": sabwt.sabwt,
    "isbwt": isbwt.isbwt,
}

for length in seq_lengths:
    runtimes[length] = {}
    for method in methods:
        runtimes[length][method] = {}
        runtimes[length][method]["timepoints"] = benchmark_transform(
            length, reps, methods[method]
        )
        runtimes[length][method]["median"] = np.median(
            runtimes[length][method]["timepoints"]
        )
        runtimes[length][method]["mean"] = np.mean(
            runtimes[length][method]["timepoints"]
        )
        runtimes[length][method]["std"] = np.std(runtimes[length][method]["timepoints"])

    myrange = (0, max(runtimes[length]["bwt"]["timepoints"]) * 1.1)

    plt.figure()

    for method in methods:
        plt.hist(
            runtimes[length][method]["timepoints"],
            bins=100,
            alpha=0.5,
            edgecolor="black",
            linewidth=1.2,
            label=method,
            range=myrange,
        )

    plt.legend(loc="upper right")
    plt.savefig(f"benchmark_{length}.svg", format="svg")

with open("runtimes.json", "w") as fp:
    json.dump(runtimes, fp)
