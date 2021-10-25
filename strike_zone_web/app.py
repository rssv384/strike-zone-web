from flask import Flask, render_template, request
import cv2
import strikezone

app = Flask(__name__)

lanzador = strikezone.Lanzador()

@app.route('/', methods=['GET','POST'])
def index():
    image = cv2.imread('./static/images/strike_zone.png')
    terminar = False
    if request.method == 'POST':
        valor = request.form['btn']
        if(valor == "Lanzar"):
            tipo_lanzamiento = lanzador.lanzar_web(image)
            #image = cv2.imread('lanzamiento.png')
            if (lanzador.lanzamientos["Strike"] == 3 or lanzador.lanzamientos["Bola"] == 4 or lanzador.lanzamientos["Golpe"] == 1 or lanzador.lanzamientos["Wild Pitch"] == 1):
                terminar = True
            return render_template('index.html', imagen='./lanzamiento.png', tipo_lanz=tipo_lanzamiento, finJuego=terminar)
        else:
            lanzador.limpiar_lanzamientos(image)
            return render_template('index.html', imagen='/static/images/strike_zone.png', tipo_lanz=None)
    else:
        return render_template('index.html', imagen='/static/images/strike_zone.png', tipo_lanz=None)
