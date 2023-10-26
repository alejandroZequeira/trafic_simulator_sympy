import matplotlib.pyplot as plt
def queue_waiting_time_graph(objeto):
    argY=[]
    argx=[]
    for p in objeto:
        if p["status_of_pakage"]=="sent":
            argY.append(p['service_waiting_time'])
        #argY.append(p["finish_time"])
            argx.append(p["started_time"])
       # print("tiempo de espera de cada paquete",p['service_waiting_time'])
    plt.figure()
    plt.plot(argx,argY)
    plt.xlabel("tiempo de creacion(min)")
    plt.ylabel("tiempo espera(min)")
    plt.show()

def queue_lost_or_sent_pakage_graph(objeto):
    
    sent=0
    lost=0
    queue=0
    colores = ["#00ba38", "#f8766d","#619cff"]
    for p in objeto:
        if p["status_of_pakage"]=="sent":
            sent+=1
        elif p["status_of_pakage"]=="lost":
            lost+=1
        elif p["status_of_pakage"]=="in_queue":
            queue+=1
       # print("tiempo de espera de cada paquete",p['service_waiting_time'])
    plt.figure()
    plt.bar(x=["sent","lost","in queue"],height=[sent,lost,queue],color=colores)
    #plt.xlabel("tiempo de creacion(min)")
    plt.ylabel("pakages")
    plt.show()