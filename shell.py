#! /usr/bin/env python3
import argparse
import os
from os import listdir
from os.path import isfile, join
import json
import inquirer

### Config Notes Dir ###

# check if config file and path val therein exist
# path = '/home/goldmund/Documents/pynotes_dir'


# Runs If Args Given
def run(args):
    path_existence = False
    path = ''
    while (path_existence == False):
        try:
            with open('.pynotes_config.json', encoding='utf-8') as config_file:
                data = json.load(config_file)
                path = data['notes_storage_path']
                path_existence = True
        except:
    # set config file, needs to read path from config file
            data = {}
            data['notes_storage_path'] = ""
            new_path = input('Set a path for your notes: ')
            data['notes_storage_path'] = f'{new_path}/pynotes_dir'
            with open('.pynotes_config.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile)
            os.mkdir(f'{new_path}/pynotes_dir')

    if (args.new is not None):
        with open(f'{path}/{args.new}.txt', mode='a') as new_arg_file:
            writable = input('Write new note: ')
            new_arg_file.write('\n' + writable)
    elif (args.read is not None):
        with open(f'{path}/{args.read}.txt', mode='r') as read_arg_file:
            print(read_arg_file.read())
    elif (args.edit is not None):
        with open(f'{path}/{args.edit}.txt', mode='r') as edit_arg_file:
            print(edit_arg_file.read())
        with open(f'{path}/{args.edit}.txt', mode='a') as edit_arg_file:
            writable = input('Add to note: ')
            edit_arg_file.write('\n' + writable)
    else:
        run_action_interface(path)

### Action Interface ### 

def run_action_interface(path):
### Format Paths ###
    print(path)
    all_files = [f for f in listdir(path) if isfile(join(path, f))]
    stripped_files = list(map(lambda x: x.replace('.txt',''),all_files))

### FUNCTIONS ###

    # New File
    def new_file():
        # write new file
        new_file_name = input('Name this new note: ')
        with open(f'{path}/{new_file_name}.txt', mode='a') as new_file:
            writable = input('Write new note: ')
            new_file.write('\n' + writable)

    # Read File
    def read_file():
        read_file_name = inquirer.list_input("Select a note to read: ",choices=stripped_files,)
        with open(f'{path}/{read_file_name}.txt', mode='r') as read_file:
            print(read_file.read())

    # Edit File
    def edit_file():
        edit_file_name = inquirer.list_input('Select a note to append to: ',choices=stripped_files,)
        with open(f'{path}/{edit_file_name}.txt', mode='r') as edit_file:
            print(edit_file.read())
        with open(f'{path}/{edit_file_name}.txt', mode='a') as edit_file:
            writable = input('Add to note: ')
            edit_file.write('\n' + writable)

### Options UI ###

    options = [("Create a new note",'n'), ("Read an existing note", 'r'), ("Append to an existing note", "a")]
    action = inquirer.list_input("Select an option: ", choices=options)
    
    if (action == 'n'):
        new_file()
    elif (action == 'r'):
        read_file()
    elif (action == 'a'):
        edit_file()


### MAIN ARGPARSE FUNC ###

# TO-DO: add direct func calls if -r or -e options are passed w/out a file arg
def main():
    parser=argparse.ArgumentParser(description="Easily take and keep notes from anywhere in the shell.")
    parser.add_argument("-r",help="name of note you want to read" ,dest="read", type=str, required=False, action='store')
    parser.add_argument("-n",help="name of new note" ,dest="new", type=str, required=False, action='store')
    parser.add_argument("-a",help="name of note you want to edit" ,dest="edit", type=str, required=False, action='store')
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
	main()


### TODOS
# need to make man page
# need to disable multiple, conflicting args
# need to display files, selectable by int
