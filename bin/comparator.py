
def compare(**param) -> bool:
    is_identical = True
    f1 = open(param.get('monpoly'), 'r')
    l1 = f1.readlines()
    f2 = open(param.get('stream'), 'r')
    l2 = f2.readlines()
    if len(l1) != len(l1):
        return False
    for i, j in zip(l1, l2):
        is_identical &= is_equal(monpoly=parse_line('monpoly', i),
                                 stream=parse_line('stream', j))
    return is_identical


def parse_line(tool: str, line: str) -> (str, [str]):
    # returns (timestamp, [output variables])
    return {
        'monpoly': (line.split(".")[0][1:], line.split(":")[-1].strip()[1:-1].split(",")),
        'stream': (line.split(":")[0][1:-1], line.split(":")[-1].strip().split(", "))
    }.get(tool)


def is_equal(**param) -> bool:
    if len(set([e[0] for e in param.values()])) != 1:  # same timestamp?
        return False
    if len(set([len(e[1]) for e in param.values()])) != 1:  # same number of output variables?
        return False
    if len(set([e for sublist in [l[1] for l in param.values()] for e in sublist])) != \
            len(set(list(param.values())[0][1])):  # same output variables?
        return False
    return True
