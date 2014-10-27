<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Facultades extends CI_Controller {

	//Constructor
	function __construct(){
		parent::__construct();
		$this->load->model('Model_Facultades');
		$this->load->library('facultadesLib');
		$this->form_validation->set_message('required', 'Debe ingresar un valor para %s');
		$this->form_validation->set_message('norepeat', 'Ya existe un registro con el mismo nombre');
	}

	public function index(){
		$data['contenido'] = 'facultades/index';
		$data['titulo'] = 'Facultades';
		$data['registros'] = $this->Model_Facultades->all();
		$this->load->view('template', $data);
	}

	public function search(){
		$data['contenido'] = 'facultades/index';
		$data['titulo'] = 'Facultades';
		$valor = $this->input->post('buscar');
		$data['registros'] = $this->Model_Facultades->allFilter('nombre', $valor);
		$this->load->view('template', $data);
	}

	public function norepeat(){
		return $this->facultadeslib->norepetir($this->input->post());
	}

	public function edit($id){
		//$id = $this->uri->segment(3);//1->controlador, 2->accion, 3->el id
		$data['contenido'] = 'facultades/edit';
		$data['titulo'] = 'Editar Facultades';
		$data['registro'] = $this->Model_Facultades->find($id);
		$this->load->view('template',$data);
	}

	public function update(){
		$registro = $this->input->post();

		$this->form_validation->set_rules('nombre', 'Nombre', 'required|callback_norepeat');
		if($this->form_validation->run() == FALSE){
			//Si no cumplio alguna de las reglas
			$this->edit($registro['id']);
		}else{
			$registro['updated'] = date('Y/m/d H:i');
			$this->Model_Facultades->update($registro);
			redirect('facultades/index');
		}
	}

	public function create(){
		$data['contenido'] = 'facultades/create';
		$data['titulo'] = 'Agregar Facultades';
		$this->load->view('template',$data);
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
 			$this->Model_Facultades->insert($registro);
			redirect('facultades/index');
		}
	}

	public function delete($id){
		$this->Model_Facultades->delete($id);
		redirect('facultades/index');
	}

}