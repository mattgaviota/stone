<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Menu extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Menu');
		$this->load->library('menuLib');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('numeric', '$s debe ser un número');
		$this->form_validation->set_message('is_natural', '%s debe ser un número natural mayor que cero');
	}

	public function index(){
		$data['contenido'] = 'menu/index';
		$data['titulo'] = 'Menú';
		$data['registros'] = $this->Model_Menu->all();
		$this->load->view('template-admin', $data);
	}

	public function search(){
		$data['contenido'] = 'menu/index';
		$data['titulo'] = 'Menú';
		$valor = $this->input->post('buscar');
		$data['registros'] = $this->Model_Menu->allFilter('nombre', $valor);
		$this->load->view('template-admin', $data);
	}

	public function my_validation(){
		return $this->menulib->norepetir($this->input->post());
	}

	public function edit($id){
		//$id = $this->uri->segment(3);//1->controlador, 2->accion, 3->el id
		$data['contenido'] = 'menu/edit';
		$data['titulo'] = 'Editar Menú';
		$data['registro'] = $this->Model_Menu->find($id);
		$this->load->view('template-admin',$data);
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
			$this->Model_Menu->update($registro);
			redirect('menu/index');
		}
	}

	public function create(){
		$data['contenido'] = 'menu/create';
		$data['titulo'] = 'Crear Menú';
		$this->load->view('template-admin',$data);
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
 			$this->Model_Menu->insert($registro);
			redirect('menu/index');
		}
	}

	public function delete($id){
		$this->Model_Menu->delete($id);
		redirect('menu/index');
	}

}