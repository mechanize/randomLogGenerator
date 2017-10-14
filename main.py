
import subprocess
import randomLogGenerator

formulas = ["CustWithInjEvents.formula", "CustWithoutInjEvents.formula"]
NUM_LOGS = 100
data = []


def run(formula, signature, log):
    console_in = ["monpoly", "-sig", signature, "-formula", formula, "-log", log, "-negate"]
    console_out = subprocess.Popen(console_in, False)
    lines = console_out.stdout.split("\n")
    time, mem = 0, 0
    for line in lines:
        args = line.split(": ").strip()
        if args[0] == "time":
            time = float(args[1])
        if args[0] == "mem":
            mem = float(args[1])
    if time == 0 or mem == 0:
        raise RuntimeError("Couldn't parse arguments")
    return time, mem

randomLogGenerator.create_logs()

for f in formulas:
    plot_data = []
    for k in range(NUM_LOGS):
        t, m = run(formula=f, signature="stockscan.signature", log="logs/" + str(k) + ".log")
        plot_data.append([k, t, m])
    data.append(plot_data)









