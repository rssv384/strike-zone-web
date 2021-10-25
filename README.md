# strike-zone-web
Programa en Python que imita el lanzamiento de pelotas de beisbol a la imagen de un bateador en el plato de home utilizando Flask para mostrar el juego en un navegador.

Para jugar, es necesario activar el programa desde la consola
  set FLASK_APP=app.py
  flask run
para luego acceder al navegador en la dirección http://127.0.0.1:5000/ y jugar ahí.

Se debe especificar un área como zona de strike, un área como zona de 'bolas' y otra zona de 'golpe'. Estas áreas están delimitadas claramente en la imagen proporcionada.

La idea principal es hacer lanzamientos continuos como en un juego de beisbol. Cada lanzamiento se hace al azar y se determina qué fue lo que se lanzó dependiendo del área en la que cae la pelota. Es necesario dibujar en la imagen un círculo en las coordenadas donde cayó la peltora. El juego termina cuando ocurra lo primero de 3 cosas:
  - 3 strikes
  - 4 bolas
  - 1 golpe

Cuenta con un botón que invita a realizar el siguiente lanzamiento, uno que reinicia el juego y uno para salir.

Programa desarollado como parte de la clase de Desarrollo de Sistemas IV en la Universidad de Sonora.
