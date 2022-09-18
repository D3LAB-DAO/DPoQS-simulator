import matplotlib.pyplot as plt
import numpy as np
import csv


def multi_logs(name: str, x, ys, legends=None, transposed=True):
    with open("logs/" + name + ".csv", "w", newline='') as f:
        wr = csv.writer(f)

        if transposed:
            yts = np.array(ys).T
        else:
            yts = np.array(ys)

        if legends is not None:
            wr.writerow(["block"] + legends)

        for i, yt, in enumerate(yts):
            wr.writerow(np.append(x[i], yt))


if __name__ == "__main__":
    multi_logs(
        "sample",
        [1, 2, 3, 4, 5, 6, 7, 8],
        [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 3, 4, 5, 6, 5, 4],
            [9, 8, 7, 6, 5, 4, 3, 2]
        ],
        legends=["first", "second", "third"]
    )
