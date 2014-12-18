<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

//Validar login de usuario, cambio de clave y CRUD en la tabla de usuarios
class TiposoperacionesLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		$this->CI->load->model('Model_Tipos_Operaciones');//Cargamos el modelo.
	}

	public function my_validation($registro){

		$controlador = ($registro['controlador'] != '');
		$accion = ($registro['accion'] != '');

		//No puede NO ingresar Controlador
		if(!$controlador AND !$accion){
			$this->CI->form_validation->set_message('my_validation', 'Debe ingresar controlador y acción');
			return false;
		}

		//Si ingreso controlador, debe ingresar acción
		if($controlador AND !$accion){
			$this->CI->form_validation->set_message('my_validation', 'Si ingreso controlador, debe ingresar acción');
			return false;
		}

		//Si ingreso acción, debe ingresar controlador
		if(!$controlador AND $accion){
			$this->CI->form_validation->set_message('my_validation', 'Si ingreso acción, debe ingresar controlador');
			return false;
		}

		return true;
	}

	public function findByController($controlador){
		$this->CI->db->where('controlador', $controlador);
		return $this->CI->db->get('tipos_operaciones')->row();
	}

	

}