<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Tickets extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Tickets');
	}

	public function index(){
		$data['contenido'] = 'tickets/index';
		$data['registros'] = $this->Model_Tickets->all();
		$this->load->view('template-admin', $data);
	}

	public function filtrar(){
		$buscar_nombre = $this->input->post('buscar_nombre');
		$buscar_dni = $this->input->post('buscar_dni');
		$buscar_id = $this->input->post('buscar_id');
		$buscar_fecha = $this->input->post('buscar_fecha');
		$query = $this->Model_Tickets->all_filter($buscar_nombre,$buscar_dni, $buscar_id, $buscar_fecha);
		echo json_encode($query);		
	}

	public function detalles($id_ticket){
		$data['contenido'] = 'tickets/detalles';
		$data['registros'] = $this->Model_Tickets->get_ticket_detalle($id_ticket);
		$this->load->view('template-admin', $data);		
	}

}