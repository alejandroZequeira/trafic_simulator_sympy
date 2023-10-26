import pakage 

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
        self.index=0
        self.meets_Quos=0
        self.processed_packages=1
        self.queue_now=[]

    def enviando(self,pkt,id,time):
       # print("id es",id)
        temp_pkt= pkt.pakage_with_json(id)
        #print(temp_pkt)
        #print("paquete llamado",temp_pkt['paked_size'])
        isok=((temp_pkt['paked_size']*8) + self.queue_occupation )
        if isok <= self.service_queue_size or self.service_queue_size==-1:
            #print("se envio un paquete...")
            self.queue_now.append({
                "size":(temp_pkt['paked_size']*8),
                "id_pkt":temp_pkt['id_pkt']
            })
            self.queue_occupation +=(temp_pkt["paked_size"]*8)
        else:
            #print("se perdio paquete")
            pkt.update_pakage(temp_pkt["id_pkt"],time,0,"lost")
    
    def transmitir(self,pkt,env):
        v=self.link_speed
        while True:
            if len(pkt.get_pakages())>0 and len(self.queue_now)>0:
                if self.queue_now[0]['size']>0:
                    if self.queue_now[0]["size"]-v<0:
                        self.queue_occupation-=self.queue_now[0]["size"]
                        self.queue_now[0]["size"]=0
                    else:
                        self.queue_occupation-=(self.queue_now[0]["size"]-v)
                        self.queue_now[0]["size"]-=v
                    if self.queue_occupation<0:
                        self.queue_occupation=0
                    yield env.timeout(1/60)
                else:
                    temp=pakage.pakage.pakage_with_json(self.queue_now[0]["id_pkt"])
                    #self.queue_occupation-=(temp['paked_size']*8000)
                    waiting=env.now - temp["started_time"]
                    pakage.pakage.update_pakage(self.queue_now[0]["id_pkt"],env.now,waiting,"sent")
                    self.index=self.queue_now[0]["id_pkt"]
                    self.queue_now.pop(0)
                    
                    yield env.timeout(1/60000)
            else:
                yield env.timeout(1/60000)
    def transmitir_v2(self,pkt,env):
        while True:
           # print(len(pkt.get_pakages()),"tamaño de la los paquetes en transmitir")
            if len(pkt.get_pakages())>0 and len(self.queue_now)>0:
                    yield env.timeout( self.queue_now[0]['size']/ self.link_speed)
                    temp=pkt.pakage_with_json(self.queue_now[0]["id_pkt"])
                    waiting=env.now - temp["started_time"]
                    if waiting<=self.Quos:
                        self.meets_Quos+=1
                    pkt.update_pakage(self.queue_now[0]["id_pkt"],env.now,waiting,"sent")
                    self.index=self.queue_now[0]["id_pkt"]
                    self.queue_occupation-=self.queue_now[0]['size']
                    self.queue_now.pop(0)
                    self.processed_packages+=1
            #        print("se envio un paquete")
                    #yield env.timeout(1/60000)
            else:
                yield env.timeout(1/60000)
    def get_Quos(self):
        print("paquetes que cumplieron", self.meets_Quos)
        return (self.meets_Quos*100)/self.processed_packages
    
    def terminar(self,pkt):
        for i in range(self.index+1,len(self.queue_now)):
            pkt_anterior=pkt.pakage_with_json(i-1)
            pkt_actual=pkt.pakage_with_json(i)
            if self.service_queue_size==-1:
                finish_time=0#pkt_anterior["finish_time"]+((pkt_actual["paked_size"]*8)/self.link_speed)
                waiting_time=0#finish_time-pkt_actual["started_time"]
                pkt.update_pakage(i,finish_time,waiting_time,"in_queue")
            else:
                waiting_time=pkt_anterior["finish_time"]-pkt_actual["started_time"]
                finish_time=waiting_time+((pkt_actual["paked_size"]*8)/self.link_speed)
                pkt.update_pakage(i,finish_time,waiting_time,"in_queue")                
        #print("ultimo tiempo de espera de la simulacion: ",pakage.pakage.pakage_with_json(self.index))
        #print("total de paquetes generados",len(pakage.pakage.get_pakages()))