from random import randint
from random import choice
import shutil
import os


materials = ["Aluminum", "Copper", "Gold", "Iron", "Sandstone", "Marble"]
signatures = ["in", "out"]
shape_weights = [100, 200, 500, 1000, 1500, 2000, 5000]
MAX_AMOUNT = 100
MAX_VAULT_NO = 20


def create_log(config: dict, log_file: str) -> None:
    fo = open(log_file, 'w')
    timestamp = 1
    counter = 0
    fo.write("@0")
    event_inj = 0
    for i in range(config["MAX_TIMESTAMP"]*config["EVENT_RATE"] - 1):
        counter += 1
        isopen = True
        last_timestamp = timestamp
        if counter == config["EVENT_RATE"]:
            timestamp += 1
            counter = 0
        if timestamp == (config["MAX_TIMESTAMP"]/2 + 1) and not event_inj:
            fo.write("@" + str(config["MAX_TIMESTAMP"]/2) + "cust(1)\n")
            event_inj = 1
        if config["INJ_WORKING_HOURS"] and last_timestamp != timestamp:
            if isopen:
                fo.write("@" + str(timestamp) + " open()\n")
                isopen = False
            else:
                fo.write("@" + str(timestamp) + " close()\n")
                isopen = True
        amount = randint(1, MAX_AMOUNT)
        shape_no = randint(1, len(shape_weights))
        fo.write("@" + str(timestamp) + " " +
                 choice(signatures) + "(" +
                 choice(materials) + " ," +
                 str(shape_weights[shape_no - 1]*amount) + " ," +
                 str(amount) + " ," +
                 str(shape_no) + " ," +
                 str(randint(1, MAX_VAULT_NO)) + ")\n")
    fo.write("@1000")
    fo.close()
    return


def create_logs(config: dict) -> None:
    config["EVENT_RATE"] = config["STARTING_EVENT_RATE"]
    shutil.rmtree("logs")  # removes all logs
    os.makedirs("logs")
    log_append = 0
    for log_no in range(log_append, config["NUM_LOGS"] + log_append):
        create_log(config, "logs/" + str(log_no) + ".log")
        if config["INCREASING_EVENT_RATE"]:
            config["EVENT_RATE"] += config["INCREASING_EVENT_RATE"]
    return

