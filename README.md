# flask-project-web

# Ignacio Alveal
# Pagina juegos panamericanos

## Requisitos previos e instalación

Para correr la pagina web de una manera correcta, primero hay que realizar un ambiente virtual que tenga las librerias mencionadas en requirementes.txt, en particular en la dirección donde esta requirements.txt se escriben las siguiente lineas de codigo para crear el ambiente virtual e instalar las librerias:

`-` Creamos el ambiente virtual:

``` python -m venv flask```

`-` Activamos el ambiente virutal

``` flask\Scripts\activate``` o ``` flask\bin\activate```

`-` Instalamos las librerias de requirements.txt

```pip install -r requirements.txt```

Una vez teniendo un ambiente virtual activado con las librerias requeridas se va a la direccion donde esta app.py y se ingresa el siguiente codigo para correr la pagina web:

```python app.py```

## Cosas a tomar en cuenta

`-` En registrar artesano y registrar hincha, cuando se envia un formulario con cierta información incorrecta mediante el procedimiento normal te da una lista con los valores invalidos para que se pueda corregir (usando la validación de javascript), en el caso en que se envie el formulario mediante un procedimiento no normal (como curl) te dice los valores invalidos para que se pueda corregir (usando la validación de python), finalmente si el formulario es valido se inserta el artesano/hincha en la base de datos y se redirige a /recibido, aqui notar que /recibido es equivalente a / (/ es el index) solo que le informa al usuario que se recibio correctamente el formulario, luego cuando se hace click en ok te redirige a /.

`-` En ver lista de artesanos y lista de hinchas, hay que notar que se muestran 5 artesanos/hinchas en simultaneo mostrando desde el mas recientemente insertado al mas viejo, tambien notar que para hacer una tabla que muestre 5 elementos y se pueda avanzar y retroceder se usa en el url de la tabla (/lista-artesano/numero o /lista-hincha/numero) un numero que indica cuales 5 elementos mostrar, siendo el numero mayor o igual a 0 (si se coloca 0 se redirige a 1, permitiendo que el boton de previo en la tabla siempre funcione), siendo  /lista-artesano/1 o /lista-hincha/1 la tabla con los 5 elemenetos mas recientes, luego /lista-artesano/2 o /lista-hincha/2 los siguientes 5 y asi sucesivamente.

`-` La url /estadistica corresponde a una nueva página que contiene 2 gráficos, uno para los artesanos y otro para los hinchas. Para los artesanos muestra el total de artesanos por tipo de artesanía. Para el caso de los hinchas muestra el total de hinchas que escogieron un deporte por deportes. Notar que se usa AJAX (fetch) para obtener los datos con los que se genera el gráficos en el lado del cliente, llamando a /get-estadistica-data-artesano para los datos de los artesanos y /get-estadistica-data-hincha para los datos de los hinchas.

`-` se corrigieron los errores detectados en la tarea 1, especificamente, en agregar-hincha se soluciono el problema con el selector de comuna que no funciona correctamente y a las validaciones tanto de javascript como de python se agrego la condicion para los nombres de que tiene que ser mayor a 3 palabras (sin contar los espacios) evitando que se puede subir un nombre de solo espacios o con menos palabras de las que se quisiese.
