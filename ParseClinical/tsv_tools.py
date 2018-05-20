"""Dump patient properties to tsv

Not generic, a bit quick and... hacky

"""
from __future__ import print_function
import csv
import utils


def create_property_tsv(objs, tsv_path='SomeObject2Prop.tsv'):
    # Get headers from first obj
    fieldnames = utils.get_property_names(objs[0])
    print("Headers are: \n{}".format("\n".join(fieldnames)))
    with open(tsv_path, 'w') as tsvf:
        writer = csv.DictWriter(tsvf, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for obj in objs:
            obj_dict = {}
            for prop_name in fieldnames:
                obj_dict[prop_name] = getattr(obj, prop_name, "SENTINEL for now, shouldn't happen")
            writer.writerow(obj_dict)
