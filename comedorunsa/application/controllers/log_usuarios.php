<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Log_Usuarios extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Log_Usuarios');
	}

	public function index(){
		$data['contenido'] = 'log_usuarios/index';
		$data['registros'] = $this->Model_Log_Usuarios->all();
		$data['acciones'] = $this->Model_Log_Usuarios->get_acciones();
		$this->load->view('template-admin', $data);
	}

	public function filtrar(){
		$accion = $this->input->post('accion');
		$buscar_dni = $this->input->post('buscar_dni');
		$query = $this->Model_Log_Usuarios->all_filter($accion, $buscar_dni);
		echo json_encode($query);
	}

}