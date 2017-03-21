import cPickle
import marshal
import types
import sys
import numpy
import os.path, time
from subprocess import call
import operator
import textract
from RAKE import Rake

tag_vs_files_dictfile = 'tag_vs_files_dictionary.pkl'
print("Running prepare_commands. . .")
call(["python","prepare_commands.py"])
#print("Running generate_tag_vs_files. . .")
#call(["python","generate_tag_vs_files.py"])


"""
::: Something for pruning out the non-existing files :::
"""
def prune_filedict(dict):
    flag=0
    for (key,value) in dict.items():
        for filename in value:
            if(not os.path.isfile(filename)):
                value.remove(filename)
                print "---pruned file:",filename
                flag=1
                if(len(value)==0):
                    del dict[key]
                    print "--prune tag: ",key
                    flag=1
    if(flag==1):
        print "++updated dictionary file"
        pkl_file = open(tag_vs_files_dictfile, 'wb')
        cPickle.dump(dict, pkl_file)
    return dict

"""Directory Scan"""
def scandir(inp, func):
    if inp==None:
        inp = ['.']
    for dir in inp:
        func([path+'/'+item for path,subdir,files in os.walk(dir) for item in files])
    return

#read tag_vs_files dictionary
pkl_file = open(tag_vs_files_dictfile, 'rb')
tag_vs_files = cPickle.load(pkl_file)

#read command dictionary
pkl_file = open('command_dictionary.pkl', 'rb')
commands = cPickle.load(pkl_file)


#read user commands
while(True):
    inp = raw_input('tagfs#: ')
    inp = inp.strip()
    inp = inp.split(' ')
    if inp[0]=='multitag':
        print "Mutitagging "
        autotag = types.FunctionType(marshal.loads(commands['autotag']), globals(), "something")
        files = []
        for dirname, dirnames, filenames in os.walk(inp[1]):
            # print path to all filenames.
            for filename in filenames:
                files.append(dirname + '\\' + filename)
        autotag(files)
    elif(inp[0] in commands):
        func = types.FunctionType(marshal.loads(commands[inp[0]]), globals(), "something")
        #try:

        print "Running function"
        func()
        #except:
        #print "Internal Error, is your syntax correct?"
    elif(inp[0]=='quit' or inp[0]=='q'):
        print "Exiting!"
        break;
    elif(inp[0]=='prune'):
        tag_vs_files = prune_filedict(tag_vs_files);
    elif(inp[0]==''):
        continue
    else:
        print "Command not found!"
