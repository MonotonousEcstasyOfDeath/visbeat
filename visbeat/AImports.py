#AImports
from ADefines import *
import os
import os.path
import errno
import json
import cPickle as pickle
import glob
import subprocess
from operator import truediv
import shutil
import time
from time import gmtime, strftime, localtime
import random
import fileui


if(AD_DEBUG):
    # import warnings
    # warnings.simplefilter('default')

    try:
        from termcolor import colored
        def AWARN(message):
            print(colored(message, 'red'))
    except ImportError:
        print("You do not have termcolor installed (pip install termcolor). AWARN will just show as plain print statements when AD_DEBUG==True...")
        def AWARN(message):
            print(message);
    #
    # def send_warnings_to_print_red(message, category, filename, lineno):
    #     print(colored('{} WARNING! file: {} Line:{}\n{}'.format(category, filename, lineno, message), 'red'))
    # old_showwarning = warnings.showwarning
    # warnings.showwarning = send_warnings_to_print_red;


def local_time_string():
    return strftime("%Y-%m-%d_%H:%M:%S", localtime());

def get_temp_file_path(final_file_path="TEMP", temp_dir_path = None):
    pparts = os.path.split(final_file_path);
    destfolder = pparts[0]+os.sep;
    tempdir = temp_dir_path;
    if(tempdir is None):
        tempdir='.';
    destfolder=pathstring(tempdir+os.sep);
    tempname = 'TEMP_'+pparts[1];
    temptry = 0;
    while(os.path.isfile(destfolder+tempname)):
        temptry=temptry+1;
        tempname = 'TEMP{}_'.format(temptry)+pparts[1];
    return pathstring(destfolder+tempname);


def runningInNotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

def getshellname():
    try:
        shell = get_ipython().__class__.__name__
        return shell;
    except NameError:
        return False      # Probably standard Python interpreter


def runningInSpyder():
    return 'SpyderKernel' in str(get_ipython().kernel.__class__);

def pickleToPath(d, path):
    # assert(False)
    print("pickling")
    f = open(path, 'wb');
    pickle.dump(d, f, protocol=2);
    f.close();
    return True;

def unpickleFromPath(path):
    f=open(path, 'rb');
    d=pickle.load(f);
    f.close();
    return d;

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def make_sure_dir_exists(path):
    pparts = os.path.split(path);
    destfolder = pparts[0]+os.sep;
    try:
        os.makedirs(destfolder)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def safe_file_name(input_string):
    return ''.join([i if ord(i) < 128 else '_' for i in input_string]);

def pathstring(path):
    return path.replace(os.sep+os.sep, os.sep);

def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')

def printOb(obj):
  for attr in dir(obj):
    print "#### Obj.%s = %s\n" % (attr, getattr(obj, attr))

def pathstring(path):
    return path.replace(os.sep+os.sep, os.sep);

def get_prepended_name_file_path(original_file_path, string_to_prepend):
    pparts = os.path.split(original_file_path);
    destfolder = pparts[0]+os.sep;
    pname = string_to_prepend+pparts[1];
    return pathstring(destfolder+pname);

def safe_file_name(input_string):
    return ''.join([i if ord(i) < 128 else '_' for i in input_string]);

def change_extension(input_path, new_ext):
    nameparts = os.path.splitext(input_path);
    return nameparts[0]+new_ext;

def printDictionary(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                printDictionary(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                printDictionary(v)
            else:
                print v
    else:
        print obj

def spotgt_shift_bit_length(x):
    #smallest power of two greater than
    return 1<<(x-1).bit_length()

def get_file_name_from_path(pth):
    return os.path.split(pth)[1];

def get_dir_from_path(pth):
    return (os.path.split(pth)[0]+os.sep);

def get_file_names_from_paths(pths):
    r = [];
    for p in pths:
        r.append(get_file_name_from_path(p));
    return r;

def writeDictionaryToJSON(d, json_path=None):
    if(json_path):
        with open(json_path, 'w') as outfile:
            json.dump(d, outfile, sort_keys = True, indent = 4, ensure_ascii=False);


def vtt_to_srt(fileContents):
	replacement = re.sub(r'([\d]+)\.([\d]+)', r'\1,\2', fileContents)
	replacement = re.sub(r'WEBVTT\n\n', '', replacement)
	replacement = re.sub(r'^\d+\n', '', replacement)
	replacement = re.sub(r'\n\d+\n', '\n', replacement)
	return replacement