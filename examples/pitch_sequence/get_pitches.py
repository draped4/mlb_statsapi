# statsapi get-gamepks --start 03/28/2019 --end 09/29/2019 --output ./output_dir

import os
import json

with open("./output_dir/get_gamepks_2020_04_30_16_53_32.json") as f:
    gamepks = json.load(f)

num_pks = len(gamepks)
count = 0
for pk in gamepks:
    print(str(count) + " out of " + str(num_pks))
    count += 1
    # get-pitches version
    os.system(
        "statsapi get-pitches --game-pk "
        + str(pk)
        + " --output ../viz/pitch_sequence/data"
    )

    # # get-re24 version
    # os.system(
    #     "statsapi get-re24 --game-pk "
    #     + str(pk)
    #     + " --output ../viz/pitch_sequence/data"
    # )
