<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class ProvinciasLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		$this->CI->load->model('Model_Provincias');//Cargamos el modelo.
	}

	public function norepetir($registro){
		$this->CI->db->where('nombre', $registro['nombre']);
		$query = $this->CI->db->get('provincias');
		if($query->num_rows() > 0 AND (!isset($registro['id']) OR ($registro['id'] != $query->row('id')))){
			return FALSE;
		}else{
			return TRUE;
		}
	}

}