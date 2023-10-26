import matplotlib.pyplot as plt
import numpy as np
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
    ##plt.show()

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
    ##plt.show()

def get_stats(objeto):
    sent=0
    lost=0
    queue=0
    for p in objeto:
        if p["status_of_pakage"]=="sent":
            sent+=1
        elif p["status_of_pakage"]=="lost":
            lost+=1
        elif p["status_of_pakage"]=="in_queue":
            queue+=1
    return {"sent":sent,"lost":lost,"in_queue":queue}

def lost_or_sent_graph(objeto,Quos,link_speed,service_queue_size):
    colores = ["#00ba38", "#f8766d","#619cff"]
    valores_sent = [item["network_statistics"]["sent"] for item in objeto]
    valores_lost = [item["network_statistics"]["lost"] for item in objeto]
    valores_in_queue = [item["network_statistics"]["in_queue"] for item in objeto]
    etiquetas = [f"{i+1}" for i in range(len(objeto))]
    x = range(len(objeto))
    ancho_barra = 0.2
    plt.bar(x, valores_sent, width=ancho_barra, color=colores[0], label="sent")
    plt.bar([i + ancho_barra for i in x], valores_lost, width=ancho_barra, color=colores[1], label="lost")
    plt.bar([i + 2 * ancho_barra for i in x], valores_in_queue, width=ancho_barra, color=colores[2], label="in_queue")
    plt.xlabel("test number")
    plt.ylabel("Values")
    plt.title("Bar Charts to see the values of sent, lost or queued packets")
    plt.xticks([i + ancho_barra for i in x], etiquetas, rotation=90 ,ha="center" )
    plt.legend()
    plt.tight_layout()
    plt.savefig('pakage_sent_lost_in_queue_Quos'+Quos+'_link_speed_'+link_speed+'_Queue_'+service_queue_size+'.jpg',dpi=600)
    ##plt.show()
    plt.close()

def throuput_graf(objeto,Quos,link_speed,service_queue_size,media,mediana,desviacion_std):
    valores = [item["M"] for item in objeto]
    etiquetas = [f"{i+1}" for i in range(len(objeto))]
    x = range(1, len(valores) + 1)
    plt.figure(figsize=(12,8))
    plt.plot(etiquetas, valores, marker='o', linestyle='-', color='b')
    for i, valor in enumerate(valores):
        plt.text(x[i], valor, '{:.2f}'.format(valores[i]), fontsize=10,  ha="center" , va='bottom')
    plt.xlabel('number of test')
    plt.ylabel('value of the average transmission rate')
    plt.title('graph of the variation of the average transmission rate')
    plt.grid(True)
    leyenda = [
        ' (Desviación Estándar: {:.2f}, Media: {:.2f}, Mediana: {:.2f})'.format( desviacion_std, media, mediana)
    ]
    plt.legend(leyenda,loc='upper right')
   
    #plt.tight_layout() 
    plt.savefig('variation_of_the_average_transmission_rate_Quos'+Quos+'_link_speed_'+link_speed+'_Queue_'+service_queue_size+'.jpg',dpi=600)
    ##plt.show()
    plt.close()

def on_off_graph(objeto,Quos,link_speed,service_queue_size):
    colores = ["#00ba38", "#f8766d"]
    valores_on = [item["time_on"] for item in objeto]
    valores_off = [item["time_off"] for item in objeto]
    etiquetas = [f"{i+1}" for i in range(len(objeto))]
    x = range(len(objeto))
    ancho_barra = 0.2
    plt.bar(x, valores_on, width=ancho_barra, color=colores[0], label="On")
    plt.bar([i + ancho_barra for i in x], valores_off, width=ancho_barra, color=colores[1], label="Off")
    plt.xlabel("test number")
    plt.ylabel("Values")
    plt.title("Bar Graphs to see the changes of states between On and Off")
    plt.xticks([i + ancho_barra for i in x], etiquetas,  rotation=90,ha="center" )
    plt.legend()
    plt.tight_layout()
    plt.savefig('changes_of_states_between_On_and_Off_Quos'+Quos+'_link_speed_'+link_speed+'_Queue_'+service_queue_size+'.jpg',dpi=600)   
    ##plt.show()
    plt.close()
def Quos_graf(objeto,Quos,link_speed,service_queue_size):
    colores = ["#00ba38", "#f8766d"]
    valores = [item["quality_of_service"] for item in objeto]
    #valores_off = [item["time_off"] for item in objeto]
    etiquetas = [f"{i+1}" for i in range(len(objeto))]
    x = range(len(objeto))
    ancho_barra = 0.2
    plt.bar(x, valores, width=ancho_barra, color=colores[0], label="packages that met the quality of service")
    #plt.bar([i + ancho_barra for i in x], valores_off, width=ancho_barra, color=colores[1], label="Off")
    plt.xlabel("test number")
    plt.ylabel("values")
    plt.title("Bar Charts for quality of service")
    plt.xticks([i + ancho_barra for i in x], etiquetas,  rotation=90,ha="center" )
    plt.tight_layout()
    plt.legend()
     
    plt.savefig('quality_of_service_Quos'+Quos+'_link_speed_'+link_speed+'_Queue_'+service_queue_size+'.jpg',dpi=600)   
    ##plt.show()
    plt.close()