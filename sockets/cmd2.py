import subprocess as sp

def cb (line:str):
    if line == "\r":
        return ""
    while '\r' in line:
        line = line.replace('\r','')
    while '  ' in line:
        line = line.replace('  ', ' ')
    return line

def extractInterfaces(line):
    target = "Dedicated"
    i = line.find(target)
    return line[i+len(target):].strip()

def getInterfaces():

    out = sp.check_output("netsh interface show interface").decode()
    out = out.split("\n")
    out = list(map(cb, out)) # filtering \r and double spaces
    out = list(filter(bool, out)) # filter empty strings

    out = out[2:]

    interfaces = list(map(extractInterfaces, out))

    return interfaces


if __name__ == "__main__":
    print("interfaces : ", getInterfaces())