#! /usr/bin/env python3
import argparse
import os
import os.path
import json
import os
import sys
import re
import inquirer
from os import listdir
from pprint import pprint
from os.path import isfile, join



### Config Notes Dir ###

# check if config file and path val therein exist
path = '/home/goldmund/Documents/pynotes_dir'
if (not os.path.exists(path)):
    new_path = input('Set a path for your notes: ')
    os.mkdir(f'{new_path}/pynotes_dir')

    # set config file, needs to read path from config file
    # with open('.pynotes_config.json') as json_data_file:
    #     datas = json.load(json_data_file)
    #     print(datas)
    
# Args Given
def run(args):
    if (args.new is not None):
        with open(f'{path}/{args.new}.txt', mode='a') as new_file:
            writable = input('Write new note: ')
            new_file.write('\n' + writable)
    elif (args.read is not None):
        with open(f'{path}/{args.read}.txt', mode='r') as read_file:
            print(read_file.read())
    elif (args.edit is not None):
        with open(f'{path}/{args.edit}.txt', mode='r') as edit_file:
            print(edit_file.read())
        with open(f'{path}/{args.edit}.txt', mode='a') as edit_file:
            writable = input('Add to note: ')
            edit_file.write('\n' + writable)
    else:
        run_action_interface()

### Action Interface ### 

def run_action_interface():
    ### Functions - Actions ###
    all_files = [f for f in listdir(path) if isfile(join(path, f))]
    stripped_files = list(map(lambda x: x.replace('.txt',''),all_files))


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
    

    action = input('Select an option: (n) Create a new note, (r) Read an existing note, (a) Append to an existing note: ')
    if (action == 'n'):
        new_file()
    elif (action == 'r'):
        read_file()
    elif (action == 'a'):
        edit_file()

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
