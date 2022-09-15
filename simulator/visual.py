import matplotlib.pyplot as plt


def multi_draw(
    name: str,
    x,
    ys,
    xlabel=None, ylabel=None,
    legends=None,
    dpi=300, show: bool = False, save: bool = True
):
    # plot
    fig, ax = plt.subplots()

    # xlabel
    if xlabel is not None:
        ax.set_xlabel(xlabel)

    # ylabel
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # legend
    if legends is not None:
        for i, y in enumerate(ys):
            ax.plot(x, y, linewidth=2.0, label=legends[i])

        fig.legend(loc='upper center', ncol=len(legends))
    else:
        for i, y in enumerate(ys):
            ax.plot(x, y, linewidth=2.0)

    # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
    #        ylim=(0, 8), yticks=np.arange(1, 8))

    # draw
    if show:
        plt.show()
    if save:
        plt.savefig("plots/" + name, dpi=dpi)


def multi_draw_axis_2(
    name: str,
    x,
    y1s, y2,
    xlabel=None, ylabels=None,
    legends=None,
    dpi=300, show: bool = False, save: bool = True
):
    # plot
    fig, ax = plt.subplots()
    # fig.subplots_adjust(right=0.75)
    twin1 = ax.twinx()

    # xlabel
    if xlabel is not None:
        ax.set_xlabel(xlabel)

    # ylabel
    if ylabels is not None:
        ax.set_ylabel(ylabels[0])
        twin1.set_ylabel(ylabels[1])

    # legend
    if legends is not None:
        ps = list()
        for i, y1 in enumerate(y1s):
            p1, = ax.plot(x, y1, label=legends[i])
            ps.append(p1)
        p2, = twin1.plot(x, y2, "r-.", label=legends[-1])

        fig.legend(
            handles=ps + [p2],
            loc='upper center', ncol=len(legends)
        )
    else:
        for i, y1 in enumerate(y1s):
            ax.plot(x, y1)
        p2, = twin1.plot(x, y2, "r-.")

    twin1.yaxis.label.set_color(p2.get_color())

    tkw = dict(size=4, width=1.5)
    twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)

    # draw
    if show:
        plt.show()
    if save:
        plt.savefig("plots/" + name, dpi=dpi)



def multi_draw_axis_3(
    name: str,
    x,
    y1s, y2, y3,
    xlabel=None, ylabels=None,
    legends=None,
    dpi=300, show: bool = False, save: bool = True
):
    # plot
    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)
    twin1 = ax.twinx()
    twin2 = ax.twinx()
    twin2.spines.right.set_position(("axes", 1.2))

    # xlabel
    if xlabel is not None:
        ax.set_xlabel(xlabel)

    # ylabel
    if ylabels is not None:
        ax.set_ylabel(ylabels[0])
        twin1.set_ylabel(ylabels[1])
        twin2.set_ylabel(ylabels[2])

    # legend
    if legends is not None:
        ps = list()
        for i, y1 in enumerate(y1s):
            p1, = ax.plot(x, y1, label=legends[i])
            ps.append(p1)
        p2, = twin1.plot(x, y2, "r-.", label=legends[-2])
        p3, = twin2.plot(x, y3, "g--", label=legends[-1])

        fig.legend(
            handles=ps + [p2, p3],
            loc='upper center', ncol=len(legends)
        )
    else:
        for i, y1 in enumerate(y1s):
            ax.plot(x, y1)
        p2, = twin1.plot(x, y2, "r-.")
        p3, = twin2.plot(x, y3, "g--")

    twin1.yaxis.label.set_color(p2.get_color())
    twin2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=1.5)
    twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)

    # draw
    if show:
        plt.show()
    if save:
        plt.savefig("plots/" + name, dpi=dpi)


if __name__ == "__main__":
    multi_draw(
        "sample",
        [1, 2, 3, 4, 5, 6, 7, 8],
        [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 3, 4, 5, 6, 5, 4],
            [9, 8, 7, 6, 5, 4, 3, 2]
        ],
        xlabel="blockNumber",
        ylabel="numbers",
        legends=["first", "second", "third"],
        save=True
    )

    multi_draw_axis_2(
        "sample_2",
        [1, 2, 3, 4, 5, 6, 7, 8],
        [[1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2]],
        [1, 2, 3, 4, 5, 6, 5, 4],
        xlabel="blockNumber",
        ylabels=["a", "b"],
        legends=["first", "second", "third"],
        save=True
    )

    multi_draw_axis_3(
        "sample_3",
        [1, 2, 3, 4, 5, 6, 7, 8],
        [[1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 3, 4, 5, 6, 1]],
        [1, 2, 3, 4, 5, 6, 5, 4],
        [9, 8, 7, 6, 5, 4, 3, 2],
        xlabel="blockNumber",
        ylabels=["a", "b", "c"],
        legends=["first", "second", "third", "fourth"],
        save=True
    )
