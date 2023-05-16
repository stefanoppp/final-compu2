import multiprocessing
import json
class LoginProcess(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)

    def run(self,user,passw):
        
        with open('users.json') as users:
            data = json.load(users)
            for clave, valor in data.items():
                if clave == user and valor == passw:
                    return True
            return False
        
process_log=LoginProcess()        

def main_log_process(user,passw):
    return process_log.run(user,passw)