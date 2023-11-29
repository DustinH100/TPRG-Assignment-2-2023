# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json
import vcgencmd

s = socket.socket()
host = '192.168.0.14' # Localhost
port = 5000
s.bind((host, port))
s.listen(5)


#gets the Core Temperature from Pi, ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
temp = os.popen("vcgencmd measure_temp").readline()
    
#temp = os.popen('vcgencmd measure_volts ain1').readline() #gets from the os, using vcgencmd - the core-temperature
# initialising json object string
ini_string = """{"Temperature": temp,}"""
# converting string to json
f_dict = eval(ini_string) # The eval() function evaluates JavaScript code represented as a string and returns its completion value.





while True:
  c, addr = s.accept()
  print ('Got connection from',addr)
  res = bytes(str(f_dict), 'utf-8') # needs to be a byte
  c.send(res) # sends data as a byte type
  c.close()