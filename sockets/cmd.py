import subprocess

# Define your desired command (replace "ipconfig" with your actual command)
command = 'netsh interface ipv4 show config name="Local Area Connection* 2"'

try:
  # Execute the command and capture the output using subprocess.check_output
  output = subprocess.check_output(command, shell=True, universal_newlines=True)
  output = output.split("\n")
  output = list(filter(lambda _ : _.strip().startswith("IP Address"), output))[0]
  while " " in output:
    output = output.replace(" ", "")
  output = output[10:]
  print(output)
except subprocess.CalledProcessError as e:
  # Handle errors if the command fails
  print(f"Error: {e}")

out = subprocess.check_output("netsh interface show interface")