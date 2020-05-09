import os

file_list = os.listdir("./data")

f = open("./data/allpitches.json", "w")
num_files = len(file_list)
count = 0
for file in file_list:
    if file == ".DS_Store" or file == "allpitches.json":
        print("Skipping " + str(count) + " out of " + str(num_files) + ". " + file)
        count += 1
        continue

    file_path = os.path.join("./data", file)

    # Skip empty files
    if os.stat(file_path).st_size > 100:
        print("Writing " + str(count) + " out of " + str(num_files) + ". " + file)
        with open(file_path, "r") as read_f:
            lines = read_f.readlines()

            # Get rid of first and last lines to make a single list object
            if count == 0:
                f.writelines([item for item in lines[:-1]])
                f.writelines(",")
            elif count == (num_files - 1):
                f.writelines([item for item in lines[1:]])
            else:
                f.writelines([item for item in lines[1:-1]])
                f.writelines(",")
    else:
        print("Skipping " + str(count) + " out of " + str(num_files) + ". " + file)

    count += 1
