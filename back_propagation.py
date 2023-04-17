from neurona_final import Neurona_final
from neuronas_ocultas import Neurona_oculta
import concurrent.futures
import random
import cv2
import multiprocessing

class Back_Propagation():
    
    def __init__(self,entradas,salidas):
        self.entradas=entradas
        self.salidas=salidas
    
    def main(self):
        cant_neuronas=int(input("Cantidad de neuronas: "))
        iteraciones=int(input("Iteraciones: "))
        neuronas=[]
        # instanciamos neuronas
        for i in range(cant_neuronas):
            pesos_neuronales=[]
            for j in range(len(self.entradas[0])):
                peso_random=random.uniform(-0.001,0.001)
                pesos_neuronales.append(peso_random)
            n=Neurona_oculta(pesos_neuronales)
            neuronas.append(n)
            pesos_finales=[]
        #  instanciamos neurona final   
        for j in range(len(neuronas)+1):
            peso_random=random.random()
            pesos_finales.append(peso_random)
        nf=Neurona_final(pesos_finales)
        errores=[]
        salidas_red=[]
        # comienza la itereacion
        def iterar():
            for iteracion in range(iteraciones):
                for i in range(len(self.entradas)):
                    salidas_ocultas=[]
                    for neurona in neuronas:
                        salida_oculta=neurona.obtener_salida(self.entradas[i])
                        salidas_ocultas.append(salida_oculta)
                    # agregamos bias final
                    salidas_ocultas.append(1)
                    # recalculamos pesos finales
                    salida_red=nf.obtener_salida(salidas_ocultas)
                    salidas_red.append(salida_red)
                    error_red=nf.obtener_error(self.salidas[i],salida_red)
                    errores.append(error_red)
                    delta_final=nf.obtener_delta_final(salida_red,error_red)
                    variaciones=[]
                    for salida in salidas_ocultas:
                        variacion=nf.variacion_pesos(salida,delta_final)
                        variaciones.append(variacion)
                    
                    nf.calcular_nuevos_pesos(variaciones)
                    # recalculamos pesos ocultos
                    variaciones=[]
                    for neurona in neuronas:
                        salida=neurona.obtener_salida(self.entradas[i])
                        delta_oculto=neurona.obtener_delta_oculto(salida,delta_final)
                        for entrada in self.entradas[i]:
                            variacion=neurona.variacion_pesos(entrada,delta_oculto)
                            variaciones.append(variacion)
                        neurona.calcular_nuevos_pesos(variaciones)
                print("Iteracion ",iteracion+1)
                print(error_red)
        
    # Paralelizamos con la mayor cantidad de hilos posibles
        cpus = multiprocessing.cpu_count()
        with concurrent.futures.ThreadPoolExecutor(max_workers=cpus) as executor:
            
            [executor.submit(iterar) for _ in range(1)]

        return [neuronas,nf]
    
    # metodo para procesar la imagen y pasarla para su devolucion
    def foto(self,foto,neuronas,pixeles_fotos):
            image = cv2.imread(foto)
            pixeles=[]
            for alto in image:
                for ancho in alto:
                    pixeles.append(ancho[0])
            pixeles.append(1)
            pixeles_fotos.append(pixeles)
    
            salidas=[]
            for neurona in neuronas[0]:
                salida=neurona.obtener_salida(pixeles)
                salidas.append(salida)
            salidas.append(1)
            salida_final=neuronas[1].obtener_salida(salidas)
            if round(salida_final)==1:
                return "Persona 1"
            else:
                return "Persona 2"

