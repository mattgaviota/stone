#-*- coding: utf-8 -*-

from modelo import db
from time import strftime, localtime, time


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
    row = db(db.categorias.nombre == nombre).select(db.categorias.id).first()
    return row.id

def get_categoria_nombre(id_categoria):
    '''Retorna el nombre de la categoria en base a un id dado'''
    row = db(db.categorias.id == id_categoria).select(db.categorias.nombre).first()
    return row.nombre

def get_categoria_importe(id_categoria):
    '''Retorna el nombre de la categoria en base a un id dado'''
    row = db(db.categorias.id == id_categoria).select(db.categorias.importe).first()
    return row.importe

##################
# Tabla usuarios #
##################
def insert_usuario(data):
    '''Inserta un nuevo usuario con los datos de la variable data'''
    db.usuarios.insert(**data)
    db.commit
    user = {'dni': data['dni']}
    insert_log(user, 'registrar')

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

def update_saldo(user, importe, band):
    '''
    Actualiza el saldo del user de acuerdo al importe del ticket.
    Si band = 0 anulación/carga => suma el saldo
    Si band = 1 compra => resta el saldo
    '''
    if band:
        db(db.usuarios.dni == user['dni']).update(saldo =
                                            db.usuarios.saldo - importe)
    else:
        db(db.usuarios.dni == user['dni']).update(saldo =
                                            db.usuarios.saldo + importe)
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

def get_nombre_accion(id_accion):
    row = db(db.acciones.id == id_accion).select().first()
    return row.nombre

#######################
# Tabla log_usuarios  #
#######################
def insert_log(user, accion, desc=''):
    '''inserta una entrada en el log, de acuerdo a la acción realizada'''
    data = {}
    data['id_accion'] = get_id_accion(accion)
    data['fecha'] = strftime('%Y-%m-%d %H:%M:%S', localtime())
    data['dni'] = user['dni']
    data['lugar'] = 2 # TODO
    data['descripcion'] = "%s %s" %(get_nombre_accion(data['id_accion']), desc)
    id_log = db.log_usuarios.insert(**data)
    db.commit()
    return id_log

##############################
# Tabla tickets_log_usuarios #
##############################
def insert_ticket_log(id_ticket, id_log_usuario):
    '''inserta una entrada en el log de tickets'''
    data = {}
    data['id_ticket'] = id_ticket
    data['id_log_usuario'] = id_log_usuario
    id_log = db.tickets_log_usuarios.insert(**data)
    db.commit()
    return id_log

#################
# Tabla tickets #
#################
def get_tickets(user, cant=5, date=strftime('%Y-%m-%d', localtime()), state=0):
    '''
    Obtiene cant números de tickets de un usuario a partir de la fecha date
    inclusive, siempre que estos estén tengan el estado = state
    '''
    tickets = db((db.tickets.id_dia == db.dias.id) &
            (db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni))
    rows = tickets((db.usuarios.dni == user['dni']) &
                (db.dias.fecha >= date) &
                (db.tickets.estado != state)).select(db.dias.fecha,
                        db.tickets.importe, db.tickets.estado, db.tickets.id,
                        db.tickets.barcode, limitby=(0, cant),
                        orderby=db.dias.fecha)
    fila = {}
    lista = []
    for row in rows:
        fila['fecha'] = row['dias']['fecha']
        fila['importe'] = row['tickets']['importe']
        fila['estado'] = row['tickets']['estado']
        fila['id'] = row['tickets']['id']
        fila['barcode'] = row['tickets']['barcode']
        lista.append(fila)
        fila = {}
    return lista

def get_ticket(user, date=strftime('%Y-%m-%d', localtime()), state=0):
    '''
    Retorna True si hay un ticket activo de ese usuario para ese día,
    en caso contrario retorna False.'''
    tickets = db((db.tickets.id_dia == db.dias.id) &
            (db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni))
    rows = tickets((db.usuarios.dni == user['dni']) &
            (db.dias.fecha == date) &
            (db.tickets.estado != state)).select(db.dias.fecha,
                            db.tickets.importe, db.tickets.estado,
                            db.tickets.id, db.tickets.barcode)
    if rows:
        row = rows.first()
        fila = {}
        fila['fecha'] = row['dias']['fecha']
        fila['importe'] = row['tickets']['importe']
        fila['estado'] = row['tickets']['estado']
        fila['id'] = row['tickets']['id']
        fila['barcode'] = row['tickets']['barcode']
        return fila
    else:
        return False

def has_ticket(user, id_ticket, state=0):
    tickets = db((db.tickets.id_dia == db.dias.id) &
            (db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == user['dni']))
    rows = tickets((db.tickets.id == id_ticket) & 
            (db.tickets.estado != state)).select(db.dias.fecha)
    if rows:
        row = rows.first()
        return row['fecha'].strftime('%d/%m/%Y')
    else:
        return ''

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
    estado = 3 -> consumido
    estado = 2 -> impreso
    estado = 1 -> activo
    estado = 0 -> anulado
    '''
    db(db.tickets.id == id_ticket).update(estado = 0)
    db.commit()

def insert_tickets(user, dias, id_log, unit):
    data = {}
    for dia in dias:
        data['id_dia'] = get_id_dia(dia)
        data['importe'] = get_categoria_importe(user['id_categoria'])
        data['unidad'] = int(unit) # terminal o web
        data['estado'] = 2 # activo e impreso
        fecha = str(int(time()))
        data['barcode'] = fecha
        id_ticket = db.tickets.insert(**data)
        db.commit()
        insert_ticket_log(id_ticket, id_log)
        id_ticket = str(id_ticket)
        codigo = fecha + '0' * (10 - len(id_ticket)) + id_ticket
        db(db.tickets.id == id_ticket).update(barcode = codigo)
        db.commit()
        
##############
# Tabla dias #
##############
def  get_dias(user, limit=20, hora=14):
    '''
    Retorna una lista de limit cantidad de dias que tengan tickets
    disponibles a partir de la fecha de hoy.'''
    today = localtime()
    if today.tm_hour < hora:
        date = strftime('%Y-%m-%d', today)
    else:
        date = '%d-%d-%d' % (today.tm_year, today.tm_mon, today.tm_mday + 1)
    rows = db((db.dias.tickets_vendidos < 700) &
            (db.dias.fecha >= date)).select(db.dias.fecha,
                                    orderby=db.dias.fecha, limitby=(0,limit))
    lista = []
    for row in rows:
        if not get_ticket(user, date=row.fecha.strftime('%d/%m/%Y')):
            lista.append(row.fecha.strftime('%d/%m/%Y'))
    return lista

def get_id_dia(dia):
    row = db(db.dias.fecha == dia).select(db.dias.id).first()
    return row.id

#########################
# Tabla configuraciones #
#########################
def get_configuracion():
    '''Retorna la fila de configuracion'''
    row = db().select(db.configuraciones.ALL).first()
    return row

def get_hora_anulacion():
    row = get_configuracion()
    return row['hora_anulacion']

def get_hora_compra():
    row = get_configuracion()
    return row['hora_compra']

def get_saldo_maximo():
    row = get_configuracion()
    return row['saldo_maximo']

##################
# Tabla imagenes #
##################
def get_images(nombre):
    row = db(db.imagenes.nombre == nombre).select(db.imagenes.ruta).first()
    return row.ruta

##################
# Tabla videos   #
##################
def get_videos():
    rows = db().select(db.videos.ruta, db.videos.nombre, db.videos.titulo)
    diccionario = {}
    for row in rows:
        diccionario[row['nombre']] = [row['ruta'], row['titulo']]
    return diccionario
