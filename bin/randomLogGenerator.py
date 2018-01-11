from random import randint
from random import choice
import shutil
import os


materials = ["Aluminum", "Copper", "Gold", "Iron", "Sandstone", "Marble"]
signatures = ["in", "out"]
shape_weights = [100, 200, 500, 1000, 1500, 2000, 5000]
MAX_AMOUNT = 100
MAX_VAULT_NO = 20


def create_logs(config: dict) -> None:
    # Clears old logs and creates new ones.
    # Also handles increasing event rate.
    config["EVENT_RATE"] = config["STARTING_EVENT_RATE"]
    shutil.rmtree("logs")
    os.makedirs("logs")
    for log_num in range(0, config["NUM_LOGS"]):
        create_log(config, log_num)
        if config["INCREASING_EVENT_RATE"]:
            config["EVENT_RATE"] += config["INCREASING_EVENT_RATE"]
    return


def create_log(config: dict, log_num: int) -> None:
    # Creates one log for each tool.
    # Uses the lists of materials, weights and signatures above to create random entries.
    # The logs for different tools have identical information.

    # Monpoly
    f_monpoly = open("logs/monpoly/" + str(log_num) + ".log")
    f_monpoly.write("@0")

    # Stream
    f_stream_in = open("logs/stream/" + str(log_num) + "_in.dat")
    f_stream_in.write("i, str, i, i, i, i")
    f_stream_out = open("logs/stream/" + str(log_num) + "_out.dat")
    f_stream_out.write("i, str, i, i, i, i")
    f_stream_isopen = open("logs/stream/" + str(log_num) + "_isopen.dat")
    f_stream_isopen.write("i, i")
    f_stream_cust = open("logs/stream/" + str(log_num) + "_cust.dat")
    f_stream_cust.write("i, i")

    # Loop init
    timestamp = 1
    counter = 0
    event_inj = False

    for i in range(config["MAX_TIMESTAMP"]*config["EVENT_RATE"] - 1):
        counter += 1
        isopen = True
        last_timestamp = timestamp

        # Events per timestamp
        if counter == config["EVENT_RATE"]:
            timestamp += 1
            counter = 0

        # One "cust(int)" event per log
        if timestamp == (config["MAX_TIMESTAMP"]/2 + 1) and not event_inj:
            vault_value = randint(1, MAX_VAULT_NO)
            create_short_entry('monpoly', f_monpoly, timestamp, signature='cust', value=vault_value)
            create_short_entry('stream', f_stream_cust, timestamp, signature='cust', value=vault_value)
            event_inj = True

        # Open/close every other timestamp
        if last_timestamp != timestamp:
            if isopen:
                create_short_entry('monpoly', f_monpoly, timestamp, signature='open')
                create_short_entry('stream', f_stream_isopen, timestamp, signature='open')
                isopen = False
            else:
                create_short_entry('monpoly', f_monpoly, timestamp, signature='close')
                create_short_entry('stream', f_stream_isopen, timestamp, signature='close')
                isopen = True

        # Random in/out event
        signature = choice(signatures)
        material = choice(materials)
        quantity = randint(1, MAX_AMOUNT)
        shape = randint(1, len(shape_weights))
        weight = shape_weights[shape - 1]*quantity
        vault_num = randint(1, MAX_VAULT_NO)
        create_entry('monpoly', f_monpoly, timestamp, signature, material, weight, quantity, shape, vault_num)
        create_entry('stream', {'in':   f_stream_in, 'out':  f_stream_out}.get(signature), timestamp, signature,
                     material, weight, quantity, shape, vault_num)

    # Cleanup
    f_monpoly.write("@1000")
    for file in [f_monpoly, f_stream_out, f_stream_in, f_stream_isopen, f_stream_cust]:
        file.close()
    return


def create_entry(m_type: str, file, timestamp: int, signature: str, material: str, weight: int, quantity: int,
                 shape: int, vault_num: int):
    # Handles in/out events
    file.write({
        'monpoly':  "@" + str(timestamp) + " " +
                    signature + "(" +
                    material + " ," +
                    str(quantity) + " ," +
                    str(weight) + " ," +
                    str(shape) + " ," +
                    str(vault_num) + ")\n",
        'stream':   str(timestamp) + ", " +
                    material + " ," +
                    str(quantity) + " ," +
                    str(weight) + " ," +
                    str(shape) + " ," +
                    str(vault_num) + "\n"
    }.get(m_type, ""))


def create_short_entry(m_type: str, file, timestamp: int, **param):
    # Handles open/close/cust events
    file.write({
        'monpoly':  "@" + str(timestamp) + " " +
                    param.get('signature') + "(" +
                    {
                        'cust': param.get('value')
                    }.get(param.get('signature'), "") + ")\n" + "bla",
        'stream':   str(timestamp) + ", " +
                    {
                        'open':     '1',
                        'close':    '0',
                        'cust':     param.get('value')
                    }.get(param.get('signature'))
    }.get(m_type, ""))





