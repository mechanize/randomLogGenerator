
import subprocess
import bin.randomLogGenerator as randomLogGenerator
import bin.plot_maker as plot_maker
import datetime
from os import listdir, makedirs
from os.path import isfile, join
from shutil import copyfile
from numpy import arange

MONPOLY = "~/Documents/Bachelorthesis/2017-jager-survey/monpoly/monpoly"
TIME = "/usr/bin/time -v"
SIGNATURE = "stockscan.sign"
CONFIG = "config.txt"
formulas = [join("formulas", f) for f in listdir("formulas") if
            isfile(join("formulas", f)) and
            f.split(".")[-1] == "formula"]


def run(formula: str, signature: str, log: str) -> (int, int):
    console_in = 'ts=$(date +%s%N); ' + TIME + ' ' + MONPOLY + ' -sig ' + signature + ' -log ' + log + \
                 ' -formula ' + formula + ' -negate; tt=$((($(date +%s%N) - $ts)/1000)); echo "Time_elapsed: $tt"'

    console_out = subprocess.Popen(console_in, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    res = console_out.communicate()
    time, mem = 0, 0
    for line in res[0].decode("utf-8").split("\n"):
        args = line.split(": ")
        if args[0].strip() == "Time_elapsed":
            time = int(args[1])  # microseconds
    for line in res[1].decode("utf-8").split("\n"):  # time command outputs in stderr
        args = line.split(": ")
        if args[0].strip() == "Maximum resident set size (kbytes)":
            mem = int(args[1])  # kB
    if time == 0 or mem == 0:
        print(log, mem, time)
        raise RuntimeError("Parse failure:", log)
    return time, mem


def read_config(file_loc: str) -> dict:
    config_dict = {"NUM_LOGS": 1,
                   "RUNS_PER_LOG": 1,
                   "MAX_TIMESTAMP": 1,
                   "EVENT_RATE:": 0,  # not in config, for internal use
                   "STARTING_EVENT_RATE": 1,
                   "INCREASING_EVENT_RATE": 0,
                   "INJ_WORKING_HOURS": 0,
                   "CREATE_LOGS": 1,  # bool
                   "OUTSIDE_WORKING_HOURS_VIOLATION": 0,  # bool
                   "NEGATIVE_AMOUNT_VIOLATION": 0}  # bool
    fo = open(file_loc, 'r')
    for line in fo.readlines():
        data = line.strip().split("=")
        if data[0].strip() in config_dict:
            config_dict[data[0].strip()] = int(data[1].split("#")[0].strip())
        elif data[0] == "":
            pass
        else:
            print('No setting named \"' + data[0].strip() + '\"')
    fo.close()
    return config_dict


def write_config(config: dict, file_loc: str) -> None:
    fo = open(file_loc, "w")
    for key in config.keys():
        fo.write(key + " = " + str(config[key]))
    return


def main():
    config = read_config(CONFIG)
    if config["CREATE_LOGS"]:
        randomLogGenerator.create_logs(config)
    else:  # counting number for logs if no new logs are created
        config["NUM_LOGS"] = len([None for f in listdir("logs") if
                                  isfile(join("logs", f)) and
                                  f.split(".")[-1] == "log"])

    data = []
    for f in formulas:
        plot_data = []
        for k in range(config["NUM_LOGS"]):
            for i in range(config["RUNS_PER_LOG"]):
                t, m = [], []
                t_val, m_val = run(formula=f, signature=SIGNATURE, log="logs/" + str(k) + ".log")
                t.append(t_val)
                m.append(m_val)
            plot_data.append([sum(t)/len(t), sum(m)/len(m)])
        data.append(plot_data)

    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    makedirs("results/" + date)
    makedirs("results/" + date + "/formulas")
    copyfile(CONFIG, "results/" + date + "/" + CONFIG)
    for f in formulas:
        copyfile(f, join("results/" + date, f))
    eRate = arange(config["STARTING_EVENT_RATE"],
                   config["STARTING_EVENT_RATE"] + config["NUM_LOGS"] * config["INCREASING_EVENT_RATE"],
                   config["INCREASING_EVENT_RATE"])

    labels = [f.split("/")[-1].split(".")[0] for f in formulas]
    plot_maker.makeplot(data, eRate, labels, date)

main()









