# import netifaces
import socket
import subprocess

def getHOTSPOT():
    output = subprocess.check_output('netsh interface ipv4 show config name="Local Area Connection* 2"', shell=True, universal_newlines=True)
    output = output.split("\n")
    output = list(filter(lambda _ : _.strip().startswith("IP Address"), output))
    if len(output) == 0:
        return None
    output = output[0]
    while " " in output:
      output = output.replace(" ", "")
    output = output[10:]
    return (output)

def getWIFI():
    output = subprocess.check_output('netsh interface ipv4 show config name="Wi-Fi"', shell=True, universal_newlines=True)
    output = output.split("\n")
    output = list(filter(lambda _ : _.strip().startswith("Default Gateway:"), output))[0]
    while " " in output:
      output = output.replace(" ", "")
    output = output[15:]
    return (output)

CLIENT = getWIFI()
HOST = getHOTSPOT()  # Standard loopback interface address (localhost)
PORT = 5002  # Port to listen on (non-privileged ports are > 1023)
# HOST = "localhost"

if __name__ == "__main__": print((CLIENT, HOST, PORT))