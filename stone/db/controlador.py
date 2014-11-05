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
    '''Obtiene cant tickets de un usuario a partir de la fecha actual
    inclusive, siempre que estos estén activos'''
    date = strftime('%Y-%m-%d', localtime())
    query = '''SELECT tickets.fecha, importe, tickets.estado, tickets.id
               FROM tickets JOIN log_usuarios
                ON id_log_usuario=log_usuarios.id JOIN usuarios
                ON log_usuarios.dni = usuarios.dni
               WHERE tickets.fecha >= '%s' AND usuarios.dni='%s'
                AND tickets.estado = 1 LIMIT %d
            ''' % (date, user['dni'], cant)
    return db.executesql(query, as_dict=True)

def anular_ticket(id_ticket):
    '''Anula el ticket a traves de su id'''
    db(db.tickets.id == id_ticket).update(estado = 0)
    db.commit()

#########################
# Tabla configuraciones #
#########################
def get_configuracion():
    '''Retorna la fila de configuracion'''
    row = db().select(db.configuraciones.ALL).first()
    return row
