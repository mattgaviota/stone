<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Tipos_Operaciones extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Tipos_Operaciones');
		$this->load->library('tiposoperacionesLib');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('numeric', '$s debe ser un número');
		$this->form_validation->set_message('is_natural', '%s debe ser un número natural mayor que cero');
	}

	public function index(){
		$data['contenido'] = 'tipos_operaciones/index';
		$data['titulo'] = 'Tipos de Operaciones';
		$data['registros'] = $this->Model_Tipos_Operaciones->all();
		$data['menu'] = $this->Model_Tipos_Operaciones->get_menu();
		$this->load->view('template', $data);
	}

	public function search(){
		$data['contenido'] = 'tipos_operaciones/index';
		$data['titulo'] = 'Tipos de Operaciones';
		$valor = $this->input->post('buscar');
		$data['registros'] = $this->Model_Tipos_Operaciones->allFilter('nombre', $valor);
		$this->load->view('template', $data);
	}

	public function my_validation(){
		return $this->tiposoperacioneslib->my_validation($this->input->post());
	}

	public function edit($id){
		//$id = $this->uri->segment(3);//1->controlador, 2->accion, 3->el id
		$data['contenido'] = 'tipos_operaciones/edit';
		$data['titulo'] = 'Editar Tipos de Operaciones';
		$data['registro'] = $this->Model_Tipos_Operaciones->find($id);
		$this->load->view('template',$data);
	}

	public function update(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required|callback_my_validation');
		$this->form_validation->set_rules('orden', 'Orden', 'numeric|is_natural');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->edit($registro['id']);
		}else{
			$registro['updated'] = date('Y/m/d H:i');
			$this->Model_Tipos_Operaciones->update($registro);
			redirect('tipos_operaciones/index');
		}
	}

	public function create(){
		$data['contenido'] = 'tipos_operaciones/create';
		$data['titulo'] = 'Crear Operación';
		$data['menu'] = $this->Model_Tipos_Operaciones->get_menu();
		$this->load->view('template',$data);
	}

	public function insert(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required|callback_my_validation');
		$this->form_validation->set_rules('orden', 'Orden', 'numeric|is_natural');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->create();
		}else{
			$registro['created'] = date('Y/m/d H:i');
			$registro['updated'] = date('Y/m/d H:i');
 			$this->Model_Tipos_Operaciones->insert($registro);
			redirect('tipos_operaciones/index');
		}
	}

	public function delete($id){
		$this->Model_Tipos_Operaciones->delete($id);
		redirect('tipos_operaciones/index');
	}

}