import math
import numpy as np
class Neurona_final:
    def __init__(self,pesos):
        self.pesos=pesos
        self.lr=0.5
    
    def obtener_salida(self,entradas):
        prod_escalar=np.dot(self.pesos,entradas)
        salida_real=self.sigmoidea(prod_escalar)
        return salida_real
    
    def obtener_error(self,salida_ideal,salida_obtenida):
        error=salida_ideal-salida_obtenida
        return error
    
    def obtener_delta_final(self,salida_obtenida,error):
        delta_final=salida_obtenida*(1-salida_obtenida)*error
        return delta_final
        
    def variacion_pesos(self,entrada,delta_final):
        variacion=self.lr*delta_final*entrada
        return variacion
    
    def calcular_nuevos_pesos(self,variaciones):
        for i in range(len(self.pesos)):
            self.pesos[i]=self.pesos[i]+variaciones[i]
    
    def sigmoidea(self,prod_escalar):
        sig = 1 / (1 + math.exp(-prod_escalar))
        return sig