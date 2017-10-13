from random import randint
from random import choice

materials = ["Aluminum", "Copper", "Gold", "Iron", "Sandstone", "Marble"]
signatures = ["in", "out"]
shape_weights = [100, 200, 500, 1000, 1500, 2000, 5000]
MAX_AMOUNT = 100
MAX_VAULT_NO = 20


def read_config(file_loc):
    config = {"NUM_LOGS": 0,
              "MIN_LOG_LENGTH": 0,
              "MAX_LOG_LENGTH": 0,
              "AVG_EVENT_DENSITY": 1,
              "OVERWRITE_LOGS": 1,  # bool
              "OUTSIDE_WORKING_HOURS_VIOLATION": 0,  # bool
              "NEGATIVE_AMOUNT_VIOLATION": 0}  # bool
    fo = open(file_loc, 'r')
    for line in fo.readlines():
        data = line.strip().split("=")
        if data[0].strip() in config or data[0].strip == "":
            config[data[0].strip()] = int(data[1].strip())
        else:
            print('No setting named \"' + data[0].strip() + '\"')
    fo.close()
    return config


def create_log(config, log_file):
    fo = open(log_file, 'w')
    timestamp = 1
    fo.write("@" + str(timestamp))
    log_length = randint(config.get("MIN_LOG_LENGTH"), config.get("MAX_LOG_LENGTH"))
    for i in range(log_length):
        # increment with prob 1/AVG_EVENT_DENSITY
        timestamp += int(randint(1, config["AVG_EVENT_DENSITY"])/config["AVG_EVENT_DENSITY"])
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


config_data = read_config("config.txt")
if config_data["OVERWRITE_LOGS"]:
    log_append = 0
else:
    log_append = 0  # TODO
for log_no in range(log_append, config_data["NUM_LOGS"] + log_append):
    create_log(config_data, "logs/" + str(log_no) + ".log")



