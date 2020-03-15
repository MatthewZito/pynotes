#! /usr/bin/env python3
import argparse, textwrap
import os
from os import listdir
from os.path import isfile, join
import json
import inquirer
import re
import pyfiglet

ascii_banner = pyfiglet.figlet_format("PyNotes")

def run(args):
    # if notes dir does not exist, create one 
    path_existence = False
    path = ''
    while (path_existence == False):
        try:
            with open('.pynotes_config.json', encoding='utf-8') as config_file:
                data = json.load(config_file)
                path = data['notes_storage_path']
                path_existence = True
        except: 
            # set config file, pynotes likes to read path from config file
            data = {}
            data['notes_storage_path'] = ""
            new_path = input('Set a path for your notes: ')
            data['notes_storage_path'] = f'{new_path}/pynotes_dir'
            with open('.pynotes_config.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile)
            os.mkdir(f'{new_path}/pynotes_dir')

    def validate(file_name):
            print('This name includes illegal characters; converting to safe filename...')
            stripped_proc = str(file_name).strip().replace(' ', '_')
            subbed_proc = re.sub(r'(?u)[^-\w.]', '', stripped_proc)
            print(f"This note has been renamed to '{subbed_proc}'")
            return subbed_proc
    # if args were passed. pynotes really likes args
    try:
        if (args.new is not None):
            new_file_name_from_args = validate(args.new)
            with open(f'{path}/{new_file_name_from_args}.txt', mode='a') as new_arg_file:
                writable = input('Write new note: ')
                new_arg_file.write('\n' + writable)
        elif (args.read is not None):
            try:
                with open(f'{path}/{args.read}.txt', mode='r') as read_arg_file:
                    print(read_arg_file.read())
            except IOError:
                print(f"Note '{args.read}' does not exist.")
        elif (args.edit is not None):
            try:
                with open(f'{path}/{args.edit}.txt', mode='r') as edit_arg_file:
                    print(edit_arg_file.read())
                with open(f'{path}/{args.edit}.txt', mode='a') as edit_arg_file:
                    writable = input('Add to note: ')
                    edit_arg_file.write('\n' + writable)
            except IOError:
                print(f"Note '{args.edit}' does not exist.")
        else:
            run_action_interface(path)
    except:
        print('Something went wrong...')
        return


def run_action_interface(path):
    # format paths
    all_files = [f for f in listdir(path) if isfile(join(path, f))]
    stripped_files = list(map(lambda x: x.replace('.txt',''),all_files))

### FUNCTIONS ###

    # create a new note
    def new_file():
        try:
            new_file_name = input('Name this new note: ')
            new_file_name = validate(new_file_name)
        except: 
            print('Something went wrong...')
        with open(f'{path}/{new_file_name}.txt', mode='a') as new_file:
            writable = input('Write new note: ')
            new_file.write('\n' + writable)

    # read an existing note
    def read_file():
        read_file_name = inquirer.list_input("Select a note to read: ",choices=stripped_files)
        # if statement to prevent inquirer from printing every selection
        if (read_file_name in stripped_files):
            with open(f'{path}/{read_file_name}.txt', mode='r') as read_file:
                print(read_file.read())
        else:
            print('The note you specified does not exist.')

    # edit an existing note
    def edit_file():
        edit_file_name = inquirer.list_input("Select a note to append to: ",choices=stripped_files)
        
        # if statement to prevent inquirer from printing every selection
        if (edit_file_name in stripped_files):
            with open(f'{path}/{edit_file_name}.txt', mode='r') as edit_file:
                print(edit_file.read())
            with open(f'{path}/{edit_file_name}.txt', mode='a') as edit_file:
                writable = input('Add to note: ')
                edit_file.write('\n' + writable)
        else:
            print('The note you specified does not exist.')

### Options UI ###
    print(ascii_banner)
    options = [("Create a new note",'n'), ("Read an existing note", 'r'), ("Append to an existing note", "a")]
    action = inquirer.list_input("Select an option: ", choices=options)
    
    if (action == 'n'):
        new_file()
    elif (action == 'r'):
        read_file()
    elif (action == 'a'):
        edit_file()

# TO-DO: add direct func calls if -r or -e options are passed w/out a file arg
def main():
    parser=argparse.ArgumentParser(description="Easily take and keep notes from anywhere in the shell.", epilog=textwrap.dedent('''\
        Note names should be passed without a file extension. Pynotes appends `.txt` by default.
        Example Usage: $ pynotes -r note5'''), formatter_class=argparse.RawTextHelpFormatter)
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
