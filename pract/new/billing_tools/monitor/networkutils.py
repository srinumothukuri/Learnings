import os
import requests
import traceback
import json
import pathlib
from datetime import datetime

MML_USER_NAME = "jeelani"
MML_PASSWORD = "js@yed@2016"
MML_HOST_URL ="http://10.20.30.139:8001"
SUCCESS = 'Operation is successful'
class NetworkUtil:
   
   def check_mml_login(self):
      req_body =  '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/><SOAP-ENV:Body><LGI><OPNAME>'+ MML_USER_NAME +'</OPNAME><PWD>'+ MML_PASSWORD +'</PWD></LGI></SOAP-ENV:Body></SOAP-ENV:Envelope>'
      response = requests.post(MML_HOST_URL, data = req_body)
      print(response)
      isActive = False
      if SUCCESS in response.content:
          isActive = True
      return {"isActive" : isActive }


   def check_server_ping(self, hostname):
      pingstatus = None 
      response = os.system("ping -c 1 " + hostname)
      if response == 0:
         pingstatus = "Active"
      else:
          pingstatus = "Link Failure"
      return pingstatus    

   def check_status_api(self, name, hostname, port, context, uri):
       response = requests.get("http://"+ hostname + ":" + port+ "/" + context + "/" + uri +  "/")
       resp = {'code': response.status_code}
       if (response.status_code != 200):
           print("HOST NAME " + name + " STATUS " + str(response.status_code))
           resp['status'] =   'inactive'
       else:
           print("HOST NAME " + name + " SERVICE STATUS ACTIVE " + response.json()['timeStamp'] )
           resp['status'] = 'active'
       return resp    

  
   def read_file_data(self, filename):
       file_data = {}
       with open(filename) as f:
            try:
               file_data = json.load(f)
            except:
               traceback.print_exc()
               file_data = {"status" : "Missing file :" + os.getcwd()  + filename}
       print(file_data)        
       return file_data  

   def record_service_status(self, filename):
       data = self.read_file_data(filename)
       update_status = []
       host_info = data["host_info"]
       for info in host_info:
          info['pingStatus'] = self.check_server_ping(info['address'])  
          if info['pingStatus'] == 'Active':
             info['serviceStatus'] = self.check_status_api(info['name'], info['address'],info['port'], info['context'], info['uri'])['status']
          else:    
             info['serviceStatus'] = 'Network failure'
          update_status.append(info)
       data = {'host_info' : update_status } 
    
       cur_time = datetime.utcnow().strftime('%Y-%m-%d-%H:%M:%S.%f')[:-3]    
       data["time"] = cur_time
       path = str(pathlib.Path(__file__).parent.absolute()) + "/host_status/" + "status_" + cur_time + ".txt"
       self.write_data_into_file(json.dumps(data), path)
       return {"status" : "success", "path" : "/host_status/" + "status_" + cur_time + ".txt", "host_info" : data["host_info"]}

   def write_data_into_file(self, data, path):
      f = open(path, "a")
      f.write(data)
      f.close()  


           
