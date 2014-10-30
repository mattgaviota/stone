#-*- coding: utf-8 -*-

from modelo import db


####################
# Tabla facultades #
####################
def get_all_facultades():
    '''Obtiene todas las facultades y devuelve un diccionario:
        clave nombre, valor id'''
    facultades = {}
    rows = db().select(db.facultades.id, db.facultades.nombre)
    for row in rows:
        facultades[row['nombre']] = row['id']
    return facultades

def get_facultad(id_facultad):
    '''Retorna el nombre de una facultad en base a un id dado'''
    row = db(db.facultades.id == id_facultad).select(db.facultades.id, db.facultades.nombre).first()
    return row.nombre

####################
# Tabla provincias #
####################
def get_all_provincias():
    '''Obtiene todas las provincias y devuelve un diccionario:
        clave nombre, valor id'''
    provincias = {}
    rows = db().select(db.provincias.id, db.provincias.nombre)
    for row in rows:
        provincias[row['nombre']] = row['id']
    return provincias

def get_provincia(id_provincia):
    '''Retorna el nombre de una provincia en base a un id dado'''
    row = db(db.provincias.id == id_provincia).select(db.provincias.id, db.provincias.nombre).first()
    return row.nombre

##################
# Tabla perfiles #
##################
def get_perfil(nombre):
    '''Retorna el id del perfil en base a un nombre dado'''
    row = db(db.perfiles.nombre == nombre).select(db.perfiles.id, db.perfiles.nombre).first()
    return row.id

####################
# Tabla categorias #
####################
def get_categoria_id(nombre):
    '''Retorna el id de la categoria en base a un nombre dado'''
    row = db(db.categorias.nombre == nombre).select(db.categorias.id, db.categorias.nombre).first()
    return row.id

def get_categoria_nombre(id_categoria):
    '''Retorna el nombre de la categoria en base a un id dado'''
    row = db(db.categorias.id == id_categoria).select(db.categorias.id, db.categorias.nombre).first()
    return row.nombre

##################
# Tabla usuarios #
##################
def insert_usuario(data):
    '''Inserta un nuevo usuario con los datos de la variable data'''
    if not get_usuario(data['dni']):
        db.usuarios.insert(**data)
        db.commit()

def get_usuario(dni):
    '''Retorna una fila de usuario en base a un dni dado'''
    rows = db(db.usuarios.dni == dni).select()
    if rows:
        return rows.first()
    else:
        return None

def update_estado(user, valor):
    '''Actualiza el estado de un usuario(user) con el valor dado'''
    db(db.usuarios.dni == user['dni']).update(estado = valor)
    db.commit()

def update_pass(user, new_pass):
    '''Actualiza el password de un usuario(user) con el new_pass dado'''
    db(db.usuarios.dni == user['dni']).update(password = new_pass)
    db.commit()

#########################
# Tabla configuraciones #
#########################
def get_configuracion():
    '''Retorna la fila de configuracion'''
    row = db().select(db.configuraciones.ALL).first()
    return row
