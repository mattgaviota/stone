<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Calendario extends CI_Controller{	
	
	//Constructor
	function __construct(){
		parent::__construct();

      	$this->load->model('Model_Calendario');
      	$this->load->library('calendarioLib');
      	$this->form_validation->set_message('descripcion', 'Debe ingresar un valor para %s');
      	$this->form_validation->set_message('my_validation', 'La fecha %s es mayor que %s, eso no es posible');
	}

	public function index(){
		$data['contenido'] = 'calendario/index';
		$data['titulo'] = 'Calendarios';
		$data['registros'] = $this->Model_Calendario->all();
		$this->load->view('template-admin', $data);
	}

	public function mostrar_calendario($year = null, $month = null, $id = null){
		$data['contenido'] = 'calendario/mostrar_calendario';
		$data['titulo'] = 'Calendario';
		$data['calendario'] = $this->Model_Calendario->generate($year, $month);
		$this->load->view('template-admin', $data);			
	}

	public function mostrar_info_dia($year = null, $month = null, $id = null){

		if(!$year){
			$year = date('Y');
		}

		if(!$month){
			$month = date('m');
		}

		if(!$id){
			$id = 1;
		}

		if($this->input->post('dia') != null){
			$dia = $this->input->post('dia');
			$fecha = date('Y-m-d', strtotime($year.'-'.$month.'-'.$dia));
			$query = $this->Model_Calendario->get_calendar_data($fecha, $id);

			echo json_encode($query);
		}
	}

	public function create(){
		$data['contenido'] = 'calendario/create';
		$data['titulo'] = 'Agregando un calendario';
		$this->load->view('template-admin', $data);
	}

	public function insert(){
		$registro = $this->input->post();
		
		$this->form_validation->set_rules('descripcion', 'Descripcion', 'required');
		$this->form_validation->set_rules('desde', 'Desde', 'required|callback_my_validation[hasta]');
		$this->form_validation->set_rules('hasta', 'Hasta', 'required');

		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->create();
		}else{

 			$this->Model_Calendario->insert($registro);

 			$this->calendariolib->generar_dias($registro['desde'], $registro['hasta']);
			redirect('calendario/index');
			//echo date('Y', strtotime($registro['desde']));
		}
	}

	public function my_validation(){
		$desde = $this->input->post('desde');
		$hasta = $this->input->post('hasta');
		return $this->calendariolib->my_validation($desde, $hasta);
	}

	public function actualizar(){
		$registro = $this->input->post();
		$this->Model_Calendario->update($registro);
		echo 'Se actualizaron los datos';
	}

}