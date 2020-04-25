"""third party modules"""
import ntpath
import subprocess
import os
import json
import base64

"""third party modules"""
import click

def write_json_to_file(data, output_path):
    file = open(output_path, "w")
    n = file.write(json.dumps(data, sort_keys=True, indent=4))
    file.close()

    return True
