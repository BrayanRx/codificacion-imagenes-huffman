import cv2
import numpy as np
class pixel:
    def __init__(self, frec, R, G, B):
        self.R = R
        self.G = G
        self.B = B
        self.frecuencia = frec
        self.izquierda = None
        self.derecha = None

    #private:
    def __inorden_recursivo(self, pixel):
        if pixel is not None:
            self.__inorden_recursivo(pixel.izquierda)
            print(f"[{pixel.R} {pixel.G} {pixel.B}]", end=" ")
            self.__inorden_recursivo(pixel.derecha)
            
    #public:
    def iguales(self, pixel):
        if self.R == pixel.R and self.G == pixel.G and self.B == pixel.B:
            return True
        return False
        
    def inorden(self):
        print("Imprimiendo árbol inorden: ")
        self.__inorden_recursivo(self)
        print("")

nombre = input("Ingrese el nombre del archivo codificado (sin extensión):\n > ")
f = open("Imagenes-codificadas/" + nombre + ".txt","r")
L=f.read().split("-")
f.close()
L[0]=L[0].split(",")
rows = int(L[0][0])
cols = int(L[0][1])

lista = []
for k in L[1].split(";"):
    q = k.split(",")
    lista.append(pixel(int(q[0]),int(q[1]),int(q[2]),int(q[3])))

while(len(lista)>1):
    nodo = pixel(lista[0].frecuencia+lista[1].frecuencia, -1,-1,-1)
    nodo.izquierda = lista[0]
    nodo.derecha = lista[1]
    lista.pop(0)
    #insercion del nuevo nodo
    for i in range(len(lista)):
        if i==len(lista)-1:
            lista[i] = nodo
            break
        if lista[i+1].frecuencia < nodo.frecuencia:
            lista[i] = lista[i+1]
        else:
            lista[i] = nodo
            break

raiz = lista[0]

channels = 3  # 3 canales de color para RGB
image = np.zeros((rows, cols, channels), dtype=np.uint8)

n = 0
for i in range(rows):
    for j in range(cols):
        p = raiz
        while p.R==-1:
            if L[2][n] == "0":
                p = p.izquierda
            elif L[2][n] == "1":
                p = p.derecha
            n+=1
        blue = p.B
        green = p.G
        red = p.R
        # Asignar los valores de los canales de color al píxel
        image[i, j] = (blue, green, red)

# Mostrar la imagen
nombrefinal = nombre[:-3] + "dec.png" 
cv2.imwrite("Imagenes-decodificadas/" + nombrefinal, image)
print("Imagen decodificada...")
cv2.waitKey(0)
cv2.destroyAllWindows()