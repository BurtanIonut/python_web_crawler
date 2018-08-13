import os
import shutil

err = ""
last_link_in_process = 0


# create a folder it it does not exist
def create_folder(arg):
    if not isinstance(arg, str):
        print "folder name must be string"
        return False
    else:
        if not os.path.isdir(arg) and not os.path.isfile(arg):
            os.mkdir(arg)
            return True
        else:
            return False


# remove a folder and all its contents
def remove_folder(arg):
    if not isinstance(arg, str):
        print "File name must be string"
    else:
        if os.path.isdir(arg):
            shutil.rmtree(arg)


# check if a file exists at the given path
def check_file(path_):
    global err
    err = ""
    if isinstance(path_, str):
        if os.path.isfile(path_):
            return True
        else:
            err += "ERROR: File does not exist at specified path "
            return False
    else:
        err += "ERROR: Path must be string "
        return False


# create a file if it does not exist
def create_file(path_):
    if isinstance(path_, str):
        if not os.path.isfile(path_):
            p = open(path_, 'w')
            p.close()
            print "FILE CREATED SUCCESSFULLY"
        else:
            print "ERROR: File already exist" + " { " + path_ + " }"
    else:
        print "File name must be string"


# remove a file if it exists
def remove_file(path_):
    if check_file(path_):
        os.remove(path_)
    else:
        print err + "IN REMOVE_FILE" + " { " + path_ + " }"


# append date to file if it exists
def append_to_file(path_, data):
    if check_file(path_):
        with open(path_, 'a') as p:
            p.write(data)
    else:
        print err + "IN APPEND_TO_FILE" + " { " + path_ + " }"


# delete the contents of a file
def overwrite_file(path_):
    if check_file(path_):
        os.remove(path_)
        p = open(path_, 'w')
        p.close()
    else:
        print err + "IN OVERWRITE_FILE" + " { " + path_ + " }"


# convert a set to a file
def set_to_file(set_, path_):
    with open(path_, 'a') as p:
        for i in set_:
            try:
                p.write(i + '\n')
            except UnicodeEncodeError:
                continue
            else:
                continue


# convert a file to a set
def file_to_set(path_):
    set_ = set()
    with open(path_, 'r') as p:
        for i in p:
            set_.add(i.strip('\n'))
    return set_
