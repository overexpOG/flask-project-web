from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
from flask_cors import cross_origin
from utils.validation import validate_artesano, validate_hincha
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/artesania'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/recibido-artesano", methods=["GET"])
def recibido_artesano():
    return render_template("index.html", recibido="artesano")

@app.route("/recibido-hincha", methods=["GET"])
def recibido_hincha():
    return render_template("index.html", recibido="hincha")

@app.route("/agregar-artesano", methods=["GET", "POST"])
def agregar_artesano():
    if request.method == "POST":
        region = request.form.get("region")
        comuna = request.form.get("comuna")
        tipo = request.form.getlist("tipo-artesania")
        descripcion = request.form.get("descripcion")
        nombre = request.form.get("name")
        email = request.form.get("email")
        celular = request.form.get("celular")
        imagen = request.files.getlist("imagen")
        error = ""
        validate, err = validate_artesano(region, comuna, tipo, descripcion, imagen, nombre, email, celular)
        if validate:
            img_filenames = []
            direcciones = []
            for im in imagen:
                _filename = hashlib.sha256(
                    secure_filename(im.filename) # nombre del archivo
                    .encode("utf-8") # encodear a bytes
                    ).hexdigest()
                _extension = filetype.guess(im).extension
                img_filename = f"{_filename}.{_extension}"
                direccion = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
                img_filenames.append(img_filename)
                direcciones.append(direccion)
                im.save(direccion)
            status, msg = db.insertar_artesano_funcion(comuna, tipo, descripcion, img_filenames, direcciones, nombre, email, celular)
            if status:
                return redirect(url_for("recibido_artesano"))
            error += msg
        else:
            error += "los siguientes campos no son validos" + err

        return render_template("agregar-artesano.html", error = error)
    
    elif request.method == "GET":
        return render_template("agregar-artesano.html")

@app.route("/agregar-hincha", methods=["GET", "POST"])
def agregar_hincha():
    if request.method == "POST":
        deportes = request.form.getlist("sport")
        region = request.form.get("region")
        comuna = request.form.get("comuna")
        transporte = request.form.getlist("transporte")
        nombre = request.form.get("name")
        email = request.form.get("email")
        celular = request.form.get("celular")
        comentario = request.form.get("comentario")
        error = ""
        validate, err = validate_hincha(deportes, region, comuna, transporte, nombre, email, celular, comentario)
        if validate:
            status, msg = db.insertar_hincha_funcion(deportes, comuna, transporte, nombre, email, celular, comentario)
            if status:
                return redirect(url_for("recibido_hincha"))
            error += msg
        else:
            error += "los siguientes campos no son validos" + err

        return render_template("agregar-hincha.html", error = error)
    
    elif request.method == "GET":
        return render_template("agregar-hincha.html")

@app.route("/lista-artesano/<int:page>", methods=["GET"])
def lista_artesano(page):
    if (page <= 0):
        return redirect(url_for('lista_artesano', page=1))
    data = []
    for artesano in db.listado_artesano_5((page-1)*5):
        id, comuna_id, descripcion_artesania, nombre, email, celular = artesano
        comuna = db.obtener_info_comuna(comuna_id)
        imagenes = []
        tipos = []
        celular = "+56" + str(celular)
        if celular == "+56":
            celular = ""
        for imagen in db.obtener_foto(id):
            imagenes.append(url_for('static', filename=f"artesania/{imagen[1]}"))
        for tipo in db.obtener_tipo_artesano(id):
            tipos.append(tipo[0])
        data.append({"id": id,
                     "nombre": nombre, 
                     "telefono": celular, 
                     "comuna": comuna[0], 
                     "tipos": tipos, 
                     "imagenes": imagenes
                     })
    return render_template("ver-artesanos.html", data=data, page=page)

@app.route("/lista-hincha/<int:page>", methods=["GET"])
def lista_hincha(page):
    if (page <= 0):
        return redirect(url_for('lista_hincha', page=1))
    data = []
    for hincha in db.listado_hincha_5((page-1)*5):
        id, comuna_id, modo_transporte, nombre, email, celular, comentario = hincha
        comuna = db.obtener_info_comuna(comuna_id)
        deportes = []
        celular = "+56" + str(celular)
        if celular == "+56":
            celular = ""
        for deporte in db.obtener_deporte_hincha(id):
            deportes.append(deporte[0])
        data.append({"id": id,
                     "nombre": nombre,
                     "comuna": comuna[0],
                     "deportes": deportes,
                     "celular": celular,
                     "modo_transporte": modo_transporte})
    return render_template("ver-hinchas.html", data=data, page=page)

@app.route("/ver-artesano/<int:a_id>", methods=["GET"])
def ver_artesano(a_id):
    comuna_id, descripcion_artesania, nombre, email, celular = db.obtener_artesano_por_id(a_id)
    comuna = db.obtener_info_comuna(comuna_id)
    region_nombre = db.obtener_nombre_region(comuna[1])
    imagenes = []
    tipos = []
    celular = "+56" + str(celular)
    if celular == "+56":
        celular = ""
    for imagen in db.obtener_foto(a_id):
        imagenes.append(url_for('static', filename=f"artesania/{imagen[1]}"))
    for tipo in db.obtener_tipo_artesano(a_id):
        tipos.append(tipo[0])
    data = {"nombre": nombre,
            "descripcion_artesania": descripcion_artesania,
            "email": email, 
            "telefono": celular, 
            "comuna": comuna[0], 
            "region": region_nombre[0],
            "tipos": tipos, 
            "imagenes": imagenes
            }
    return render_template("informacion-artesano.html", data=data)

@app.route("/ver-hincha/<int:h_id>", methods=["GET"])
def ver_hincha(h_id):
    comuna_id, modo_transporte, nombre, email, celular, comentario = db.obtener_hincha_por_id(h_id)
    comuna = db.obtener_info_comuna(comuna_id)
    region_nombre = db.obtener_nombre_region(comuna[1])
    deportes = []
    celular = "+56" + str(celular)
    if celular == "+56":
        celular = ""
    for deporte in db.obtener_deporte_hincha(id):
        deportes.append(deporte[0])
    data = {"nombre": nombre,
            "region": region_nombre[0],
            "comuna": comuna[0],
            "email": email,
            "telefono": celular,    
            "deportes": deportes, 
            "transporte": modo_transporte,
            "comentario": comentario
            }
    return render_template("informacion-hincha.html", data=data)

@app.route("/estadistica", methods=["GET"])
def ver_estadisticas():
    return render_template("estadisticas.html")

@app.route("/get-estadistica-data-hincha", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_estadistica_data_hincha():
    contador_deportes = {}
    for hincha in db.listado_hincha():
        id, _, _, _, _, _, _ = hincha
        for deporte in db.obtener_deporte_hincha(id):
            deporte =deporte[0]
            if deporte in contador_deportes:
                contador_deportes[deporte] += 1
            else:
                contador_deportes[deporte] = 1
    data = [{
        "name":clave,
        "count":contador_deportes[clave]
    } for clave in contador_deportes]
    return jsonify(data)

@app.route("/get-estadistica-data-artesano", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_estadistica_data_artesano():
    contador_tipos = {}
    for artesano in db.listado_artesano():
        id, _, _, _, _, _ = artesano
        for tipo in db.obtener_tipo_artesano(id):
            tipo =tipo[0]
            if tipo in contador_tipos:
                contador_tipos[tipo] += 1
            else:
                contador_tipos[tipo] = 1
    data = [{
        "name":clave,
        "count":contador_tipos[clave]
    } for clave in contador_tipos]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)