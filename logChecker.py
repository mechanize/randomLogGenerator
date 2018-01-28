import subprocess
import sys

from bin import comparator
from bin import util
from bin import input_parser

monpoly = "~/Documents/Bachelorthesis/2017-jager-survey/monpoly/monpoly"
stream = "~/Documents/Bachelorthesis/stream/stream/bin/gen_client"
stream_config = "~/Documents/Bachelorthesis/stream/config"

inp = sys.argv[1:]

param = input_parser.get_param(inp)
for tool, paths in zip(param, param.values()):
    if tool == 'monpoly':
        popen = subprocess.Popen("monpoly" + " -sig " + paths.get('signature') + " -formula " + paths.get('formula') +
                                 " -log " + paths.get('log') + " -negate > m_out", shell=True)
        popen.communicate()
        param.get('monpoly').update({'out': 'm_out'})
    elif tool == 'stream':
        util.stream_set_src(paths.get('script'), paths.get('logs'))
        dest = util.stream_get_dest(paths.get('script'))
        popen = subprocess.Popen(stream + " -c " + stream_config + " -l log " + paths.get('script'), shell=True)
        popen.communicate()
        param.get('stream').update({'out': dest})
print(comparator.compare(monpoly=param.get('monpoly').get('out'),
                         stream=param.get('stream').get('out')))

