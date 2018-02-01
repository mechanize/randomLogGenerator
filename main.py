
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


def main():
    config = util.read_config(config_file)
    if config["CREATE_LOGS"]:
        randomLogGenerator.create_logs(config)
    else:  # counting number for logs if no new logs are created
        config["NUM_LOGS"] = len([None for f in listdir("logs/monpoly") if
                                  isfile(join("logs/monpoly", f)) and
                                  f.split(".")[-1] == "log"])

    formulalist = util.parse_formulas()

    console_in = "parallel ./bin/run.py ::: " + \
                 " ".join(formulalist) + " ::: " + \
                 "{0.." + config["NUM_LOGS"] + "}" + " ::: " + \
                 "{0.." + config["RUNS_PER_LOG"] + "}"
    console_out = subprocess.Popen(console_in, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    res = console_out.communicate()

    # Running logs
    data = {'Cust': {},
            'Workinghours': {}
            }

    for formula in formulalist:
        f_type, tool, label = formula.split(".")[0].split("/")[1:4]
        data.get(f_type)[tool + " - " + label] = {'time': [[]]*config["NUM_LOGS"],
                                                  'mem': [[]]*config["NUM_LOGS"]}

    for line in res[0].decode("utf-8").split("\n"):
        tool, f_type, label, lognum, mem, time = line.split(" ")
        data.get(f_type).get(tool + " - " + label).get('time')[lognum].append(time)
        data.get(f_type).get(tool + " - " + label).get('mem')[lognum].append(mem)

    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    makedirs("results/" + date)
    copyfile(config_file, "results/" + date + "/" + config_file)
    copytree("formulas", join("results", date, "formulas"))
    e_rate = arange(config["STARTING_EVENT_RATE"],
                    config["STARTING_EVENT_RATE"] + config["NUM_LOGS"] * config["INCREASING_EVENT_RATE"],
                    config["INCREASING_EVENT_RATE"])

    plot_maker.makeplot(data, e_rate, date)


main()
