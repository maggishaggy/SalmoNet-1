#!/usr/bin/env python3
import subprocess
import os
import sys
import json
import shutil
from import_HC_data import import_HC_data, export_strain_select_json,\
    export_strain_node_lists, export_protein_data

DEV = False
if len(sys.argv) == 2:
    if sys.argv[1] == "dev":
        DEV = True

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SalmoNetJson = "SalmoNet.json"
temp_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "scripts","temp_data"))
data_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "data"))
dev_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "template","src","data"))
deploy_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","data"))
download_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","download"))
pages_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","content","protein"))

# make dirs
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
if not os.path.exists(pages_path):
    os.makedirs(pages_path)
if not os.path.exists(download_path):
    os.makedirs(download_path)
if not os.path.exists(dev_path):
    os.makedirs(dev_path)
if not os.path.exists(deploy_path):
	os.makedirs(deploy_path)

# clear temp
subprocess.call(["rm", "-rf", temp_path+"/*"], stdout=subprocess.PIPE)

# import data
SalmoNet = import_HC_data(
    os.path.join(data_path, "HC_nodes.csv"),
    os.path.join(data_path,"HC_interactions.csv"),
    os.path.join(data_path,"HC_xref_source.csv"),
    os.path.join(data_path,"HC_xref_matrix.csv"),
    os.path.join(data_path,"HC_xref.csv"),
)
with open(os.path.join(temp_path, SalmoNetJson), "w") as f:
    json.dump(SalmoNet, f)

# export strain nodes
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_strain_node_lists(SalmoNet, temp_path)

# export strain select
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_strain_select_json(SalmoNet, os.path.join(temp_path, "strain_select.json"))

# clear protein pages
subprocess.call(["rm","-rf", pages_path+"/*"], stdout=subprocess.PIPE)

# export protein pages
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_protein_data(SalmoNet, pages_path, DEV)

# copy deploy
for src_file in os.listdir(temp_path):
	if src_file == "SalmoNet.json":
		continue
	shutil.copy(os.path.join(temp_path, src_file), os.path.join(deploy_path,src_file))
for src_file in os.listdir(os.path.join(data_path, "download")):
	shutil.copy(os.path.join(data_path, "download", src_file), os.path.join(download_path,src_file))
