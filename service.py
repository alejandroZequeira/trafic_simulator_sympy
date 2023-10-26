import pakage 
pkt=pakage.pakage()

class red:
    global queue_now
    link_speed=0
    service_queue_size=0
    queue_now=[]
    queue_occupation=0
    index=0
    Quos=0
    meets_Quos=0
    processed_packages=0
    
    def __init__(self,link_speed,service_queue_size,Quos):
        self.link_speed=link_speed*1000
        self.service_queue_size=service_queue_size
        self.queue_occupation=0
        self.Quos=Quos

    def enviando(self,id,time):
       # print("id es",id)
        temp_pkt= pakage.pakage.pakage_with_json(id)
        #print("paquete llamado",temp_pkt['paked_size'])
        isok=((temp_pkt['paked_size']*8) + self.queue_occupation )
        if isok <= self.service_queue_size or self.service_queue_size==-1:
           # print("se envio un paquete...")
            queue_now.append({
                "size":(temp_pkt['paked_size']*8),
                "id_pkt":temp_pkt['id_pkt']
            })
            self.queue_occupation +=(temp_pkt["paked_size"]*8)
        else:
            #print("se perdio paquete")
            pakage.pakage.update_pakage(temp_pkt["id_pkt"],time,0,"lost")
    
    def transmitir(self,env):
        v=self.link_speed
        while True:
            if len(pakage.pakages)>0 and len(queue_now)>0:
                if queue_now[0]['size']>0:
                    #print("velocidad de enlace:",self.link_speed)
                    if queue_now[0]["size"]-v<0:
                        self.queue_occupation-=queue_now[0]["size"]
                        queue_now[0]["size"]=0
                    else:
                        self.queue_occupation-=(queue_now[0]["size"]-v)
                        queue_now[0]["size"]-=v
                    if self.queue_occupation<0:
                        self.queue_occupation=0
                    yield env.timeout(1/60)
                else:
                    temp=pakage.pakage.pakage_with_json(queue_now[0]["id_pkt"])
                    #self.queue_occupation-=(temp['paked_size']*8000)
                    waiting=env.now - temp["started_time"]
                    pakage.pakage.update_pakage(queue_now[0]["id_pkt"],env.now,waiting,"sent")
                    self.index=queue_now[0]["id_pkt"]
                    queue_now.pop(0)
                    
                    yield env.timeout(1/60000)
            else:
                yield env.timeout(1/60000)
    
    def terminar(self):
        for i in range(self.index+1,len(queue_now)):
            pkt_anterior=pakage.pakage.pakage_with_json(i-1)
            pkt_actual=pakage.pakage.pakage_with_json(i)
            if self.service_queue_size==-1:
                finish_time=pkt_anterior["finish_time"]+((pkt_actual["paked_size"]*8)/self.link_speed)
                waiting_time=finish_time-pkt_actual["started_time"]
                pakage.pakage.update_pakage(i,finish_time,waiting_time,"in_queue")
            else:
                waiting_time=pkt_anterior["finish_time"]-pkt_actual["started_time"]
                finish_time=waiting_time+((pkt_actual["paked_size"]*8)/self.link_speed)
                pakage.pakage.update_pakage(i,finish_time,waiting_time,"in_queue")                
        print("ultimo tiempo de espera de la simulacion: ",pakage.pakage.pakage_with_json(self.index))
        print("total de paquetes generados",len(pakage.pakage.get_pakages()))