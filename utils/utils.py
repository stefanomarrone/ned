import os
import string
import random

def tostring(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        file_content = ''.join(lines)
    return file_content

def tolist(value):
    retval = value.split(',')
    return retval


def check_first_line(inifilename):
    retval = False
    try:
        with open(inifilename, 'r') as file:
            first_line = file.readline().strip()
            retval = (first_line == "[main]")
    except FileNotFoundError:
        print(f"Error: The file '{inifilename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return retval


def clear_folder(dir):
    if os.path.exists(dir):
        for the_file in os.listdir(dir):
            file_path = os.path.join(dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                else:
                    clear_folder(file_path)
                    os.rmdir(file_path)
            except Exception as e:
                print(e)

def id_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))