import cv2

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

nombre = input("Ingrese el nombre de la imagen (sin extensión): ")

image = cv2.imread("Imagenes-a-codificar/" + nombre + ".png")

if image is None:
    print("No se pudo cargar la imagen")
    exit()

rows, cols, channels = image.shape
lista = []
def agregar(A, px):
    for i in range(len(A)):
        if A[i].R==px.R and A[i].G==px.G and A[i].B==px.B:
            A[i].frecuencia += 1
            return
    A.append(px)

print("Leyendo imagen...")

for i in range(rows):
    for j in range(cols):
        # Obtener el valor del píxel en la posición (i, j)
        p = image[i, j]
        # Acceder a los canales de color del píxel (B, G, R)
        blue = p[0]
        green = p[1]
        red = p[2]

        px = pixel(1, red, green, blue)
        agregar(lista, px)

def ordlistap(A):
    for i in range(len(A)-1):
        for j in range(i+1, len(A)):
            if A[i].frecuencia > A[j].frecuencia:
                aux = A[i]
                A[i] = A[j]
                A[j] = aux
ordlistap(lista)

#copiar los pixeles en otra lista para escribirla
listacop = []
for k in lista:
    listacop.append(k)

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

def buscar_codigo(raiz, el):
    if raiz is None:
        return None

    if raiz.R==el.R and raiz.G==el.G and raiz.B==el.B:
        return ""
    codigo_izquierda = buscar_codigo(raiz.izquierda, el)
    if codigo_izquierda is not None:
        return "0" + codigo_izquierda

    codigo_derecha = buscar_codigo(raiz.derecha, el)
    if codigo_derecha is not None:
        return "1" + codigo_derecha
    return None

#raiz.inorden()
#una vez construido el árbol, se codifica la imágen en una archivo de texto:
print("Codificando imagen...")
nombrefinal = nombre + "-cod.txt"
f = open("Imagenes-codificadas/" + nombrefinal, "w")
f.write(f"{rows},{cols}-")
for i in range(len(listacop)):
    if i==len(listacop)-1:
        f.write(f"{listacop[i].frecuencia},{listacop[i].R},{listacop[i].G},{listacop[i].B}")
        break
    f.write(f"{listacop[i].frecuencia},{listacop[i].R},{listacop[i].G},{listacop[i].B};")
f.write("-")
for i in range(rows):
    print(f"{int((i/rows)*100)}%")
    for j in range(cols):
        p = image[i, j]
        blue = p[0]
        green = p[1]
        red = p[2]
        px = pixel(1, red, green, blue)
        f.write(buscar_codigo(raiz,px))
f.close()
print("Imagen codificada...")