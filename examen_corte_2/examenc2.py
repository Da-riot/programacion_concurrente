import queue, time
import threading 
import random

COMENSALES = 20
colaM = queue.Queue(maxsize=20)
colaRes2 = queue.Queue(maxsize=20)
colaRes = queue.Queue(maxsize=20)
total = float(10)
waiter = int(total * colaRes2.maxsize/100)
waiters = queue.Queue(maxsize=waiter)
mutex = threading.Lock()
Ordenes = queue.Queue()   
cocinero = queue.Queue()


class Restaurant(threading.Thread):
    def __init__(self, id, monitor):
        threading.Thread.__init__(self)
        self.id= id
        self.monitor = monitor

    def reservar(self):
        flotante = float(20)
        recepcion = int(flotante * colaM.maxsize/100)
        if not colaM.full():
            for x in range(recepcion):
                colaM.put(self.id)
                print("Reservacion para:"+ str(self.id+1))
                self.atencion()
                self.monitor.wait()
        else:
            self.atencion()

    def espera(self):
        with self.monitor:
            if colaRes.full():
                print("Comensal "+str(self.id+1)+" esperando")
                time.sleep(3)
                self.monitor.wait()
                if not colaRes.empty():
                    self.ingreso()
            else:
                self.ingreso()   


    def entregar(self):
        with self.monitor:
            while not cocinero.empty():
                cocinero.get(self.id)
                print("Mesero entregando orden a comensal "+str(self.id+1))
                colaRes.put(self.id)
                self.cenando()
                self.monitor.wait()

    def cenando(self):
        with self.monitor:
            if not cocinero.full():
                print("Comensal "+str(self.id+1)+" esta comiendo")
                time.sleep(random.randint(2, 4))
                print("Comensal "+str(self.id+1)+" esta satisfecho")
                colaRes.get(self.id)
                self.monitor.wait()
            else:
                self.espera()  

    def cocinar(self):
        with self.monitor:
            while not Ordenes.empty():
                if not cocinero.full():
                    Ordenes.get(self.id)
                    print("Cocinero trbajando en la orden del comensal "+str(self.id+1))
                    time.sleep(3)
                    cocinero.put(self.id)
                    self.monitor.wait()
                    self.entregar()
                else:
                    self.ordenar()
                    self.espera()   


    def ordenar(self):
        cant = float(10)
        waiter = int(cant * colaRes2.maxsize/100)
        waiters = queue.Queue(maxsize=waiter)
        with self.monitor:
            while not colaRes2.empty():
                if not Ordenes.full():
                    colaRes2.get(self.id)
                    for i in range(waiters.maxsize):
                        print("Mesero tomando la orden del comensal "+str(self.id+1))
                        time.sleep(3)
                        Ordenes.put(self.id)
                        self.monitor.notify()
                        self.cocinar()
                else:
                    self.cocinar()      

    def atencion(self):
        while  not colaM.empty():
            if not colaRes2.full():     
                colaM.get(self.id)
                print("atencion comensal:" + str(self.id+1))
                time.sleep(3)
                colaRes2.put(self.id)
                print("Comensal: " +str(self.id+1)+ " ha entrado al restaurante")
                time.sleep(4)
                self.ordenar()
                self.monitor.notify()
                    
            else:
                self.reservar()
                self.ordenar()
    
    def ingreso(self):
        if not colaM.full():
            colaM.put(self.id)
            print("Un nuevo comensal ha ingresado: " + str(self.id+1))
            self.atencion()
            self.reserva()
        else:
            self.espera()
            self.reserva()
    def run(self):
        self.ingreso()
        self.reservar()
        self.atencion()
        self.ordenar()
        self.cocinar()
        self.entregar()

monitoreo = threading.Condition()           
recepcionista = [1]   

def main():
    personas = []

    for col in range(COMENSALES):
        personas.append(Restaurant(col,monitoreo))

    for per in personas:
        per.start()
    
    for per in personas:
        per.join()
        
    
    print("Los comensales estan satisfechos, el trabajo esta hecho")

if __name__ == "__main__":
    main()