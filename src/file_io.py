import os

###################
# Used to delete files in
# /equilibria/preprocessed
# if user chooses
###################
def clear_directory(directory):
    files = visible_files(directory)
    if len(files) == 0:
        print("Directory empty")
    else:
        for file in files:
            print(f"Removing {file}")
            os.remove(os.path.join(directory, file))

###################
# Used to list files in
# /equilibria/preprocessed
# if user chooses
###################
def list_directory(directory):
    files = visible_files(directory)
    if len(files) == 0:
        print("Directory empty")
    else:
        for file in files:
            print(f"{file}")

###################
# On Mac, extraneous 
# hidden files can be 
# created in the directory
###################
def visible_files(directory):
    visible_files = []
    for item in os.listdir(directory):
        if not item.startswith("."):
            visible_files.append(item)
    return visible_files
