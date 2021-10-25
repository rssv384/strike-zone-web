import cv2
import skimage.viewer
import enum
import os
import random

class Graficas(enum.Enum):
    cv2 = 0
    skimg = 1

class Tipo(enum.Enum):
    Sin_lanzar = 0
    Bola   = 1
    Strike = 2
    Golpe  = 3
    Wild_Pitch = 4

class Punto:
    x = None
    y = None
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

class Pelota:
    diametro = None
    color = None
    tipo  = None 
    x     = None
    y     = None
    def __init__(self,x,y) -> None:
        self.diametro = 15
        self.color    = 45
        self.x        = x
        self.y        = y
        self.tipo     = Tipo.Sin_lanzar

class Lanzador:
    xmin = None
    xmax = None
    ymin = None
    ymax = None
    lanzamientos = None
    def __init__(self) -> None:
        self.xmin = 20
        self.xmax = 620
        self.ymin = 0
        self.ymax = 528
        self.lanzamientos = {"Strike":0, "Bola":0, "Golpe":0, "Wild Pitch":0}
    
    def lanzar(self):
        # Obtener lac oordenadas del lanzamiento
        eje_x, eje_y = self.obtener_coords()
        # Crear la Pelota lanzada
        bola = Pelota(eje_x,eje_y)
        # Obtener tipo de lanzamiento
        tipo_lanzamiento = self.obtener_tipo_lanzamiento(bola)
        # Actualizar el diccionario de tipos de lanzamiento
        self.lanzamientos[tipo_lanzamiento] += 1
        # Ajustar los limites del área de lanzamiento del lanzador
        self.mejorar_punteria(eje_x,eje_y)
        print(self.lanzamientos)
        return bola, tipo_lanzamiento
        
    def obtener_coords(self) -> int:
        return random.randint(self.xmin, self.xmax), random.randint(self.ymin, self.ymax)
    
    def obtener_tipo_lanzamiento(self, a:Pelota) -> str:
        SZ = {"ESI":Punto(315,170), "ESD":Punto(415,170), "EII":Punto(315,360), "EID":Punto(415,360)} # Zona de Strike (Strike Zone)
        BZ = {"ESI":Punto(230,120), "ESD":Punto(555,120), "EII":Punto(230,475), "EID":Punto(555,360)} # Zona de Bola (Ball Zone)
        HBZ = {"ESI":Punto(35,40), "ESD":Punto(210,40), "EII":Punto(35,480), "EID":Punto(210,480)}    # Zona de Golpe al Bateador (Hit the Batter Zone)

        if (a.x >= SZ["ESI"].x and a.x <= SZ["EID"].x and a.y >= SZ["ESI"].y and a.y <= SZ["EII"].y):   # Límites de la zona de strike
            a.color = 50
            a.tipo = Tipo.Strike
            print("Strike!")
            return "Strike"
        elif (a.x >= BZ["ESI"].x and a.x <= BZ["EID"].x and a.y >= BZ["ESI"].y and a.y <= BZ["EII"].y): # Límites de la zona de bola
            a.color = 100
            a.tipo = Tipo.Bola
            print("Bola!")
            return "Bola"
        elif (a.x >= HBZ["ESI"].x and a.x <= HBZ["EID"].x and a.y >= HBZ["ESI"].y and a.y <= HBZ["EII"].y): # Límites de la zona de golpe al bateado
            a.color = 125
            a.tipo = Tipo.Golpe
            print("Golpe al bateador!")
            return "Golpe"
        else:
            a.color = 150
            a.tipo = Tipo.Wild_Pitch
            print("Wild Pitch!")
            return "Wild Pitch"
    
    def mejorar_punteria(self,tiro_x,tiro_y):
        SZ = {"ESI":Punto(315,170), "ESD":Punto(415,170), "EII":Punto(315,360), "EID":Punto(415,360)}
        if (tiro_x <= SZ["ESI"].x):
            self.xmin = tiro_x       # Acercar a la SZ el límite inferior en el eje X del área de lanzamiento
        else:
            self.xmax = tiro_x       # Acercar a la SZ el límite superior en el eje X del área de lanzamiento
        
        if (tiro_y <= SZ["ESD"].y):
            self.ymin = tiro_y       # Acercar a la SZ el límite inferior en el eje Y del área de lanzamiento
        else:
            self.ymax = tiro_y       # Acercar a la SZ el límite superior en el eje Y del área de lanzamiento
    
    def dibujar_lanzamiento(self,image,bola):
        # Red color in BGR
        color = (255, bola.color, 50)
        # Line thickness of -1 px
        thickness = -1
        # Using cv2.circle() method
        # Draw a circle of red color of thickness -1 px
        img = cv2.circle(image, (bola.x,bola.y), bola.diametro, color, thickness)
        cv2.imwrite('lanzamiento.png', img)
    
    def lanzar_web(self, imagen):
        bola, tipo = self.lanzar()
        self.dibujar_lanzamiento(imagen, bola)
        return tipo
    
    def limpiar_lanzamientos(self,imagen):
        self.xmin = 20
        self.xmax = 620
        self.ymin = 0
        self.ymax = 528
        for key,value in self.lanzamientos.items():
            self.lanzamientos[key] = 0        

def dibujar_imagen(image,grafica,lista_bolas):
    if grafica == Graficas.skimg:
        for bola in lista_bolas:
            r,c = skimage.draw.disk((bola.y,bola.x),bola.diametro)
            image[r,c] = bola.color
        viewer = skimage.viewer.ImageViewer(image)
        viewer.show() 
    else:
        for bola in lista_bolas:
            # Red color in BGR
            color = (255, bola.color, 50)
            # Line thickness of -1 px
            thickness = -1
            # Using cv2.circle() method
            # Draw a circle of red color of thickness -1 px
            image = cv2.circle(image, (bola.x,bola.y), bola.diametro, color, thickness)
        cv2.imshow('image',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main(image,GRAFICAS):
    xmin = 20
    xmax = 620
    ymin = 0
    ymax = 528
    eje_x,eje_y = obtener_coords(xmin,xmax,ymin,ymax)
    a = Pelota(eje_x,eje_y)
    lanzamientos = {"Strike":0, "Bola":0, "Golpe":0, "Wild Pitch":0}
    orden_lanzamientos = []
    enJuego = True
    while (enJuego == True):
        orden_lanzamientos.append(a)
        tipo_lanzamiento = obtener_tipo_lanzamiento(a)
        lanzamientos[tipo_lanzamiento] += 1
        if (lanzamientos["Strike"] == 3 or lanzamientos["Bola"] == 4 or lanzamientos["Golpe"] == 1 or lanzamientos["Wild Pitch"] == 1):
            enJuego = False
        else:
            xmin,xmax,ymin,ymax = mejorar_punteria(eje_x,eje_y)
            eje_x,eje_y = obtener_coords(xmin,xmax,ymin,ymax)
            a = Pelota(eje_x,eje_y)
    dibujar_imagen(image,GRAFICAS,orden_lanzamientos)
    print(lanzamientos)


def obtener_coords(xmin,xmax,ymin,ymax) -> int:
    return random.randint(xmin,xmax), random.randint(ymin,ymax)


def mejorar_punteria(tiro_x,tiro_y):
    SZ = {"ESI":Punto(315,170), "ESD":Punto(415,170), "EII":Punto(315,360), "EID":Punto(415,360)}
    nva_xmin = 0
    nva_xmax = 620
    nva_ymin = 0
    nva_ymax = 528
    if (tiro_x <= SZ["ESI"].x):
        nva_xmin = tiro_x       # Acercar a la SZ el límite inferior en el eje X del área de lanzamiento
    else:
        nva_xmax = tiro_x       # Acercar a la SZ el límite superior en el eje X del área de lanzamiento
    
    if (tiro_y <= SZ["ESD"].y):
        nva_ymin = tiro_y       # Acercar a la SZ el límite inferior en el eje Y del área de lanzamiento
    else:
        nva_ymax = tiro_y       # Acercar a la SZ el límite superior en el eje Y del área de lanzamiento
    
    return nva_xmin,nva_xmax,nva_ymin,nva_ymax

def obtener_tipo_lanzamiento(a:Pelota) -> str:
    SZ = {"ESI":Punto(315,170), "ESD":Punto(415,170), "EII":Punto(315,360), "EID":Punto(415,360)} # Zona de Strike (Strike Zone)
    BZ = {"ESI":Punto(230,120), "ESD":Punto(555,120), "EII":Punto(230,475), "EID":Punto(555,360)} # Zona de Bola (Ball Zone)
    HBZ = {"ESI":Punto(35,40), "ESD":Punto(210,40), "EII":Punto(35,480), "EID":Punto(210,480)}    # Zona de Golpe al Bateador (Hit the Batter Zone)

    if (a.x >= SZ["ESI"].x and a.x <= SZ["EID"].x and a.y >= SZ["ESI"].y and a.y <= SZ["EII"].y):   # Límites de la zona de strike
        a.color = 50
        a.tipo = Tipo.Strike
        print("Strike!")
        return "Strike"
    elif (a.x >= BZ["ESI"].x and a.x <= BZ["EID"].x and a.y >= BZ["ESI"].y and a.y <= BZ["EII"].y): # Límites de la zona de bola
        a.color = 100
        a.tipo = Tipo.Bola
        print("Bola!")
        return "Bola"
    elif (a.x >= HBZ["ESI"].x and a.x <= HBZ["EID"].x and a.y >= HBZ["ESI"].y and a.y <= HBZ["EII"].y): # Límites de la zona de golpe al bateado
        a.color = 125
        a.tipo = Tipo.Golpe
        print("Golpe al bateador!")
        return "Golpe"
    else:
        a.color = 150
        a.tipo = Tipo.Wild_Pitch
        print("Wild Pitch!")
        return "Wild Pitch"


if __name__ == "__main__":
    #path = 'C:/Users/rsoto/desarrollo4/strike_zone'
    #strike_zone_file = os.path.join(path,"strike_zone.png")
    #print(strike_zone_file)
    strike_zone_file = './strike_zone/strike_zone.png'
    #GRAFICAS = Graficas.skimg
    GRAFICAS = Graficas.cv2
    if (GRAFICAS == Graficas.skimg):
        image = skimage.io.imread( strike_zone_file )
    else:
        image = cv2.imread(strike_zone_file)
    main(image, GRAFICAS)


'''
a = Pelota()
image = skimage.io.imread("./strike_zone.png")
r,c = skimage.draw.disk((200,300),a.diametro)
image[r,c] = a.color 
viewer = skimage.viewer.ImageViewer(image)
viewer.show()


image = cv2.imread(path)
   
# Window name in which image is displayed
window_name = 'Image'
  
# Center coordinates
center_coordinates = (120, 100)
 
# Radius of circle
radius = 30
  
# Red color in BGR
color = (0, 0, 255)
  
# Line thickness of -1 px
thickness = -1
  
# Using cv2.circle() method
# Draw a circle of red color of thickness -1 px
image = cv2.circle(image, center_coordinates, radius, color, thickness)
  
# Displaying the image 
cv2.imshow(window_name, image) 
'''