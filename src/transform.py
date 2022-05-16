#!/usr/bin/env python3
"""
transform AAS from XML to JSON
"""

import io
import json
import os

import aas
from aas.adapter.xml import read_aas_xml_file
from aas.adapter.json import write_aas_json_file
from check_conceptdesc import check_conceptdesc, preprocess


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


def get_aas_ids(in_path: str, id_file: str) -> None:
    aas_id_dict: dict = {}
    files = [os.path.join(in_path, f) for f in os.listdir(in_path) if os.path.isfile(os.path.join(in_path, f)) and f.split('.')[-1] == "json"]
    for f in files:
        with open(f, "r") as af:
            aas_content = json.load(af)
        assert len(aas_content["assetAdministrationShells"]) == 1, f"ambiguity in {f}: file does not include exactly one AAS"
        aas_id_dict[f] = aas_content["assetAdministrationShells"][0]["identification"]["id"]
    with open(id_file, "w") as f:
        json.dump(aas_id_dict, f, indent=4)


if __name__ == "__main__":
    in_path = "../res/"
    in_path2 = "../res_new/"
    id_dict = "../res/_id_dict.json"
    check_conceptdesc(in_path)
    transform_several(in_path2)
    get_aas_ids(in_path, id_dict)
