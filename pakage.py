import json 
class pakage:
    global pakages
    paked_size=0
    id_pkt=0
    started_time=0
    finish_time=0
    service_waiting_time=0
    status_of_pakage=""
    pakages=[]
    throuput=0
    def __init__(self):
        self.paked_size=0
        self.id_pkt=0
        self.started_time=0
        self.finish_time=0
        self.service_waiting_time=0
        self.status_of_pakage=""
        self.pakages=[]
        self.throuput=0
    def set_pakage(self,id_pakage,paked_size,started_time):
       # print("se creo paquete")
        self.throuput+=paked_size
        self.pakages.append({"id_pkt":id_pakage,
                        "paked_size":paked_size,
                        "started_time":started_time,
                        "finish_time":0,
                        "service_waiting_time":0,
                        "status_of_pakage":""})
        
    def pakage_with_json( self,index ):
        #print("entro a get pakage la id es: ",index)
        for pkt in self.pakages:
            if pkt["id_pkt"]==index:
                return pkt
    
    def get_pakages(self):
        return self.pakages
    
    def get_throuput(self):
        return self.throuput

        
    def update_pakage(self,id_pkt,finish_time,service_waiting_time,status_of_pakage):
        for pkt in self.pakages:
            if pkt["id_pkt"]==id_pkt:
                pkt["finish_time"]=finish_time
                pkt["status_of_pakage"]=status_of_pakage
                pkt["service_waiting_time"]=service_waiting_time
                break
            
