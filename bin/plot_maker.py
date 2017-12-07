import matplotlib.pyplot as plt
import datetime
# import main


def makeplot(data: [[[int]]], event_rate: [int], labels: [str], date: str) -> None:
    fig = plt.figure(1, figsize=(10, 5))
    new_data = []
    # rearranging data so all data for one curve is in the same list
    for values in data:
        new_data.append(list(zip(*values)))
    new_data = list(zip(*new_data))

    ax0 = fig.add_subplot(121)
    ax1 = fig.add_subplot(122)
    for i, elem in enumerate(new_data[0]):
        ax0.plot(event_rate, [e/1000 for e in elem], label=labels[i])
    for elem in new_data[1]:
        ax1.plot(event_rate, elem)

    ax0.set_ylabel(u"Time in ms")
    ax0.set_xlabel("Event rate")
    ax1.set_ylabel("Memory in kB")
    ax1.set_xlabel("Event rate")
    ax0.set_ylim(0)
    ax1.set_ylim(0)
    ax0.legend()
    fig.savefig("results/" + date + "/fig.pdf")
    return





