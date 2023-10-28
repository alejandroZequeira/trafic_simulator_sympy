import simpy
import numpy as np
import service as sv
import pakage as pk
import time
import graficador as graf
global time_in_on,time_in_off,time_on, time_off, media,simulation_time,id_pkt ,service,pakage,inter_arrival_time,Quos

class on_state:
    def generate_pkt(env,time_on):
        global id_pkt,inter_arrival_time
        #print("entro en on")
        while env.now < time_on:
            if env.now+inter_arrival_time<=time_on:
                #print("tiempo ahora:",env.now," tiempo de simulacion:",time_on)
                pakage.set_pakage(id_pakage=id_pkt,paked_size=generate_size(),started_time=env.now)
                service.enviando(pakage,id_pkt,time=env.now)
                id_pkt+=1
            yield env.timeout(inter_arrival_time)
def generate_size():
    size=np.random.uniform(1,40,1)
    return size[0]

def generate_time_exp():
    time=np.random.exponential(1/media,1)
    return time[0]

def states(env):
    global time_in_off,time_in_on,time_on,time_off
    while True:
        time_aleatorio=generate_time_exp()
        time_on=env.now+time_aleatorio
        if time_on<=simulation_time:
            time_in_on+=time_aleatorio
            yield env.process(on_state.generate_pkt(env,time_on))
        time_off=generate_time_exp()
        time_in_off +=time_off
        yield env.timeout(time_off)

def simular(link,quos,service_queue):
    global time_in_on,time_in_off,media,simulation_time,id_pkt ,service,pakage,inter_arrival_time,Quos
    id_pkt=0
    simulation_time=30 #min
    media=3
    Quos=quos/60000
    link_speed=link # kbits/seg
    if service_queue=="infinite":
        service_queue_size= -1 #bits
    else:
        service_queue_size= 64000 #bits
    #service_queue_size= -1 #bits
    inter_arrival_time=20/60000 #milisegundos convestidos a minutos 
    #inicializar servicios
    service=sv.red(link_speed=link_speed,service_queue_size=service_queue_size,Quos=Quos)
    pakage=pk.pakage()
    #times
    #np.random.seed(10)
    time_in_on=0
    time_in_off=0
    t_initial=time.time()
    env=simpy.Environment()
    
    env.process(states(env))
    env.process(service.transmitir_v2(pakage,env))
    env.run(until=simulation_time)
    service.terminar(pakage)
    result={
        "time_on":time_in_on,
        "time_off":time_in_off,
        "M":(pakage.get_throuput())/(simulation_time*60),
        "network_statistics": graf.get_stats(pakage.get_pakages()),
        "quality_of_service": service.get_Quos()
    }
    #graf.queue_waiting_time_graph(pakage.get_pakages())
    print("taza media de la simulacion",result["M"])
    print("termino en: ",time.time()-t_initial)
    return result    