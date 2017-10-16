from random import randint
from random import choice

materials = ["Aluminum", "Copper", "Gold", "Iron", "Sandstone", "Marble"]
signatures = ["in", "out"]
shape_weights = [100, 200, 500, 1000, 1500, 2000, 5000]
MAX_AMOUNT = 100
MAX_VAULT_NO = 20


def read_config(file_loc):
    # type: (str) -> dict
    config = {"NUM_LOGS": 0,
              "MAX_TIMESTAMP": 0,
              "EVENT_RATE": 0,
              "INCREASING_EVENT_RATE": 0,
              "OVERWRITE_LOGS": 1,  # bool
              "OUTSIDE_WORKING_HOURS_VIOLATION": 0,  # bool
              "NEGATIVE_AMOUNT_VIOLATION": 0}  # bool
    fo = open(file_loc, 'r')
    for line in fo.readlines():
        data = line.strip().split("=")
        if data[0].strip() in config:
            config[data[0].strip()] = int(data[1].strip())
        elif data[0] == "":
            pass
        else:
            print('No setting named \"' + data[0].strip() + '\"')
    fo.close()
    return config


def write_config(config, file_loc):
    fo = open(file_loc, "w")
    for key in config.keys():
        fo.write(key + " = " + str(config[key]))
    return


def create_log(config, log_file):
    fo = open(log_file, 'w')
    timestamp = 1
    counter = 0
    fo.write("@" + str(timestamp))
    for i in range(config["MAX_TIMESTAMP"]):
        counter += 1
        if counter == config["EVENT_RATE"]:
            timestamp += 1
            counter = 0
        amount = randint(1, MAX_AMOUNT)
        shape_no = randint(1, len(shape_weights))
        fo.write("@" + str(timestamp) + " " +
                 choice(signatures) + "(" +
                 choice(materials) + " ," +
                 str(shape_weights[shape_no - 1]*amount) + " ," +
                 str(amount) + " ," +
                 str(shape_no) + " ," +
                 str(randint(1, MAX_VAULT_NO)) + ")\n")
    fo.close()
    return


def create_logs():
    config_data = read_config("config.txt")
    if config_data["OVERWRITE_LOGS"]:
        log_append = 0
    else:
        log_append = 0  # TODO
    for log_no in range(log_append, config_data["NUM_LOGS"] + log_append):
        if config_data["INCREASING_EVENT_RATE"]:
            config_data["EVENT_RATE"] += 1
        create_log(config_data, "logs/" + str(log_no) + ".log")
    return


create_logs()
