<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

//Validar login de usuario, cambio de clave y CRUD en la tabla de usuarios
class MenuLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		$this->CI->load->model('Model_Menu');//Cargamos el modelo.
	}

	public function norepetir($registro){
		$this->CI->db->where('nombre', $registro['nombre']);
		$query = $this->CI->db->get('menu');
		if($query->num_rows() > 0 AND (!isset($registro['id']) OR ($registro['id'] != $query->row('id')))){
			return FALSE;
		}else{
			return TRUE;
		}
	}

}