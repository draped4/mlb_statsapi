import pandas as pd
import json

#### Use this segment to read appended file and output csv
with open("./data/allpitches.json") as f:
    pitches = json.load(f)


def flatten_json(nested_json, exclude=[""]):
    """Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name="", exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude:
                    flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


pitches_df = pd.DataFrame([flatten_json(x) for x in pitches])
compression_opts = dict(method="zip", archive_name="out.csv")
pitches_df.to_csv("out.zip", index=False, compression=compression_opts)
