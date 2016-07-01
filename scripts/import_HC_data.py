#!/bin/env python3

import csv
import json
import yaml

def import_HC_data(node_file, interaction_file):
    SalmoNet = {"node": {}, "interaction": {}, "groups": {}, "strains": []}
    with open(node_file) as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            SalmoNet["node"][row[0]] = {
                "name": row[1],
                "locus": row[2].replace(",", ";"),
                "group": row[3],
                "strain": row[4],
                "num_ortholog": 0,
                "num_interaction": 0,
            }
            if row[3] not in SalmoNet["groups"]:
                SalmoNet["groups"][row[3]] = []
            SalmoNet["groups"][row[3]].append(row[0])
            if row[4] not in SalmoNet["strains"]:
                SalmoNet["strains"].append(row[4])
    with open(interaction_file) as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            ref = row[2].replace(",", "").replace("__", "_").split("_")
            SalmoNet["interaction"]["%s-%s"%(row[0],row[1])] = {
                "source": row[0],
                "target": row[1],
                "ref": ref,
                "layer": row[3],
            }
            SalmoNet["node"][row[0]]["num_interaction"] += 1
            SalmoNet["node"][row[1]]["num_interaction"] += 1
    for node in SalmoNet["node"]:
        SalmoNet["node"][node]["num_ortholog"] = len(SalmoNet["groups"][SalmoNet["node"][node]["group"]])
    return SalmoNet


def export_strain_select_json(SalmoNet, out_file):
    select = []
    select.append({"value": "Select a strain", "id": 0})
    for id, strain in enumerate(SalmoNet["strains"]):
        select.append({"id": id+1, "value": strain})
    with open(out_file, "w") as f:
        json.dump(select, f)


def export_strain_node_lists(SalmoNet, files_prefix):
    for id, strain in enumerate(SalmoNet["strains"]):
        with open("%s/nodes%s.csv" % (files_prefix, id+1), "w") as f:
            for nid, node in enumerate(SalmoNet["node"]):
                if SalmoNet["node"][node]["strain"] == strain:
                    f.write("%s,%s,%s,%s,%s,%s\n" % (
                        nid,
                        node,
                        SalmoNet["node"][node]["name"],
                        SalmoNet["node"][node]["locus"],
                        SalmoNet["node"][node]["num_ortholog"],
                        SalmoNet["node"][node]["num_interaction"],
                    ))

def export_protein_data(SalmoNet, path):
    for uniprot in SalmoNet["node"]:
        with open("%s/%s.md" % (path, uniprot), "w") as f:
            md_data = {}
            md_data["title"] = uniprot
            md = yaml.dump(md_data, allow_unicode=True,
                      default_flow_style=False,
                      explicit_start=True, explicit_end=True,
                      default_style="'", line_break="/n")
            f.write(md+"\ntest\n")
        return
