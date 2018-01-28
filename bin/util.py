from shutil import move
from os import remove, listdir, path


def stream_set_src(src: str, params: [str]) -> None:
    src_temp = '/'.join(src.split('/')[:-1] + ["temp.dat"])  # creates a tmp file at the same location as src
    f_src = open(src, 'r')
    f_temp = open(src_temp, 'w+')
    i = 0
    for line in f_src.readlines():
        if line.startswith("source") and len(params) > i:
            f_temp.write("source: " + params[i] + "\n")
            i += 1
        else:
            f_temp.write(line)
    f_temp.close()
    f_src.close()
    remove(src)
    move(src_temp, src)


def stream_get_dest(src: str) -> str:
    f_src = open(src, 'r')
    dest = ""
    for line in f_src.readlines():
        if line.startswith("dest"):
            dest = line.split(":")[-1].strip()
    return dest


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


def parse_formulas() -> [dict]:
    directories = ["formulas/Cust/monpoly", "formulas/Cust/stream", "formulas/Workinghours/monpoly",
                   "formulas/Workinghours/stream"]
    formulas = []
    for prefix in directories:
        formulas += [path.join(prefix, name) for name in listdir(prefix)]
    return [{'type': formula.split("/")[1],
             'tool': formula.split("/")[2],
             'path': formula}
            for formula in formulas]


def create_log_name(tool: str, formula: str, num: int) -> [str]:
    return {
        'monpoly': ["logs/monpoly/" + str(num) + ".log"],
        'stream': {
            'Workinghours': ["logs/stream/" + str(num) + e + ".dat" for e in ["_in", "_out", "_isopen"]],
            'Cust': ["logs/stream/" + str(num) + e + ".dat" for e in ["_in", "_cust"]]
        }.get(formula)
    }.get(tool)


def get_static_data() -> (str, str, str, str, str, str):
    fo = open("staticData.txt", "r")
    dic = {}
    for line in fo.readlines():
        dic.update({line.split("=")[0].strip(): line.split("=")[1].strip()})
    return dic.get('monpoly'), dic.get('monpoly_signature'), dic.get('stream'), dic.get('stream_config'), \
        dic.get('time_loc'), dic.get('config')







