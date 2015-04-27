#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
from dal import DAL, Field
import json
from os import path

# Cargamos el archivo de configuración
file_path = path.join(path.split(path.abspath(path.dirname(__file__)))[0],
                '.config/db.json')
with open(file_path) as data_file:    
    data = json.load(data_file)

db = DAL("postgres://%s:%s@%s:%s/%s" % (data['user'], data['pass'], 
                data['host'], data['port'], data['db']), pool_size=0)

migrate = False

# Modelo de las tablas de la base de datos

db.define_table('acciones',
    Field('id', type='id'),
    Field('nombre', type='string', length=50),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('nombre_canonico', type='string', length=15),
    migrate=migrate)

db.define_table('alumnos',
    Field('id', type='id'),
    Field('facultad', type='string', length=5),
    Field('lu', type='string', length=10),
    Field('nombre', type='string', length=70),
    Field('dni', type='string', length=12),
    Field('materias', type='string', length=3),
    migrate=migrate)

db.define_table('billetes',
    Field('id', type='id'),
    Field('fecha', type='datetime'),
    Field('dni', type='reference usuarios'),
    Field('id_maquina', type='reference maquinas'),
    Field('valor', type='double'),
    migrate=migrate)

db.define_table('calendario',
    Field('id', type='id'),
    Field('desde', type='datetime'),
    Field('hasta', type='datetime'),
    Field('descripcion', type='string', length=200),
    migrate=migrate)

db.define_table('categorias',
    Field('id', type='id'),
    Field('nombre', type='string', length=100),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('importe', type='double'),
    Field('dias_maximos', type='integer'),
    migrate=migrate)

db.define_table('configuraciones',
    Field('id', type='id'),
    Field('email', type='string', length=50),
    Field('password', type='string', length=50),
    Field('puerto', type='integer'),
    Field('mensaje_email', type='string', length=300),
    Field('smtp', type='string', length=50),
    Field('asunto', type='string', length=100),
    Field('charset', type='string', length=20),
    Field('email_type', type='string', length=10),
    Field('hora_anulacion', type='integer'),
    Field('hora_compra', type='integer'),
    Field('saldo_maximo', type='integer'),
    Field('session_time', type='integer'),
    migrate=migrate)

db.define_table('dias',
    Field('id', type='id'),
    Field('fecha', type='datetime', unique=True),
    Field('tickets_totales', type='integer'),
    Field('tickets_vendidos', type='integer'),
    Field('evento', type='string', length=200),
    Field('id_calendario', type='reference calendario', ondelete='SET DEFAULT'),
    migrate=migrate)

db.define_table('estados_maquina',
    Field('id', type='id'),
    Field('descripcion', type='string', length=100),
    migrate=migrate)

db.define_table('estados_tickets',
    Field('id', type='integer'),
    Field('nombre', type='string', length=30),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    primarykey=['id'],
    migrate=migrate)

db.define_table('estados_usuarios',
    Field('id', type='integer'),
    Field('nombre', type='string', length=30),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    primarykey=['id'],
    migrate=migrate)

db.define_table('facultades',
    Field('id', type='id'),
    Field('nombre', type='string', length=50),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('nombre_canonico', type='string'),
    migrate=migrate)

db.define_table('feriados',
    Field('id', type='id'),
    Field('descripcion', type='string', length=150),
    Field('fecha', type='datetime'),
    Field('tipo', type='integer'),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    migrate=migrate)

db.define_table('imagenes',
    Field('id', type='id'),
    Field('ruta', type='string', length=300),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('nombre', type='string', length=30),
    migrate=migrate)

db.define_table('log_usuarios',
    Field('id', type='id'),
    Field('dni', type='reference usuarios'),
    Field('fecha', type='datetime'),
    Field('id_accion', type='reference acciones'),
    Field('lugar', type='integer'),
    Field('descripcion', type='string', length=200),
    migrate=migrate)

db.define_table('maquinas',
    Field('id', type='integer'),
    Field('ubicacion', type='reference facultades'),
    Field('estado', type='reference estados_maquina'),
    primarykey=['id'],
    migrate=migrate)

db.define_table('menu',
    Field('id', type='id'),
    Field('nombre', type='string', length=100),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('orden', type='integer'),
    Field('estado', type='integer'),
    migrate=migrate)

db.define_table('perfiles',
    Field('id', type='id'),
    Field('nombre', type='string', length=30),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    migrate=migrate)

db.define_table('perfiles_tipos_operaciones',
    Field('id', type='id'),
    Field('id_perfil', type='reference perfiles', ondelete='SET NULL'),
    Field('id_tipo_operacion', type='reference tipos_operaciones', ondelete='SET NULL'),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    migrate=migrate)

db.define_table('provincias',
    Field('id', type='id'),
    Field('nombre', type='string', length=50),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    migrate=migrate)

db.define_table('tickets',
    Field('id', type='id'),
    Field('id_dia', type='reference dias', ondelete='SET DEFAULT'),
    Field('importe', type='double'),
    Field('unidad', type='integer'),
    Field('estado', type='reference estados_tickets', ondelete='SET DEFAULT'),
    Field('barcode', type='string', length=20),
    migrate=migrate)

db.define_table('tickets_cierre',
    Field('id', type='id'),
    Field('fecha', type='datetime'),
    Field('id_log_usuario', type='reference log_usuarios'),
    Field('id_maquina', type='reference maquinas'),
    Field('total', type='double'),
    Field('barcode', type='string', length=20),
    migrate=migrate)

db.define_table('tickets_log_usuarios',
    Field('id', type='id'),
    Field('id_ticket', type='reference tickets', ondelete='SET DEFAULT'),
    Field('id_log_usuario', type='reference log_usuarios', ondelete='SET DEFAULT'),
    migrate=migrate)

db.define_table('tipos_operaciones',
    Field('id', type='id'),
    Field('nombre', type='string', length=30),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('controlador', type='string', length=50),
    Field('accion', type='string', length=50),
    Field('orden', type='integer'),
    Field('id_menu', type='reference menu', ondelete='SET NULL'),
    migrate=migrate)

db.define_table('usuarios',
    Field('dni', type='string', length=8),
    Field('nombre', type='string', length=200),
    Field('password', type='string', length=40),
    Field('email', type='string', length=200),
    Field('lu', type='string', length=7),
    Field('estado', type='reference estados_usuarios', ondelete='SET DEFAULT'),
    Field('id_provincia', type='reference provincias', ondelete='SET DEFAULT'),
    Field('id_facultad', type='reference facultades', ondelete='SET DEFAULT'),
    Field('id_perfil', type='reference perfiles', ondelete='SET DEFAULT'),
    Field('id_categoria', type='reference categorias', ondelete='SET DEFAULT'),
    Field('saldo', type='double', default=0),
    Field('ruta_foto', type='string', length=300),
    Field('activo',type='integer'),
    primarykey=['dni'],
    migrate=migrate)

db.define_table('videos',
    Field('id', type='id'),
    Field('ruta', type='string', length=300),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('nombre', type='string', length=30),
    Field('titulo', type='string', length=100),
    migrate=migrate)
