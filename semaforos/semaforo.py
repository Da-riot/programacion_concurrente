from threading import Thread, Semaphore
import final
from pytube import YouTube

semaforo = Semaphore(1) #Crea la variable semáforo


def download_video(id):
    global x;
    urls_video = ["https://www.youtube.com/watch?v=bp_IXqYRgYw"]
    destino = ("C:/Users/Dario/Documents/concurrente/videos")
    x = x + id
    print("Hilo =" +str(id)+ " =>" +str(x))
    x=1
    for link in urls_video:
      yt = YouTube(link)
      video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first() 
      save_video(video,destino)


def save_video(video,destino):    
    video.download(destino)
    print("El video ha sido descargado en la ruta: "+destino)

class Hilo(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id=id
    
    def run(self):
        semaforo.acquire() #inicializa el semaforo, lo adquiere
        download_video(self.id)
        semaforo.release() #libera un semáforo e incrementa la variable semáforo

threads_semafore = [Hilo(1),Hilo(2),Hilo(3)]
x=1;
for t in threads_semafore:
    t.start()