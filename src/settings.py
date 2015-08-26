# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
import os
import json
from lib import session
from db import controlador


# session
user_session = session.Session()
# Cargamos el archivo de configuración
file_path = os.path.join(
    os.path.split(os.path.abspath(os.path.dirname(__file__)))[0],
    '.config/parametros.json'
)
with open(file_path) as data_file:
    parametros = json.load(data_file)
    UNIDAD = int(controlador.get_maquina(parametros['terminal']))

# Cargamos el archivo de versión
path = os.path.join(
    os.path.split(os.path.abspath(os.path.dirname(__file__)))[0],
    'VERSION'
)
with open(path) as file_data:
    version_file = json.load(file_data)
    VERSION = version_file['Version']['numero']
