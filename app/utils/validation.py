from database import db
import re
import filetype

def validate_region(region):
    try:
        return True if (0 <= int(region) <= 15) else False
    except:
        return False
    
def validate_comuna(comuna):
    return True if (db.obtener_id_comuna(comuna) is not None) else False

def validate_tipo(tipo):
    try:
        if (not (1 <= len(tipo) <= 3)):
            return False
        for t in tipo:
            if not (1 <= int(t) <= 9):
                return False
        return True
    except:
        return False

def validate_descripcion(descripcion):
    expresion_regular_descripcion = r'^[a-zA-Z0-9.,!?¡¿\sáéíóúüñÁÉÍÓÚÜÑ]+$'
    return True if (re.match(expresion_regular_descripcion, descripcion)) else False

def validate_comentario(comentario):
    expresion_regular_comentario = r'^[a-zA-Z0-9.,!?¡¿\sáéíóúüñÁÉÍÓÚÜÑ]+$'
    return True if (re.match(expresion_regular_comentario, comentario)) else False

def validate_imagen(imagen):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}
    if (not (1 <= len(imagen) <= 3)):
        return False
    for im in imagen:
        if im is None:
            return False
        if im.filename == "":
            return False
        ftype_guess = filetype.guess(im)
        if ftype_guess.extension not in ALLOWED_EXTENSIONS:
            return False
        if ftype_guess.mime not in ALLOWED_MIMETYPES:
            return False
    return True

def validate_nombre(nombre):
    expresion_regular_nombres = r"^[A-Za-z\s\'\u00E1\u00E9\u00ED\u00F3\u00FA]+$"
    return True if (re.match(expresion_regular_nombres, nombre) and 3 <= len(nombre.strip()) and len(nombre) <= 80) else False

def validate_email(email):
    expresion_regular_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z_]+?\.[a-zA-Z.]{2,}$"
    return True if (re.match(expresion_regular_email, email)) else False

def validate_celular(celular):
    if celular=="":
        return True
    expresion_regular_celular = r"^\d*$"
    return True if (re.match(expresion_regular_celular, celular) and 9 == len(celular)) else False

def validate_deporte(deporte):
    try:
        if (not (1 <= len(deporte) <= 3)):
            return False
        for d in deporte:
            if not (1 <= int(d) <= 60):
                return False
        return True
    except:
        return False
    
def validate_transporte(transporte):
    try:
        if transporte[0] == 'Particular' or transporte[0] == 'Locomoción pública':
            return True
        else:
            return False
    except:
        return False

def validate_artesano(region, comuna, tipo, descripcion, imagen, nombre, email, celular):
    error = ""
    if (not validate_region(region)):
        error += ", region"
    if (not validate_comuna(comuna)):
        error +=  ", comuna"
    if (not validate_tipo(tipo)):
        error +=  ", tipo"
    if (not validate_descripcion(descripcion)):
        error +=  ", descripcion"
    if (not validate_imagen(imagen)):
        error +=  ", imagen"
    if (not validate_nombre(nombre)):
        error +=  ", nombre"
    if (not validate_email(email)):
        error += ", email"
    if (not validate_celular(celular)):
        error +=  ", celular"
    if error != "":
        return False, error
    return True, None

def validate_hincha(deportes, region, comuna, transporte, nombre, email, celular, comentario):
    error = ""
    if (not validate_deporte(deportes)):
        error += ", deportes"
    if (not validate_region(region)):
        error += ", region"
    if (not validate_comuna(comuna)):
        error +=  ", comuna"
    if (not validate_transporte(transporte)):
        error += ", transporte"
    if (not validate_nombre(nombre)):
        error +=  ", nombre"
    if (not validate_email(email)):
        error += ", email"
    if (not validate_celular(celular)):
        error +=  ", celular"
    if (not validate_comentario(comentario)):
        error += ", comentario"
    if error != "":
        return False, error
    return True, None