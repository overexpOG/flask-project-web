import pymysql
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

with open('database/querys.json', 'r') as querys:
	QUERY_DICT = json.load(querys)
	
# -- conn ---

def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn

# -- querys --

def insertar_artesano(comuna_id, descripcion, nombre, email, celular):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insertar_artesano"], (comuna_id, descripcion, nombre, email, celular))
	conn.commit()
	last_id = cursor.lastrowid
	return last_id

def listado_artesano():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["listado_artesano"])
	artesanos = cursor.fetchall()
	return artesanos
	
def listado_artesano_5(page):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["listado_artesano_5"], (page,))
	artesanos = cursor.fetchall()
	return artesanos
	
def insertar_tipo_artesano(artesano_id, tipo_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insertar_tipo_artesano"], (artesano_id, tipo_id))
	conn.commit()
	
def obtener_tipo_artesano(artesano_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_tipo_artesano"], (artesano_id,))
	nombre = cursor.fetchall()
	return nombre
	
def insertar_foto(ruta_archivo, nombre_archivo, artesano_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insertar_foto"], (ruta_archivo, nombre_archivo, artesano_id))
	conn.commit()
	
def obtener_foto(artesano_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_foto"], (artesano_id,))
	imagen = cursor.fetchall()
	return imagen
	
def obtener_ultimo_id():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_ultimo_id"])
	id = cursor.fetchone()
	return id
	
def obtener_id_comuna(comuna):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_id_comuna"], (comuna,))
	id = cursor.fetchone()
	return id

def obtener_info_comuna(comuna_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_info_comuna"], (comuna_id,))
	nombre = cursor.fetchone()
	return nombre

def obtener_artesano_por_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_artesano_por_id"], (id,))
	artesano = cursor.fetchone()
	return artesano

def obtener_nombre_region(region_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_nombre_region"], (region_id,))
	nombre = cursor.fetchone()
	return nombre

def insertar_hincha(comuna_id, modo_transporte, nombre, email, celular, comentarios):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insertar_hincha"], (comuna_id, modo_transporte, nombre, email, celular, comentarios))
	conn.commit()
	last_id = cursor.lastrowid
	return last_id

def listado_hincha():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["listado_hincha"])
	hinchas = cursor.fetchall()
	return hinchas

def listado_hincha_5(page):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["listado_hincha_5"], (page,))
	hinchas = cursor.fetchall()
	return hinchas

def insertar_deporte_hincha(hincha_id, deporte_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insertar_deporte_hincha"], (hincha_id, deporte_id))
	conn.commit()

def obtener_deporte_hincha(hincha_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_deporte_hincha"], (hincha_id,))
	deportes = cursor.fetchall()
	return deportes

def obtener_hincha_por_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["obtener_hincha_por_id"], (id,))
	hincha = cursor.fetchone()
	return hincha
	

# -- db-related functions --

def insertar_artesano_funcion(comuna, tipo, descripcion, imagen, direccion, nombre, email, celular):
	comuna_id = obtener_id_comuna(comuna)
	if comuna_id is None:
		return False, "No se encuentra la comuna en la base de datos."
	artesano_id = insertar_artesano(comuna_id, descripcion, nombre, email, celular)
	#artesano_id = obtener_ultimo_id()
	if artesano_id is None:
		return False, "error al insertar artesano"
	for t in tipo:
		insertar_tipo_artesano(artesano_id, t)
	for i in range(len(imagen)):
	    insertar_foto(direccion[i], imagen[i], artesano_id)
	return True, None

def insertar_hincha_funcion(deportes, comuna, transporte, nombre, email, celular, comentario):
	comuna_id = obtener_id_comuna(comuna)
	if comuna_id is None:
		return False, "No se encuentra la comuna en la base de datos."
	hincha_id = insertar_hincha(comuna_id, transporte, nombre, email, celular, comentario)
	if hincha_id is None:
		return False, "error al insertar artesano"
	for d in deportes:
		insertar_deporte_hincha(hincha_id, d)
	return True, None
