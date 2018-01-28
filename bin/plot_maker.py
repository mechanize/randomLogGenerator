import matplotlib.pyplot as plt


def makeplot(data: dict, event_rate: [int], date: str) -> None:
    fig = plt.figure(1, figsize=(10, 7))
    ax0 = fig.add_subplot(221)
    ax1 = fig.add_subplot(222)
    ax2 = fig.add_subplot(223)
    ax3 = fig.add_subplot(224)
    for dic in data.get('Workinghours'):
        ax0.plot(event_rate, dic.get('time'), label=dic.get('label'))
        ax1.plot(event_rate, dic.get('mem'))
    for dic in data.get('Cust'):
        ax2.plot(event_rate, dic.get('time'), label=dic.get('label'))
        ax3.plot(event_rate, dic.get('mem'))

    ax0.set_ylabel(u"Time in ms")
    ax0.set_xlabel("Event rate")
    ax1.set_ylabel("Memory in kB")
    ax1.set_xlabel("Event rate")
    ax2.set_ylabel(u"Time in ms")
    ax2.set_xlabel("Event rate")
    ax3.set_ylabel("Memory in kB")
    ax3.set_xlabel("Event rate")

    ax0.set_ylim(0)
    ax2.set_ylim(0)

    ax0.legend()
    ax2.legend()
    fig.savefig("results/" + date + "/fig.pdf")
    return





