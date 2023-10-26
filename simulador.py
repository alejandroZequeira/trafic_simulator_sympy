import simpy
import numpy as np
import service as sv
import pakage as pk
import matplotlib.pyplot as plt
import graficador as graf
global time_on, time_off, media,simulation_time,id_pkt ,service,pakage,inter_arrival_time,Quos
id_pkt=0
simulation_time=30 #min
media=3
Quos=20/60000
link_speed=2000 # kbits/seg
service_queue_size= 44000 #bits
inter_arrival_time=20/60000
#inicializar servicios
service=sv.red(link_speed=link_speed,service_queue_size=service_queue_size,Quos=Quos)
pakage=pk.pakage()
#times
np.random.seed(300)
stats_on_off_x=[]
stats_on_off_y=[]
class on_state:
    def generate_pkt(env,time_on):
        global id_pkt,inter_arrival_time
        #print("entro en on")
        while env.now < time_on:
            if env.now+inter_arrival_time<=time_on:
                #print("tiempo ahora:",env.now," tiempo de simulacion:",time_on)
                pakage.set_pakage(id_pakage=id_pkt,paked_size=generate_size(),started_time=env.now)
                service.enviando(id_pkt,time=env.now)
                id_pkt+=1
            yield env.timeout(inter_arrival_time)
            


def generate_size():
    size=np.random.uniform(1,40,1)
    return size[0]

def generate_time_exp():
    time=np.random.exponential(1/media,1)
    return time[0]

def states(env):
    while True:
        print("tiempo actual",env.now)
        stats_on_off_x.append(env.now)
        stats_on_off_y.append(4)
        time_on=env.now+generate_time_exp()
        if time_on<=simulation_time:
            print("entro en on",env.now)
            yield env.process(on_state.generate_pkt(env,time_on))
            stats_on_off_x.append(env.now)
            stats_on_off_y.append(4)
        stats_on_off_x.append(env.now)
        stats_on_off_y.append(1)
        print("cambio de estado estado off",env.now)
        time_off=generate_time_exp()
        yield env.timeout(time_off)
        stats_on_off_x.append(env.now)
        stats_on_off_y.append(1)

if __name__=='__main__':
    env=simpy.Environment()
    
    env.process(states(env))
    env.process(service.transmitir(env))
    env.run(until=simulation_time)
    service.terminar()
    plt.figure()
    plt.plot(stats_on_off_x,stats_on_off_y)
    plt.xlabel("tiempo(seg)")
    plt.ylabel("estados On/Off")
    plt.show()
    print("taza media ", (pakage.get_throuput()*1000)/(simulation_time*60))
    graf.queue_waiting_time_graph(pk.pakage.get_pakages())
    graf.queue_lost_or_sent_pakage_graph(pk.pakage.get_pakages())