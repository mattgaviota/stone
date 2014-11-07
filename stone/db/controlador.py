#-*- coding: utf-8 -*-

from modelo import db
from time import strftime, localtime


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
    row = db(db.facultades.id == id_facultad).select(db.facultades.id,
                                                db.facultades.nombre).first()
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
    row = db(db.provincias.id == id_provincia).select(db.provincias.id,
                                                db.provincias.nombre).first()
    return row.nombre

##################
# Tabla perfiles #
##################
def get_perfil(nombre):
    '''Retorna el id del perfil en base a un nombre dado'''
    row = db(db.perfiles.nombre == nombre).select(db.perfiles.id,
                                                db.perfiles.nombre).first()
    return row.id

####################
# Tabla categorias #
####################
def get_categoria_id(nombre):
    '''Retorna el id de la categoria en base a un nombre dado'''
    row = db(db.categorias.nombre == nombre).select(db.categorias.id,
                                                db.categorias.nombre).first()
    return row.id

def get_categoria_nombre(id_categoria):
    '''Retorna el nombre de la categoria en base a un id dado'''
    row = db(db.categorias.id == id_categoria).select(db.categorias.id,
                                                db.categorias.nombre).first()
    return row.nombre

##################
# Tabla usuarios #
##################
def insert_usuario(data):
    '''Inserta un nuevo usuario con los datos de la variable data'''
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

def update_saldo(user, id_ticket, band):
    '''
    Actualiza el saldo del user de acuerdo al importe del ticket.
    Si band = 1 lo suma / anulación
    Si band = 2 lo resta / compra
    '''
    importe = get_importe_ticket(id_ticket)
    if band:
        db(db.usuarios.dni == user['dni']).update(saldo =
                                            db.usuarios.saldo + importe)
    else:
        db(db.usuarios.dni == user['dni']).update(saldo =
                                            db.usuarios.saldo - importe)
    db.commit()

def update_usuario(user, data):
    '''Actualiza los datos de un usuario con un diccionario de valores'''
    db(db.usuarios.dni == user['dni']).update(**data)
    db.commit()

##################
# Tabla acciones #
##################
def get_id_accion(accion):
    '''Retorna el id de una acción dada por su nombre'''
    row = db(db.acciones.nombre_canonico == accion).select().first()
    return row.id

#######################
# Tabla log_usuarios  #
#######################
def insert_log(user, accion):
    '''inserta una entrada en el log, de acuerdo a la acción realizada'''
    data = {}
    data['id_accion'] = get_id_accion(accion)
    data['fecha'] = strftime('%Y-%m-%d %H:%M:%S', localtime())
    data['dni'] = user['dni']
    data['lugar'] = 2
    db.log_usuarios.insert(**data)
    db.commit()

#################
# Tabla tickets #
#################
def get_tickets(user, cant=5):
    '''
    Obtiene cant números de tickets de un usuario a partir de la fecha actual
    inclusive, siempre que estos estén activos(estado = 1)
    '''
    date = strftime('%Y-%m-%d', localtime())
    tickets = db((db.tickets.id_dia == db.dias.id) &
                    (db.tickets.id_log_usuario == db.log_usuarios.id) &
                    (db.log_usuarios.dni == db.usuarios.dni))
    rows = tickets((db.usuarios.dni == user['dni']) &
                    (db.dias.fecha >= date) &
                    (db.tickets.estado == 1)).select(db.dias.fecha,
                    db.tickets.importe, db.tickets.estado, db.tickets.id,
                    limitby=(0, cant), orderby=db.dias.fecha)
    fila = {}
    lista = []
    for row in rows:
        fila['fecha'] = row['dias']['fecha']
        fila['importe'] = row['tickets']['importe']
        fila['estado'] = row['tickets']['estado']
        fila['id'] = row['tickets']['id']
        lista.append(fila)
        fila = {}
    return lista

def get_importe_ticket(id_ticket):
    '''
    Retorna el importe del ticket con el id = id_ticket, en caso de no
    encontrar ninguno retorna 0
    '''
    row = db(db.tickets.id == id_ticket).select().first()
    if row:
        return row.importe
    else:
        return 0

def anular_ticket(id_ticket):
    '''
    Anula el ticket a traves de su id actualizando el estado.
    estado = 1 -> activo
    estado = 0 -> anulado
    '''
    db(db.tickets.id == id_ticket).update(estado = 0)
    db.commit()

#########################
# Tabla configuraciones #
#########################
def get_configuracion():
    '''Retorna la fila de configuracion'''
    row = db().select(db.configuraciones.ALL).first()
    return row
