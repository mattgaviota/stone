#-*- coding: utf-8 -*-

from modelo import db


def get_all_facultades():
    facultades = {}
    rows = db().select(db.facultades.id, db.facultades.nombre)
    for row in rows:
        facultades[row['nombre']] = row['id']
    return facultades

def get_all_provincias():
    provincias = {}
    rows = db().select(db.provincias.id, db.provincias.nombre)
    for row in rows:
        provincias[row['nombre']] = row['id']
    return provincias


def get_perfil(nombre):
    row = db(db.perfiles.nombre == nombre).select(db.perfiles.id, db.perfiles.nombre).first()
    return row.id


def get_categoria(nombre):
    row = db(db.categorias.nombre == nombre).select(db.categorias.id, db.categorias.nombre).first()
    return row.id


def insert_usuario(data):
    if not get_usuario(data['dni']):
        db.usuarios.insert(**data)
        db.commit()

def get_usuario(dni):
    rows = db(db.usuarios.dni == dni).select()
    if rows:
        return rows.first()
    else:
        return None

def update_estado(user, valor):
    db(db.usuarios.dni == user['dni']).update(estado = valor)
    db.commit()

def update_pass(user, new_pass):
    db(db.usuarios.dni == user['dni']).update(password = new_pass)
    db.commit()

def get_configuracion():
    row = db().select(db.configuraciones.ALL).first()
    return row
