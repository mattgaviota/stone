#-*- coding: utf-8 -*-

from dal import DAL, Field
import json
from os import path

# Cargamos el archivo de configuración
file_path = path.join(path.split(path.abspath(path.dirname(__file__)))[0],
                'conf/db.json')
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
    migrate=migrate)

db.define_table('dias',
    Field('fecha', type='datetime'),
    Field('tickets_disponibles', type='integer'),
    Field('tickets_vendidos', type='integer'),
    Field('evento', type='string', length=200),
    Field('estado', type='integer'),
    Field('id_calendario', type='integer'),
    primarykey=['fecha'],
    migrate=migrate)

db.define_table('facultades',
    Field('id', type='id'),
    Field('nombre', type='string', length=50),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    migrate=migrate)

db.define_table('feriados',
    Field('id', type='id'),
    Field('descripcion', type='string', length=150),
    Field('fecha', type='datetime'),
    Field('tipo', type='integer'),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    migrate=migrate)

db.define_table('log_operaciones',
    Field('id', type='id'),
    Field('id_tipo_operacion', type='integer'),
    Field('fecha', type='datetime'),
    Field('dni', type='reference usuarios', ondelete='SET DEFAULT'),
    migrate=migrate)

db.define_table('log_usuarios',
    Field('id', type='id'),
    Field('dni', type='string', length=8),
    Field('fecha', type='datetime'),
    Field('id_accion', type='reference acciones'),
    Field('lugar', type='integer'),
    migrate=migrate)

db.define_table('menu',
    Field('id', type='id'),
    Field('nombre', type='string', length=100),
    Field('created', type='datetime'),
    Field('updated', type='datetime'),
    Field('orden', type='integer'),
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
    Field('unidad', type='integer'),
    Field('importe', type='integer'),
    Field('fecha_alta', type='datetime'),
    Field('id_operacion', type='reference log_operaciones', ondelete='SET NULL'),
    Field('estado', type='string', length=50),
    Field('fecha', type='reference dias'),
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
    Field('estado', type='integer'),
    Field('id_provincia', type='reference provincias', ondelete='SET DEFAULT'),
    Field('id_facultad', type='reference facultades', ondelete='SET DEFAULT'),
    Field('id_perfil', type='reference perfiles', ondelete='SET DEFAULT'),
    Field('id_categoria', type='reference categorias', ondelete='SET DEFAULT'),
    primarykey=['dni'],
    migrate=migrate)
