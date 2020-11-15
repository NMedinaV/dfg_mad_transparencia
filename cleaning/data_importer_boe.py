import pandas as pd
import glob
import os
import json
from io import StringIO

def load_data(path_to_data='../data', fecha_publicacion='*', seccion='*', subseccion='*', departamento='*'):
    filelist = glob.glob(f"{path_to_data}/{fecha_publicacion}/{seccion}/{subseccion}/{departamento}/*.json")
    lines = []
    for file in filelist:
        if os.path.isfile(file):
            with open(f'../data/{file}', 'r') as line:
                line_str = line.read()
                json_line = json.loads(line_str)
                lines.append(json_line)
    lines = json.dumps(lines)
    df = pd.read_json(StringIO(lines))
    return df
