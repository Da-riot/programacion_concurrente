import threading
import time

                    
def locker(lock):
    while True:
        lock.acquire()
        try:
            time.sleep(1.0)
        finally:
            lock.release()
        time.sleep(1.0)
    return
                    
def amigo(lock):
    global i;
    global j;
    for i in range(1,9):
        print("Amigo "+str(i)+" esta comiendo")    
        num_tries = 0
        num_acquires = 0
        while num_acquires < 1:
            time.sleep(1.0)
            acquired = lock.acquire(0)
            try:
                num_tries += 1
                if acquired:
                    print("Desocupando palillo")
                    num_acquires += 1
                else:
                    print("Palillo aun no disponible")
            finally:
                if acquired:
                    lock.release()
                    if(i!=8):
                        print("Pasando palillo a amigo "+str(i+1))
                    
        

if __name__ == '__main__':
    i=1;
    lock = threading.Lock()

    locker = threading.Thread(target=locker, args=(lock,), name='Locker')
    daemon=True
    locker.daemon=daemon
    locker.start()
    
    amigo = threading.Thread(target=amigo, args=(lock,), name='Amigo ')
    amigo.start()