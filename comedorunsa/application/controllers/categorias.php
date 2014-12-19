<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Categorias extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Categorias');
		$this->load->library('categoriasLib');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('norepeat', 'Ya existe un registro con el mismo nombre');
	}

	public function index(){
		$data['contenido'] = 'categorias/index';
		$data['registros'] = $this->Model_Categorias->all();
		$this->load->view('template-admin', $data);
	}

	public function search(){
		$data['contenido'] = 'categorias/index';
		$valor = $this->input->post('buscar');
		$data['registros'] = $this->Model_Categorias->allFilter('nombre', $valor);
		$this->load->view('template-admin', $data);
	}

	public function norepeat(){
		return $this->categoriaslib->norepetir($this->input->post());
	}

	public function update(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required|callback_norepeat');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->edit($registro['id']);
		}else{
			$registro['updated'] = date('Y/m/d H:i');
			$this->Model_Perfiles->update($registro);
			redirect('perfiles/index');
		}
	}

	public function create(){
		$data['contenido'] = 'categorias/create';
		$this->load->view('template-admin',$data);
	}

	public function insert(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required|callback_norepeat');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->create();
		}else{
			$registro['created'] = date('Y/m/d H:i');
			$registro['updated'] = date('Y/m/d H:i');
 			$this->Model_Categorias->insert($registro);
			redirect('categorias/index');
		}
	}

	public function delete($id){
		$this->Model_Categorias->delete($id);
		redirect('categorias/index');
	}

}