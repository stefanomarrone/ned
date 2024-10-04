
def tostring(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        file_content = ''.join(lines)
    return file_content

def tolist(value):
    retval = value.split(',')
    return retval
