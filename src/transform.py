#!/usr/bin/env python3
"""
transform AAS from XML to JSON
"""

import io
import os

import aas
from aas.adapter.xml import read_aas_xml_file
from aas.adapter.json import write_aas_json_file


def xml_to_json(in_path: str) -> None:
    out_path = in_path.split(".xml")[0] + ".json"
    data: aas.model.DictObjectStore[aas.model.Identifiable] = aas.model.DictObjectStore()
    # read from XML
    with open(in_path, 'r', encoding='utf-8') as f:
        in_data = f.read()
    bytes_io = io.BytesIO(in_data.encode("utf-8"))
    data = read_aas_xml_file(bytes_io)
    # write to JSON
    with open(out_path, 'w', encoding='utf-8') as f:
        write_aas_json_file(file=f, data=data)


def transform_several(aas_dir: str) -> None:
    files = [os.path.join(aas_dir, f) for f in os.listdir(aas_dir) if os.path.isfile(os.path.join(aas_dir, f)) and f.split('.')[-1] == "xml"]
    for f in files:
        preprocess(f)
        xml_to_json(f)


def preprocess(in_path: str) -> None:
    with open(in_path, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('REAL_MEASURE', 'decimal')
    filedata = filedata.replace('True', 'true')
    with open(in_path, 'w') as file:
        file.write(filedata)


if __name__ == "__main__":
    in_path = "../res/"
    transform_several(in_path)
