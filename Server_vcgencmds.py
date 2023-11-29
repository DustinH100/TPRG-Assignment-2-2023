import socket
import os
import json
import vcgencmd

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
        "Memory_Info": memory_info,
    }

    res = bytes(json.dumps(data), 'utf-8')  # convert the dictionary to a JSON-encoded string and encode it to bytes
    c.send(res)
    c.close()