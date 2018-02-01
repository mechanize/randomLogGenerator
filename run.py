#!/usr/bin/python3

import subprocess
from sys import argv
from bin import util


inp = argv[1:]
formula, lognum = tuple(inp)
f_type, tool, label = formula.split(".")[0].split("/")[1:4]

monpoly, monpoly_signature, stream, stream_config, time_loc, config_file = util.get_static_data()

console_in = ""
if tool == "monpoly":
    console_in = 'ts=$(date +%s%N); ' + time_loc + ' ' + monpoly + \
                 ' -sig ' + monpoly_signature + \
                 ' -log ' + 'logs/monpoly/' + str(lognum) + '.log' + \
                 ' -formula ' + formula + \
                 ' -negate > output/' + lognum + '_' + tool + '_' + f_type + \
                 '; tt=$((($(date +%s%N) - $ts)/1000000)); echo "Time_elapsed: $tt"'

if tool == "stream":
    logs = util.create_log_names(tool, f_type, lognum)
    dest = "output/" + lognum + "_" + tool + "_" + f_type
    copy_loc = "formulas/temp/" + lognum + "_" + tool + "_" + f_type
    util.stream_src_copy(formula, copy_loc, dest, logs)
    console_in = 'ts=$(date +%s%N); ' + time_loc + ' ' + stream + \
                 ' -c ' + stream_config + \
                 ' -l log ' + \
                 formula + \
                 '; tt=$((($(date +%s%N) - $ts)/1000000)); echo "Time_elapsed: $tt"'

# Running tool
console_out = subprocess.Popen(console_in, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
res = console_out.communicate()

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
if time == -1 or mem == -1:
    raise RuntimeError("Parse failure:", tool, f_type, label, lognum, mem, time)

print(tool, f_type, label, lognum, mem, time)
