#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
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

def get_id_facultad(canonico):
    '''Retorna el id de una facultad en base a un nombre dado'''
    row = db(db.facultades.nombre_canonico == canonico).select(db.facultades.id,
                                                db.facultades.nombre).first()
    return row.id

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
    row = db(db.categorias.id == id_categoria).select(
                                                db.categorias.nombre).first()
    return row.nombre

def get_categoria_importe(id_categoria):
    '''Retorna el importe de la categoria en base a un id dado'''
    row = db(db.categorias.id == id_categoria).select(
                                                db.categorias.importe).first()
    return row.importe

def get_categoria_limite(id_categoria):
    '''Retorna el limite máximo de días de la categoria en base a un id dado'''
    row = db(db.categorias.id == id_categoria).select(
                                            db.categorias.dias_maximos).first()
    return row.dias_maximos

##################
# Tabla usuarios #
##################
def insert_usuario(data, unidad):
    '''Inserta un nuevo usuario con los datos de la variable data'''
    db.usuarios.insert(**data)
    db.commit
    user = {'dni': data['dni']}
    insert_log(user, 'registrar', unidad)

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

def update_all_activos():
    db(db.usuarios.dni != '').update(activo = 0)
    db.commit()

def update_activo(user, valor):
    '''
    Actualiza el campo activo de un usuario(user) con el valor dado.
    valor = 1 -> usuario activo(logueado en el sistema)
    valor = 0 -> usuario inactivo(no está logueado en el sistema)
    '''
    db(db.usuarios.dni == user['dni']).update(activo = valor)
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
def insert_log(user, accion, unidad, desc=''):
    '''inserta una entrada en el log, de acuerdo a la acción realizada'''
    data = {}
    data['id_accion'] = get_id_accion(accion)
    data['fecha'] = strftime('%Y-%m-%d %H:%M:%S', localtime())
    data['dni'] = user['dni']
    data['lugar'] = unidad
    data['descripcion'] = "%s %s" %(get_nombre_accion(data['id_accion']), desc)
    id_log = db.log_usuarios.insert(**data)
    db.commit()
    return id_log

def get_hora_inicio(unidad, date=strftime('%Y-%m-%d', localtime())):
    ''' Obtiene la hora de inicio de la maquina. '''
    rows = db((db.log_usuarios.id_accion == get_id_accion('iniciar')) &
              (db.log_usuarios.lugar == unidad)).select(db.log_usuarios.ALL)
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date and "1er" in row.descripcion:
            return row.fecha.strftime('%H:%M:%S')

def get_hora_cierre(unidad, date=strftime('%Y-%m-%d', localtime())):
    ''' Obtiene la hora de cierre de la maquina. '''
    rows = db((db.log_usuarios.id_accion == get_id_accion('retiro')) &
              (db.log_usuarios.lugar == unidad)).select(db.log_usuarios.ALL)
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date:
            return row.fecha.strftime('%H:%M:%S')

def get_log(unidad, accion, date=strftime('%Y-%m-%d', localtime())):
    ''' Obtiene el log de cierta accion en cierta maquina el dia de hoy. '''
    rows = db((db.log_usuarios.id_accion == get_id_accion(accion)) &
              (db.log_usuarios.lugar == unidad)).select(db.log_usuarios.ALL)
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date:
            return row

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

def get_count_tickets(user, state=2, accion=3):
    '''Retorna la cantidad de tickets impresos de un usuario que tengan el
    estado 2(impreso) y la accion 3 (imprimir).'''
    tickets = db((db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni))
    cantidad = tickets((db.usuarios.dni == user['dni']) &
            (db.tickets.estado == state) &
            (db.log_usuarios.id_accion == accion)).count()
    return cantidad

def get_select_tickets(user, state=2, accion=3):
    '''Retorna la cantidad de tickets impresos de un usuario que tengan el
    estado 2(impreso) y la accion 3 (imprimir).'''
    tickets = db((db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni))
    cantidad = tickets((db.usuarios.dni == user['dni']) &
            (db.tickets.estado == state) &
            (db.log_usuarios.id_accion == accion)).select()
    return cantidad

def get_ticket(user, date=strftime('%Y-%m-%d', localtime()), state=0):
    '''
    Retorna la fila de un ticket si hay un ticket activo de ese usuario para
    ese día, en caso contrario retorna False.'''
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
    ''' Retorna la fecha de un ticket, si es que existe para el usuario user.'''
    tickets = db((db.tickets.id_dia == db.dias.id) &
            (db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni) &
            (db.usuarios.dni == user['dni']))
    rows = tickets((db.tickets.id == id_ticket) &
            ((db.tickets.estado == 1) |
            (db.tickets.estado == 2))).select(db.dias.fecha)
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

def get_dia_ticket(id_ticket):
    '''
    Retorna el id del día del ticket a traves de su id, en caso de no
    encontrar ninguno retorna None
    '''
    row = db(db.tickets.id == id_ticket).select().first()
    if row:
        return row.id_dia
    else:
        return None

def update_ticket(id_ticket, user, unidad, state):
    ''' Actualiza el estado del ticket por su id.
    estado = 4 -> vencido
    estado = 3 -> consumido
    estado = 2 -> impreso
    estado = 1 -> activo
    estado = 0 -> anulado
    '''
    db(db.tickets.id == id_ticket).update(estado = state)
    db.commit()
    if state == 4:
        id_log = insert_log(user, 'vencer', unidad)
        insert_ticket_log(id_ticket, id_log)
    elif state == 3:
        id_log = insert_log(user, 'consumir', unidad)
        insert_ticket_log(id_ticket, id_log)
    elif state == 2:
        id_log = insert_log(user, 'imprimir', unidad)
        insert_ticket_log(id_ticket, id_log)
    elif state == 0:
        id_log = insert_log(user, 'anular', unidad)
        insert_ticket_log(id_ticket, id_log)
    else:
        pass

def anular_ticket(id_ticket, user, unidad):
    '''
    Anula el ticket a traves de su id actualizando el estado.
    estado = 3 -> consumido
    estado = 2 -> impreso
    estado = 1 -> activo
    estado = 0 -> anulado
    Además inserta en el log el ticket anulado, actualiza el saldo
    y los tickets vendidos de ese día.
    '''
    db(db.tickets.id == id_ticket).update(estado = 0)
    db.commit()
    id_log = insert_log(user, 'anular', unidad)
    insert_ticket_log(id_ticket, id_log)
    importe = get_importe_ticket(id_ticket)
    update_saldo(user, importe, 0)
    update_tickets_dia(get_dia_ticket(id_ticket), band=0)

def insert_tickets(user, dias, id_log, unit):
    ''' Inserta tickets de acuerdo a los días pasados como parametros para ese
    usuario. '''
    data = {}
    for dia in dias:
        if not get_ticket(user, date=dia):
            data['id_dia'] = get_id_dia(dia)
            data['importe'] = get_categoria_importe(user['id_categoria'])
            data['unidad'] = unit # terminal o web
            data['estado'] = 2 # activo e impreso
            fecha = str(int(time()))
            data['barcode'] = fecha
            update_tickets_dia(data['id_dia'])
            id_ticket = db.tickets.insert(**data)
            db.commit()
            insert_ticket_log(id_ticket, id_log)
            id_ticket = str(id_ticket)
            codigo = fecha + '0' * (10 - len(id_ticket)) + id_ticket
            db(db.tickets.id == id_ticket).update(barcode = codigo)
            db.commit()
            data = {}
        else:
            data = {}

##############
# Tabla dias #
##############
def  get_dias(user, limit):
    '''
    Retorna una lista de limit cantidad de dias que tengan tickets
    disponibles a partir de la fecha de hoy.'''
    cantidad = get_count_tickets(user)
    weekdays = {0: 'Lu', 1: 'Ma', 2: 'Mi', 3: 'Ju', 4: 'Vi'}
    lista_nombres = []
    lista_dias = []
    if limit > cantidad:
        limit -= cantidad
        today = localtime()
        hora = get_hora_compra()
        if today.tm_hour < hora:
            date = strftime('%Y-%m-%d', today)
        else:
            date = '%d-%d-%d' % (today.tm_year, today.tm_mon, today.tm_mday + 1)
        rows = db((db.dias.tickets_vendidos < db.dias.tickets_totales) &
                (db.dias.fecha >= date)).select(db.dias.fecha,
                                        orderby=db.dias.fecha)
        for row in rows:
            date = row.fecha.strftime('%d/%m/%Y')
            if ((not get_ticket(user, date)) and (len(lista_dias) < limit)):
                fecha = row.fecha
                fecha = "%s %s" % (weekdays[fecha.weekday()], date)
                lista_nombres.append(fecha)
                lista_dias.append(date)
        return lista_dias, lista_nombres
    else:
        return lista_dias, lista_nombres

def get_tickets_disponibles(date=strftime('%Y-%m-%d', localtime())):
    '''Devuelve los tickets disponibles para cierto día. Por defecto para
    el día de hoy. '''
    row = db(db.dias.fecha == date).select(db.dias.ALL).first()
    today = localtime()
    hora = get_hora_compra()
    if row:
        disponibles = row.tickets_totales - row.tickets_vendidos
        if disponibles >= 0:
            if today.tm_hour <= hora:
                return disponibles
            else:
                return 0
        else:
            return 0
    else:
        return 0

def get_id_dia(dia):
    '''Retorna el id de un día de acuerdo a la fecha'''
    row = db(db.dias.fecha == dia).select(db.dias.id).first()
    return row.id

def update_tickets_dia(id_dia, cant=1, band=1):
    '''
    Actualiza la cantidad de tickets vendidos de acuerdo a band en cant veces.

        band = 1 -> compra aumenta la cantidad de tickets vendidos
        band = 0 -> anulación disminuye la cantidad de tickets vendidos
    '''
    if band:
        db(db.dias.id == id_dia).update(tickets_vendidos =
                                            db.dias.tickets_vendidos + cant)
    else:
        db(db.dias.id == id_dia).update(tickets_vendidos =
                                            db.dias.tickets_vendidos - cant)
    db.commit()

#########################
# Tabla configuraciones #
#########################
def get_configuracion():
    '''Retorna la fila de configuracion'''
    row = db().select(db.configuraciones.ALL).first()
    return row

def get_hora_anulacion():
    ''' Retorna la hora máxima de anulación de un ticket'''
    row = get_configuracion()
    return row['hora_anulacion']

def get_hora_compra():
    ''' Retorna la hora máxima de compra de un ticket'''
    row = get_configuracion()
    return row['hora_compra']

def get_saldo_maximo():
    ''' Retorna el saldo máximo posible para un usuario. '''
    row = get_configuracion()
    return row['saldo_maximo']

def get_session_time():
    ''' Retorna el tiempo máximo de sesión para un usuario. '''
    row = get_configuracion()
    return row['session_time']

##################
# Tabla imagenes #
##################
def get_images(nombre):
    ''' Obtiene las rutas a las imágenes del sistema. '''
    row = db(db.imagenes.nombre == nombre).select(db.imagenes.ruta).first()
    return row.ruta

##################
# Tabla videos   #
##################
def get_videos():
    ''' Obtiene la ruta, nombre y título de los videos de ayuda. '''
    rows = db().select(db.videos.ruta, db.videos.nombre, db.videos.titulo)
    diccionario = {}
    for row in rows:
        diccionario[row['nombre']] = [row['ruta'], row['titulo']]
    return diccionario

#################
# Tabla alumnos #
#################
def get_alumno(lu, dni):
    ''' Obtiene el id de un alumno si que es existe el par lu y dni. '''
    rows = db((db.alumnos.lu == lu) & (db.alumnos.dni == dni)).select()
    if rows:
        row = rows.first()
        return row.id
    else:
        return None

def get_materias(id_alumno):
    ''' Retorna la cantidad de materias aprobadas para cierto alumno(lu). '''
    row = db(db.alumnos.id == id_alumno).select().first()
    if row:
        if row.materias:
            return int(row.materias)
        else:
            return 0
    else:
        return None


##################
# Tabla maquinas #
##################
def get_maquina(ubicacion):
    '''Obtiene el número de maquina de acuerdo a su ubicación. '''
    id_facultad = get_id_facultad(ubicacion)
    row = db(db.maquinas.ubicacion == id_facultad).select().first()
    if row:
        return row.id
    else:
        return None

def get_maquina_ubicacion(id_facultad):
    row = db(db.maquinas.ubicacion == id_facultad).select().first()
    if row:
        return row.id
    else:
        return None

def get_ubicacion(id_maquina):
    ''' Obtiene la ubicación de una maquina de acuerdo al número '''
    row = db(db.maquinas.id == id_maquina).select().first()
    if row:
        return get_facultad(row.ubicacion)
    else:
        None

def update_estado_maquina(id_maquina, state):
    ''' Actualiza el estado de una maquina.'''
    db(db.maquinas.id == id_maquina).update(estado = state)
    db.commit()

##################
# Tabla billetes #
##################
def insert_billete(user, valor, id_maquina):
    ''' Registra el ingreso de billetes, indicando el valor y la maquina. '''
    data = {}
    data['fecha'] = strftime('%Y-%m-%d %H:%M:%S', localtime())
    data['dni'] = user['dni']
    data['valor'] = valor
    data['id_maquina'] = id_maquina
    db.billetes.insert(**data)
    db.commit()

def get_total(unidad, date=strftime('%Y-%m-%d', localtime())):
    ''' Obtiene el total de billetes ingresados en una maquina'''
    rows = db((db.billetes.id_maquina == db.maquinas.id) &
              (db.maquinas.id == unidad)).select(db.billetes.ALL)
    total = 0
    billetes = {2: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0}
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date:
            total += row.valor
            try:
                billetes[row.valor] += 1
            except KeyError:
                pass
    return total, billetes

########################
# Tabla tickets_cierre #
########################
def insert_ticket_cierre(id_log, total, unidad):
    ''' Registra el ticket de cierre de acuerdo al total de dinero retirado y
    la maquina donde se hace. '''
    data = {}
    data['fecha'] = strftime('%Y-%m-%d %H:%M:%S', localtime())
    data['total'] = total
    data['id_log_usuario'] = id_log
    data['id_maquina'] = unidad
    fecha = str(int(time()))
    data['barcode'] = fecha
    id_ticket = db.tickets_cierre.insert(**data)
    db.commit()
    id_ticket = str(id_ticket)
    codigo = fecha + '0' * (10 - len(id_ticket)) + id_ticket
    db(db.tickets_cierre.id == id_ticket).update(barcode = codigo)
    db.commit()
    return id_ticket

def get_ticket_cierre(id_ticket):
    ''' Obtiene el ticket de cierre de acuerdo al id. '''
    row = db(db.tickets_cierre.id == id_ticket).select().first()
    if row:
        return row
    else:
        return None

def get_id_ticket_cierre(unidad, date=strftime('%Y-%m-%d', localtime())):
    ''' Obtiene el id del ticket de  cierre de acuerdo al día
    y a la unidad. '''
    rows = db(db.tickets_cierre.id_maquina == unidad).select()
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date:
            return row.id
    return None
