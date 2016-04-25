import socket
import struct
import threading
import time
from thread import *
from stack import Stack
from MaxHeap import MaxHeap


def get_actual_data(conn, size):
    full_data = conn.recv(size)
    return full_data


def encode(data):
    return struct.pack("<B%ds" % (len(data),), len(data), data.encode("utf8"))


def safe_remove_from_termination_list(thread_id):
    if thread_termination_list.__contains__(thread_id):
        thread_termination_list.remove(thread_id)


def delegate_request(conn, header):
    first_bit = header & 0x80  # check if this works actually
    print str(first_bit)
    thread_id = threading.current_thread()
    if first_bit:
        while stack.empty() and not thread_termination_list.__contains__(thread_id):
            pass
        popped = stack.pop()
        conn.sendall(encode(popped))
    else:
        while stack.full() and not thread_termination_list.__contains__(thread_id):
            pass
        data = get_actual_data(conn, header)
        stack.push(data)
        conn.sendall(struct.pack("B", 0x00))
    conn.close()
    safe_remove_from_termination_list(thread_id)
    thread_heap.remove(thread_id)
    return


stack = Stack()
thread_termination_list = []
thread_heap = MaxHeap()
HOST = "127.0.0.1"
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(100)

while 1:
    conn, addr = s.accept()
    print "Connected by", addr
    data = conn.recv(1)
    if not data:
        continue
    size = struct.unpack("!B", data[0])

    if thread_heap.full():
        thread_time, thread_id = thread_heap.peek()
        if int(time.time()) - thread_time > 10:
            thread_termination_list.append(thread_id)
            print "eliminated"
        else:
            conn.sendall(struct.pack("B", 0xFF))
            print " full , reject request"
            continue
    tid = start_new_thread(delegate_request, (conn, size[0],))

    thread_heap.push(tid)
    print "Size of Stack"
    print stack.size()
