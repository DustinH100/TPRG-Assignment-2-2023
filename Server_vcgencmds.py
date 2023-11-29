"""TPRG Assignment 2 Dustin Horne, Server to obtain
internal readings from pi400
"""
import signal
import sys
import socket
import os
import json
import vcgencmd

def grace_exit(sig, frame):
    print("Closing the server.")
    s.close()
    sys.exit(0)
    
signal.signal(signal.SIGINT, grace_exit)

s = socket.socket()
host = '192.168.0.14'  # Localhost 192.168.0.14	10.102.13.212
port = 5000
s.bind((host, port))
s.listen(5)

def get_temperature():
    return os.popen("vcgencmd measure_temp").readline()

def get_cpu_speed():
    return os.popen("vcgencmd measure_clock arm").readline()

def get_gpu_speed():
    return os.popen("vcgencmd measure_clock core").readline()

def get_memory_info():
    mem_info = os.popen("free").readlines()
    used_memory = mem_info[1].split()[2]
    total_memory = mem_info[1].split()[1]
    return {'used_memory': used_memory, 'total_memory': total_memory}

while True:
    c, addr = s.accept()
    print('Got connection from', addr)

    temperature = get_temperature()
    cpu_speed = get_cpu_speed()
    gpu_speed = get_gpu_speed()
    memory_info = get_memory_info()

    data = {
        "Temperature": temperature,
        "CPU_Speed": cpu_speed,
        "GPU_Speed": gpu_speed,
        "Used_Memory": memory_info['used_memory'],
        "Total_Memory": memory_info['total_memory'],
    }

    for key, value in data.items():
        res = bytes(json.dumps({key: value}), 'utf-8')  # convert the dictionary to a JSON-encoded string and encode it to bytes
        c.send(res)
        
    c.close()