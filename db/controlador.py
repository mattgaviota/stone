#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
from modelo import db
from psycopg2 import IntegrityError
from time import time
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


####################
# Tabla facultades #
####################
def get_all_facultades():
    """Obtiene todas las facultades y devuelve un diccionario:
        clave nombre, valor id"""
    facultades = {}
    rows = db().select(db.facultades.id, db.facultades.nombre)
    for row in rows:
        facultades[row['nombre']] = row['id']
    return facultades


def get_facultad(id_facultad):
    """Retorna el nombre de una facultad en base a un id dado"""
    row = db(db.facultades.id == id_facultad).select(db.facultades.id,
                                                db.facultades.nombre).first()
    return row.nombre


def get_id_facultad(canonico):
    """Retorna el id de una facultad en base a un nombre dado"""
    row = db(db.facultades.nombre_canonico == canonico).select(
                            db.facultades.id, db.facultades.nombre).first()
    return row.id


####################
# Tabla provincias #
####################
def get_all_provincias():
    """Obtiene todas las provincias y devuelve un diccionario:
        clave nombre, valor id"""
    provincias = {}
    rows = db().select(db.provincias.id, db.provincias.nombre)
    for row in rows:
        provincias[row['nombre']] = row['id']
    return provincias


def get_provincia(id_provincia):
    """Retorna el nombre de una provincia en base a un id dado"""
    row = db(db.provincias.id == id_provincia).select(db.provincias.id,
                                                db.provincias.nombre).first()
    return row.nombre


##################
# Tabla perfiles #
##################
def get_perfil(nombre):
    """Retorna el id del perfil en base a un nombre dado"""
    row = db(db.perfiles.nombre == nombre).select(db.perfiles.id,
                                                db.perfiles.nombre).first()
    return row.id


####################
# Tabla categorias #
####################
def get_categoria_id(nombre):
    """Retorna el id de la categoria en base a un nombre dado"""
    row = db(db.categorias.nombre == nombre).select(db.categorias.id).first()
    return row.id


def get_categoria_nombre(id_categoria):
    """Retorna el nombre de la categoria en base a un id dado"""
    row = db(db.categorias.id == id_categoria).select(
                                                db.categorias.nombre).first()
    return row.nombre


def get_categoria_importe(id_categoria):
    """Retorna el importe de la categoria en base a un id dado"""
    row = db(db.categorias.id == id_categoria).select(
                                                db.categorias.importe).first()
    return row.importe


def get_categoria_limite(id_categoria):
    """Retorna el limite máximo de días de la categoria en base a un id dado"""
    row = db(db.categorias.id == id_categoria).select(
                                            db.categorias.dias_maximos).first()
    return row.dias_maximos


def get_categorias():
    """ Retorna todas las categorias (id, nombre) """
    rows = db().select(db.categorias.importe, db.categorias.nombre)
    categorias = {}
    if rows:
        for row in rows:
            categorias[row['nombre']] = row['importe']
    else:
        return None
    return categorias


##################
# Tabla usuarios #
##################
def insert_usuario(data, unidad):
    """Inserta un nuevo usuario con los datos de la variable data"""
    db.usuarios.insert(**data)
    db.commit
    user = {'dni': data['dni']}
    insert_log(user, 'registrar', unidad)


def get_usuario(dni):
    """Retorna una fila de usuario en base a un dni dado"""
    rows = db(db.usuarios.dni == dni).select()
    if rows:
        return rows.first()
    else:
        return None


def update_estado(user, valor):
    """Actualiza el estado de un usuario(user) con el valor dado"""
    db(db.usuarios.dni == user['dni']).update(estado=valor)
    db.commit()


def update_all_activos():
    """Actualiza el estado de todos los usuarios"""
    db(db.usuarios.dni != '').update(activo=0)
    db.commit()


def update_activo(user, valor):
    """
    Actualiza el campo activo de un usuario(user) con el valor dado.
    valor = 1 -> usuario activo(logueado en el sistema)
    valor = 0 -> usuario inactivo(no está logueado en el sistema)
    """
    db(db.usuarios.dni == user['dni']).update(activo=valor)
    db.commit()


def update_pass(user, new_pass):
    """Actualiza el password de un usuario(user) con el new_pass dado"""
    db(db.usuarios.dni == user['dni']).update(password=new_pass)
    db.commit()


def update_saldo(user, importe, band):
    """
    Actualiza el saldo del user de acuerdo al importe del ticket.
    Si band = 0 anulación/carga => suma el saldo
    Si band = 1 compra => resta el saldo
    """
    if band:
        db(db.usuarios.dni == user['dni']).update(
                                            saldo=db.usuarios.saldo - importe)
    else:
        db(db.usuarios.dni == user['dni']).update(
                                            saldo=db.usuarios.saldo + importe)
    db.commit()


def update_usuario(user, data):
    """Actualiza los datos de un usuario con un diccionario de valores"""
    db(db.usuarios.dni == user['dni']).update(**data)
    db.commit()


##################
# Tabla acciones #
##################
def get_id_accion(accion):
    """Retorna el id de una acción dada por su nombre"""
    row = db(db.acciones.nombre_canonico == accion).select().first()
    return row.id


def get_nombre_accion(id_accion):
    """Retorna el nombre de una acción dado su id."""
    row = db(db.acciones.id == id_accion).select().first()
    return row.nombre


#######################
# Tabla log_usuarios  #
#######################
def insert_log(user, accion, unidad, desc=''):
    """inserta una entrada en el log, de acuerdo a la acción realizada"""
    data = {}
    data['id_accion'] = get_id_accion(accion)
    data['fecha'] = datetime.now()
    data['dni'] = user['dni']
    data['lugar'] = unidad
    data['descripcion'] = "%s %s" % (
        get_nombre_accion(data['id_accion']),
         desc
    )
    id_log = db.log_usuarios.insert(**data)
    db.commit()
    if id_log:
        return id_log
    else:
        return None


def get_hora_inicio(unidad, date=datetime.now()):
    """ Obtiene la hora de inicio de la maquina. """
    rows = db((db.log_usuarios.id_accion == get_id_accion('iniciar')) &
              (db.log_usuarios.lugar == unidad)).select(db.log_usuarios.ALL)
    for row in rows:
        if (row.fecha.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d')
                                                and "1er" in row.descripcion):
            return row.fecha.strftime('%H:%M:%S')


def get_hora_cierre(unidad, date=datetime.now()):
    """ Obtiene la hora de cierre de la maquina. """
    rows = db((db.log_usuarios.id_accion == get_id_accion('retiro')) &
              (db.log_usuarios.lugar == unidad)).select(db.log_usuarios.ALL)
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
            return row.fecha.strftime('%H:%M:%S')


def get_log(unidad, accion, date=datetime.now()):
    """ Obtiene el log de cierta accion en cierta maquina el dia de hoy. """
    rows = db((db.log_usuarios.id_accion == get_id_accion(accion)) &
              (db.log_usuarios.lugar == unidad)).select(db.log_usuarios.ALL)
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
            return row


##############################
# Tabla tickets_log_usuarios #
##############################
def insert_ticket_log(id_ticket, id_log_usuario):
    """inserta una entrada en el log de tickets"""
    try:
        data = {}
        data['id_ticket'] = id_ticket
        data['id_log_usuario'] = id_log_usuario
        id_log = db.tickets_log_usuarios.insert(**data)
        db.commit()
        if id_log:
            return id_log
        else:
            return None
    except IntegrityError:
        db.rollback()
        return None


#######################################
# Tabla tickets_grupales_log_usuarios #
#######################################
def insert_ticket_grupal_log(id_ticket, id_log_usuario):
    """inserta una entrada en el log de tickets grupales"""
    try:
        data = {}
        data['id_ticket_grupal'] = id_ticket
        data['id_log_usuario'] = id_log_usuario
        id_log = db.tickets_grupales_log_usuarios.insert(**data)
        db.commit()
        if id_log:
            return id_log
        else:
            return None
    except IntegrityError:
        db.rollback()
        return None


#################
# Tabla tickets #
#################
def get_count_tickets(user, state=2, accion=3):
    """Retorna la cantidad de tickets impresos de un usuario que tengan el
    estado 2(impreso) y la accion 3 (imprimir)."""
    tickets = db((db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni))
    cantidad = tickets((db.usuarios.dni == user['dni']) &
            (db.tickets.estado == state) &
            (db.log_usuarios.id_accion == accion)).count()
    return cantidad


def get_select_tickets(user, state=2, accion=3):
    """Retorna la cantidad de tickets impresos de un usuario que tengan el
    estado 2(impreso) y la accion 3 (imprimir)."""
    tickets = db((db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni))
    cantidad = tickets((db.usuarios.dni == user['dni']) &
            (db.tickets.estado == state) &
            (db.log_usuarios.id_accion == accion)).select()
    return cantidad


def get_ticket_by_id(id_ticket):
    """ Retorna la fila de un ticket de acuerdo al id_ticket """
    rows = db((db.tickets.id == id_ticket) &
            (db.tickets.id_dia == db.dias.id)).select(db.dias.fecha,
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
        return None


def get_ticket(user, date):
    """
    Retorna la fila de un ticket si hay un ticket activo de ese usuario para
    ese día, en caso contrario retorna False."""
    tickets = db((db.tickets.id_dia == db.dias.id) &
            (db.tickets.id == db.tickets_log_usuarios.id_ticket) &
            (db.tickets_log_usuarios.id_log_usuario == db.log_usuarios.id) &
            (db.log_usuarios.dni == db.usuarios.dni))
    rows = tickets((db.usuarios.dni == user['dni']) &
            (db.dias.fecha == date) &
            ((db.tickets.estado == 2) |
            (db.tickets.estado == 1) |
            (db.tickets.estado == 3))).select(db.dias.fecha,
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
        return None


def has_ticket(user, id_ticket, state=0):
    """
    Retorna la fecha de un ticket, si es que existe para el usuario user.
    """
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
        return row['fecha']
    else:
        return None


def get_importe_ticket(id_ticket):
    """
    Retorna el importe del ticket con el id = id_ticket, en caso de no
    encontrar ninguno retorna 0
    """
    row = db(db.tickets.id == id_ticket).select().first()
    if row:
        return row.importe
    else:
        return 0


def get_dia_ticket(id_ticket):
    """
    Retorna el id del día del ticket a traves de su id, en caso de no
    encontrar ninguno retorna None
    """
    row = db(db.tickets.id == id_ticket).select().first()
    if row:
        return row.id_dia
    else:
        return None


def update_ticket(id_ticket, user, unidad, state):
    """ Actualiza el estado del ticket por su id.
    estado = 4 -> vencido
    estado = 3 -> consumido
    estado = 2 -> impreso
    estado = 1 -> reservado
    estado = 0 -> anulado
    """
    db(db.tickets.id == id_ticket).update(estado=state)
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
    """
    Anula el ticket a traves de su id actualizando el estado.
    estado = 3 -> consumido
    estado = 2 -> impreso
    estado = 1 -> activo
    estado = 0 -> anulado
    Además inserta en el log el ticket anulado, actualiza el saldo
    y los tickets vendidos de ese día.
    """
    db(db.tickets.id == id_ticket).update(estado=0)
    db.commit()
    id_log = insert_log(user, 'anular', unidad)
    insert_ticket_log(id_ticket, id_log)
    importe = get_importe_ticket(id_ticket)
    update_saldo(user, importe, 0)
    update_tickets_dia(get_dia_ticket(id_ticket), band=0)


def reservar_tickets(user, dias, id_log, unit):
    """ Reserva tickets de acuerdo a los días pasados como parametros para ese
    usuario. """
    data = {}
    tickets_reservados = []
    dias_full = []
    for dia in dias:
        disponibles = get_tickets_libres(dia)
        if disponibles:
            data['id_dia'] = get_id_dia(dia)
            data['importe'] = get_categoria_importe(user['id_categoria'])
            data['unidad'] = unit  # terminal o web
            data['estado'] = 1  # reservado
            fecha = str(int(time()))
            data['barcode'] = fecha
            update_tickets_dia(data['id_dia'])  # tickets_vendidos + 1
            id_ticket = db.tickets.insert(**data)
            db.commit()
            # agregar el ticket y el día como reservado
            tickets_reservados.append((id_ticket, data['id_dia']))
            insert_ticket_log(id_ticket, id_log)
            id_ticket = str(id_ticket)
            codigo = fecha + '0' * (10 - len(id_ticket)) + id_ticket
            db(db.tickets.id == id_ticket).update(barcode=codigo)
            db.commit()
        else:
            # agregar el día como no disponible
            dias_full.append(dia)
        data = {}
    if len(dias) == (len(tickets_reservados) + len(dias_full)):
        return tickets_reservados, dias_full, 1
    else:
        return tickets_reservados, dias_full, 0


def comprar_tickets(tickets_reservados, id_log):
    """ compra los tickets reservados al cambiarles el estado de reservado(1)
    a impresos(2) e inserta el log de compra para cada ticket."""
    for id_ticket, dia in tickets_reservados:
        insert_ticket_log(id_ticket, id_log)
        db(db.tickets.id == id_ticket).update(estado=2)
        db.commit()


def cancelar_tickets(tickets_reservados):
    """ Cancela los tickets pasados como parametro cambiando el estado de
    reservado(1) a cancelado (5) y aumenta los tickets disponibles para ese
    día."""
    for id_ticket, id_dia in tickets_reservados:
        db(db.tickets.id == id_ticket).update(estado=5)
        db.commit()
        update_tickets_dia(id_dia, band=0)


##############
# Tabla dias #
##############
def get_dias(user, limit, date=datetime.now()):
    """
    Retorna una lista de limit cantidad de dias que tengan tickets
    disponibles a partir de la fecha de hoy."""
    cantidad = get_count_tickets(user)
    weekdays = {0: 'Lu', 1: 'Ma', 2: 'Mi', 3: 'Ju', 4: 'Vi'}
    lista_nombres = []
    lista_dias = []
    if limit > cantidad:
        limit -= cantidad
        hora = get_hora_compra()
        if date.hour >= hora:
            date = date + relativedelta(days=1)
        rows = db((db.dias.tickets_vendidos < db.dias.tickets_totales) &
                (db.dias.fecha >= date.date())).select(db.dias.fecha,
                                        orderby=db.dias.fecha)
        for row in rows:
            if ((not get_ticket(user, row.fecha)) and
                    (len(lista_dias) < limit)):
                fecha = "%s %s" % (weekdays[row.fecha.weekday()],
                                                row.fecha.strftime('%d/%m/%Y'))
                lista_nombres.append(fecha)
                lista_dias.append(row.fecha)
        return lista_dias, lista_nombres
    else:
        return lista_dias, lista_nombres


def get_next_day(date):
    """ Devuelve el siguiente día hábil con sus tickets disponibles. """
    dia = date + timedelta(1)
    dias_habiles = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miercoles',
        4: 'Jueves',
        5: 'Viernes'
    }
    anio, sem, dow = dia.isocalendar()
    while dow > 5:
        dia = dia + timedelta(1)
        anio, sem, dow = dia.isocalendar()
    row = db(db.dias.fecha == dia.date()).select(db.dias.ALL).first()
    if row:
        disponibles = row.tickets_totales - row.tickets_vendidos
        disponibles = str(disponibles)
        return [dias_habiles[dow], dia.strftime('%d/%m/%Y'), disponibles, dia]
    else:
        return None


def get_tickets_disponibles(date=datetime.now()):
    """Devuelve los tickets disponibles para la semana dado cierto día. Por
    defecto para el día de hoy. """
    hora_actual = date.hour
    hora_compra = get_hora_compra()
    anio, sem, dow = date.isocalendar()
    dias_hab = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miercoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Sábado',
        7: 'Domingo'
    }
    semana = {}
    if hora_compra >= hora_actual:
        row = db(db.dias.fecha == date.date()).select(db.dias.ALL).first()
        if row:
            disponibles = row.tickets_totales - row.tickets_vendidos
        else:
            disponibles = '0'
    else:
        disponibles = '0'
    semana['dia1'] = [dias_hab[dow], date.strftime('%d/%m/%Y'), disponibles]
    semana['dia2'] = get_next_day(date)
    semana['dia3'] = get_next_day(semana['dia2'][3])
    semana['dia4'] = get_next_day(semana['dia3'][3])
    semana['dia5'] = get_next_day(semana['dia4'][3])
    return semana


def get_tickets_libres(date=datetime.now()):
    ''' Retorna la cantidad de tickets disponibles para el
    día pasado por parametro. por defecto el día de hoy.'''
    row = db(db.dias.fecha == date.date()).select(db.dias.ALL).first()
    if row:
        disponibles = row.tickets_totales - row.tickets_vendidos
        if disponibles > 0:
            return disponibles
        else:
            return 0


def get_id_dia(dia):
    """Retorna el id de un día de acuerdo a la fecha"""
    row = db(db.dias.fecha == dia).select(db.dias.id).first()
    return row.id


def update_totales_dia(id_dia, cantidad=1, band=1):
    """
    Actualiza la cantidad de tickets totales de acuerdo a band en cantidad
    de veces:

        band = 1 -> aumenta la cantidad de tickets totales
        band = 0 -> disminuye la cantidad de tickets totales
    """
    if band:
        db(db.dias.id == id_dia).update(
            tickets_totales=db.dias.tickets_totales + cantidad
        )
    else:
        db(db.dias.id == id_dia).update(
            tickets_totales=db.dias.tickets_totales - cantidad
        )
    db.commit()


def update_tickets_dia(id_dia, cantidad=1, band=1):
    """
    Actualiza la cantidad de tickets vendidos de acuerdo a band en cant veces.

        band = 1 -> compra aumenta la cantidad de tickets vendidos
        band = 0 -> anulación disminuye la cantidad de tickets vendidos
    """
    if band:
        db(db.dias.id == id_dia).update(
            tickets_vendidos=db.dias.tickets_vendidos + cantidad
            )
    else:
        db(db.dias.id == id_dia).update(
            tickets_vendidos=db.dias.tickets_vendidos - cantidad
        )
    db.commit()


#########################
# Tabla configuraciones #
#########################
def get_configuracion(id_conf=0):
    """Retorna la fila de configuracion"""
    row = db(db.configuraciones.id == id_conf).select(
        db.configuraciones.ALL).first()
    return row


def get_hora_anulacion():
    """ Retorna la hora máxima de anulación de un ticket"""
    row = get_configuracion()
    return row['hora_anulacion']


def get_hora_compra():
    """ Retorna la hora máxima de compra de un ticket"""
    row = get_configuracion()
    return row['hora_compra']


def get_saldo_maximo():
    """ Retorna el saldo máximo posible para un usuario. """
    row = get_configuracion()
    return row['saldo_maximo']


def get_session_time():
    """ Retorna el tiempo máximo de sesión para un usuario. """
    row = get_configuracion()
    return row['session_time']


##################
# Tabla imagenes #
##################
def get_images(nombre):
    """ Obtiene las rutas a las imágenes del sistema. """
    row = db(db.imagenes.nombre == nombre).select(db.imagenes.ruta).first()
    return row.ruta


##################
# Tabla videos   #
##################
def get_videos():
    """ Obtiene la ruta, nombre y título de los videos de ayuda. """
    rows = db().select(db.videos.ruta, db.videos.nombre, db.videos.titulo)
    diccionario = {}
    for row in rows:
        diccionario[row['nombre']] = [row['ruta'], row['titulo']]
    return diccionario


#################
# Tabla alumnos #
#################
def get_alumno(lu, dni):
    """ Obtiene el id de un alumno si que es existe el par lu y dni. """
    rows = db((db.alumnos.lu == lu) & (db.alumnos.dni == dni)).select()
    if rows:
        row = rows.first()
        return row.id
    else:
        return None


def get_materias(id_alumno):
    """ Retorna la cantidad de materias aprobadas para cierto alumno(lu). """
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
    """Obtiene el número de maquina de acuerdo a su ubicación. """
    id_facultad = get_id_facultad(ubicacion)
    row = db(db.maquinas.ubicacion == id_facultad).select().first()
    if row:
        return row.id
    else:
        return None


def get_maquina_ubicacion(id_facultad):
    """Retorna el id de una maquina dado el id de una facultad"""
    row = db(db.maquinas.ubicacion == id_facultad).select().first()
    if row:
        return row.id
    else:
        return None


def get_ubicacion(id_maquina):
    """ Obtiene la ubicación de una maquina de acuerdo al número """
    row = db(db.maquinas.id == id_maquina).select().first()
    if row:
        return get_facultad(row.ubicacion)
    else:
        None


def get_papel_disponible(id_maquina):
    """ Obtiene la cantidad de tickets que se pueden imprimir una vez
    que tiene poco papel."""
    row = db(db.maquinas.id == id_maquina).select().first()
    if row:
        return row.tickets_disponibles
    else:
        return None


def update_papel_disponible(id_maquina, band=0, cant=1):
    """
    Actualiza al cantidad de tickets que se pueden imprimir una vez
    que tiene poco papel.
    band:
        0 -> tickets_disponibles -= cant
        1 -> tickets_disponibles += cant
        2 -> tickets_disponibles = cant
    """
    if band == 1:
        db(db.maquinas.id == id_maquina).update(
            tickets_disponibles=db.maquinas.tickets_disponibles + cant
        )
    elif band == 2:
        db(db.maquinas.id == id_maquina).update(tickets_disponibles=cant)
    elif band == 0:
        db(db.maquinas.id == id_maquina).update(
            tickets_disponibles=db.maquinas.tickets_disponibles - cant
        )
    else:
        return 1
    db.commit()
    return 0


def get_estado(id_maquina):
    """Obtiene el estado actual de la maquina dado su id."""
    row = db(db.maquinas.id == id_maquina).select().first()
    if row:
        return row.estado
    else:
        return None


def update_estado_maquina(id_maquina, state):
    """ Actualiza el estado de una maquina."""
    db(db.maquinas.id == id_maquina).update(estado=state)
    db.commit()


##################
# Tabla billetes #
##################
def insert_billete(user, valor, id_maquina):
    """ Registra el ingreso de billetes, indicando el valor y la maquina. """
    data = {}
    data['fecha'] = datetime.now()
    data['dni'] = user['dni']
    data['valor'] = valor
    data['id_maquina'] = id_maquina
    db.billetes.insert(**data)
    db.commit()


def get_total(unidad, date=datetime.now()):
    """ Obtiene el total de billetes ingresados en una maquina"""
    rows = db((db.billetes.id_maquina == db.maquinas.id) &
              (db.maquinas.id == unidad)).select(db.billetes.ALL)
    total = 0
    billetes = {2: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0}
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
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
    """ Registra el ticket de cierre de acuerdo al total de dinero retirado y
    la maquina donde se hace. """
    data = {}
    data['fecha'] = datetime.now()
    data['total'] = total
    data['id_log_usuario'] = id_log
    data['id_maquina'] = unidad
    fecha = str(int(time()))
    data['barcode'] = fecha
    id_ticket = db.tickets_cierre.insert(**data)
    db.commit()
    id_ticket = str(id_ticket)
    codigo = fecha + '0' * (10 - len(id_ticket)) + id_ticket
    db(db.tickets_cierre.id == id_ticket).update(barcode=codigo)
    db.commit()
    return id_ticket


def get_ticket_cierre(id_ticket):
    """ Obtiene el ticket de cierre de acuerdo al id. """
    row = db(db.tickets_cierre.id == id_ticket).select().first()
    if row:
        return row
    else:
        return None


def get_id_ticket_cierre(unidad, date=datetime.now()):
    """ Obtiene el id del ticket de  cierre de acuerdo al día
    y a la unidad. """
    rows = db(db.tickets_cierre.id_maquina == unidad).select()
    for row in rows:
        if row.fecha.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
            return row.id
    return None


##########################
# Tabla tickets_grupales #
##########################
def comprar_ticket_grupal(cant, delegacion, categoria, date, recibo, id_log):
    """Compra un ticket grupal agregando la cant extra de días necesarios
    para la fecha date, indicando la delegación."""
    data = {}
    data['id_dia'] = get_id_dia(date)
    data['importe'] = categoria[0]  # 0 -> importe
    data['id_categoria'] = get_categoria_id(categoria[1])  # 1 -> nombre
    data['cantidad'] = cant
    data['id_estado'] = 2  # impreso
    data['delegacion'] = delegacion
    data['recibo'] = recibo
    fecha = str(int(time()))
    data['barcode'] = fecha
    update_tickets_dia(data['id_dia'], cant, 1)  # tickets_vendidos + cant
    update_totales_dia(data['id_dia'], cant, 1)  # tickets_totales + cant
    id_ticket = db.tickets_grupales.insert(**data)
    db.commit()
    insert_ticket_grupal_log(id_ticket['id'], id_log)
    id_ticket = str(id_ticket['id'])
    codigo = 'G' + fecha[1:] + '0' * (10 - len(id_ticket)) + id_ticket
    db(db.tickets_grupales.id == id_ticket).update(barcode=codigo)
    db.commit()
    return id_ticket


def get_ticket_grupal_by_id(id_ticket):
    """ Retorna la fila de un ticket grupal de acuerdo al id_ticket """
    rows = db(
            (db.tickets_grupales.id == id_ticket) &
            (db.tickets_grupales.id_dia == db.dias.id)).select(
                                                db.dias.fecha,
                                                db.tickets_grupales.importe,
                                                db.tickets_grupales.id,
                                                db.tickets_grupales.cantidad,
                                                db.tickets_grupales.delegacion,
                                                db.tickets_grupales.recibo,
                                                db.tickets_grupales.barcode
            )
    if rows:
        row = rows.first()
        fila = {}
        fila['fecha'] = row['dias']['fecha']
        fila['importe'] = row['tickets_grupales']['importe']
        fila['delegacion'] = row['tickets_grupales']['delegacion']
        fila['recibo'] = row['tickets_grupales']['recibo']
        fila['cantidad'] = row['tickets_grupales']['cantidad']
        fila['id'] = row['tickets_grupales']['id']
        fila['barcode'] = row['tickets_grupales']['barcode']
        return fila
    else:
        return None


def has_ticket_grupal(id_ticket, state=0):
    """ Retorna la fecha de un ticket grupal, si es que existe."""
    tickets = db((db.tickets_grupales.id_dia == db.dias.id) &
            (db.tickets_grupales.id == id_ticket) &
            ((db.tickets.estado == 1) |
            (db.tickets.estado == 2))).select(db.dias.fecha)
    if tickets:
        ticket = tickets.first()
        return ticket['fecha']
    else:
        return None


def get_dia_ticket_grupal(id_ticket):
    """
    Retorna el id del día del ticket grupal a traves de su id, en caso de no
    encontrar ninguno retorna None
    """
    row = db(db.tickets_grupales.id == id_ticket).select().first()
    if row:
        return row.id_dia
    else:
        return None


def get_cant_ticket_grupal(id_ticket):
    """
    Retorna la cantidad del día del ticket grupal a traves de su id,
    en caso de no encontrar ninguno retorna None
    """
    row = db(db.tickets_grupales.id == id_ticket).select().first()
    if row:
        return row.cantidad
    else:
        return None


def update_ticket_grupal(id_ticket, user, unidad, state):
    """ Actualiza el estado del ticket por su id.
    estado = 4 -> vencido
    estado = 3 -> consumido
    estado = 2 -> impreso
    estado = 1 -> reservado
    estado = 0 -> anulado
    """
    db(db.tickets_grupales.id == id_ticket).update(id_estado=state)
    db.commit()
    if state == 2:
        id_log = insert_log(user, 'imprimir_grupal', unidad)
        insert_ticket_grupal_log(id_ticket, id_log)
    elif state == 0:
        id_log = insert_log(user, 'anular_grupal', unidad)
        insert_ticket_grupal_log(id_ticket, id_log)
    else:
        pass


def anular_ticket_grupal(id_ticket, user, unidad):
    """
    Anula el ticket grupal a traves de su id actualizando el estado.
    estado = 0 -> anulado
    Además inserta en el log el ticket anulado y los tickets vendidos de
    ese día.
    """
    update_ticket_grupal(id_ticket, user, unidad, 0)
    dia = get_dia_ticket_grupal(id_ticket)
    cant = get_cant_ticket_grupal(id_ticket)
    update_tickets_dia(dia, cant, 0)  # tickets_vendidos - cant
    update_totales_dia(dia, cant, 0)  # tickets_totales - cant
