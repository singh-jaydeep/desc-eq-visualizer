import os

def clear_directory(directory):
    files = visible_files(directory)
    if len(files) == 0:
        print('Directory empty')
    else: 
        for file in files:
            print(f'Removing {file}')
            os.remove(os.path.join(directory, file))

def list_directory(directory):
    files = visible_files(directory)
    if len(files) == 0:
        print('Directory empty')
    else: 
        for file in files:
            print(f'{file}')

def visible_files(directory):
    visible_files = [] 
    for item in os.listdir(directory):
        if not item.startswith('.'):
            visible_files.append(item)
    return visible_files