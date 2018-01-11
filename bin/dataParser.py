from os import listdir
from os.path import isfile, join


def get_formula_files(tool: str, formula: str):
    return {
        'monpoly': [join("formulas", formula, tool, f) for f in listdir(join("formulas", formula, tool))
                    if isfile(join("formulas", formula, tool, f))],
        'stream': [join("formulas", formula, tool, f) for f in listdir(join("formulas", formula, tool))
                    if isfile(join("formulas", formula, tool, f))]
    }.get(tool)



