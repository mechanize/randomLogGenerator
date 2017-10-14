
import subprocess
import randomLogGenerator

MONPOLY = "~/Documents/Bachelorthesis/2017-jager-survey/monpoly/monpoly"
TIME = "/usr/bin/time -v"
DATE_1 = "ts=$(date +%s%N)"
DATE_2 = "tt=$(($(date +%s%N) - $ts)/1000000)"
PRINT = "echo \"Time_elapsed: $tt\""

formulas = ["CustWithInjEvents.formula", "CustWithoutInjEvents.formula"]
SIGNATURE = "stockscan.sign"
NUM_LOGS = 100
data = []


def run(formula, signature, log):
    console_in = [DATE_1, ";", TIME, MONPOLY, "-sig", signature, "-formula", formula, "-log", log, "-negate", ";", DATE_2, ";", PRINT]
    console_out = subprocess.Popen(console_in, False)
    lines = console_out.stdout.split("\n")
    time, mem = 0, 0
    for line in lines:
        args = line.split(": ").strip()
        if args[0] == "Time_elapsed":
            time = int(args[1])  # nanoseconds
        if args[0] == "Maximum resident set size (kbytes)":
            mem = int(args[1])  # kB
    if time == 0 or mem == 0:
        raise RuntimeError("Couldn't parse arguments")
    return time, mem

randomLogGenerator.create_logs()

for f in formulas:
    plot_data = []
    for k in range(NUM_LOGS):
        t, m = run(formula=f, signature=SIGNATURE, log="logs/" + str(k) + ".log")
        plot_data.append([k, t, m])
    data.append(plot_data)









