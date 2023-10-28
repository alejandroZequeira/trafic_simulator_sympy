import simulador
import merge
import graficador as graf
import numpy as np
def get_media(objeto):
    sigma=0
    for o in objeto:
        print("carga media ",o["M"])
        sigma+=o["M"]
    return sigma/len(objeto)

def get_mediana(objeto):
    array=[]
    for o in objeto:
        array.append(o["M"])
    #print ("arreglo en la mediana", array)
    merge.mergeSort(array)
    #print ("arreglo en la mediana", array)
    index=len(array)/2
    if type(index)=="int":
        return (array[index-1]+array[index])/2
    else:
        return array[int(index-1)+1]

def get_std(objeto):
    array=[]
    for o in objeto:
        array.append(o["M"])
    return np.std(array)

if __name__=="__main__":
    
    link=[20,150,200,500,1000]
    quos=[40,120,300,200]
    service_queue=["infinite","finite"]
    for p in service_queue:
        n=32
        for q in quos:
            for l in link:
                statistics=[]
            Quos=str(q)+"ms"
            link_speed=str(l)+"_kbits_seg"
            service_queue_size= p
            while True:
                for i in range(n):
                    print("simulando:", i+1," de ", n )
                    result=simulador.simular(l,q,p)
                    statistics.append(result)
                media=get_media(statistics)
                mediana=get_mediana(statistics)
                error=(media-mediana)/mediana
                if media==mediana or error <= 0.02:
                        break
                else:
                        statistics=[]
                        print("no cumplio.." )
                        n+=1
            desviacion_std=get_std(statistics)
            graf.lost_or_sent_graph(statistics,Quos,link_speed,service_queue_size)
            graf.on_off_graph(statistics,Quos,link_speed,service_queue_size)
            graf.Quos_graf(statistics,Quos,link_speed,service_queue_size)
            graf.throuput_graf(statistics,Quos,link_speed,service_queue_size,media,mediana,desviacion_std)
