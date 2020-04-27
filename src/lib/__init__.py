"""third party modules"""
import ntpath
import subprocess
import os
import json
import base64
import csv

"""third party modules"""
import click


def write_json_to_file(data, output_path):
    file = open(output_path, "w")
    n = file.write(json.dumps(data, sort_keys=True, indent=4))
    file.close()

    return True


def get_re24(year):
    # Do not calculate RE24 for years before 2001
    if int(year) < 2001:
        return []

    with open("./src/lib/re24.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        re24 = []
        for row in csv_reader:
            if row[2] == str(year):
                re24.append(row)
            if len(re24) == 8:
                break

    return re24


# TODO: Add more than just the MLB venues
def get_venue_latlong(venue):
    with open("./src/lib/venues.json") as json_file:
        venues = json.load(json_file)
        for v in venues:
            if v["name"] == venue:
                return v

    return None
