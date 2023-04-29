import multiprocessing
import json

class LoginProcess(multiprocessing.Process):
    def __init__(self, user, passw):
        multiprocessing.Process.__init__(self)
        self.user = user
        self.passw = passw

    def run(self):
        with open('users.json') as users:
            data = json.load(users)
            for clave, valor in data.items():
                if clave == self.user and valor == self.passw:
                    return True
            return False
        
# if __name__=="__main__":
#     process_log=LoginProcess("juanchi","123")