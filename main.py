
import subprocess
from bin import randomLogGenerator
from bin import plot_maker
from bin import util
import datetime
from os import listdir, makedirs
from os.path import isfile, join
from shutil import copyfile, copytree
from numpy import arange

monpoly, monpoly_signature, stream, stream_config, time_loc, config_file = util.get_static_data()


def run(tool: str, **param) -> (int, int):

    # Building bash command
    console_in = ""
    if tool == "monpoly":
        console_in = 'ts=$(date +%s%N); ' + time_loc + ' ' + monpoly + ' -sig ' + monpoly_signature + ' -log ' + \
                     param.get('log')[0] + ' -formula ' + param.get('formula') + ' -negate; tt=$((($(date +%s%N) - $ts)' \
                                                                      '/1000000)); echo "Time_elapsed: $tt"'
    if tool == "stream":
        util.stream_set_src(param.get('formula'), param.get('log'))
        console_in = 'ts=$(date +%s%N); ' + time_loc + ' ' + stream + ' -c ' + stream_config + ' -l log ' + \
                     param.get('formula') + '; tt=$((($(date +%s%N) - $ts)/1000000)); echo "Time_elapsed: $tt"'

    # Running tool
    console_out = subprocess.Popen(console_in, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    res = console_out.communicate()
    streamlog = subprocess.Popen("cat log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(streamlog)

    # Parsing time, mem
    time, mem = -1, -1
    for line in res[0].decode("utf-8").split("\n"):
        args = line.split(": ")
        if args[0].strip() == "Time_elapsed":
            time = int(args[1])  # microseconds
    for line in res[1].decode("utf-8").split("\n"):  # time command outputs in stderr
        args = line.split(": ")
        if args[0].strip() == "Maximum resident set size (kbytes)":
            mem = int(args[1])  # kB
            # print(line)
            # print(param.get("formula"), param.get("log"), mem)
    if time == -1 or mem == -1:
        print(param.get("log"), mem, time)
        raise RuntimeError("Parse failure:", param.get("log"))

    return time, mem


def main():
    config = util.read_config(config_file)
    if config["CREATE_LOGS"]:
        randomLogGenerator.create_logs(config)
    else:  # counting number for logs if no new logs are created
        config["NUM_LOGS"] = len([None for f in listdir("logs/monpoly") if
                                  isfile(join("logs/monpoly", f)) and
                                  f.split(".")[-1] == "log"])

    formulalist = util.parse_formulas()
    # Running logs
    data = {'Cust': [],
            'Workinghours': []
            }
    for f in formulalist:
        plot_data = {'label': f.get('tool') + " - " + f.get('path').split("/")[-1].split(".")[0],
                     'time': [],
                     'mem': []}
        for k in range(config["NUM_LOGS"]):
            logs = util.create_log_name(f.get('tool'), f.get('type'), k)
            for i in range(config["RUNS_PER_LOG"]):
                t, m = [], []
                t_val, m_val = run(f.get('tool'), formula=f.get('path'), log=logs)
                t.append(t_val)
                m.append(m_val)
            plot_data.get('time').append(sum(t)/len(t))
            plot_data.get('mem').append(sum(m)/len(m))
        data.get(f.get('type')).append(plot_data)

    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    makedirs("results/" + date)
    copyfile(config_file, "results/" + date + "/" + config_file)
    copytree("formulas", join("results", date, "formulas"))
    e_rate = arange(config["STARTING_EVENT_RATE"],
                    config["STARTING_EVENT_RATE"] + config["NUM_LOGS"] * config["INCREASING_EVENT_RATE"],
                    config["INCREASING_EVENT_RATE"])

    plot_maker.makeplot(data, e_rate, date)

main()









